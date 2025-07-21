from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional, Dict, Any
from uuid import UUID
import logging

from app.models.session import Session, SessionStatus
from app.models.team import Team
from app.models.agent import Agent
from app.models.message import Message, MessageType
from app.schemas.session import SessionCreate, SessionUpdate
from app.services.llm_service import llm_service, orchestrator

logger = logging.getLogger(__name__)


class SessionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_session(self, session_data: SessionCreate) -> Session:
        """Create a new collaboration session"""
        db_session = Session(
            team_id=session_data.team_id,
            task_description=session_data.task_description,
            status=SessionStatus.PENDING,
            user_id=session_data.user_id,
            scenario_type=session_data.scenario_type,
            learning_phase=session_data.learning_phase,
            metrics=session_data.metrics,
            configuration=session_data.configuration
        )
        self.db.add(db_session)
        await self.db.flush()
        await self.db.refresh(db_session)
        return db_session

    async def get_session(self, session_id: UUID) -> Optional[Session]:
        """Get session by ID with related data"""
        result = await self.db.execute(
            select(Session)
            .options(selectinload(Session.team).selectinload(Team.agents))
            .where(Session.id == session_id)
        )
        return result.scalar_one_or_none()

    async def list_sessions(self, skip: int = 0, limit: int = 100) -> List[Session]:
        """List all sessions with pagination"""
        result = await self.db.execute(
            select(Session)
            .options(selectinload(Session.team))
            .offset(skip)
            .limit(limit)
            .order_by(Session.created_at.desc())
        )
        return result.scalars().all()

    async def update_session(self, session_id: UUID, session_data: SessionUpdate) -> Optional[Session]:
        """Update an existing session"""
        session = await self.get_session(session_id)
        if not session:
            return None

        update_data = session_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(session, field, value)

        await self.db.flush()
        await self.db.refresh(session)
        return session

    async def start_session(self, session_id: UUID) -> Optional[Session]:
        """Start a session and begin processing"""
        session = await self.get_session(session_id)
        if not session:
            return None

        session.status = SessionStatus.RUNNING
        await self.db.flush()

        # If this is a customer support scenario, use the multi-agent orchestrator
        if session.scenario_type == "customer_support":
            await self._process_customer_support_session(session)
        else:
            # For other scenarios, use individual agents
            await self._process_generic_session(session)

        await self.db.refresh(session)
        return session

    async def _process_customer_support_session(self, session: Session):
        """Process a customer support session using the multi-agent orchestrator"""
        try:
            # Get customer context from session configuration
            customer_context = session.configuration.get("customer_context", {})
            
            # Use the orchestrator to process the request
            results = await orchestrator.process_customer_support_request(
                request=session.task_description,
                customer_context=customer_context
            )

            # Save each agent's response as a message
            for agent_type, agent_response in results.items():
                await self._save_agent_message(
                    session_id=session.id,
                    agent_type=agent_type,
                    content=agent_response.content,
                    confidence=agent_response.confidence,
                    reasoning=agent_response.reasoning,
                    escalation_needed=agent_response.escalation_needed
                )

            # Update session metrics
            session.metrics = {
                "agent_responses": len(results),
                "overall_confidence": min(r.confidence for r in results.values()),
                "escalation_needed": any(r.escalation_needed for r in results.values()),
                "processing_results": {k: v.dict() for k, v in results.items()}
            }

            # Determine final status
            if any(r.escalation_needed for r in results.values()):
                session.status = SessionStatus.COMPLETED
                session.metrics["requires_human_review"] = True
            else:
                session.status = SessionStatus.COMPLETED
                session.metrics["requires_human_review"] = False

        except Exception as e:
            logger.error(f"Error processing customer support session {session.id}: {e}")
            session.status = SessionStatus.FAILED
            session.metrics = {"error": str(e)}

    async def _process_generic_session(self, session: Session):
        """Process a generic session using team agents individually"""
        try:
            team_agents = session.team.agents if session.team else []
            
            if not team_agents:
                session.status = SessionStatus.FAILED
                session.metrics = {"error": "No agents available in team"}
                return

            agent_responses = []
            for agent in team_agents:
                try:
                    # Process task with individual agent
                    response = await llm_service.process_agent_request(
                        agent_type=agent.template_type or "generic",
                        task=session.task_description,
                        context=session.configuration.get("context", {}),
                        capabilities=agent.capabilities or [],
                        goals=agent.goals or [],
                        constraints=agent.constraints or []
                    )

                    agent_responses.append(response)
                    
                    # Save agent message
                    await self._save_agent_message(
                        session_id=session.id,
                        agent_id=agent.id,
                        agent_type=agent.template_type,
                        content=response.content,
                        confidence=response.confidence,
                        reasoning=response.reasoning,
                        escalation_needed=response.escalation_needed
                    )

                except Exception as e:
                    logger.error(f"Error processing with agent {agent.id}: {e}")
                    await self._save_agent_message(
                        session_id=session.id,
                        agent_id=agent.id,
                        agent_type=agent.template_type,
                        content=f"Error processing request: {str(e)}",
                        confidence=0.0,
                        reasoning="Technical error occurred",
                        escalation_needed=True
                    )

            # Update session metrics
            if agent_responses:
                session.metrics = {
                    "agent_count": len(agent_responses),
                    "average_confidence": sum(r.confidence for r in agent_responses) / len(agent_responses),
                    "escalation_needed": any(r.escalation_needed for r in agent_responses)
                }
                session.status = SessionStatus.COMPLETED
            else:
                session.status = SessionStatus.FAILED
                session.metrics = {"error": "No agent responses generated"}

        except Exception as e:
            logger.error(f"Error processing generic session {session.id}: {e}")
            session.status = SessionStatus.FAILED
            session.metrics = {"error": str(e)}

    async def _save_agent_message(
        self,
        session_id: UUID,
        content: str,
        confidence: float,
        reasoning: str,
        escalation_needed: bool,
        agent_type: str = None,
        agent_id: UUID = None
    ):
        """Save an agent's response as a message"""
        message = Message(
            session_id=session_id,
            sender_id=agent_id,
            message_type=MessageType.RESPONSE,
            content=content,
            message_metadata={
                "confidence": confidence,
                "reasoning": reasoning,
                "escalation_needed": escalation_needed,
                "agent_type": agent_type
            }
        )
        self.db.add(message)
        await self.db.flush()

    async def get_session_messages(self, session_id: UUID) -> List[Message]:
        """Get all messages for a session"""
        result = await self.db.execute(
            select(Message)
            .where(Message.session_id == session_id)
            .order_by(Message.timestamp)
        )
        return result.scalars().all()

    async def add_human_message(
        self,
        session_id: UUID,
        content: str,
        user_id: UUID = None
    ) -> Message:
        """Add a human message to the session"""
        message = Message(
            session_id=session_id,
            sender_id=user_id,
            message_type=MessageType.HUMAN,
            content=content,
            message_metadata={"source": "human"}
        )
        self.db.add(message)
        await self.db.flush()
        await self.db.refresh(message)
        return message