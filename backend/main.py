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
from backend.logging_config import setup_logging
from backend.middleware import (
    request_id_middleware, rate_limit_middleware,
    debate_agent_error_handler, generic_error_handler,
    DebateAgentError
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    setup_logging(config.DEBUG and "DEBUG" or "INFO")
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

# Error handlers
app.add_exception_handler(DebateAgentError, debate_agent_error_handler)
app.add_exception_handler(Exception, generic_error_handler)

# Middleware (order matters: last added = first executed)
app.middleware("http")(rate_limit_middleware)
app.middleware("http")(request_id_middleware)

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
