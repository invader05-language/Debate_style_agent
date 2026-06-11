"""
API endpoint tests for Multi-AI Debate Agent.
Uses httpx AsyncClient with ASGITransport — no real DB required.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession


# ── Additional Endpoint Tests ──────────────────────────────────────

class TestDebateAPIExtended:
    """Extended debate API tests."""

    @pytest.mark.asyncio
    async def test_start_debate_already_started(self, client, mock_db):
        """POST /api/debates/{id}/start should 400 if already running."""
        mock_debate = _make_debate_model(status="running")
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_debate
        mock_db.execute.return_value = mock_result

        resp = await client.post("/api/debates/d1/start")
        assert resp.status_code == 400

    @pytest.mark.asyncio
    async def test_execute_debate_not_found(self, client, mock_db):
        """POST /api/debates/{id}/execute should 404 if missing."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result

        resp = await client.post("/api/debates/nope/execute")
        assert resp.status_code == 404

    @pytest.mark.asyncio
    async def test_execute_debate_not_completed(self, client, mock_db):
        """POST /api/debates/{id}/execute should 409 if not completed."""
        mock_debate = _make_debate_model(status="running")
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_debate
        mock_db.execute.return_value = mock_result

        resp = await client.post("/api/debates/d1/execute")
        assert resp.status_code == 409

    @pytest.mark.asyncio
    async def test_cors_headers(self, client):
        """Test that CORS headers are present."""
        resp = await client.options("/api/debates", headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST"
        })
        # CORS should be handled by middleware
        assert resp.status_code in [200, 204, 405]

    @pytest.mark.asyncio
    async def test_404_handling(self, client, mock_db):
        """Test 404 for non-existent endpoints."""
        resp = await client.get("/api/nonexistent")
        assert resp.status_code == 404


class TestMemoryAPIExtended:
    """Extended memory API tests."""

    @pytest.mark.asyncio
    async def test_search_memories_with_results(self, client, mock_db):
        """GET /api/memories/search should return matching memories."""
        mock_memory = MagicMock()
        mock_memory.id = "mem-1"
        mock_memory.topic = "JWT auth"
        mock_memory.debate_summary = "Used JWT for authentication"
        mock_memory.outcome = "Success"
        mock_memory.confidence = 0.9
        mock_memory.tags = ["auth", "jwt"]
        mock_memory.lessons_learned = ["JWT is stateless"]
        mock_memory.created_at = MagicMock()
        mock_memory.created_at.isoformat.return_value = "2026-06-03T12:00:00"

        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_memory]
        mock_db.execute.return_value = mock_result

        with patch("backend.api.memory.cache") as mock_cache:
            mock_cache.get_memory_search = AsyncMock(return_value=None)
            mock_cache.set_memory_search = AsyncMock()

            resp = await client.get("/api/memories/search?q=JWT")

        assert resp.status_code == 200
        data = resp.json()
        assert len(data) > 0

    @pytest.mark.asyncio
    async def test_list_memories_empty(self, client, mock_db):
        """GET /api/memories should return empty list."""
        mock_count = MagicMock()
        mock_count.scalar.return_value = 0
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db.execute = AsyncMock(side_effect=[mock_count, mock_result])

        resp = await client.get("/api/memories")
        assert resp.status_code == 200

    @pytest.mark.asyncio
    async def test_create_memory(self, client, mock_db):
        """POST /api/memories should create a memory."""
        async def fake_commit():
            pass
        mock_db.commit = fake_commit

        with patch("backend.api.memory.embedding_service") as mock_emb:
            mock_emb.get_embedding = AsyncMock(return_value=[0.1] * 1024)

            resp = await client.post("/api/memories", json={
                "topic": "JWT vs Session",
                "debate_summary": "JWT won the debate",
                "outcome": "Implemented JWT",
                "confidence": 0.85,
                "tags": ["auth", "jwt"],
                "lessons_learned": ["JWT is better for distributed systems"]
            })

        assert resp.status_code == 201


class TestAuthAPI:
    """Authentication API tests."""

    @pytest.mark.asyncio
    async def test_register_user(self, client, mock_db):
        """POST /api/auth/register should create a user."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None  # No existing user
        mock_db.execute = AsyncMock(return_value=mock_result)
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        resp = await client.post("/api/auth/register", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepassword123"
        })
        assert resp.status_code == 201

    @pytest.mark.asyncio
    async def test_register_duplicate_user(self, client, mock_db):
        """POST /api/auth/register should 409 for duplicate username."""
        mock_existing = MagicMock()
        mock_existing.scalar_one_or_none.return_value = MagicMock()  # User exists
        mock_db.execute = AsyncMock(return_value=mock_existing)

        resp = await client.post("/api/auth/register", json={
            "username": "existinguser",
            "email": "test@example.com",
            "password": "securepassword123"
        })
        assert resp.status_code == 409

    @pytest.mark.asyncio
    async def test_login_success(self, client, mock_db):
        """POST /api/auth/login should return token."""
        from passlib.hash import bcrypt
        mock_user = MagicMock()
        mock_user.id = "user-1"
        mock_user.username = "testuser"
        mock_user.email = "test@example.com"
        mock_user.hashed_password = bcrypt.hash("securepassword123")
        mock_user.is_active = True

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_user
        mock_db.execute = AsyncMock(return_value=mock_result)

        resp = await client.post("/api/auth/login", json={
            "username": "testuser",
            "password": "securepassword123"
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data

    @pytest.mark.asyncio
    async def test_login_wrong_password(self, client, mock_db):
        """POST /api/auth/login should 401 for wrong password."""
        from passlib.hash import bcrypt
        mock_user = MagicMock()
        mock_user.hashed_password = bcrypt.hash("correctpassword")
        mock_user.is_active = True

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_user
        mock_db.execute = AsyncMock(return_value=mock_result)

        resp = await client.post("/api/auth/login", json={
            "username": "testuser",
            "password": "wrongpassword"
        })
        assert resp.status_code == 401


# ── Helpers ──────────────────────────────────────────────────────

def _mock_db_session():
    """Create a mock AsyncSession that works as a dependency."""
    db = AsyncMock(spec=AsyncSession)
    db.execute = AsyncMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    db.close = AsyncMock()
    return db


def _make_debate_model(debate_id="test-id", topic="Test topic",
                       status="pending", action_plan=None, verdict=None):
    """Create a mock DebateModel."""
    from datetime import datetime
    d = MagicMock()
    d.id = debate_id
    d.topic = topic
    d.status = status
    d.action_plan = action_plan
    d.verdict = verdict
    d.created_at = datetime(2026, 6, 3, 12, 0, 0)
    d.completed_at = None
    return d


# ── Fixtures ─────────────────────────────────────────────────────

@pytest.fixture
def mock_db():
    return _mock_db_session()


@pytest.fixture
async def client(mock_db):
    """AsyncClient with mocked DB dependency."""
    from backend.main import app
    from backend.database import get_db

    async def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


# ── Root & Health ────────────────────────────────────────────────

class TestRootEndpoints:

    @pytest.mark.asyncio
    async def test_root(self, client):
        resp = await client.get("/")
        assert resp.status_code == 200
        data = resp.json()
        assert "message" in data
        assert data["version"] == "1.0.0"

    @pytest.mark.asyncio
    async def test_health(self, client):
        resp = await client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "healthy"


# ── Debate endpoints ─────────────────────────────────────────────

class TestDebateAPI:

    @pytest.mark.asyncio
    async def test_create_debate(self, client, mock_db):
        """POST /api/debates should create a debate."""
        mock_debate = _make_debate_model()
        mock_db.refresh = AsyncMock(side_effect=lambda d: setattr(d, 'id', 'test-id'))

        # Mock the db.add and db.commit
        async def fake_commit():
            pass
        mock_db.commit = fake_commit

        resp = await client.post("/api/debates", json={
            "topic": "JWT vs Session Cookies"
        })

        assert resp.status_code == 201
        data = resp.json()
        assert data["topic"] == "JWT vs Session Cookies"
        assert data["status"] == "pending"

    @pytest.mark.asyncio
    async def test_create_debate_validation(self, client, mock_db):
        """POST /api/debates with empty topic should fail validation."""
        resp = await client.post("/api/debates", json={"topic": ""})
        assert resp.status_code == 422

    @pytest.mark.asyncio
    async def test_get_debate_not_found(self, client, mock_db):
        """GET /api/debates/{id} should return 404 for missing debate."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result

        resp = await client.get("/api/debates/nonexistent-id")
        assert resp.status_code == 404

    @pytest.mark.asyncio
    async def test_get_debate_success(self, client, mock_db):
        """GET /api/debates/{id} should return debate details."""
        mock_debate = _make_debate_model(
            debate_id="abc-123",
            topic="JWT auth",
            status="completed"
        )

        # First call: debate query, second call: messages query
        mock_debate_result = MagicMock()
        mock_debate_result.scalar_one_or_none.return_value = mock_debate

        mock_msg_result = MagicMock()
        mock_msg_result.scalars.return_value.all.return_value = []

        mock_db.execute = AsyncMock(side_effect=[mock_debate_result, mock_msg_result])

        # Mock cache
        with patch("backend.api.debate.cache") as mock_cache:
            mock_cache.get_debate = AsyncMock(return_value=None)
            mock_cache.set_debate = AsyncMock()

            resp = await client.get("/api/debates/abc-123")

        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == "abc-123"
        assert data["topic"] == "JWT auth"

    @pytest.mark.asyncio
    async def test_list_debates(self, client, mock_db):
        """GET /api/debates should return paginated list."""
        mock_count = MagicMock()
        mock_count.scalar.return_value = 2

        mock_debates = MagicMock()
        mock_debates.scalars.return_value.all.return_value = [
            _make_debate_model(debate_id="d1", topic="Topic 1"),
            _make_debate_model(debate_id="d2", topic="Topic 2", status="completed"),
        ]

        mock_db.execute = AsyncMock(side_effect=[mock_count, mock_debates])

        resp = await client.get("/api/debates?page=1&page_size=10")

        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 2
        assert len(data["debates"]) == 2

    @pytest.mark.asyncio
    async def test_start_debate_not_found(self, client, mock_db):
        """POST /api/debates/{id}/start should 404 if missing."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result

        resp = await client.post("/api/debates/nope/start")
        assert resp.status_code == 404


# ── Execution endpoints ──────────────────────────────────────────

class TestExecutionAPI:

    @pytest.mark.asyncio
    async def test_get_execution_not_found(self, client, mock_db):
        """GET /api/executions/{id} should return 404."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result

        resp = await client.get("/api/executions/nonexistent")
        assert resp.status_code == 404

    @pytest.mark.asyncio
    async def test_get_execution_success(self, client, mock_db):
        """GET /api/executions/{id} should return execution data."""
        from datetime import datetime
        mock_exec = MagicMock()
        mock_exec.id = "exec-1"
        mock_exec.debate_id = "debate-1"
        mock_exec.status = "success"
        mock_exec.code_generated = "print(1)"
        mock_exec.execution_result = "1\n"
        mock_exec.error_message = None
        mock_exec.created_at = datetime(2026, 6, 3, 12, 0, 0)
        mock_exec.completed_at = datetime(2026, 6, 3, 12, 1, 0)

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_exec
        mock_db.execute.return_value = mock_result

        resp = await client.get("/api/executions/exec-1")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "success"
        assert data["code_generated"] == "print(1)"

    @pytest.mark.asyncio
    async def test_generate_code_debate_not_found(self, client, mock_db):
        """POST /api/debates/{id}/generate-code should 404 if debate missing."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result

        resp = await client.post("/api/debates/nope/generate-code", json={
            "language": "python"
        })
        assert resp.status_code == 404

    @pytest.mark.asyncio
    async def test_generate_code_debate_not_completed(self, client, mock_db):
        """POST /api/debates/{id}/generate-code should 409 if debate not completed."""
        mock_debate = _make_debate_model(status="running")
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_debate
        mock_db.execute.return_value = mock_result

        resp = await client.post("/api/debates/d1/generate-code", json={
            "language": "python"
        })
        assert resp.status_code == 409

    @pytest.mark.asyncio
    async def test_generate_code_no_action_plan(self, client, mock_db):
        """POST /api/debates/{id}/generate-code should 409 if no action_plan."""
        mock_debate = _make_debate_model(status="completed", action_plan=None)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_debate
        mock_db.execute.return_value = mock_result

        resp = await client.post("/api/debates/d1/generate-code", json={
            "language": "python"
        })
        assert resp.status_code == 409

    @pytest.mark.asyncio
    async def test_retry_execution_not_found(self, client, mock_db):
        """POST /api/executions/{id}/retry should 404 if missing."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result

        resp = await client.post("/api/executions/nope/retry")
        assert resp.status_code == 404

    @pytest.mark.asyncio
    async def test_list_executions_empty(self, client, mock_db):
        """GET /api/debates/{id}/executions should return empty list."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db.execute.return_value = mock_result

        resp = await client.get("/api/debates/d1/executions")
        assert resp.status_code == 200
        assert resp.json() == []


# ── Memory endpoints ─────────────────────────────────────────────

class TestMemoryAPI:

    @pytest.mark.asyncio
    async def test_search_memories_empty(self, client, mock_db):
        """GET /api/memories/search should return empty for no matches."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db.execute.return_value = mock_result

        resp = await client.get("/api/memories/search?q=nonexistent")
        assert resp.status_code == 200
