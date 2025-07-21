from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.services.session_service import SessionService
from app.schemas.session import SessionCreate, SessionUpdate, SessionResponse
from app.schemas.message import MessageResponse

router = APIRouter()


async def get_session_service(db: AsyncSession = Depends(get_db)) -> SessionService:
    return SessionService(db)


@router.post("/", response_model=SessionResponse)
async def create_session(
    session_data: SessionCreate,
    service: SessionService = Depends(get_session_service)
):
    """Create a new collaboration session"""
    try:
        session = await service.create_session(session_data)
        await service.db.commit()
        return session
    except Exception as e:
        await service.db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[SessionResponse])
async def list_sessions(
    skip: int = 0,
    limit: int = 100,
    service: SessionService = Depends(get_session_service)
):
    """List all sessions"""
    return await service.list_sessions(skip=skip, limit=limit)


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: UUID,
    service: SessionService = Depends(get_session_service)
):
    """Get a specific session"""
    session = await service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.post("/{session_id}/start", response_model=SessionResponse)
async def start_session(
    session_id: UUID,
    service: SessionService = Depends(get_session_service)
):
    """Start processing a session"""
    try:
        session = await service.start_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        await service.db.commit()
        return session
    except Exception as e:
        await service.db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}/messages", response_model=List[MessageResponse])
async def get_session_messages(
    session_id: UUID,
    service: SessionService = Depends(get_session_service)
):
    """Get all messages for a session"""
    messages = await service.get_session_messages(session_id)
    return messages


@router.post("/{session_id}/messages", response_model=MessageResponse)
async def add_human_message(
    session_id: UUID,
    content: str,
    service: SessionService = Depends(get_session_service)
):
    """Add a human message to the session"""
    try:
        message = await service.add_human_message(session_id, content)
        await service.db.commit()
        return message
    except Exception as e:
        await service.db.rollback()
        raise HTTPException(status_code=500, detail=str(e))