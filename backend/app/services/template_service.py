from typing import List, Dict
from app.schemas.agent import AgentTemplate


class TemplateService:
    """Service for managing agent and team templates from PRD v22"""
    
    @staticmethod
    def get_agent_templates() -> List[Dict]:
        """Get all available agent templates from PRD v22"""
        return [
            {
                "name": "Triage Specialist",
                "description": "Categorizes issues, identifies urgency, routes appropriately",
                "template_type": "triage_specialist",
                "capabilities": [
                    "categorize_issues",
                    "identify_urgency", 
                    "route_appropriately",
                    "priority_detection",
                    "routing_rules",
                    "urgency_markers"
                ],
                "default_goals": [
                    "Categorize incoming requests accurately",
                    "Identify urgent issues requiring immediate attention",
                    "Route issues to appropriate team members"
                ],
                "constraints": [
                    "Must escalate if unsure about urgency",
                    "Follow established routing rules",
                    "Document categorization reasoning"
                ]
            },
            {
                "name": "Solution Researcher",
                "description": "Finds answers in docs, past tickets, knowledge base",
                "template_type": "solution_researcher",
                "capabilities": [
                    "search_knowledge_base",
                    "find_past_tickets",
                    "match_solutions",
                    "search_patterns",
                    "doc_relevance",
                    "solution_matching"
                ],
                "default_goals": [
                    "Find relevant solutions quickly",
                    "Ensure solution accuracy and completeness",
                    "Learn from past successful resolutions"
                ],
                "constraints": [
                    "Cite sources for all solutions",
                    "Verify solution applicability",
                    "Escalate if no solution found"
                ]
            },
            {
                "name": "Response Crafter",
                "description": "Writes empathetic, accurate, brand-aligned responses",
                "template_type": "response_crafter",
                "capabilities": [
                    "write_empathetic_responses",
                    "maintain_brand_voice",
                    "ensure_accuracy",
                    "brand_voice",
                    "empathy_patterns", 
                    "clarity_rules"
                ],
                "default_goals": [
                    "Create clear, helpful responses",
                    "Maintain consistent brand voice",
                    "Show empathy and understanding"
                ],
                "constraints": [
                    "Never promise what cannot be delivered",
                    "Use approved language and tone",
                    "Include relevant next steps"
                ]
            },
            {
                "name": "Escalation Analyst",
                "description": "Identifies when human intervention needed",
                "template_type": "escalation_analyst",
                "capabilities": [
                    "identify_complex_cases",
                    "determine_human_need",
                    "route_to_experts",
                    "assess_complexity",
                    "expert_matching"
                ],
                "default_goals": [
                    "Identify cases requiring human expertise",
                    "Route to appropriate specialists",
                    "Preserve context during handoffs"
                ],
                "constraints": [
                    "Err on side of escalation when uncertain",
                    "Provide complete context to humans",
                    "Track escalation patterns"
                ]
            },
            {
                "name": "Requirements Analyst",
                "description": "Parses RFP requirements into discrete needs",
                "template_type": "requirements_analyst",
                "capabilities": [
                    "parse_rfp_requirements",
                    "extract_discrete_needs",
                    "prioritize_requirements",
                    "requirement_mapping",
                    "compliance_checking"
                ],
                "default_goals": [
                    "Extract all requirements completely",
                    "Organize requirements by priority",
                    "Identify mandatory vs optional items"
                ],
                "constraints": [
                    "Must capture all stated requirements",
                    "Flag ambiguous or unclear items",
                    "Document assumptions made"
                ]
            },
            {
                "name": "Content Assembler", 
                "description": "Pulls from past proposals, case studies, docs",
                "template_type": "content_assembler",
                "capabilities": [
                    "pull_past_proposals",
                    "access_case_studies",
                    "organize_content",
                    "content_matching",
                    "template_management"
                ],
                "default_goals": [
                    "Find relevant existing content",
                    "Organize content logically",
                    "Ensure content freshness"
                ],
                "constraints": [
                    "Verify content is current",
                    "Maintain client confidentiality",
                    "Attribute sources properly"
                ]
            }
        ]
    
    @staticmethod
    def get_team_templates() -> List[AgentTemplate]:
        """Get all available team templates from PRD v22"""
        return [
            AgentTemplate(
                name="Customer Success Response Team",
                description="Scale support quality across all representatives",
                use_case="Handle customer support tickets efficiently",
                target_metric="Resolve tickets in 2 minutes vs 20 minutes",
                coordination_pattern="sequential_pipeline",
                agents=[
                    {
                        "role": "Triage Specialist",
                        "capabilities": ["categorize_issues", "identify_urgency", "route_appropriately"]
                    },
                    {
                        "role": "Solution Researcher",
                        "capabilities": ["search_knowledge_base", "find_past_tickets", "match_solutions"]
                    },
                    {
                        "role": "Response Crafter", 
                        "capabilities": ["write_empathetic_responses", "maintain_brand_voice", "ensure_accuracy"]
                    },
                    {
                        "role": "Escalation Analyst",
                        "capabilities": ["identify_complex_cases", "determine_human_need", "route_to_experts"]
                    }
                ]
            ),
            AgentTemplate(
                name="RFP/Proposal Acceleration Team",
                description="Win more deals by responding to RFPs 10x faster",
                use_case="Complete comprehensive responses to RFPs",
                target_metric="Complete 50-page RFP in 1 hour vs 1 week",
                coordination_pattern="parallel_assembly",
                agents=[
                    {
                        "role": "Requirements Analyst",
                        "capabilities": ["parse_rfp_requirements", "extract_discrete_needs", "prioritize_requirements"]
                    },
                    {
                        "role": "Content Assembler",
                        "capabilities": ["pull_past_proposals", "access_case_studies", "organize_content"]
                    },
                    {
                        "role": "Compliance Checker",
                        "capabilities": ["verify_requirement_coverage", "ensure_compliance", "validate_completeness"]
                    },
                    {
                        "role": "Customization Writer",
                        "capabilities": ["tailor_content", "client_specific_customization", "personalize_proposals"]
                    }
                ]
            ),
            AgentTemplate(
                name="Product Intelligence Team",
                description="Synthesize customer feedback into actionable insights",
                use_case="Analyze customer feedback from multiple channels",
                target_metric="Process 1,000 inputs into 5 insights daily",
                coordination_pattern="parallel_synthesis",
                agents=[
                    {
                        "role": "Feedback Aggregator",
                        "capabilities": ["collect_support_feedback", "monitor_reviews", "gather_surveys"]
                    },
                    {
                        "role": "Pattern Detector",
                        "capabilities": ["identify_trends", "detect_emerging_themes", "spot_anomalies"]
                    },
                    {
                        "role": "Impact Analyzer",
                        "capabilities": ["estimate_business_value", "assess_improvement_impact", "prioritize_features"]
                    },
                    {
                        "role": "Insight Reporter",
                        "capabilities": ["create_exec_summaries", "generate_reports", "present_findings"]
                    }
                ]
            )
        ]
    
    @staticmethod
    def create_agent_from_template(template_name: str, custom_name: str = None) -> Dict:
        """Create an agent configuration from a template"""
        templates = TemplateService.get_agent_templates()
        template = next((t for t in templates if t["name"] == template_name), None)
        
        if not template:
            raise ValueError(f"Template '{template_name}' not found")
        
        return {
            "name": custom_name or template["name"],
            "description": template["description"],
            "capabilities": template["capabilities"],
            "goals": template["default_goals"],
            "constraints": template["constraints"],
            "template_type": template["template_type"],
            "beliefs": {},
            "memory": {}
        }