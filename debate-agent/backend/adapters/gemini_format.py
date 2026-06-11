"""
Google Gemini adapter.
Uses the Google GenAI API format.
"""

import json
from typing import AsyncGenerator, Optional
import httpx
from backend.adapters.base_adapter import BaseModelAdapter


class GeminiFormatAdapter(BaseModelAdapter):
    """Adapter for Google Gemini API."""

    async def chat(
        self,
        messages: list[dict],
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> str:
        headers = {
            "Content-Type": "application/json",
        }

        contents = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({"role": role, "parts": [{"text": msg["content"]}]})

        payload = {"contents": contents}
        if system_prompt:
            payload["systemInstruction"] = {"parts": [{"text": system_prompt}]}

        generation_config = {
            "maxOutputTokens": kwargs.get("max_tokens", self.max_tokens),
            "temperature": kwargs.get("temperature", self.temperature),
        }
        payload["generationConfig"] = generation_config

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"

        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]

    async def chat_json(
        self,
        messages: list[dict],
        system_prompt: Optional[str] = None,
        schema: Optional[dict] = None,
        **kwargs,
    ) -> dict:
        headers = {"Content-Type": "application/json"}

        contents = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({"role": role, "parts": [{"text": msg["content"]}]})

        payload = {"contents": contents}
        if system_prompt:
            payload["systemInstruction"] = {"parts": [{"text": system_prompt}]}

        generation_config = {
            "maxOutputTokens": kwargs.get("max_tokens", self.max_tokens),
            "temperature": kwargs.get("temperature", self.temperature),
            "responseMimeType": "application/json",
        }
        if schema:
            generation_config["responseSchema"] = schema
        payload["generationConfig"] = generation_config

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"

        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(text)

    async def chat_stream(
        self,
        messages: list[dict],
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> AsyncGenerator[str, None]:
        headers = {"Content-Type": "application/json"}

        contents = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({"role": role, "parts": [{"text": msg["content"]}]})

        payload = {"contents": contents}
        if system_prompt:
            payload["systemInstruction"] = {"parts": [{"text": system_prompt}]}

        generation_config = {
            "maxOutputTokens": kwargs.get("max_tokens", self.max_tokens),
            "temperature": kwargs.get("temperature", self.temperature),
        }
        payload["generationConfig"] = generation_config

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:streamGenerateContent?key={self.api_key}"

        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream("POST", url, headers=headers, json=payload) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if line.startswith("data: "):
                        chunk = json.loads(line[6:])
                        candidates = chunk.get("candidates", [])
                        if candidates:
                            parts = candidates[0].get("content", {}).get("parts", [])
                            for part in parts:
                                if "text" in part:
                                    yield part["text"]
