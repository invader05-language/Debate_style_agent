"""
Tests for memory store — covers save, search, get_by_topic, get_relevant.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from memory.store import MemoryStore, MemoryModel


class TestMemoryStoreInit:
    """Initialization tests."""

    def test_init_with_default_agent(self):
        """Should lazy-init MIMOAgent when none provided."""
        with patch("agents.mimo_agent.MIMOAgent") as MockMIMO:
            mock_agent = MagicMock()
            MockMIMO.return_value = mock_agent
            store = MemoryStore()
            assert store.embedding_agent is mock_agent

    def test_init_with_custom_agent(self):
        """Should use provided agent."""
        custom = MagicMock()
        store = MemoryStore(embedding_agent=custom)
        assert store.embedding_agent is custom


class TestToDict:
    """Model-to-dict conversion."""

    def test_to_dict_all_fields(self):
        store = MemoryStore(embedding_agent=MagicMock())

        mock_mem = MagicMock()
        mock_mem.id = "abc-123"
        mock_mem.topic = "JWT vs Session"
        mock_mem.debate_summary = "Summary text"
        mock_mem.outcome = "Use JWT"
        mock_mem.confidence = 0.85
        mock_mem.tags = ["JWT", "security"]
        mock_mem.lessons_learned = ["Lesson 1"]
        mock_mem.created_at = None

        result = store._to_dict(mock_mem)

        assert result["id"] == "abc-123"
        assert result["topic"] == "JWT vs Session"
        assert result["debate_summary"] == "Summary text"
        assert result["outcome"] == "Use JWT"
        assert result["confidence"] == 0.85
        assert result["tags"] == ["JWT", "security"]
        assert result["lessons_learned"] == ["Lesson 1"]
        assert result["created_at"] is None

    def test_to_dict_with_datetime(self):
        store = MemoryStore(embedding_agent=MagicMock())

        from datetime import datetime
        mock_mem = MagicMock()
        mock_mem.id = "id-1"
        mock_mem.topic = "t"
        mock_mem.debate_summary = "s"
        mock_mem.outcome = "o"
        mock_mem.confidence = 0.5
        mock_mem.tags = []
        mock_mem.lessons_learned = []
        mock_mem.created_at = datetime(2026, 6, 3, 12, 0, 0)

        result = store._to_dict(mock_mem)
        assert "2026-06-03" in result["created_at"]


class TestSave:
    """save() method tests."""

    @pytest.mark.asyncio
    async def test_save_calls_db(self):
        """save() should add to DB and return ID."""
        store = MemoryStore(embedding_agent=MagicMock())

        mock_db = MagicMock()
        mock_db.add = MagicMock()
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()
        mock_db.close = MagicMock()

        mock_mem = MagicMock()
        mock_mem.id = "new-id-123"

        with patch("memory.store.SessionLocal", return_value=mock_db):
            # Patch MemoryModel to capture the created instance
            with patch("memory.store.MemoryModel", return_value=mock_mem):
                result = await store.save({
                    "topic": "Test",
                    "debate_summary": "Summary",
                    "outcome": "Outcome",
                    "confidence": 0.8,
                    "tags": ["tag1"],
                    "lessons_learned": ["lesson1"]
                })

        assert result == "new-id-123"
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_save_with_defaults(self):
        """save() should use defaults for missing fields."""
        store = MemoryStore(embedding_agent=MagicMock())

        mock_db = MagicMock()
        mock_db.add = MagicMock()
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()
        mock_db.close = MagicMock()

        mock_mem = MagicMock()
        mock_mem.id = "id-2"

        with patch("memory.store.SessionLocal", return_value=mock_db):
            with patch("memory.store.MemoryModel", return_value=mock_mem):
                result = await store.save({"topic": "T"})

        assert result == "id-2"


class TestSearch:
    """search() method tests."""

    @pytest.mark.asyncio
    async def test_search_returns_results(self):
        """search() should query DB and return list of dicts."""
        store = MemoryStore(embedding_agent=MagicMock())

        mock_mem = MagicMock()
        mock_mem.id = "r1"
        mock_mem.topic = "JWT auth"
        mock_mem.debate_summary = "About JWT"
        mock_mem.outcome = "Use JWT"
        mock_mem.confidence = 0.8
        mock_mem.tags = ["JWT"]
        mock_mem.lessons_learned = []
        mock_mem.created_at = None

        mock_query = MagicMock()
        mock_query.filter.return_value.limit.return_value.all.return_value = [mock_mem]

        mock_db = MagicMock()
        mock_db.query.return_value = mock_query
        mock_db.close = MagicMock()

        with patch("memory.store.SessionLocal", return_value=mock_db):
            results = await store.search("JWT", limit=5)

        assert len(results) == 1
        assert results[0]["id"] == "r1"
        assert results[0]["topic"] == "JWT auth"

    @pytest.mark.asyncio
    async def test_search_empty(self):
        """search() should return empty list when no matches."""
        store = MemoryStore(embedding_agent=MagicMock())

        mock_query = MagicMock()
        mock_query.filter.return_value.limit.return_value.all.return_value = []

        mock_db = MagicMock()
        mock_db.query.return_value = mock_query
        mock_db.close = MagicMock()

        with patch("memory.store.SessionLocal", return_value=mock_db):
            results = await store.search("nonexistent")

        assert results == []


class TestGetByTopic:
    """get_by_topic() method tests."""

    @pytest.mark.asyncio
    async def test_get_by_topic_match(self):
        store = MemoryStore(embedding_agent=MagicMock())

        mock_mem = MagicMock()
        mock_mem.id = "t1"
        mock_mem.topic = "JWT vs Session"
        mock_mem.debate_summary = "summary"
        mock_mem.outcome = "JWT"
        mock_mem.confidence = 0.9
        mock_mem.tags = []
        mock_mem.lessons_learned = []
        mock_mem.created_at = None

        mock_query = MagicMock()
        mock_query.filter.return_value.all.return_value = [mock_mem]

        mock_db = MagicMock()
        mock_db.query.return_value = mock_query
        mock_db.close = MagicMock()

        with patch("memory.store.SessionLocal", return_value=mock_db):
            results = await store.get_by_topic("JWT vs Session")

        assert len(results) == 1
        assert results[0]["topic"] == "JWT vs Session"

    @pytest.mark.asyncio
    async def test_get_by_topic_no_match(self):
        store = MemoryStore(embedding_agent=MagicMock())

        mock_query = MagicMock()
        mock_query.filter.return_value.all.return_value = []

        mock_db = MagicMock()
        mock_db.query.return_value = mock_query
        mock_db.close = MagicMock()

        with patch("memory.store.SessionLocal", return_value=mock_db):
            results = await store.get_by_topic("Unknown topic")

        assert results == []


class TestGetRelevant:
    """get_relevant() method tests."""

    @pytest.mark.asyncio
    async def test_get_relevant_exact_match(self):
        """Should return exact topic match first."""
        store = MemoryStore(embedding_agent=MagicMock())

        mock_mem = MagicMock()
        mock_mem.id = "rel-1"
        mock_mem.topic = "JWT authentication"
        mock_mem.debate_summary = "summary"
        mock_mem.outcome = "JWT"
        mock_mem.confidence = 0.9
        mock_mem.tags = []
        mock_mem.lessons_learned = []
        mock_mem.created_at = None

        with patch.object(store, 'get_by_topic', return_value=[{
            "id": "rel-1", "topic": "JWT authentication",
            "debate_summary": "summary", "outcome": "JWT",
            "confidence": 0.9, "tags": [], "lessons_learned": [],
            "created_at": None
        }]):
            results = await store.get_relevant("JWT authentication", limit=3)

        assert len(results) == 1
        assert results[0]["id"] == "rel-1"

    @pytest.mark.asyncio
    async def test_get_relevant_falls_back_to_search(self):
        """Should fall back to keyword search when no exact match."""
        store = MemoryStore(embedding_agent=MagicMock())

        with patch.object(store, 'get_by_topic', return_value=[]):
            with patch.object(store, 'search', return_value=[{
                "id": "rel-2", "topic": "auth methods",
                "debate_summary": "s", "outcome": "o",
                "confidence": 0.7, "tags": [], "lessons_learned": [],
                "created_at": None
            }]):
                results = await store.get_relevant("authentication methods", limit=3)

        assert len(results) == 1

    @pytest.mark.asyncio
    async def test_get_relevant_deduplicates(self):
        """Should deduplicate results from multiple keyword searches."""
        store = MemoryStore(embedding_agent=MagicMock())

        same_mem = {
            "id": "dup-1", "topic": "JWT",
            "debate_summary": "s", "outcome": "o",
            "confidence": 0.8, "tags": [], "lessons_learned": [],
            "created_at": None
        }

        with patch.object(store, 'get_by_topic', return_value=[]):
            with patch.object(store, 'search', return_value=[same_mem]):
                results = await store.get_relevant("JWT auth tokens", limit=3)

        # Should only have 1 result despite multiple keywords
        ids = [r["id"] for r in results]
        assert ids.count("dup-1") == 1

    @pytest.mark.asyncio
    async def test_get_relevant_respects_limit(self):
        """Should respect limit parameter."""
        store = MemoryStore(embedding_agent=MagicMock())

        memories = [
            {"id": f"m{i}", "topic": f"topic{i}", "debate_summary": "s",
             "outcome": "o", "confidence": 0.5, "tags": [], "lessons_learned": [],
             "created_at": None}
            for i in range(10)
        ]

        with patch.object(store, 'get_by_topic', return_value=[]):
            with patch.object(store, 'search', return_value=memories):
                results = await store.get_relevant("test query here", limit=2)

        assert len(results) <= 2
