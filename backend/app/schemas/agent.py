from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from uuid import UUID
from datetime import datetime


class AgentBase(BaseModel):
    name: str = Field(..., description="Agent name like 'Triage Specialist'")
    description: Optional[str] = Field(None, description="Human-readable purpose")
    capabilities: List[str] = Field(default_factory=list, description="What this agent can do")
    beliefs: Dict[str, float] = Field(default_factory=dict, description="Knowledge with confidence scores")
    goals: List[str] = Field(default_factory=list, description="Current objectives")
    constraints: List[str] = Field(default_factory=list, description="Limitations and boundaries")
    memory: Dict[str, Any] = Field(default_factory=dict, description="Persistent learning storage")
    template_type: Optional[str] = Field(None, description="Template this agent was created from")


class AgentCreate(AgentBase):
    pass


class AgentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    capabilities: Optional[List[str]] = None
    beliefs: Optional[Dict[str, float]] = None
    goals: Optional[List[str]] = None
    constraints: Optional[List[str]] = None
    memory: Optional[Dict[str, Any]] = None
    template_type: Optional[str] = None


class AgentResponse(AgentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AgentTemplate(BaseModel):
    name: str
    description: str
    use_case: str
    target_metric: str
    coordination_pattern: str
    agents: List[Dict[str, Any]]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Customer Success Response Team",
                "description": "Scale support quality across all representatives",
                "use_case": "Handle customer support tickets efficiently",
                "target_metric": "Resolve tickets in 2 minutes vs 20 minutes",
                "coordination_pattern": "sequential_pipeline",
                "agents": [
                    {
                        "role": "Triage Specialist",
                        "capabilities": ["categorize_issues", "identify_urgency", "route_appropriately"]
                    },
                    {
                        "role": "Solution Researcher", 
                        "capabilities": ["search_knowledge_base", "find_past_tickets", "match_solutions"]
                    }
                ]
            }
        }