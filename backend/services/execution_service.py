"""
Execution service for Multi-AI Debate Agent.
Business logic for execution operations.
"""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.models.execution import ExecutionModel
from execution.executor import CodeExecutor


class ExecutionService:
    """Service for execution operations."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.executor = CodeExecutor()

    async def create_execution(self, debate_id: str,
                              code_generated: str) -> ExecutionModel:
        """Create a new execution."""
        execution = ExecutionModel(
            debate_id=debate_id,
            status="pending",
            code_generated=code_generated
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

    async def execute_code(self, execution: ExecutionModel) -> ExecutionModel:
        """Execute code and update execution record."""
        from datetime import datetime

        try:
            execution.status = "running"
            await self.db.commit()

            # Execute code
            result = await self.executor.execute(execution.code_generated, "python")

            # Update execution
            execution.status = "success" if result.success else "failed"
            execution.execution_result = result.output
            execution.error_message = result.error
            execution.completed_at = datetime.utcnow()

            await self.db.commit()
            return execution

        except Exception as e:
            execution.status = "failed"
            execution.error_message = str(e)
            execution.completed_at = datetime.utcnow()
            await self.db.commit()
            raise e
