"""
Base agent interface for Multi-AI Debate Agent.
Provides unified interface for different AI models.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from debate.protocol import Message


class BaseAgent(ABC):
    """
    Base agent interface.

    ┌─────────────────────────────────────────────┐
    │              BaseAgent                       │
    ├─────────────────────────────────────────────┤
    │ + chat(message: str, context: List) -> str  │
    │ + get_embedding(text: str) -> List[float]   │
    └─────────────────────────────────────────────┘
    """

    def __init__(self, model_name: str, api_key: str = ""):
        self.model_name = model_name
        self.api_key = api_key
        self.max_retries = 3
        self.retry_delay = 1.0

    @abstractmethod
    async def chat(self, system_prompt: str, user_message: str,
                   context: Optional[List[Message]] = None) -> str:
        """
        Chat with the AI model.

        Args:
            system_prompt: System prompt for the model
            user_message: User message
            context: Previous messages for context

        Returns:
            Model response as string
        """
        pass

    @abstractmethod
    async def get_embedding(self, text: str) -> List[float]:
        """
        Get embedding vector for text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        pass

    def _build_messages(self, system_prompt: str, user_message: str,
                       context: Optional[List[Message]] = None) -> List[dict]:
        """Build message list for API call."""
        messages = [{"role": "system", "content": system_prompt}]

        # Add context messages
        if context:
            for msg in context:
                role = "assistant" if msg.role in ["pro", "judge"] else "user"
                messages.append({"role": role, "content": msg.content})

        # Add current user message
        messages.append({"role": "user", "content": user_message})

        return messages

    async def _retry_with_backoff(self, func, *args, **kwargs):
        """Retry function with exponential backoff."""
        import asyncio
        for attempt in range(self.max_retries):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise e
                await asyncio.sleep(self.retry_delay * (2 ** attempt))
