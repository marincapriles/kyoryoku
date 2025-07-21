from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import socketio

from app.core.config import settings
from app.api import agents, teams, sessions, health, llm
from app.core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    # Add cleanup code here if needed


app = FastAPI(
    title="Kyoryoku API",
    description="Multi-agent AI collaboration platform",
    version="0.1.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Socket.IO setup
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=settings.CORS_ORIGINS
)
socket_app = socketio.ASGIApp(sio, app)

# Include routers
app.include_router(health.router, prefix="/api/health", tags=["health"])
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
app.include_router(teams.router, prefix="/api/teams", tags=["teams"])
app.include_router(sessions.router, prefix="/api/sessions", tags=["sessions"])
app.include_router(llm.router, prefix="/api/llm", tags=["llm"])


@app.get("/")
async def root():
    return {"message": "Kyoryoku API is running"}


# WebSocket event handlers
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    await sio.emit('connected', {'message': 'Connected to Kyoryoku server'}, to=sid)


@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")


@sio.event
async def agent_message(sid, data):
    # Handle agent messages
    await sio.emit('agent_response', data, to=sid)