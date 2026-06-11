"""
Seed script — populates the database with initial FAQ and preset model data.
Models are routed through SiliconFlow (硅基流动) platform.
Run after migrations: python -m backend.seed
"""

import os
import asyncio
from backend.database import AsyncSessionLocal, init_db
from backend.models.faq import FAQ
from backend.models.ai_model import AIModel


FAQ_DATA = [
    {"question": "How do I switch between different LLM models?",
     "answer": "Go to Model Management page. All models are available through SiliconFlow (硅基流动) platform.",
     "category": "Models", "sort_order": 1},
    {"question": "Can multiple agents debate on the same topic simultaneously?",
     "answer": "Yes. In Debate Mode, you can assign different models (e.g. Qwen vs Kimi) to opposing sides.",
     "category": "Debate", "sort_order": 2},
    {"question": "Is my data used to train the underlying models?",
     "answer": "No. AuraSynth uses enterprise-grade APIs that do not use customer data for training.",
     "category": "Security", "sort_order": 3},
    {"question": "What is the Think Engine?",
     "answer": "The Think Engine lets multiple AI models independently analyze a problem, then synthesizes their insights.",
     "category": "Think", "sort_order": 4},
    {"question": "How does the Memory Bank work?",
     "answer": "The Memory Bank stores insights from past sessions. It supports semantic search via vector embeddings.",
     "category": "Memory", "sort_order": 5},
    {"question": "What is SiliconFlow (硅基流动)?",
     "answer": "SiliconFlow is a unified AI model platform that provides access to many models (Qwen, Kimi, DeepSeek, etc.) through a single API endpoint.",
     "category": "Platform", "sort_order": 6},
]

# All models routed through SiliconFlow (硅基流动)
SILICONFLOW_URL = os.getenv("SILICONFLOW_API_URL", "https://api.siliconflow.cn/v1")
SILICONFLOW_KEY = os.getenv("SILICONFLOW_API_KEY", "")

PRESET_MODELS = [
    {
        "name": "Qwen3.5-397B",
        "provider": "SiliconFlow",
        "model_id": "Qwen/Qwen3.5-397B-A17B",
        "api_url": SILICONFLOW_URL,
        "api_key": SILICONFLOW_KEY,
        "api_format": "openai",
        "max_tokens": 120000,
        "temperature": 0.7,
        "is_preset": True,
        "is_active": True,
        "icon": "sparkles",
        "color": "#6366f1",
    },
    {
        "name": "Qwen2.5-72B",
        "provider": "SiliconFlow",
        "model_id": "Qwen/Qwen2.5-72B-Instruct",
        "api_url": SILICONFLOW_URL,
        "api_key": SILICONFLOW_KEY,
        "api_format": "openai",
        "max_tokens": 131072,
        "temperature": 0.7,
        "is_preset": True,
        "is_active": True,
        "icon": "cpu",
        "color": "#8b5cf6",
    },
    {
        "name": "Kimi K2.6",
        "provider": "SiliconFlow",
        "model_id": "Pro/moonshotai/Kimi-K2.6",
        "api_url": SILICONFLOW_URL,
        "api_key": SILICONFLOW_KEY,
        "api_format": "openai",
        "max_tokens": 120000,
        "temperature": 0.7,
        "is_preset": True,
        "is_active": True,
        "icon": "moon",
        "color": "#f59e0b",
    },
    {
        "name": "DeepSeek V4 Pro",
        "provider": "SiliconFlow",
        "model_id": "deepseek-ai/DeepSeek-V4-Pro",
        "api_url": SILICONFLOW_URL,
        "api_key": SILICONFLOW_KEY,
        "api_format": "openai",
        "max_tokens": 1048576,
        "temperature": 0.7,
        "is_preset": True,
        "is_active": True,
        "icon": "brain",
        "color": "#10b981",
    },
]

# Additional models via direct API (not SiliconFlow)
MIMO_URL = os.getenv("MIMO_API_URL", "https://token-plan-sgp.xiaomimimo.com/v1")
MIMO_KEY = os.getenv("MIMO_API_KEY", "")

EXTRA_MODELS = [
    {
        "name": "MIMO v2.5 Pro",
        "provider": "Xiaomi",
        "model_id": "mimo-v2.5-pro",
        "api_url": MIMO_URL,
        "api_key": MIMO_KEY,
        "api_format": "openai",
        "max_tokens": 131072,
        "temperature": 0.7,
        "is_preset": True,
        "is_active": True,
        "icon": "zap",
        "color": "#f97316",
    },
]


async def seed():
    await init_db()
    async with AsyncSessionLocal() as db:
        from sqlalchemy import select

        # Seed FAQs
        existing = await db.execute(select(FAQ))
        if existing.scalars().first() is None:
            for faq_data in FAQ_DATA:
                db.add(FAQ(**faq_data))
            print(f"Seeded {len(FAQ_DATA)} FAQs")
        else:
            print("FAQs already exist, skipping.")

        # Seed preset models (SiliconFlow)
        existing_models = await db.execute(select(AIModel))
        if existing_models.scalars().first() is None:
            for model_data in PRESET_MODELS:
                db.add(AIModel(**model_data))
            print(f"Seeded {len(PRESET_MODELS)} preset models (via SiliconFlow)")
        else:
            print("Models already exist, skipping.")

        # Seed extra models (direct API like MIMO)
        for model_data in EXTRA_MODELS:
            existing = await db.execute(
                select(AIModel).where(AIModel.model_id == model_data["model_id"])
            )
            if existing.scalars().first() is None:
                db.add(AIModel(**model_data))
                print(f"Seeded extra model: {model_data['name']}")
            else:
                print(f"Extra model {model_data['name']} already exists, skipping.")

        await db.commit()
    print("Seed complete.")


if __name__ == "__main__":
    asyncio.run(seed())
