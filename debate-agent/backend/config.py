"""
Backend configuration for Multi-AI Debate Agent.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


class BackendConfig:
    """Backend configuration."""

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/debate_agent"
    )

    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # FastAPI
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # CORS
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

    # WebSocket
    WS_HEARTBEAT: int = int(os.getenv("WS_HEARTBEAT", "30"))  # seconds

    # JWT Authentication
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "debate-agent-secret-key-change-in-production")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "1440"))  # 24 hours

    # AI API Keys
    MIMO_API_KEY: str = os.getenv("MIMO_API_KEY", "")
    MIMO_API_URL: str = os.getenv("MIMO_API_URL", "https://token-plan-sgp.xiaomimimo.com/v1")
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_API_URL: str = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1")

    # SiliconFlow (硅基流动) — unified model platform
    SILICONFLOW_API_KEY: str = os.getenv("SILICONFLOW_API_KEY", "")
    SILICONFLOW_API_URL: str = os.getenv("SILICONFLOW_API_URL", "https://api.siliconflow.cn/v1")

    # Qwen3.5-397B model config (replaces Qwen3-235B which is disabled on SiliconFlow)
    QWEN3_235B_MODEL_ID: str = os.getenv("QWEN3_235B_MODEL_ID", "Qwen/Qwen3.5-397B-A17B")
    QWEN3_235B_MAX_TOKENS: int = int(os.getenv("QWEN3_235B_MAX_TOKENS", "120000"))
    QWEN3_235B_TEMPERATURE: float = float(os.getenv("QWEN3_235B_TEMPERATURE", "0.7"))
    QWEN3_235B_ENABLE_THINKING: bool = os.getenv("QWEN3_235B_ENABLE_THINKING", "true").lower() == "true"
    QWEN3_235B_THINKING_BUDGET: int = int(os.getenv("QWEN3_235B_THINKING_BUDGET", "16384"))

    # Qwen2.5-72B model config
    QWEN25_72B_MODEL_ID: str = os.getenv("QWEN25_72B_MODEL_ID", "Qwen/Qwen2.5-72B-Instruct")
    QWEN25_72B_MAX_TOKENS: int = int(os.getenv("QWEN25_72B_MAX_TOKENS", "120000"))
    QWEN25_72B_TEMPERATURE: float = float(os.getenv("QWEN25_72B_TEMPERATURE", "0.7"))

    # Kimi K2.6 model config (replaces K2 which is disabled on SiliconFlow)
    KIMI_K2_MODEL_ID: str = os.getenv("KIMI_K2_MODEL_ID", "Pro/moonshotai/Kimi-K2.6")
    KIMI_K2_MAX_TOKENS: int = int(os.getenv("KIMI_K2_MAX_TOKENS", "120000"))
    KIMI_K2_TEMPERATURE: float = float(os.getenv("KIMI_K2_TEMPERATURE", "0.7"))

    # DeepSeek V4 Pro model config
    DEEPSEEK_V4_MODEL_ID: str = os.getenv("DEEPSEEK_V4_MODEL_ID", "deepseek-ai/DeepSeek-V4-Pro")
    DEEPSEEK_V4_MAX_TOKENS: int = int(os.getenv("DEEPSEEK_V4_MAX_TOKENS", "1038000"))
    DEEPSEEK_V4_TEMPERATURE: float = float(os.getenv("DEEPSEEK_V4_TEMPERATURE", "0.7"))


config = BackendConfig()
