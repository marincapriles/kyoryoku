from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from uuid import UUID
from datetime import datetime
from enum import Enum


class MessageType(str, Enum):
    DIRECT = "DIRECT"
    BROADCAST = "BROADCAST"
    REQUEST = "REQUEST"
    RESPONSE = "RESPONSE"
    ESCALATION = "ESCALATION"
    SYSTEM = "SYSTEM"
    HUMAN = "HUMAN"


class MessageBase(BaseModel):
    session_id: UUID = Field(..., description="ID of the session this message belongs to")
    sender_id: Optional[UUID] = Field(None, description="ID of the agent/user sending the message")
    recipient_id: Optional[UUID] = Field(None, description="ID of the agent/user receiving the message")
    message_type: MessageType = Field(..., description="Type of message being sent")
    content: str = Field(..., description="The actual message content")
    message_metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional message metadata")
    is_suggestion: Optional[str] = Field(None, max_length=10, description="Whether this is a suggestion during shadow learning")
    human_approved: Optional[str] = Field(None, max_length=10, description="Whether a human approved this suggestion")
    learning_confidence: Dict[str, Any] = Field(default_factory=dict, description="Confidence scores for shadow learning")


class MessageCreate(MessageBase):
    pass


class MessageUpdate(BaseModel):
    sender_id: Optional[UUID] = None
    recipient_id: Optional[UUID] = None
    message_type: Optional[MessageType] = None
    content: Optional[str] = None
    message_metadata: Optional[Dict[str, Any]] = None
    is_suggestion: Optional[str] = Field(None, max_length=10)
    human_approved: Optional[str] = Field(None, max_length=10)
    learning_confidence: Optional[Dict[str, Any]] = None


class MessageResponse(MessageBase):
    id: UUID
    timestamp: datetime

    class Config:
        from_attributes = True