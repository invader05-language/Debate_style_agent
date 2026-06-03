"""
Memory API endpoints for Multi-AI Debate Agent.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_db
from backend.cache import cache
from backend.schemas.memory import MemoryCreate, MemoryResponse, MemorySearchResponse
from backend.models.memory import MemoryModel

router = APIRouter()


@router.get("/memories", response_model=MemorySearchResponse)
async def list_memories(
    page: int = 1,
    page_size: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """获取记忆列表"""
    from sqlalchemy import select, func

    # Get total count
    count_query = select(func.count(MemoryModel.id))
    result = await db.execute(count_query)
    total = result.scalar()

    # Get memories
    query = select(MemoryModel).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    memories = result.scalars().all()

    return MemorySearchResponse(
        memories=[
            MemoryResponse(
                id=str(m.id),
                topic=m.topic,
                debate_summary=m.debate_summary,
                outcome=m.outcome,
                confidence=m.confidence,
                tags=m.tags,
                lessons_learned=m.lessons_learned,
                created_at=m.created_at.isoformat() if m.created_at else None
            )
            for m in memories
        ],
        total=total,
        query=""
    )


@router.get("/memories/search", response_model=MemorySearchResponse)
async def search_memories(
    q: str = Query(..., min_length=1, description="搜索关键词"),
    limit: int = Query(default=10, ge=1, le=100, description="返回数量"),
    db: AsyncSession = Depends(get_db)
):
    """搜索记忆"""
    # Try cache first
    cached = await cache.get_memory_search(q)
    if cached:
        return MemorySearchResponse(
            memories=[MemoryResponse(**m) for m in cached],
            total=len(cached),
            query=q
        )

    # Search in database
    from sqlalchemy import select
    query = select(MemoryModel).where(
        MemoryModel.topic.ilike(f"%{q}%") |
        MemoryModel.debate_summary.ilike(f"%{q}%")
    ).limit(limit)
    result = await db.execute(query)
    memories = result.scalars().all()

    response_memories = [
        MemoryResponse(
            id=str(m.id),
            topic=m.topic,
            debate_summary=m.debate_summary,
            outcome=m.outcome,
            confidence=m.confidence,
            tags=m.tags,
            lessons_learned=m.lessons_learned,
            created_at=m.created_at.isoformat() if m.created_at else None
        )
        for m in memories
    ]

    # Cache the result
    await cache.set_memory_search(q, [m.dict() for m in response_memories])

    return MemorySearchResponse(
        memories=response_memories,
        total=len(response_memories),
        query=q
    )


@router.get("/memories/{memory_id}", response_model=MemoryResponse)
async def get_memory(
    memory_id: str,
    db: AsyncSession = Depends(get_db)
):
    """获取记忆详情"""
    from sqlalchemy import select
    query = select(MemoryModel).where(MemoryModel.id == memory_id)
    result = await db.execute(query)
    memory = result.scalar_one_or_none()

    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")

    return MemoryResponse(
        id=str(memory.id),
        topic=memory.topic,
        debate_summary=memory.debate_summary,
        outcome=memory.outcome,
        confidence=memory.confidence,
        tags=memory.tags,
        lessons_learned=memory.lessons_learned,
        created_at=memory.created_at.isoformat() if memory.created_at else None
    )
