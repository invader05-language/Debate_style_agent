"""
Adapter factory - creates the correct adapter based on API format.
"""

from backend.adapters.base_adapter import BaseModelAdapter
from backend.adapters.openai_format import OpenAIFormatAdapter
from backend.adapters.anthropic_format import AnthropicFormatAdapter
from backend.adapters.gemini_format import GeminiFormatAdapter


class AdapterFactory:
    """Creates AI model adapters based on format type."""

    _adapters = {
        "openai": OpenAIFormatAdapter,
        "anthropic": AnthropicFormatAdapter,
        "gemini": GeminiFormatAdapter,
    }

    @classmethod
    def create(
        cls,
        api_format: str,
        model_name: str,
        api_url: str,
        api_key: str,
        **kwargs,
    ) -> BaseModelAdapter:
        adapter_cls = cls._adapters.get(api_format)
        if not adapter_cls:
            raise ValueError(f"Unknown API format: {api_format}. Supported: {list(cls._adapters.keys())}")
        return adapter_cls(
            model_name=model_name,
            api_url=api_url,
            api_key=api_key,
            **kwargs,
        )

    @classmethod
    def from_db_model(cls, db_model) -> BaseModelAdapter:
        """Create adapter from an AIModel database record."""
        return cls.create(
            api_format=db_model.api_format,
            model_name=db_model.model_id,
            api_url=db_model.api_url,
            api_key=db_model.api_key,
            max_tokens=db_model.max_tokens,
            temperature=db_model.temperature,
        )
