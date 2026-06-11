"""
Anthropic adapter for Claude models.
Uses the Anthropic Messages API format.
"""

import json
from typing import AsyncGenerator, Optional
import httpx
from backend.adapters.base_adapter import BaseModelAdapter


class AnthropicFormatAdapter(BaseModelAdapter):
    """Adapter for Anthropic Claude API."""

    async def chat(
        self,
        messages: list[dict],
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> str:
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model_name,
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
            "messages": messages,
        }
        if system_prompt:
            payload["system"] = system_prompt

        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload,
            )
            resp.raise_for_status()
            data = resp.json()
            return data["content"][0]["text"]

    async def chat_json(
        self,
        messages: list[dict],
        system_prompt: Optional[str] = None,
        schema: Optional[dict] = None,
        **kwargs,
    ) -> dict:
        json_instruction = "\n\nYou MUST respond with valid JSON only, no markdown formatting."
        if system_prompt:
            system_prompt += json_instruction
        else:
            system_prompt = json_instruction.strip()

        text = await self.chat(messages, system_prompt=system_prompt, **kwargs)
        text = text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1] if "\n" in text else text[3:]
            if text.endswith("```"):
                text = text[:-3]
        return json.loads(text)

    async def chat_stream(
        self,
        messages: list[dict],
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> AsyncGenerator[str, None]:
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model_name,
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
            "messages": messages,
            "stream": True,
        }
        if system_prompt:
            payload["system"] = system_prompt

        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream(
                "POST",
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload,
            ) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if line.startswith("data: "):
                        event = json.loads(line[6:])
                        if event.get("type") == "content_block_delta":
                            delta = event.get("delta", {})
                            if delta.get("type") == "text_delta":
                                yield delta["text"]
