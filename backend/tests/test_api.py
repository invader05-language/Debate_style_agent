"""
API tests for Multi-AI Debate Agent.
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestRootEndpoints:
    """Test root endpoints."""

    def test_root(self, client):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data

    def test_health(self, client):
        """Test health endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestDebateEndpoints:
    """Test debate endpoints."""

    def test_create_debate(self, client):
        """Test creating a new debate."""
        response = client.post(
            "/api/debates",
            json={"topic": "Test topic", "max_rounds": 3}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["topic"] == "Test topic"
        assert data["status"] == "pending"

    def test_list_debates(self, client):
        """Test listing debates."""
        response = client.get("/api/debates")
        assert response.status_code == 200
        data = response.json()
        assert "debates" in data
        assert "total" in data

    def test_get_debate_not_found(self, client):
        """Test getting non-existent debate."""
        response = client.get("/api/debates/non-existent-id")
        assert response.status_code == 404


class TestMemoryEndpoints:
    """Test memory endpoints."""

    def test_list_memories(self, client):
        """Test listing memories."""
        response = client.get("/api/memories")
        assert response.status_code == 200
        data = response.json()
        assert "memories" in data
        assert "total" in data

    def test_search_memories(self, client):
        """Test searching memories."""
        response = client.get("/api/memories/search?q=test")
        assert response.status_code == 200
        data = response.json()
        assert "memories" in data
        assert data["query"] == "test"

    def test_search_memories_empty_query(self, client):
        """Test searching memories with empty query."""
        response = client.get("/api/memories/search?q=")
        assert response.status_code == 422  # Validation error
