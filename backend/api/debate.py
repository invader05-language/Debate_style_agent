"""
Debate API endpoints for Multi-AI Debate Agent.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_db
from backend.cache import cache
from backend.schemas.debate import (
    DebateCreate, DebateResponse, DebateListResponse, MessageResponse
)
from backend.models.debate import DebateModel
from backend.models.message import MessageModel
from debate.engine import DebateEngine
from debate.protocol import DebateConfig
from memory.store import MemoryStore

router = APIRouter()


@router.post("/debates", response_model=DebateResponse, status_code=201)
async def create_debate(
    debate_create: DebateCreate,
    db: AsyncSession = Depends(get_db)
):
    """创建新辩论"""
    # Create debate in database
    debate = DebateModel(
        topic=debate_create.topic,
        status="pending"
    )
    db.add(debate)
    await db.commit()
    await db.refresh(debate)

    return DebateResponse(
        id=str(debate.id),
        topic=debate.topic,
        status=debate.status,
        created_at=debate.created_at.isoformat() if debate.created_at else None
    )


@router.get("/debates", response_model=DebateListResponse)
async def list_debates(
    page: int = 1,
    page_size: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """获取辩论列表"""
    from sqlalchemy import select, func

    # Get total count
    count_query = select(func.count(DebateModel.id))
    result = await db.execute(count_query)
    total = result.scalar()

    # Get debates
    query = select(DebateModel).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    debates = result.scalars().all()

    return DebateListResponse(
        debates=[
            DebateResponse(
                id=str(d.id),
                topic=d.topic,
                status=d.status,
                created_at=d.created_at.isoformat() if d.created_at else None,
                completed_at=d.completed_at.isoformat() if d.completed_at else None,
                verdict=d.verdict,
                action_plan=d.action_plan
            )
            for d in debates
        ],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/debates/{debate_id}", response_model=DebateResponse)
async def get_debate(
    debate_id: str,
    db: AsyncSession = Depends(get_db)
):
    """获取辩论详情"""
    # Try cache first
    cached = await cache.get_debate(debate_id)
    if cached:
        return DebateResponse(**cached)

    # Get from database
    from sqlalchemy import select
    query = select(DebateModel).where(DebateModel.id == debate_id)
    result = await db.execute(query)
    debate = result.scalar_one_or_none()

    if not debate:
        raise HTTPException(status_code=404, detail="Debate not found")

    # Get messages
    msg_query = select(MessageModel).where(MessageModel.debate_id == debate_id)
    msg_result = await db.execute(msg_query)
    messages = msg_result.scalars().all()

    response = DebateResponse(
        id=str(debate.id),
        topic=debate.topic,
        status=debate.status,
        created_at=debate.created_at.isoformat() if debate.created_at else None,
        completed_at=debate.completed_at.isoformat() if debate.completed_at else None,
        verdict=debate.verdict,
        action_plan=debate.action_plan,
        messages=[
            MessageResponse(
                id=str(m.id),
                debate_id=str(m.debate_id),
                round_number=m.round_number,
                role=m.role,
                content=m.content,
                model_used=m.model_used,
                confidence=m.confidence,
                created_at=m.created_at.isoformat() if m.created_at else None
            )
            for m in messages
        ]
    )

    # Cache the result
    await cache.set_debate(debate_id, response.dict())

    return response


@router.post("/debates/{debate_id}/start", response_model=DebateResponse)
async def start_debate(
    debate_id: str,
    db: AsyncSession = Depends(get_db)
):
    """开始辩论"""
    from sqlalchemy import select
    from datetime import datetime

    # Get debate
    query = select(DebateModel).where(DebateModel.id == debate_id)
    result = await db.execute(query)
    debate = result.scalar_one_or_none()

    if not debate:
        raise HTTPException(status_code=404, detail="Debate not found")

    if debate.status != "pending":
        raise HTTPException(status_code=400, detail="Debate already started")

    # Update status
    debate.status = "running"
    await db.commit()

    # Start debate engine
    memory_store = MemoryStore()
    engine = DebateEngine(memory_store=memory_store)

    # Create debate config
    debate_config = DebateConfig(
        topic=debate.topic,
        max_rounds=3,
        models={"pro": "mimo", "con": "deepseek", "judge": "mimo"}
    )

    # Run debate (async)
    import asyncio
    asyncio.create_task(_run_debate(db, engine, debate, debate_config))

    return DebateResponse(
        id=str(debate.id),
        topic=debate.topic,
        status=debate.status,
        created_at=debate.created_at.isoformat() if debate.created_at else None
    )


async def _run_debate(db: AsyncSession, engine: DebateEngine,
                      debate: DebateModel, config: DebateConfig):
    """Run debate in background."""
    from backend.websocket.debate_ws import (
        broadcast_debate_message, broadcast_debate_status, broadcast_debate_verdict
    )
    from debate.protocol import Message

    # Wire WebSocket callback to engine
    async def on_message(message: Message):
        await broadcast_debate_message(
            debate_id=str(debate.id),
            role=message.role.value if hasattr(message.role, 'value') else str(message.role),
            content=message.content,
            round_number=message.round_number,
            model_used=message.model_used
        )

    engine.set_on_message_callback(on_message)

    try:
        # Broadcast debate started
        await broadcast_debate_status(str(debate.id), "running", "辩论开始")

        # Run debate
        result = await engine.start_debate(config)

        # Update debate in database
        debate.status = "completed"
        debate.completed_at = datetime.utcnow()
        debate.verdict = result.verdict.dict() if result.verdict else None
        debate.action_plan = result.verdict.action_plan if result.verdict else None

        # Save messages
        for round in result.rounds:
            for msg in [round.pro_message, round.con_message, round.judge_message]:
                if msg:
                    db_msg = MessageModel(
                        debate_id=debate.id,
                        round_number=msg.round_number,
                        role=msg.role,
                        content=msg.content,
                        model_used=msg.model_used,
                        confidence=msg.confidence
                    )
                    db.add(db_msg)

        await db.commit()

        # Clear cache
        await cache.delete(f"debate:{debate.id}")

        # Broadcast verdict and completion
        if result.verdict:
            await broadcast_debate_verdict(str(debate.id), result.verdict.dict())
        await broadcast_debate_status(str(debate.id), "completed", "辩论完成")

    except Exception as e:
        debate.status = "failed"
        await db.commit()
        await broadcast_debate_status(str(debate.id), "failed", f"辩论失败: {str(e)}")
        raise e
