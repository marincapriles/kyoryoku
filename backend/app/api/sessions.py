from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_sessions():
    """List all sessions"""
    return {"message": "Sessions endpoint - to be implemented"}