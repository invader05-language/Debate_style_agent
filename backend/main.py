"""
FastAPI entry point for Multi-AI Debate Agent Web Backend.
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.api import debate, memory, execution
from backend.websocket import debate_ws
from backend.database import init_db
from backend.config import config

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    await init_db()
    yield
    # Shutdown
    pass


app = FastAPI(
    title="Multi-AI Debate Agent API",
    description="辩论式多AI协作系统 API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(debate.router, prefix="/api", tags=["debates"])
app.include_router(memory.router, prefix="/api", tags=["memories"])
app.include_router(execution.router, prefix="/api", tags=["executions"])
app.include_router(debate_ws.router, tags=["websocket"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Multi-AI Debate Agent API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}
