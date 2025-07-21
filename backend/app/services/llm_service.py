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
            model="claude-3-5-sonnet-20241022",
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
- escalation_needed: always true for this agent type""",

            # Content Creation Team Agents (Demo/Validation Use Case)
            "story_miner": """You are a Story Miner agent for content creation. Your role is to extract compelling narratives and human elements from source material.

CAPABILITIES: {capabilities}
GOALS: {goals}
CONSTRAINTS: {constraints}

For each piece of source material:
1. Identify the most compelling human stories and experiences
2. Extract key moments that create emotional connection
3. Find relatable elements that resonate with audiences
4. Surface authentic experiences and genuine insights

Respond in JSON format with:
- content: The compelling narratives and stories you've extracted
- confidence: 0.0-1.0 confidence in story relevance and impact
- reasoning: Why these stories are compelling and authentic
- suggestions: Alternative narrative angles or additional story elements
- escalation_needed: true if source material lacks compelling narratives""",

            "technical_translator": """You are a Technical Translator agent for content creation. Your role is to simplify complex concepts for general audiences without losing essential meaning.

CAPABILITIES: {capabilities}
GOALS: {goals}
CONSTRAINTS: {constraints}

For each technical concept:
1. Break down complex ideas into understandable components
2. Create analogies and metaphors that clarify meaning
3. Remove jargon while preserving accuracy
4. Make concepts accessible to non-technical audiences

Respond in JSON format with:
- content: Simplified, accessible explanation of the technical concepts
- confidence: 0.0-1.0 confidence in translation accuracy and clarity
- reasoning: How you maintained accuracy while simplifying
- suggestions: Alternative explanations or additional clarifications
- escalation_needed: true if concepts are too complex to simplify safely""",

            "voice_crafter": """You are a Voice Crafter agent for content creation. Your role is to maintain authentic, personal tone throughout content.

CAPABILITIES: {capabilities}
GOALS: {goals}
CONSTRAINTS: {constraints}

For each piece of content:
1. Ensure authentic, human voice that connects with readers
2. Maintain consistent tone and personality
3. Balance professionalism with genuine warmth
4. Make content feel personal and engaging

Respond in JSON format with:
- content: Content refined for authentic voice and tone
- confidence: 0.0-1.0 confidence in voice consistency and authenticity
- reasoning: How you enhanced the human connection and authenticity
- suggestions: Alternative tone approaches or voice adjustments
- escalation_needed: true if content feels too corporate or impersonal""",

            "structure_architect": """You are a Structure Architect agent for content creation. Your role is to organize ideas into compelling narrative flow.

CAPABILITIES: {capabilities}
GOALS: {goals}
CONSTRAINTS: {constraints}

For each piece of content:
1. Create logical progression that builds engagement
2. Organize ideas for maximum impact and clarity
3. Ensure smooth transitions between concepts
4. Structure content for optimal readability and flow

Respond in JSON format with:
- content: Content restructured for optimal narrative flow
- confidence: 0.0-1.0 confidence in structural improvements
- reasoning: How the new structure enhances readability and impact
- suggestions: Alternative structural approaches or organization methods
- escalation_needed: true if content lacks sufficient substance for good structure""",

            "hook_designer": """You are a Hook Designer agent for content creation. Your role is to create engaging openings and maintain momentum throughout.

CAPABILITIES: {capabilities}
GOALS: {goals}
CONSTRAINTS: {constraints}

For each piece of content:
1. Create compelling opening that captures immediate attention
2. Design hooks that maintain reader interest throughout
3. Craft memorable conclusions that leave lasting impact
4. Ensure momentum builds naturally from start to finish

Respond in JSON format with:
- content: Content enhanced with engaging hooks and strong momentum
- confidence: 0.0-1.0 confidence in engagement and memorability
- reasoning: How the hooks enhance reader engagement and retention
- suggestions: Alternative hook approaches or engagement techniques
- escalation_needed: true if content lacks engaging elements to work with"""
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
            model="claude-3-5-sonnet-20241022",
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
                
                # Handle flexible response formats from Claude
                content = data.get("content", "")
                if isinstance(content, dict):
                    content = json.dumps(content, indent=2)
                elif not isinstance(content, str):
                    content = str(content)
                
                # Handle reasoning field
                reasoning = data.get("reasoning", "")
                if isinstance(reasoning, list):
                    reasoning = ". ".join(str(r) for r in reasoning)
                elif not isinstance(reasoning, str):
                    reasoning = str(reasoning)
                
                # Handle suggestions field
                suggestions = data.get("suggestions", [])
                if isinstance(suggestions, dict):
                    # Convert dict suggestions to list of strings
                    suggestions = [f"{k}: {v}" for k, v in suggestions.items()]
                elif not isinstance(suggestions, list):
                    suggestions = [str(suggestions)]
                
                # Ensure all suggestion items are strings
                suggestions = [str(s) for s in suggestions]
                
                return AgentResponse(
                    content=content,
                    confidence=float(data.get("confidence", 0.5)),
                    reasoning=reasoning,
                    suggestions=suggestions,
                    escalation_needed=bool(data.get("escalation_needed", False)),
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

    async def process_content_creation_request(
        self,
        source_material: str,
        content_type: str = "blog_post",
        target_audience: str = "business_professionals",
        iterations: int = 2
    ) -> Dict[str, Any]:
        """Process content creation through iterative refinement pipeline"""
        
        content_context = {
            "content_type": content_type,
            "target_audience": target_audience,
            "iteration": 0
        }
        
        iteration_results = {}
        current_content = source_material
        
        # Iterative refinement process
        for iteration in range(iterations):
            iteration_results[f"iteration_{iteration + 1}"] = {}
            
            # Round 1: Story Mining
            story_response = await self.llm_service.process_agent_request(
                agent_type="story_miner",
                task=f"Extract compelling narratives from this material: {current_content}",
                context={**content_context, "iteration": iteration + 1},
                capabilities=["extract_narratives", "identify_compelling_stories", "find_human_elements"],
                goals=["Find the most compelling stories in source material", "Identify relatable human elements"],
                constraints=["Stay true to source material facts", "Focus on authentic experiences"]
            )
            iteration_results[f"iteration_{iteration + 1}"]["story_mining"] = story_response
            current_content = story_response.content
            
            # Round 2: Structure Architecture  
            structure_response = await self.llm_service.process_agent_request(
                agent_type="structure_architect",
                task=f"Organize this content into compelling narrative flow: {current_content}",
                context={**content_context, "iteration": iteration + 1, "story_mining_result": story_response.dict()},
                capabilities=["organize_narrative_flow", "create_logical_progression", "build_compelling_structure"],
                goals=["Create clear, logical narrative progression", "Organize ideas for maximum impact"],
                constraints=["Maintain logical coherence", "Keep reader engagement high"]
            )
            iteration_results[f"iteration_{iteration + 1}"]["structure"] = structure_response
            current_content = structure_response.content
            
            # Round 3: Technical Translation
            translation_response = await self.llm_service.process_agent_request(
                agent_type="technical_translator",
                task=f"Simplify complex concepts for {target_audience}: {current_content}",
                context={**content_context, "iteration": iteration + 1, "structure_result": structure_response.dict()},
                capabilities=["simplify_complex_concepts", "create_analogies", "bridge_technical_gaps"],
                goals=["Make complex ideas accessible to everyone", "Bridge technical and non-technical worlds"],
                constraints=["Maintain technical accuracy", "Preserve essential meaning"]
            )
            iteration_results[f"iteration_{iteration + 1}"]["translation"] = translation_response
            current_content = translation_response.content
            
            # Round 4: Voice Crafting
            voice_response = await self.llm_service.process_agent_request(
                agent_type="voice_crafter",
                task=f"Enhance authentic voice and tone: {current_content}",
                context={**content_context, "iteration": iteration + 1, "translation_result": translation_response.dict()},
                capabilities=["maintain_authentic_voice", "create_personal_tone", "ensure_consistency"],
                goals=["Create authentic, personal connection", "Ensure content feels genuinely human"],
                constraints=["Stay true to brand personality", "Avoid generic corporate speak"]
            )
            iteration_results[f"iteration_{iteration + 1}"]["voice"] = voice_response
            current_content = voice_response.content
            
            # Round 5: Hook Design
            hook_response = await self.llm_service.process_agent_request(
                agent_type="hook_designer",
                task=f"Create engaging hooks and maintain momentum: {current_content}",
                context={**content_context, "iteration": iteration + 1, "voice_result": voice_response.dict()},
                capabilities=["create_compelling_openings", "maintain_reader_interest", "design_engaging_hooks"],
                goals=["Capture attention from the first sentence", "Create memorable, impactful endings"],
                constraints=["Stay relevant to core message", "Maintain credibility and trust"]
            )
            iteration_results[f"iteration_{iteration + 1}"]["hooks"] = hook_response
            current_content = hook_response.content
            
            # Calculate iteration confidence
            iteration_confidence = min(
                story_response.confidence,
                structure_response.confidence,
                translation_response.confidence,
                voice_response.confidence,
                hook_response.confidence
            )
            iteration_results[f"iteration_{iteration + 1}"]["overall_confidence"] = iteration_confidence
            iteration_results[f"iteration_{iteration + 1}"]["final_content"] = current_content
            
            # If confidence is high enough, we can stop early
            if iteration_confidence > 0.9 and iteration > 0:
                break
        
        # Final summary
        final_result = {
            "iterations": iteration_results,
            "final_content": current_content,
            "content_type": content_type,
            "target_audience": target_audience,
            "total_iterations": len(iteration_results),
            "platform_validation": {
                "coordination_success": all(
                    iter_data.get("overall_confidence", 0) > 0.6 
                    for iter_data in iteration_results.values()
                ),
                "iterative_improvement": len(iteration_results) > 1,
                "agent_handoffs": len(iteration_results) * 5  # 5 agents per iteration
            }
        }
        
        return final_result


# Global instances
llm_service = LLMService()
orchestrator = MultiAgentOrchestrator(llm_service)