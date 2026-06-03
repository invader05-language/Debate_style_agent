"""
Tests for memory store.
"""

import pytest
from memory.store import MemoryStore


class TestMemoryStore:
    """Test memory store."""

    def test_memory_store_initialization(self):
        """Test memory store initialization."""
        store = MemoryStore()
        assert store.embedding_agent is not None

    def test_to_dict(self):
        """Test memory model to dict conversion."""
        store = MemoryStore()

        # Create mock memory model
        class MockMemory:
            id = "test-id"
            topic = "Test topic"
            debate_summary = "Test summary"
            outcome = "Test outcome"
            confidence = 0.8
            tags = ["test", "memory"]
            lessons_learned = ["Lesson 1"]
            created_at = None

        memory = MockMemory()
        result = store._to_dict(memory)

        assert result["id"] == "test-id"
        assert result["topic"] == "Test topic"
        assert result["debate_summary"] == "Test summary"
        assert result["outcome"] == "Test outcome"
        assert result["confidence"] == 0.8
        assert result["tags"] == ["test", "memory"]
        assert result["lessons_learned"] == ["Lesson 1"]
        assert result["created_at"] is None
