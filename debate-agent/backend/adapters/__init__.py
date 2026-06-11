"""
AI Model Adapters - Unified interface for different AI model providers.
"""

from backend.adapters.base_adapter import BaseModelAdapter
from backend.adapters.factory import AdapterFactory

__all__ = ["BaseModelAdapter", "AdapterFactory"]
