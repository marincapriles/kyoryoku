from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, Optional
from pydantic import BaseModel
import logging

from app.services.llm_service import llm_service, orchestrator, AgentResponse

logger = logging.getLogger(__name__)

router = APIRouter()


class AgentRequest(BaseModel):
    agent_type: str
    task: str
    context: Dict[str, Any] = {}
    capabilities: list[str] = []
    goals: list[str] = []
    constraints: list[str] = []


class CustomerSupportRequest(BaseModel):
    request: str
    customer_context: Dict[str, Any] = {}


class AgentTestRequest(BaseModel):
    message: str
    agent_type: str = "triage_specialist"


@router.post("/agent/process", response_model=AgentResponse)
async def process_agent_request(request: AgentRequest):
    """Process a request through a specific agent"""
    try:
        response = await llm_service.process_agent_request(
            agent_type=request.agent_type,
            task=request.task,
            context=request.context,
            capabilities=request.capabilities,
            goals=request.goals,
            constraints=request.constraints
        )
        return response
    except Exception as e:
        logger.error(f"Error processing agent request: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/customer-support/process")
async def process_customer_support(request: CustomerSupportRequest):
    """Process a customer support request through the multi-agent pipeline"""
    try:
        results = await orchestrator.process_customer_support_request(
            request=request.request,
            customer_context=request.customer_context
        )
        return results
    except Exception as e:
        logger.error(f"Error processing customer support request: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agent/test")
async def test_agent(request: AgentTestRequest):
    """Quick test endpoint for agent functionality"""
    try:
        # Get agent template capabilities
        template_capabilities = {
            "triage_specialist": ["categorize_issues", "identify_urgency", "route_appropriately"],
            "solution_researcher": ["search_knowledge_base", "find_past_tickets", "match_solutions"],
            "response_crafter": ["write_empathetic_responses", "maintain_brand_voice", "ensure_accuracy"],
            "escalation_analyst": ["assess_complexity", "expert_matching"]
        }
        
        template_goals = {
            "triage_specialist": ["Categorize incoming requests accurately", "Identify urgent issues"],
            "solution_researcher": ["Find relevant solutions quickly", "Ensure solution accuracy"],
            "response_crafter": ["Create clear, helpful responses", "Maintain consistent brand voice"],
            "escalation_analyst": ["Identify cases requiring human expertise", "Route to appropriate specialists"]
        }
        
        template_constraints = {
            "triage_specialist": ["Must escalate if unsure about urgency", "Follow established routing rules"],
            "solution_researcher": ["Cite sources for all solutions", "Verify solution applicability"],
            "response_crafter": ["Never promise what cannot be delivered", "Include relevant next steps"],
            "escalation_analyst": ["Err on side of escalation when uncertain", "Provide complete context"]
        }
        
        capabilities = template_capabilities.get(request.agent_type, [])
        goals = template_goals.get(request.agent_type, [])
        constraints = template_constraints.get(request.agent_type, [])
        
        response = await llm_service.process_agent_request(
            agent_type=request.agent_type,
            task=request.message,
            context={"test_mode": True},
            capabilities=capabilities,
            goals=goals,
            constraints=constraints
        )
        
        return {
            "agent_type": request.agent_type,
            "input": request.message,
            "response": response
        }
    except Exception as e:
        logger.error(f"Error testing agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents/available")
async def get_available_agents():
    """Get list of available agent types and their capabilities"""
    return {
        "agents": {
            "triage_specialist": {
                "name": "Triage Specialist",
                "description": "Categorizes issues, identifies urgency, routes appropriately",
                "capabilities": ["categorize_issues", "identify_urgency", "route_appropriately"],
                "use_case": "First point of contact for customer requests"
            },
            "solution_researcher": {
                "name": "Solution Researcher", 
                "description": "Finds answers in docs, past tickets, knowledge base",
                "capabilities": ["search_knowledge_base", "find_past_tickets", "match_solutions"],
                "use_case": "Research and find solutions to customer issues"
            },
            "response_crafter": {
                "name": "Response Crafter",
                "description": "Writes empathetic, accurate, brand-aligned responses", 
                "capabilities": ["write_empathetic_responses", "maintain_brand_voice", "ensure_accuracy"],
                "use_case": "Craft customer-facing responses"
            },
            "escalation_analyst": {
                "name": "Escalation Analyst",
                "description": "Identifies when human intervention needed",
                "capabilities": ["assess_complexity", "expert_matching"],
                "use_case": "Determine when to escalate to human agents"
            }
        }
    }


@router.get("/health")
async def health_check():
    """Health check for LLM service"""
    try:
        # Test basic functionality
        test_response = await llm_service.process_agent_request(
            agent_type="triage_specialist",
            task="Health check test",
            context={"test": True},
            capabilities=["categorize_issues"],
            goals=["Test functionality"],
            constraints=["Keep response brief"]
        )
        
        return {
            "status": "healthy",
            "llm_service": "operational",
            "test_confidence": test_response.confidence
        }
    except Exception as e:
        logger.error(f"LLM health check failed: {e}")
        return {
            "status": "unhealthy", 
            "error": str(e)
        }