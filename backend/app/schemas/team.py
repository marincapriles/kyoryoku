from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from uuid import UUID
from datetime import datetime

from .agent import AgentResponse


class TeamBase(BaseModel):
    name: str = Field(..., description="Team name like 'Customer Success Response Team'")
    description: Optional[str] = Field(None, description="Team purpose and description")
    coordination_pattern: str = Field(..., description="How agents work together")
    communication_rules: Dict[str, Any] = Field(default_factory=dict, description="Team communication protocols")
    shared_memory: Dict[str, Any] = Field(default_factory=dict, description="Team-wide knowledge")
    goal: Optional[str] = Field(None, description="Team-level objective")
    template_type: Optional[str] = Field(None, description="Template this team was created from")


class TeamCreate(TeamBase):
    agent_ids: List[UUID] = Field(default_factory=list, description="List of agent IDs to add to team")


class TeamUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    coordination_pattern: Optional[str] = None
    communication_rules: Optional[Dict[str, Any]] = None
    shared_memory: Optional[Dict[str, Any]] = None
    goal: Optional[str] = None
    template_type: Optional[str] = None


class TeamResponse(TeamBase):
    id: UUID
    agents: List[AgentResponse] = Field(default_factory=list, description="Team members")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True