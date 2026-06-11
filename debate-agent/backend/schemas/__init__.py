"""
Pydantic schemas for Multi-AI Debate Agent API.
"""

from backend.schemas.debate import (
    DebateCreate, DebateResponse, DebateListResponse,
    MessageResponse, VerdictResponse
)
from backend.schemas.memory import (
    MemoryCreate, MemoryResponse, MemorySearchResponse
)

__all__ = [
    "DebateCreate", "DebateResponse", "DebateListResponse",
    "MessageResponse", "VerdictResponse",
    "MemoryCreate", "MemoryResponse", "MemorySearchResponse"
]
