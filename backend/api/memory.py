"""
Memory API endpoints for Multi-AI Debate Agent.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.database import get_db
from backend.cache import cache
from backend.schemas.memory import MemoryCreate, MemoryResponse, MemorySearchResponse
from backend.models.memory import MemoryModel
from backend.services.embedding_service import embedding_service

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
    use_semantic: bool = Query(default=True, description="是否使用语义搜索"),
    db: AsyncSession = Depends(get_db)
):
    """搜索记忆 (支持语义搜索)"""
    # Try cache first
    cached = await cache.get_memory_search(q)
    if cached:
        return MemorySearchResponse(
            memories=[MemoryResponse(**m) for m in cached],
            total=len(cached),
            query=q
        )

    memories = []

    # Try semantic search with pgvector
    if use_semantic:
        embedding = await embedding_service.get_embedding(q)
        if embedding:
            from sqlalchemy import text
            stmt = text("""
                SELECT id, topic, debate_summary, outcome, confidence,
                       tags, lessons_learned, created_at,
                       1 - (embedding <=> :query_embedding) as similarity
                FROM memories
                WHERE embedding IS NOT NULL
                ORDER BY embedding <=> :query_embedding
                LIMIT :limit
            """)
            result = await db.execute(stmt, {
                "query_embedding": str(embedding),
                "limit": limit
            })
            rows = result.fetchall()

            for row in rows:
                memories.append(MemoryResponse(
                    id=str(row.id),
                    topic=row.topic,
                    debate_summary=row.debate_summary,
                    outcome=row.outcome,
                    confidence=row.confidence,
                    tags=row.tags or [],
                    lessons_learned=row.lessons_learned or [],
                    created_at=row.created_at.isoformat() if row.created_at else None
                ))

    # Fallback to ILIKE text search if no semantic results
    if not memories:
        query = select(MemoryModel).where(
            MemoryModel.topic.ilike(f"%{q}%") |
            MemoryModel.debate_summary.ilike(f"%{q}%")
        ).limit(limit)
        result = await db.execute(query)
        db_memories = result.scalars().all()

        memories = [
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
            for m in db_memories
        ]

    # Cache the result
    await cache.set_memory_search(q, [m.dict() for m in memories])

    return MemorySearchResponse(
        memories=memories,
        total=len(memories),
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


@router.post("/memories/{memory_id}/generate-embedding")
async def generate_embedding(
    memory_id: str,
    db: AsyncSession = Depends(get_db)
):
    """为记忆生成向量嵌入"""
    from sqlalchemy import select

    query = select(MemoryModel).where(MemoryModel.id == memory_id)
    result = await db.execute(query)
    memory = result.scalar_one_or_none()

    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")

    # Generate embedding from topic + debate_summary
    text_to_embed = f"{memory.topic} {memory.debate_summary}"
    embedding = await embedding_service.get_embedding(text_to_embed)

    if not embedding:
        raise HTTPException(status_code=500, detail="Failed to generate embedding")

    # Update memory with embedding
    memory.embedding = embedding
    await db.commit()

    return {"message": "Embedding generated successfully", "memory_id": memory_id}


@router.post("/memories/generate-all-embeddings")
async def generate_all_embeddings(
    db: AsyncSession = Depends(get_db)
):
    """为所有没有嵌入的记忆生成向量嵌入"""
    from sqlalchemy import select, func

    # Get memories without embeddings
    query = select(MemoryModel).where(MemoryModel.embedding.is_(None))
    result = await db.execute(query)
    memories = result.scalars().all()

    if not memories:
        return {"message": "All memories already have embeddings", "count": 0}

    # Generate embeddings in batch
    texts = [f"{m.topic} {m.debate_summary}" for m in memories]
    embeddings = await embedding_service.get_embeddings_batch(texts)

    # Update memories
    updated_count = 0
    for memory, embedding in zip(memories, embeddings):
        if embedding:
            memory.embedding = embedding
            updated_count += 1

    await db.commit()

    return {
        "message": f"Generated embeddings for {updated_count} memories",
        "total": len(memories),
        "updated": updated_count
    }
