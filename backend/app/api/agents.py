from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.schemas.agent import AgentCreate, AgentResponse, AgentUpdate, AgentTemplate
from app.services.agent_service import AgentService
from app.services.template_service import TemplateService

router = APIRouter()


@router.post("/", response_model=AgentResponse)
async def create_agent(
    agent_data: AgentCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new agent with specified capabilities"""
    service = AgentService(db)
    return await service.create_agent(agent_data)


@router.post("/from-template/{template_name}", response_model=AgentResponse)
async def create_agent_from_template(
    template_name: str,
    custom_name: str = None,
    db: AsyncSession = Depends(get_db)
):
    """Create a new agent from a template"""
    try:
        agent_config = TemplateService.create_agent_from_template(template_name, custom_name)
        agent_data = AgentCreate(**agent_config)
        service = AgentService(db)
        return await service.create_agent(agent_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=List[AgentResponse])
async def list_agents(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all available agents"""
    service = AgentService(db)
    return await service.list_agents(skip=skip, limit=limit)


@router.get("/templates", response_model=List[dict])
async def list_agent_templates():
    """List available agent templates from PRD v22"""
    return TemplateService.get_agent_templates()


@router.get("/team-templates", response_model=List[AgentTemplate])
async def list_team_templates():
    """List available team templates from PRD v22"""
    return TemplateService.get_team_templates()


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific agent by ID"""
    service = AgentService(db)
    agent = await service.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: UUID,
    agent_data: AgentUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an agent's configuration"""
    service = AgentService(db)
    agent = await service.update_agent(agent_id, agent_data)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.delete("/{agent_id}")
async def delete_agent(
    agent_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Delete an agent"""
    service = AgentService(db)
    success = await service.delete_agent(agent_id)
    if not success:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"message": "Agent deleted successfully"}