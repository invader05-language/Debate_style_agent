"""
Tests for Agent fallback strategy.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from agents.fallback import AgentFallback


class MockAgent:
    """Mock agent for testing."""

    def __init__(self, name: str, should_fail: bool = False):
        self.name = name
        self.should_fail = should_fail
        self.chat = AsyncMock(side_effect=self._chat)

    async def _chat(self, system_prompt: str, user_message: str, context=None):
        if self.should_fail:
            raise ConnectionError(f"{self.name} is unavailable")
        return f"Response from {self.name}"


@pytest.fixture
def mock_agents():
    """Create mock agents for testing."""
    return {
        "mimo": MockAgent("mimo"),
        "deepseek": MockAgent("deepseek"),
    }


@pytest.fixture
def fallback(mock_agents):
    """Create AgentFallback instance."""
    return AgentFallback(agents=mock_agents)


class TestAgentFallback:
    """Test suite for AgentFallback."""

    @pytest.mark.asyncio
    async def test_preferred_agent_success(self, fallback, mock_agents):
        """Test that preferred agent is used when healthy."""
        result = await fallback.chat(
            preferred="mimo",
            fallback="deepseek",
            system_prompt="test",
            user_message="hello"
        )
        assert result == "Response from mimo"
        mock_agents["mimo"].chat.assert_called_once()
        mock_agents["deepseek"].chat.assert_not_called()

    @pytest.mark.asyncio
    async def test_fallback_on_preferred_failure(self, fallback, mock_agents):
        """Test fallback to backup when preferred agent fails."""
        mock_agents["mimo"].should_fail = True

        result = await fallback.chat(
            preferred="mimo",
            fallback="deepseek",
            system_prompt="test",
            user_message="hello"
        )
        assert result == "Response from deepseek"
        mock_agents["mimo"].chat.assert_called_once()
        mock_agents["deepseek"].chat.assert_called_once()

    @pytest.mark.asyncio
    async def test_both_agents_fail_raises(self, fallback, mock_agents):
        """Test that RuntimeError is raised when both agents fail."""
        mock_agents["mimo"].should_fail = True
        mock_agents["deepseek"].should_fail = True

        with pytest.raises(ConnectionError):
            await fallback.chat(
                preferred="mimo",
                fallback="deepseek",
                system_prompt="test",
                user_message="hello"
            )

    @pytest.mark.asyncio
    async def test_unhealthy_agent_skipped(self, fallback, mock_agents):
        """Test that unhealthy agent is skipped without calling."""
        # Mark mimo as unhealthy
        fallback.health_status["mimo"] = False
        fallback.failure_counts["mimo"] = 3
        fallback.last_failure["mimo"] = 9999999999  # Far in the future

        result = await fallback.chat(
            preferred="mimo",
            fallback="deepseek",
            system_prompt="test",
            user_message="hello"
        )
        assert result == "Response from deepseek"
        mock_agents["mimo"].chat.assert_not_called()
        mock_agents["deepseek"].chat.assert_called_once()

    @pytest.mark.asyncio
    async def test_recovery_after_interval(self, fallback, mock_agents):
        """Test that agent recovers after recovery interval."""
        import time
        # Mark mimo as unhealthy but with old failure timestamp
        fallback.health_status["mimo"] = False
        fallback.failure_counts["mimo"] = 3
        fallback.last_failure["mimo"] = time.time() - 120  # 2 minutes ago

        # Should try mimo again (recovery probe)
        result = await fallback.chat(
            preferred="mimo",
            fallback="deepseek",
            system_prompt="test",
            user_message="hello"
        )
        assert result == "Response from mimo"
        assert fallback.health_status["mimo"] is True
        assert fallback.failure_counts["mimo"] == 0

    def test_record_failure_marks_unhealthy(self, fallback):
        """Test that max failures marks agent as unhealthy."""
        for _ in range(3):
            fallback._record_failure("mimo", Exception("test error"))

        assert fallback.health_status["mimo"] is False
        assert fallback.failure_counts["mimo"] == 3

    def test_record_success_resets_counts(self, fallback):
        """Test that success resets failure counts."""
        fallback.failure_counts["mimo"] = 2
        fallback.health_status["mimo"] = False

        fallback._record_success("mimo")

        assert fallback.failure_counts["mimo"] == 0
        assert fallback.health_status["mimo"] is True

    def test_is_healthy_default(self, fallback):
        """Test that all agents start healthy."""
        assert fallback._is_healthy("mimo") is True
        assert fallback._is_healthy("deepseek") is True

    def test_is_healthy_unknown_agent(self, fallback):
        """Test that unknown agent is considered unhealthy."""
        assert fallback._is_healthy("unknown") is False

    @pytest.mark.asyncio
    async def test_context_passed_to_agent(self, fallback, mock_agents):
        """Test that context is passed through to the agent."""
        context = [{"role": "user", "content": "previous message"}]

        await fallback.chat(
            preferred="mimo",
            fallback="deepseek",
            system_prompt="test",
            user_message="hello",
            context=context
        )

        mock_agents["mimo"].chat.assert_called_once_with(
            system_prompt="test",
            user_message="hello",
            context=context
        )
