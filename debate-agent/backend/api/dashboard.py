"""
Dashboard API endpoints — aggregated stats for the home page.
"""

from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from backend.database import get_db
from backend.models.debate import DebateModel
from backend.models.memory import MemoryModel
from backend.models.task import Task
from backend.models.ai_model import AIModel

router = APIRouter()


@router.get("/dashboard/stats")
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    """获取仪表盘统计数据"""
    # Total debates
    debate_count = await db.execute(select(func.count(DebateModel.id)))
    total_debates = debate_count.scalar() or 0

    # Total think sessions
    think_count = await db.execute(
        select(func.count(Task.id)).where(Task.type == "think")
    )
    total_thinks = think_count.scalar() or 0

    # Total memories
    memory_count = await db.execute(select(func.count(MemoryModel.id)))
    total_memories = memory_count.scalar() or 0

    # Active models
    model_count = await db.execute(
        select(func.count(AIModel.id)).where(AIModel.is_active == True)
    )
    active_models = model_count.scalar() or 0

    # Recent activity (last 7 days)
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_debates = await db.execute(
        select(func.count(DebateModel.id)).where(DebateModel.created_at >= week_ago)
    )
    recent_debate_count = recent_debates.scalar() or 0

    recent_thinks = await db.execute(
        select(func.count(Task.id)).where(
            Task.type == "think", Task.created_at >= week_ago
        )
    )
    recent_think_count = recent_thinks.scalar() or 0

    # Completed vs running
    completed = await db.execute(
        select(func.count(DebateModel.id)).where(DebateModel.status == "completed")
    )
    completed_count = completed.scalar() or 0

    running = await db.execute(
        select(func.count(DebateModel.id)).where(DebateModel.status == "running")
    )
    running_count = running.scalar() or 0

    return {
        "total_debates": total_debates,
        "total_thinks": total_thinks,
        "total_memories": total_memories,
        "active_models": active_models,
        "recent_debates_7d": recent_debate_count,
        "recent_thinks_7d": recent_think_count,
        "completed_debates": completed_count,
        "running_debates": running_count,
    }


@router.get("/dashboard/recent-activity")
async def get_recent_activity(
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    """获取最近活动"""
    activities = []

    # Recent debates
    debate_query = (
        select(DebateModel)
        .order_by(DebateModel.created_at.desc())
        .limit(limit)
    )
    debate_result = await db.execute(debate_query)
    debates = debate_result.scalars().all()

    for d in debates:
        activities.append({
            "id": str(d.id),
            "type": "debate",
            "title": d.topic,
            "status": d.status,
            "created_at": d.created_at.isoformat() if d.created_at else None,
        })

    # Recent think sessions
    think_query = (
        select(Task)
        .where(Task.type == "think")
        .order_by(Task.created_at.desc())
        .limit(limit)
    )
    think_result = await db.execute(think_query)
    thinks = think_result.scalars().all()

    for t in thinks:
        activities.append({
            "id": str(t.id),
            "type": "think",
            "title": t.topic,
            "status": t.status,
            "created_at": t.created_at.isoformat() if t.created_at else None,
        })

    # Sort by created_at descending
    activities.sort(key=lambda x: x.get("created_at") or "", reverse=True)
    return {"activities": activities[:limit]}
