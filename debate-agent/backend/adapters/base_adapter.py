"""
Base adapter interface for AI model providers.
All format-specific adapters implement this interface.
"""

from abc import ABC, abstractmethod
from typing import AsyncGenerator, Optional


class BaseModelAdapter(ABC):
    """Unified interface for AI model chat."""

    def __init__(self, model_name: str, api_url: str, api_key: str, **kwargs):
        self.model_name = model_name
        self.api_url = api_url
        self.api_key = api_key
        self.max_tokens = kwargs.get("max_tokens", 4096)
        self.temperature = kwargs.get("temperature", 0.7)

    @abstractmethod
    async def chat(
        self,
        messages: list[dict],
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> str:
        """Send a chat request and return the full response text."""

    @abstractmethod
    async def chat_json(
        self,
        messages: list[dict],
        system_prompt: Optional[str] = None,
        schema: Optional[dict] = None,
        **kwargs,
    ) -> dict:
        """Send a chat request expecting structured JSON output."""

    @abstractmethod
    async def chat_stream(
        self,
        messages: list[dict],
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> AsyncGenerator[str, None]:
        """Stream chat response chunks."""
