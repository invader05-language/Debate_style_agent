"""
Configuration management for Multi-AI Debate Agent.
Uses .env file for sensitive configuration (API Keys, database connection, etc.).
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)


class Config:
    """Application configuration."""

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/debate_agent"
    )

    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # MIMO API
    MIMO_API_KEY: str = os.getenv("MIMO_API_KEY", "")
    MIMO_API_URL: str = os.getenv("MIMO_API_URL", "https://api.mimo.com/v1")
    MIMO_MODEL: str = os.getenv("MIMO_MODEL", "mimo-7b")

    # DeepSeek API
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_API_URL: str = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1")
    DEEPSEEK_MODEL: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

    # LangChain
    LANGCHAIN_API_KEY: str = os.getenv("LANGCHAIN_API_KEY", "")
    LANGCHAIN_TRACING_V2: bool = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"

    # Debate settings
    MAX_DEBATE_ROUNDS: int = int(os.getenv("MAX_DEBATE_ROUNDS", "3"))
    DEBATE_TIMEOUT: int = int(os.getenv("DEBATE_TIMEOUT", "300"))  # seconds

    # Execution settings
    EXECUTION_TIMEOUT: int = int(os.getenv("EXECUTION_TIMEOUT", "30"))  # seconds
    EXECUTION_MEMORY_LIMIT: str = os.getenv("EXECUTION_MEMORY_LIMIT", "256m")

    # Retry settings
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_DELAY: float = float(os.getenv("RETRY_DELAY", "1.0"))  # seconds

    # Application
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


config = Config()
