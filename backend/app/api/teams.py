from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_teams():
    """List all teams"""
    return {"message": "Teams endpoint - to be implemented"}