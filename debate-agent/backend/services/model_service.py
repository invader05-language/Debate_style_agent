"""
AI Model management service.
"""

import time
import logging
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.models.ai_model import AIModel
from backend.adapters.factory import AdapterFactory

logger = logging.getLogger(__name__)


class ModelService:
    """Service for AI model CRUD and testing."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_models(self, include_inactive: bool = False):
        """List all AI models."""
        query = select(AIModel)
        if not include_inactive:
            query = query.where(AIModel.is_active == True)
        query = query.order_by(AIModel.created_at.desc())
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_model(self, model_id: str) -> Optional[AIModel]:
        """Get model by ID."""
        query = select(AIModel).where(AIModel.id == model_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create_model(self, **kwargs) -> AIModel:
        """Create a new AI model."""
        model = AIModel(**kwargs)
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return model

    async def update_model(self, model_id: str, **kwargs) -> Optional[AIModel]:
        """Update an AI model."""
        model = await self.get_model(model_id)
        if not model:
            return None
        for key, value in kwargs.items():
            if value is not None and hasattr(model, key):
                setattr(model, key, value)
        await self.db.commit()
        await self.db.refresh(model)
        return model

    async def delete_model(self, model_id: str) -> bool:
        """Delete an AI model."""
        model = await self.get_model(model_id)
        if not model:
            return False
        await self.db.delete(model)
        await self.db.commit()
        return True

    async def test_model(self, model_id: str) -> dict:
        """Test an AI model by sending a simple request."""
        from datetime import datetime

        model = await self.get_model(model_id)
        if not model:
            return {"model_id": model_id, "status": "failed", "error": "Model not found"}

        try:
            adapter = AdapterFactory.from_db_model(model)
            start = time.time()
            response = await adapter.chat(
                [{"role": "user", "content": "Hello, please respond with a short greeting."}],
                max_tokens=50,
            )
            latency = (time.time() - start) * 1000

            model.last_tested_at = datetime.utcnow()
            model.last_test_status = "success"
            await self.db.commit()

            return {
                "model_id": model_id,
                "status": "success",
                "latency_ms": round(latency, 2),
                "response_preview": response[:200] if response else "",
            }
        except Exception as e:
            logger.exception(f"Model test failed for {model_id}: {e}")
            model.last_tested_at = datetime.utcnow()
            model.last_test_status = "failed"
            await self.db.commit()

            return {
                "model_id": model_id,
                "status": "failed",
                "error": str(e),
            }
