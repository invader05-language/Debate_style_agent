"""
Think engine service.
Business logic for multi-model thinking/collaboration.
"""

import logging
from typing import Optional, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.models.task import Task
from backend.models.task_message import TaskMessage
from backend.models.ai_model import AIModel
from backend.adapters.factory import AdapterFactory

logger = logging.getLogger(__name__)

THINK_SYSTEM_PROMPTS = {
    "quick": "你是一个快速分析助手。请用简洁的语言分析以下主题，给出核心观点和关键洞察。",
    "standard": "你是一个深度分析助手。请从多个角度分析以下主题，包括：核心观点、支持论据、潜在风险、行动建议。",
    "deep": "你是一个专家级分析助手。请对以下主题进行全面深入的分析，包括：背景与现状、核心问题、多维度分析（技术/商业/用户/风险）、关键洞察、具体行动方案、预期结果与风险评估。",
}


class ThinkService:
    """Service for think/collaboration operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_session(self, topic: str, depth: str = "standard", models: List[str] = None) -> Task:
        """Create a new think session."""
        task = Task(
            type="think",
            topic=topic,
            status="pending",
            config={"depth": depth, "models": models or ["mimo"]},
        )
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def get_session(self, task_id: str) -> Optional[Task]:
        """Get think session by ID."""
        query = select(Task).where(Task.id == task_id, Task.type == "think")
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def list_sessions(self, page: int = 1, page_size: int = 10):
        """List think sessions with pagination."""
        from sqlalchemy import func

        count_query = select(func.count(Task.id)).where(Task.type == "think")
        result = await self.db.execute(count_query)
        total = result.scalar()

        query = (
            select(Task)
            .where(Task.type == "think")
            .order_by(Task.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self.db.execute(query)
        sessions = result.scalars().all()

        return sessions, total

    async def run_session(self, task_id: str) -> Task:
        """Execute the think session with AI models."""
        task = await self.get_session(task_id)
        if not task:
            raise ValueError("Think session not found")
        if task.status != "pending":
            raise ValueError(f"Think session is not pending (status: {task.status})")

        task.status = "running"
        await self.db.commit()

        config = task.config or {}
        depth = config.get("depth", "standard")
        model_names = config.get("models", ["mimo"])
        system_prompt = THINK_SYSTEM_PROMPTS.get(depth, THINK_SYSTEM_PROMPTS["standard"])

        try:
            all_responses = []

            for model_name in model_names:
                # Get model from database
                model_query = select(AIModel).where(AIModel.name == model_name, AIModel.is_active == True)
                model_result = await self.db.execute(model_query)
                db_model = model_result.scalar_one_or_none()

                if not db_model:
                    logger.warning(f"Model {model_name} not found or inactive, skipping")
                    continue

                # Create adapter
                adapter = AdapterFactory.from_db_model(db_model)

                # Build messages
                messages = [{"role": "user", "content": f"请分析以下主题：\n\n{task.topic}"}]

                # Get response
                response_text = await adapter.chat(messages, system_prompt=system_prompt)

                # Save message
                task_msg = TaskMessage(
                    task_id=task.id,
                    model_id=db_model.id,
                    role="thinker",
                    round_number=1,
                    content=response_text,
                )
                self.db.add(task_msg)
                all_responses.append(response_text)

            # Synthesize if multiple models
            synthesis = ""
            if len(all_responses) > 1:
                synthesis = await self._synthesize(task.topic, all_responses)
            elif all_responses:
                synthesis = all_responses[0]

            # Update task
            task.status = "completed"
            task.completed_at = datetime.utcnow()
            task.result = {
                "synthesis": synthesis,
                "insights": self._extract_insights(synthesis),
            }
            await self.db.commit()

        except Exception as e:
            logger.exception(f"Think session {task_id} failed: {e}")
            task.status = "failed"
            task.result = {"error": str(e)}
            await self.db.commit()
            raise

        return task

    async def _synthesize(self, topic: str, responses: List[str]) -> str:
        """Synthesize multiple model responses into a unified analysis."""
        combined = "\n\n---\n\n".join([f"分析 {i+1}:\n{r}" for i, r in enumerate(responses)])

        synthesis_prompt = f"""你是一个综合分析专家。以下是对主题「{topic}」的多个AI模型分析结果。
请将这些分析综合成一个统一、全面的分析报告，保留最有价值的洞察，消除重复内容。

{combined}

请输出综合分析报告："""

        # Use first available model for synthesis
        model_query = select(AIModel).where(AIModel.is_active == True).limit(1)
        result = await self.db.execute(model_query)
        db_model = result.scalar_one_or_none()

        if not db_model:
            return responses[0]

        adapter = AdapterFactory.from_db_model(db_model)
        messages = [{"role": "user", "content": synthesis_prompt}]
        return await adapter.chat(messages, system_prompt="你是综合分析专家，请输出结构化的分析报告。")

    def _extract_insights(self, text: str) -> List[str]:
        """Extract key insights from synthesis text."""
        insights = []
        for line in text.split("\n"):
            line = line.strip()
            if line.startswith(("- ", "* ", "• ")) or (len(line) > 2 and line[0].isdigit() and line[1] in ".、"):
                insight = line.lstrip("-*•0123456789.、 ").strip()
                if insight and len(insight) > 5:
                    insights.append(insight)
        return insights[:10]
