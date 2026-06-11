"""
Analytics API endpoints.
"""

from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text
from backend.database import get_db
from backend.models.debate import DebateModel
from backend.models.task import Task
from backend.models.message import MessageModel
from backend.models.task_message import TaskMessage

router = APIRouter()


@router.get("/analytics/overview")
async def get_analytics_overview(db: AsyncSession = Depends(get_db)):
    """获取分析概览"""
    # Debate stats
    total_debates = (await db.execute(select(func.count(DebateModel.id)))).scalar() or 0
    completed_debates = (await db.execute(
        select(func.count(DebateModel.id)).where(DebateModel.status == "completed")
    )).scalar() or 0

    # Think stats
    total_thinks = (await db.execute(
        select(func.count(Task.id)).where(Task.type == "think")
    )).scalar() or 0

    # Average rounds per debate
    avg_msg_result = await db.execute(
        select(func.count(MessageModel.id)).where(MessageModel.debate_id.isnot(None))
    )
    total_msgs = avg_msg_result.scalar() or 0
    avg_rounds = round(total_msgs / max(completed_debates, 1), 1)

    # Most active models
    model_usage = await db.execute(
        select(MessageModel.model_used, func.count(MessageModel.id))
        .group_by(MessageModel.model_used)
        .order_by(func.count(MessageModel.id).desc())
        .limit(5)
    )
    top_models = [{"model": row[0], "usage_count": row[1]} for row in model_usage.fetchall()]

    return {
        "total_debates": total_debates,
        "completed_debates": completed_debates,
        "total_thinks": total_thinks,
        "total_messages": total_msgs,
        "avg_rounds_per_debate": avg_rounds,
        "top_models": top_models,
    }


@router.get("/analytics/activity")
async def get_activity_trend(
    days: int = Query(default=30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
):
    """获取活动趋势（按天）"""
    start_date = datetime.utcnow() - timedelta(days=days)

    # Debates per day
    debate_trend = await db.execute(
        select(
            func.date(DebateModel.created_at).label("date"),
            func.count(DebateModel.id).label("count"),
        )
        .where(DebateModel.created_at >= start_date)
        .group_by(func.date(DebateModel.created_at))
        .order_by(func.date(DebateModel.created_at))
    )
    debates_by_day = {str(row.date): row.count for row in debate_trend.fetchall()}

    # Tasks per day
    task_trend = await db.execute(
        select(
            func.date(Task.created_at).label("date"),
            func.count(Task.id).label("count"),
        )
        .where(Task.created_at >= start_date)
        .group_by(func.date(Task.created_at))
        .order_by(func.date(Task.created_at))
    )
    tasks_by_day = {str(row.date): row.count for row in task_trend.fetchall()}

    # Merge into timeline
    all_dates = sorted(set(list(debates_by_day.keys()) + list(tasks_by_day.keys())))
    timeline = [
        {
            "date": d,
            "debates": debates_by_day.get(d, 0),
            "tasks": tasks_by_day.get(d, 0),
        }
        for d in all_dates
    ]

    return {"timeline": timeline, "days": days}
