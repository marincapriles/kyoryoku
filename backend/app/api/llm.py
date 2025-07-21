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


class ContentCreationRequest(BaseModel):
    source_material: str
    content_type: str = "blog_post"
    target_audience: str = "business_professionals"
    iterations: int = 2


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


@router.post("/content-creation/process")
async def process_content_creation(request: ContentCreationRequest):
    """Process content creation through iterative refinement pipeline"""
    try:
        results = await orchestrator.process_content_creation_request(
            source_material=request.source_material,
            content_type=request.content_type,
            target_audience=request.target_audience,
            iterations=request.iterations
        )
        return results
    except Exception as e:
        logger.error(f"Error processing content creation request: {e}")
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
            "escalation_analyst": ["assess_complexity", "expert_matching"],
            # Content Creation Team
            "story_miner": ["extract_narratives", "identify_compelling_stories", "find_human_elements"],
            "technical_translator": ["simplify_complex_concepts", "create_analogies", "bridge_technical_gaps"],
            "voice_crafter": ["maintain_authentic_voice", "create_personal_tone", "ensure_consistency"],
            "structure_architect": ["organize_narrative_flow", "create_logical_progression", "build_compelling_structure"],
            "hook_designer": ["create_compelling_openings", "maintain_reader_interest", "design_engaging_hooks"]
        }
        
        template_goals = {
            "triage_specialist": ["Categorize incoming requests accurately", "Identify urgent issues"],
            "solution_researcher": ["Find relevant solutions quickly", "Ensure solution accuracy"],
            "response_crafter": ["Create clear, helpful responses", "Maintain consistent brand voice"],
            "escalation_analyst": ["Identify cases requiring human expertise", "Route to appropriate specialists"],
            # Content Creation Team
            "story_miner": ["Find compelling stories in source material", "Identify relatable human elements"],
            "technical_translator": ["Make complex ideas accessible", "Bridge technical and non-technical worlds"],
            "voice_crafter": ["Create authentic personal connection", "Ensure content feels genuinely human"],
            "structure_architect": ["Create clear narrative progression", "Organize ideas for maximum impact"],
            "hook_designer": ["Capture attention from first sentence", "Create memorable impactful endings"]
        }
        
        template_constraints = {
            "triage_specialist": ["Must escalate if unsure about urgency", "Follow established routing rules"],
            "solution_researcher": ["Cite sources for all solutions", "Verify solution applicability"],
            "response_crafter": ["Never promise what cannot be delivered", "Include relevant next steps"],
            "escalation_analyst": ["Err on side of escalation when uncertain", "Provide complete context"],
            # Content Creation Team
            "story_miner": ["Stay true to source material facts", "Focus on authentic experiences"],
            "technical_translator": ["Maintain technical accuracy", "Preserve essential meaning"],
            "voice_crafter": ["Stay true to brand personality", "Avoid generic corporate speak"],
            "structure_architect": ["Maintain logical coherence", "Keep reader engagement high"],
            "hook_designer": ["Stay relevant to core message", "Maintain credibility and trust"]
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
            # Customer Support Team
            "triage_specialist": {
                "name": "Triage Specialist",
                "description": "Categorizes issues, identifies urgency, routes appropriately",
                "capabilities": ["categorize_issues", "identify_urgency", "route_appropriately"],
                "use_case": "First point of contact for customer requests",
                "team": "Customer Support"
            },
            "solution_researcher": {
                "name": "Solution Researcher", 
                "description": "Finds answers in docs, past tickets, knowledge base",
                "capabilities": ["search_knowledge_base", "find_past_tickets", "match_solutions"],
                "use_case": "Research and find solutions to customer issues",
                "team": "Customer Support"
            },
            "response_crafter": {
                "name": "Response Crafter",
                "description": "Writes empathetic, accurate, brand-aligned responses", 
                "capabilities": ["write_empathetic_responses", "maintain_brand_voice", "ensure_accuracy"],
                "use_case": "Craft customer-facing responses",
                "team": "Customer Support"
            },
            "escalation_analyst": {
                "name": "Escalation Analyst",
                "description": "Identifies when human intervention needed",
                "capabilities": ["assess_complexity", "expert_matching"],
                "use_case": "Determine when to escalate to human agents",
                "team": "Customer Support"
            },
            # Content Creation Team (Demo/Validation)
            "story_miner": {
                "name": "Story Miner",
                "description": "Extract compelling narratives from source material",
                "capabilities": ["extract_narratives", "identify_compelling_stories", "find_human_elements"],
                "use_case": "Find compelling stories and human elements",
                "team": "Content Creation (Demo)"
            },
            "technical_translator": {
                "name": "Technical Translator",
                "description": "Simplify complex concepts for general audiences",
                "capabilities": ["simplify_complex_concepts", "create_analogies", "bridge_technical_gaps"],
                "use_case": "Make technical content accessible",
                "team": "Content Creation (Demo)"
            },
            "voice_crafter": {
                "name": "Voice Crafter",
                "description": "Maintain authentic, personal tone",
                "capabilities": ["maintain_authentic_voice", "create_personal_tone", "ensure_consistency"],
                "use_case": "Create authentic voice and tone",
                "team": "Content Creation (Demo)"
            },
            "structure_architect": {
                "name": "Structure Architect",
                "description": "Organize ideas into compelling narrative flow",
                "capabilities": ["organize_narrative_flow", "create_logical_progression", "build_compelling_structure"],
                "use_case": "Structure content for maximum impact",
                "team": "Content Creation (Demo)"
            },
            "hook_designer": {
                "name": "Hook Designer",
                "description": "Create engaging openings and maintain momentum",
                "capabilities": ["create_compelling_openings", "maintain_reader_interest", "design_engaging_hooks"],
                "use_case": "Design hooks and maintain engagement",
                "team": "Content Creation (Demo)"
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