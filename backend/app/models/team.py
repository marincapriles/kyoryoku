from sqlalchemy import Column, String, JSON, DateTime, Integer, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base

# Association table for team-agent relationships
team_members = Table(
    'team_members',
    Base.metadata,
    Column('team_id', UUID(as_uuid=True), ForeignKey('teams.id'), primary_key=True),
    Column('agent_id', UUID(as_uuid=True), ForeignKey('agents.id'), primary_key=True),
    Column('role', String(100)),
    Column('joined_at', DateTime, default=datetime.utcnow)
)


class Team(Base):
    __tablename__ = "teams"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    coordination_pattern = Column(String(50))  # sequential_pipeline, parallel_assembly, etc.
    communication_rules = Column(JSON, default=dict)
    shared_memory = Column(JSON, default=dict)
    goal = Column(String(500))  # Team-level objective
    template_type = Column(String(50))  # customer_success, rfp_acceleration, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    agents = relationship("Agent", secondary=team_members, back_populates="teams")
    sessions = relationship("Session", back_populates="team")