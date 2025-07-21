from sqlalchemy import Column, String, JSON, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base


class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    capabilities = Column(JSON, default=list)
    beliefs = Column(JSON, default=dict)
    goals = Column(JSON, default=list)
    constraints = Column(JSON, default=list)
    memory = Column(JSON, default=dict)
    template_type = Column(String(50))  # triage_specialist, solution_researcher, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    teams = relationship("Team", secondary="team_members", back_populates="agents")