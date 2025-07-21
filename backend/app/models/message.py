from sqlalchemy import Column, String, JSON, DateTime, ForeignKey, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.core.database import Base


class MessageType(enum.Enum):
    DIRECT = "direct"
    BROADCAST = "broadcast"
    REQUEST = "request"
    RESPONSE = "response"
    ESCALATION = "escalation"
    SYSTEM = "system"
    HUMAN = "human"


class Message(Base):
    __tablename__ = "messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey('sessions.id'), nullable=False)
    sender_id = Column(UUID(as_uuid=True), ForeignKey('agents.id'))  # None for human messages
    recipient_id = Column(UUID(as_uuid=True), ForeignKey('agents.id'))  # None for broadcast
    message_type = Column(Enum(MessageType), nullable=False)
    content = Column(Text, nullable=False)
    message_metadata = Column(JSON, default=dict)  # Reasoning traces, confidence, etc.
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Shadow learning specific fields
    is_suggestion = Column(String(10), default="false")  # true/false as string for JSON compatibility
    human_approved = Column(String(10))  # true/false/modified
    learning_confidence = Column(JSON, default=dict)  # Confidence scores for learning
    
    # Relationships
    session = relationship("Session", back_populates="messages")
    sender = relationship("Agent", foreign_keys=[sender_id], post_update=True)
    recipient = relationship("Agent", foreign_keys=[recipient_id], post_update=True)