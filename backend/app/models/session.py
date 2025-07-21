from sqlalchemy import Column, String, JSON, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.core.database import Base


class SessionStatus(enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    team_id = Column(UUID(as_uuid=True), ForeignKey('teams.id'), nullable=False)
    task_description = Column(String(2000), nullable=False)
    status = Column(Enum(SessionStatus), default=SessionStatus.PENDING)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    metrics = Column(JSON, default=dict)  # Performance measurements
    configuration = Column(JSON, default=dict)  # Snapshot of team config at execution
    user_id = Column(UUID(as_uuid=True))  # For authentication
    scenario_type = Column(String(100))  # customer_support, rfp_response, etc.
    learning_phase = Column(String(50))  # shadow, suggestion, assisted
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    team = relationship("Team", back_populates="sessions")
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")