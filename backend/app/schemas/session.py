from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from uuid import UUID
from datetime import datetime
from enum import Enum


class SessionStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class SessionBase(BaseModel):
    team_id: UUID = Field(..., description="ID of the team handling this session")
    task_description: str = Field(..., max_length=2000, description="Description of the task to be performed")
    status: SessionStatus = Field(default=SessionStatus.PENDING, description="Current session status")
    user_id: Optional[UUID] = Field(None, description="ID of the user who initiated the session")
    scenario_type: Optional[str] = Field(None, max_length=100, description="Type of scenario (e.g., customer_support, rfp_response)")
    learning_phase: Optional[str] = Field(None, max_length=50, description="Shadow learning phase (observation, suggestion, assisted)")
    metrics: Dict[str, Any] = Field(default_factory=dict, description="Performance and outcome metrics")
    configuration: Dict[str, Any] = Field(default_factory=dict, description="Session-specific configuration")


class SessionCreate(SessionBase):
    pass


class SessionUpdate(BaseModel):
    task_description: Optional[str] = Field(None, max_length=2000)
    status: Optional[SessionStatus] = None
    user_id: Optional[UUID] = None
    scenario_type: Optional[str] = Field(None, max_length=100)
    learning_phase: Optional[str] = Field(None, max_length=50)
    metrics: Optional[Dict[str, Any]] = None
    configuration: Optional[Dict[str, Any]] = None


class SessionResponse(SessionBase):
    id: UUID
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True