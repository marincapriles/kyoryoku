import asyncio
import json
from typing import Dict, List, Optional, Any
from anthropic import AsyncAnthropic
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class AgentResponse(BaseModel):
    content: str
    confidence: float
    reasoning: str
    suggestions: List[str] = []
    escalation_needed: bool = False
    metadata: Dict[str, Any] = {}


class LLMService:
    def __init__(self):
        self.client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.chat_model = ChatAnthropic(
            model="claude-3-sonnet-20240229",
            api_key=settings.ANTHROPIC_API_KEY,
            max_tokens=2048,
            temperature=0.3
        )
    
    async def process_agent_request(
        self,
        agent_type: str,
        task: str,
        context: Dict[str, Any],
        capabilities: List[str],
        goals: List[str],
        constraints: List[str]
    ) -> AgentResponse:
        """Process a request for a specific agent type"""
        
        system_prompt = self._build_agent_system_prompt(
            agent_type, capabilities, goals, constraints
        )
        
        user_prompt = self._build_user_prompt(task, context)
        
        try:
            response = await self._call_claude(system_prompt, user_prompt)
            return self._parse_agent_response(response)
        except Exception as e:
            logger.error(f"Error processing agent request: {e}")
            return AgentResponse(
                content="I encountered an error processing your request.",
                confidence=0.0,
                reasoning="Technical error occurred",
                escalation_needed=True,
                metadata={"error": str(e)}
            )
    
    def _build_agent_system_prompt(
        self,
        agent_type: str,
        capabilities: List[str],
        goals: List[str],
        constraints: List[str]
    ) -> str:
        """Build system prompt based on agent configuration"""
        
        prompts = {
            "triage_specialist": """You are a Customer Support Triage Specialist agent. Your role is to categorize incoming support requests, assess their urgency, and route them appropriately.

CAPABILITIES: {capabilities}
GOALS: {goals}
CONSTRAINTS: {constraints}

For each request:
1. Categorize the issue type (technical, billing, account, etc.)
2. Assess urgency level (low, medium, high, critical)
3. Determine appropriate routing
4. Provide clear reasoning for your decisions

Respond in JSON format with:
- content: Your triage decision and routing recommendation
- confidence: 0.0-1.0 confidence in your assessment
- reasoning: Brief explanation of your decision process
- suggestions: Alternative actions if confidence is low
- escalation_needed: true if human review required""",

            "solution_researcher": """You are a Solution Research Specialist agent. Your role is to find relevant answers in documentation, past tickets, and knowledge bases.

CAPABILITIES: {capabilities}
GOALS: {goals}
CONSTRAINTS: {constraints}

For each query:
1. Search through available knowledge sources
2. Find the most relevant and accurate solutions
3. Rank solutions by relevance and confidence
4. Cite sources for all recommendations

Respond in JSON format with:
- content: The solution or information found
- confidence: 0.0-1.0 confidence in the solution
- reasoning: How you found and validated the solution
- suggestions: Alternative solutions or next steps
- escalation_needed: true if no sufficient solution found""",

            "response_crafter": """You are a Response Crafting Specialist agent. Your role is to write empathetic, accurate, and brand-aligned customer responses.

CAPABILITIES: {capabilities}
GOALS: {goals}
CONSTRAINTS: {constraints}

For each response:
1. Maintain empathetic and professional tone
2. Ensure accuracy and completeness
3. Follow brand voice guidelines
4. Include clear next steps

Respond in JSON format with:
- content: The customer-ready response
- confidence: 0.0-1.0 confidence in response quality
- reasoning: Why this response addresses the customer's needs
- suggestions: Alternative phrasings or approaches
- escalation_needed: true if complex issues require human touch""",

            "escalation_analyst": """You are an Escalation Analysis Specialist agent. Your role is to identify when human intervention is needed and prepare proper handoffs.

CAPABILITIES: {capabilities}
GOALS: {goals}
CONSTRAINTS: {constraints}

For each case:
1. Assess complexity and risk factors
2. Determine if human expertise is needed
3. Identify the right specialist type
4. Prepare comprehensive handoff documentation

Respond in JSON format with:
- content: Escalation recommendation and handoff notes
- confidence: 0.0-1.0 confidence in escalation decision
- reasoning: Factors leading to escalation decision
- suggestions: Specialist type and handoff approach
- escalation_needed: always true for this agent type"""
        }
        
        base_prompt = prompts.get(agent_type, prompts["triage_specialist"])
        
        return base_prompt.format(
            capabilities=", ".join(capabilities),
            goals="; ".join(goals),
            constraints="; ".join(constraints)
        )
    
    def _build_user_prompt(self, task: str, context: Dict[str, Any]) -> str:
        """Build user prompt with task and context"""
        
        context_str = ""
        if context:
            context_str = f"\n\nCONTEXT:\n{json.dumps(context, indent=2)}"
        
        return f"TASK: {task}{context_str}\n\nPlease process this request according to your role and respond in the specified JSON format."
    
    async def _call_claude(self, system_prompt: str, user_prompt: str) -> str:
        """Call Claude API with prompts"""
        
        response = await self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2048,
            temperature=0.3,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )
        
        return response.content[0].text
    
    def _parse_agent_response(self, response_text: str) -> AgentResponse:
        """Parse Claude's response into AgentResponse object"""
        
        try:
            # Try to extract JSON from response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = response_text[start_idx:end_idx]
                data = json.loads(json_str)
                
                return AgentResponse(
                    content=data.get("content", ""),
                    confidence=float(data.get("confidence", 0.5)),
                    reasoning=data.get("reasoning", ""),
                    suggestions=data.get("suggestions", []),
                    escalation_needed=data.get("escalation_needed", False),
                    metadata=data.get("metadata", {})
                )
            else:
                # Fallback if no JSON found
                return AgentResponse(
                    content=response_text,
                    confidence=0.7,
                    reasoning="Parsed from natural language response",
                    escalation_needed=False
                )
                
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON response: {e}")
            return AgentResponse(
                content=response_text,
                confidence=0.5,
                reasoning="Could not parse structured response",
                escalation_needed=True,
                metadata={"parse_error": str(e)}
            )


class MultiAgentOrchestrator:
    """Orchestrates multiple agents working together"""
    
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
    
    async def process_customer_support_request(
        self,
        request: str,
        customer_context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Process a customer support request through the multi-agent pipeline"""
        
        if customer_context is None:
            customer_context = {}
        
        pipeline_results = {}
        
        # Step 1: Triage
        triage_response = await self.llm_service.process_agent_request(
            agent_type="triage_specialist",
            task=f"Triage this customer support request: {request}",
            context=customer_context,
            capabilities=["categorize_issues", "identify_urgency", "route_appropriately"],
            goals=["Categorize incoming requests accurately", "Identify urgent issues requiring immediate attention"],
            constraints=["Must escalate if unsure about urgency", "Follow established routing rules"]
        )
        pipeline_results["triage"] = triage_response
        
        # If confidence is too low, escalate immediately
        if triage_response.confidence < 0.6 or triage_response.escalation_needed:
            escalation_response = await self.llm_service.process_agent_request(
                agent_type="escalation_analyst",
                task=f"Analyze escalation need for: {request}",
                context={**customer_context, "triage_result": triage_response.dict()},
                capabilities=["assess_complexity", "expert_matching"],
                goals=["Identify cases requiring human expertise"],
                constraints=["Err on side of escalation when uncertain"]
            )
            pipeline_results["escalation"] = escalation_response
            return pipeline_results
        
        # Step 2: Solution Research
        research_response = await self.llm_service.process_agent_request(
            agent_type="solution_researcher",
            task=f"Find solution for: {request}",
            context={**customer_context, "triage_result": triage_response.dict()},
            capabilities=["search_knowledge_base", "find_past_tickets", "match_solutions"],
            goals=["Find relevant solutions quickly", "Ensure solution accuracy"],
            constraints=["Cite sources for all solutions", "Verify solution applicability"]
        )
        pipeline_results["research"] = research_response
        
        # Step 3: Response Crafting
        response_context = {
            **customer_context,
            "triage_result": triage_response.dict(),
            "research_result": research_response.dict()
        }
        
        crafting_response = await self.llm_service.process_agent_request(
            agent_type="response_crafter",
            task=f"Craft customer response for: {request}",
            context=response_context,
            capabilities=["write_empathetic_responses", "maintain_brand_voice", "ensure_accuracy"],
            goals=["Create clear, helpful responses", "Maintain consistent brand voice"],
            constraints=["Never promise what cannot be delivered", "Include relevant next steps"]
        )
        pipeline_results["response"] = crafting_response
        
        # Final confidence check
        overall_confidence = min(
            triage_response.confidence,
            research_response.confidence,
            crafting_response.confidence
        )
        
        if overall_confidence < 0.8:
            escalation_response = await self.llm_service.process_agent_request(
                agent_type="escalation_analyst",
                task=f"Review overall confidence for: {request}",
                context=response_context,
                capabilities=["assess_complexity", "expert_matching"],
                goals=["Identify cases requiring human expertise"],
                constraints=["Err on side of escalation when uncertain"]
            )
            pipeline_results["escalation"] = escalation_response
        
        return pipeline_results


# Global instances
llm_service = LLMService()
orchestrator = MultiAgentOrchestrator(llm_service)