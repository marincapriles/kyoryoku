from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from uuid import UUID

from app.models.agent import Agent
from app.schemas.agent import AgentCreate, AgentUpdate


class AgentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_agent(self, agent_data: AgentCreate) -> Agent:
        """Create a new agent"""
        db_agent = Agent(
            name=agent_data.name,
            description=agent_data.description,
            capabilities=agent_data.capabilities,
            beliefs=agent_data.beliefs,
            goals=agent_data.goals,
            constraints=agent_data.constraints,
            memory=agent_data.memory,
            template_type=agent_data.template_type
        )
        self.db.add(db_agent)
        await self.db.flush()
        await self.db.refresh(db_agent)
        return db_agent

    async def get_agent(self, agent_id: UUID) -> Optional[Agent]:
        """Get agent by ID"""
        result = await self.db.execute(
            select(Agent).where(Agent.id == agent_id)
        )
        return result.scalar_one_or_none()

    async def list_agents(self, skip: int = 0, limit: int = 100) -> List[Agent]:
        """List all agents with pagination"""
        result = await self.db.execute(
            select(Agent).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def update_agent(self, agent_id: UUID, agent_data: AgentUpdate) -> Optional[Agent]:
        """Update an existing agent"""
        agent = await self.get_agent(agent_id)
        if not agent:
            return None

        update_data = agent_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(agent, field, value)

        await self.db.flush()
        await self.db.refresh(agent)
        return agent

    async def delete_agent(self, agent_id: UUID) -> bool:
        """Delete an agent"""
        agent = await self.get_agent(agent_id)
        if not agent:
            return False

        await self.db.delete(agent)
        await self.db.flush()
        return True

    async def get_agents_by_template(self, template_type: str) -> List[Agent]:
        """Get all agents of a specific template type"""
        result = await self.db.execute(
            select(Agent).where(Agent.template_type == template_type)
        )
        return result.scalars().all()