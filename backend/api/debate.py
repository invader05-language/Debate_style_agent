"""
Debate API endpoints for Multi-AI Debate Agent.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_db, AsyncSessionLocal
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
    """开始辩论 (同步执行，等待完成)"""
    import logging
    from sqlalchemy import select
    from datetime import datetime

    logger = logging.getLogger(__name__)

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

    debate_id_str = str(debate.id)
    debate_topic = debate.topic

    # Run debate synchronously in this request
    try:
        await _run_debate(debate_id_str, debate_topic, db)
    except Exception as e:
        logger.exception(f"Debate failed: {e}")

    # Refresh debate from db
    await db.refresh(debate)

    return DebateResponse(
        id=debate_id_str,
        topic=debate_topic,
        status=debate.status,
        created_at=debate.created_at.isoformat() if debate.created_at else None,
        completed_at=debate.completed_at.isoformat() if debate.completed_at else None,
        verdict=debate.verdict,
        action_plan=debate.action_plan
    )


async def _run_debate(debate_id: str, topic: str, db: AsyncSession = None):
    """Run debate, using provided db session or creating its own."""
    import logging
    from datetime import datetime
    from sqlalchemy import select
    from backend.websocket.debate_ws import (
        broadcast_debate_message, broadcast_debate_status, broadcast_debate_verdict
    )
    from debate.protocol import Message

    logger = logging.getLogger(__name__)

    # Create engine and config
    memory_store = MemoryStore()
    engine = DebateEngine(memory_store=memory_store)
    config = DebateConfig(
        topic=topic,
        max_rounds=3,
        models={"pro": "deepseek", "con": "deepseek", "judge": "deepseek"}
    )

    # Wire WebSocket callback to engine
    async def on_message(message: Message):
        try:
            await broadcast_debate_message(
                debate_id=debate_id,
                role=message.role.value if hasattr(message.role, 'value') else str(message.role),
                content=message.content,
                round_number=message.round_number,
                model_used=message.model_used
            )
        except Exception:
            pass  # WebSocket broadcast failure shouldn't stop debate

    engine.set_on_message_callback(on_message)

    async def _save_results(db_session: AsyncSession, result):
        """Save debate results to database."""
        query = select(DebateModel).where(DebateModel.id == debate_id)
        db_result = await db_session.execute(query)
        debate = db_result.scalar_one_or_none()
        if not debate:
            logger.error(f"Debate {debate_id} not found in database")
            return

        debate.status = "completed"
        debate.completed_at = datetime.utcnow()
        debate.verdict = result.verdict.dict() if result.verdict else None
        debate.action_plan = result.verdict.action_plan if result.verdict else None

        for r in result.rounds:
            for msg in [r.pro_message, r.con_message, r.judge_message]:
                if msg:
                    db_msg = MessageModel(
                        debate_id=debate.id,
                        round_number=msg.round_number,
                        role=msg.role,
                        content=msg.content,
                        model_used=msg.model_used,
                        confidence=msg.confidence
                    )
                    db_session.add(db_msg)

        await db_session.commit()
        await cache.delete(f"debate:{debate_id}")

        if result.verdict:
            await broadcast_debate_verdict(debate_id, result.verdict.dict())
        await broadcast_debate_status(debate_id, "completed", "辩论完成")

    try:
        await broadcast_debate_status(debate_id, "running", "辩论开始")
        logger.info(f"Starting debate {debate_id}: {topic}")

        result = await engine.start_debate(config)
        logger.info(f"Debate {debate_id} completed with {len(result.rounds)} rounds")

        if db is not None:
            await _save_results(db, result)
        else:
            async with AsyncSessionLocal() as own_db:
                await _save_results(own_db, result)

    except Exception as e:
        logger.exception(f"Debate {debate_id} failed: {e}")
        try:
            if db is not None:
                query = select(DebateModel).where(DebateModel.id == debate_id)
                db_result = await db.execute(query)
                debate = db_result.scalar_one_or_none()
                if debate:
                    debate.status = "failed"
                    await db.commit()
            else:
                async with AsyncSessionLocal() as own_db:
                    query = select(DebateModel).where(DebateModel.id == debate_id)
                    db_result = await own_db.execute(query)
                    debate = db_result.scalar_one_or_none()
                    if debate:
                        debate.status = "failed"
                        await own_db.commit()
        except Exception:
            pass
        await broadcast_debate_status(debate_id, "failed", f"辩论失败: {str(e)}")
