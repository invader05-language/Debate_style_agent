"""
Tests for debate engine.
"""

import pytest
from debate.protocol import (
    DebateStatus, Role, Message, Round, Verdict,
    DebateResult, DebateConfig
)
from debate.roles import get_role, ProRole, ConRole, JudgeRole
from debate.engine import DebateEngine


class TestDebateProtocol:
    """Test debate protocol definitions."""

    def test_debate_status_enum(self):
        """Test DebateStatus enum values."""
        assert DebateStatus.PENDING == "pending"
        assert DebateStatus.RUNNING == "running"
        assert DebateStatus.COMPLETED == "completed"
        assert DebateStatus.EXECUTED == "executed"
        assert DebateStatus.FAILED == "failed"

    def test_role_enum(self):
        """Test Role enum values."""
        assert Role.PRO == "pro"
        assert Role.CON == "con"
        assert Role.JUDGE == "judge"

    def test_message_creation(self):
        """Test Message model creation."""
        message = Message(
            debate_id="test-debate-123",
            round_number=1,
            role=Role.PRO,
            content="Test content",
            model_used="mimo",
            confidence=0.8
        )
        assert message.debate_id == "test-debate-123"
        assert message.round_number == 1
        assert message.role == Role.PRO
        assert message.content == "Test content"
        assert message.model_used == "mimo"
        assert message.confidence == 0.8

    def test_message_confidence_validation(self):
        """Test Message confidence validation."""
        # Valid confidence
        message = Message(
            debate_id="test",
            round_number=1,
            role=Role.PRO,
            content="Test",
            model_used="mimo",
            confidence=0.5
        )
        assert message.confidence == 0.5

        # Invalid confidence (should raise error)
        with pytest.raises(Exception):
            Message(
                debate_id="test",
                round_number=1,
                role=Role.PRO,
                content="Test",
                model_used="mimo",
                confidence=1.5  # Invalid
            )

    def test_verdict_creation(self):
        """Test Verdict model creation."""
        verdict = Verdict(
            recommendation="Use JWT",
            winner="pro",
            confidence=0.85,
            action_plan=["Step 1", "Step 2"]
        )
        assert verdict.recommendation == "Use JWT"
        assert verdict.winner == "pro"
        assert verdict.confidence == 0.85
        assert len(verdict.action_plan) == 2

    def test_verdict_winner_validation(self):
        """Test Verdict winner validation."""
        # Valid winners
        Verdict(recommendation="Test", winner="pro", confidence=0.5, action_plan=[])
        Verdict(recommendation="Test", winner="con", confidence=0.5, action_plan=[])
        Verdict(recommendation="Test", winner="draw", confidence=0.5, action_plan=[])

        # Invalid winner
        with pytest.raises(Exception):
            Verdict(recommendation="Test", winner="invalid", confidence=0.5, action_plan=[])

    def test_debate_config_creation(self):
        """Test DebateConfig model creation."""
        config = DebateConfig(
            topic="Test topic",
            max_rounds=3,
            models={"pro": "mimo", "con": "deepseek", "judge": "mimo"}
        )
        assert config.topic == "Test topic"
        assert config.max_rounds == 3
        assert config.models["pro"] == "mimo"


class TestDebateRoles:
    """Test debate roles."""

    def test_get_role_pro(self):
        """Test getting pro role."""
        role = get_role(Role.PRO, "mimo")
        assert isinstance(role, ProRole)
        assert role.role == Role.PRO
        assert role.model_name == "mimo"

    def test_get_role_con(self):
        """Test getting con role."""
        role = get_role(Role.CON, "deepseek")
        assert isinstance(role, ConRole)
        assert role.role == Role.CON
        assert role.model_name == "deepseek"

    def test_get_role_judge(self):
        """Test getting judge role."""
        role = get_role(Role.JUDGE, "mimo")
        assert isinstance(role, JudgeRole)
        assert role.role == Role.JUDGE
        assert role.model_name == "mimo"

    def test_pro_system_prompt(self):
        """Test pro role system prompt."""
        role = ProRole()
        prompt = role.get_system_prompt("Test topic")
        assert "正方" in prompt
        assert "Test topic" in prompt

    def test_con_system_prompt(self):
        """Test con role system prompt."""
        role = ConRole()
        prompt = role.get_system_prompt("Test topic")
        assert "反方" in prompt
        assert "Test topic" in prompt

    def test_judge_system_prompt(self):
        """Test judge role system prompt."""
        role = JudgeRole()
        prompt = role.get_system_prompt("Test topic")
        assert "裁判" in prompt
        assert "Test topic" in prompt


class TestDebateEngine:
    """Test debate engine."""

    def test_engine_initialization(self):
        """Test engine initialization."""
        engine = DebateEngine()
        assert engine.memory_store is None
        assert "mimo" in engine.agents
        assert "deepseek" in engine.agents

    def test_get_all_messages(self):
        """Test extracting all messages from result."""
        engine = DebateEngine()

        # Create test messages
        pro_msg = Message(
            debate_id="test",
            round_number=1,
            role=Role.PRO,
            content="Pro argument",
            model_used="mimo",
            confidence=0.8
        )
        con_msg = Message(
            debate_id="test",
            round_number=1,
            role=Role.CON,
            content="Con argument",
            model_used="deepseek",
            confidence=0.8
        )

        # Create round
        round_result = Round(
            round_number=1,
            pro_message=pro_msg,
            con_message=con_msg
        )

        # Create result
        result = DebateResult(
            topic="Test",
            status=DebateStatus.RUNNING,
            rounds=[round_result]
        )

        messages = engine._get_all_messages(result)
        assert len(messages) == 2
        assert messages[0].content == "Pro argument"
        assert messages[1].content == "Con argument"
