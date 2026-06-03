"""
DeepSeek agent implementation for Multi-AI Debate Agent.
Implements the BaseAgent interface for DeepSeek model.
"""

import httpx
from typing import List, Optional
from agents.base_agent import BaseAgent
from debate.protocol import Message
from config import config


class DeepSeekAgent(BaseAgent):
    """
    DeepSeek model agent implementation.

    Uses LangChain for unified interface with DeepSeek API.
    """

    def __init__(self):
        super().__init__(
            model_name=config.DEEPSEEK_MODEL,
            api_key=config.DEEPSEEK_API_KEY
        )
        self.api_url = config.DEEPSEEK_API_URL

    async def chat(self, system_prompt: str, user_message: str,
                   context: Optional[List[Message]] = None) -> str:
        """
        Chat with DeepSeek model.

        Args:
            system_prompt: System prompt
            user_message: User message
            context: Previous messages

        Returns:
            Model response
        """
        return await self._retry_with_backoff(
            self._chat_impl, system_prompt, user_message, context
        )

    async def _chat_impl(self, system_prompt: str, user_message: str,
                         context: Optional[List[Message]] = None) -> str:
        """Implementation of chat method."""
        messages = self._build_messages(system_prompt, user_message, context)

        # Use httpx for API call
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model_name,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 1024
                },
                timeout=30.0
            )

            if response.status_code != 200:
                raise Exception(f"DeepSeek API error: {response.status_code} - {response.text}")

            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def get_embedding(self, text: str) -> List[float]:
        """
        Get embedding from DeepSeek model.

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        return await self._retry_with_backoff(
            self._get_embedding_impl, text
        )

    async def _get_embedding_impl(self, text: str) -> List[float]:
        """Implementation of get_embedding method."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/embeddings",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-embedding",
                    "input": text
                },
                timeout=30.0
            )

            if response.status_code != 200:
                raise Exception(f"DeepSeek embedding API error: {response.status_code}")

            data = response.json()
            return data["data"][0]["embedding"]
