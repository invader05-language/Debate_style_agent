"""
Execution service for Multi-AI Debate Agent.
Business logic for execution operations.
"""

import logging
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from backend.models.execution import ExecutionModel
from execution.executor import CodeExecutor

logger = logging.getLogger(__name__)


class ExecutionService:
    """Service for execution operations."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.executor = CodeExecutor(use_sandbox=True)

    async def create_execution(self, debate_id: str,
                               code_generated: str = "") -> ExecutionModel:
        """Create a new execution record."""
        execution = ExecutionModel(
            debate_id=debate_id,
            status="pending",
            code_generated=code_generated,
        )
        self.db.add(execution)
        await self.db.commit()
        await self.db.refresh(execution)
        return execution

    async def get_execution(self, execution_id: str) -> Optional[ExecutionModel]:
        """Get execution by ID."""
        query = select(ExecutionModel).where(ExecutionModel.id == execution_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def list_by_debate(self, debate_id: str) -> List[ExecutionModel]:
        """List all executions for a debate."""
        query = (
            select(ExecutionModel)
            .where(ExecutionModel.debate_id == debate_id)
            .order_by(ExecutionModel.created_at.desc())
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def execute_code(self, execution: ExecutionModel) -> ExecutionModel:
        """Execute code directly and update record."""
        try:
            execution.status = "running"
            await self.db.commit()

            result = await self.executor.execute(
                execution.code_generated, "python"
            )

            execution.status = "success" if result.success else "failed"
            execution.execution_result = result.output
            execution.error_message = result.error if not result.success else ""
            execution.completed_at = datetime.utcnow()

            await self.db.commit()
            return execution

        except Exception as e:
            execution.status = "failed"
            execution.error_message = str(e)
            execution.completed_at = datetime.utcnow()
            await self.db.commit()
            raise

    async def generate_and_execute(
        self,
        execution: ExecutionModel,
        action_plan: List[str],
        language: str = "python",
        max_retries: int = 3,
    ) -> ExecutionModel:
        """
        Generate code from action_plan and execute with auto-fix.
        """
        try:
            execution.status = "running"
            await self.db.commit()

            result = await self.executor.generate_and_execute(
                action_plan=action_plan,
                language=language,
                max_retries=max_retries,
            )

            execution.status = "success" if result.success else "failed"
            execution.execution_result = result.output
            execution.error_message = result.error if not result.success else ""
            execution.completed_at = datetime.utcnow()

            await self.db.commit()
            return execution

        except Exception as e:
            logger.exception(f"generate_and_execute failed: {e}")
            execution.status = "failed"
            execution.error_message = str(e)
            execution.completed_at = datetime.utcnow()
            await self.db.commit()
            raise
