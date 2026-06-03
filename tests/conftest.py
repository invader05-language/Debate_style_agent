"""
测试配置和公共 fixtures for Multi-AI Debate Agent.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from typing import List

from debate.protocol import (
    DebateStatus, Role, Message, Round, Verdict,
    DebateResult, DebateConfig
)


@pytest.fixture
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def sample_debate_config():
    """标准辩论配置."""
    return DebateConfig(
        topic="JWT vs Session Cookies for authentication",
        max_rounds=2,
        models={"pro": "mimo", "con": "deepseek", "judge": "mimo"}
    )


@pytest.fixture
def sample_message():
    """单条辩论消息."""
    return Message(
        debate_id="test-debate-id",
        round_number=1,
        role=Role.PRO,
        content="JWT 的优势在于无状态性和跨域支持...",
        model_used="mimo",
        confidence=0.85
    )


@pytest.fixture
def sample_round():
    """单轮辩论结果."""
    return Round(
        round_number=1,
        pro_message=Message(
            debate_id="test-id",
            round_number=1,
            role=Role.PRO,
            content="JWT 支持跨域认证",
            model_used="mimo",
            confidence=0.8
        ),
        con_message=Message(
            debate_id="test-id",
            round_number=1,
            role=Role.CON,
            content="Session cookies 更安全",
            model_used="deepseek",
            confidence=0.8
        ),
        judge_message=Message(
            debate_id="test-id",
            round_number=1,
            role=Role.JUDGE,
            content="双方各有优势",
            model_used="mimo",
            confidence=0.9
        )
    )


@pytest.fixture
def sample_verdict():
    """标准裁决结果."""
    return Verdict(
        recommendation="建议使用 JWT 结合 refresh token 机制",
        winner="pro",
        confidence=0.85,
        action_plan=[
            "实现 JWT 认证中间件",
            "添加 refresh token 刷新逻辑",
            "配置 token 过期时间"
        ]
    )


@pytest.fixture
def sample_debate_result(sample_round, sample_verdict):
    """完整辩论结果."""
    return DebateResult(
        id="test-debate-id",
        topic="JWT vs Session Cookies",
        status=DebateStatus.COMPLETED,
        rounds=[sample_round],
        verdict=sample_verdict
    )


@pytest.fixture
def mock_agent():
    """Mock AI Agent."""
    agent = AsyncMock()
    agent.chat = AsyncMock(return_value="这是 AI 的回复内容")
    agent.get_embedding = AsyncMock(return_value=[0.1, 0.2, 0.3])
    return agent


@pytest.fixture
def mock_memory_store():
    """Mock 记忆存储."""
    store = AsyncMock()
    store.save = AsyncMock(return_value=True)
    store.search = AsyncMock(return_value=[])
    store.get_by_topic = AsyncMock(return_value=None)
    store.get_relevant = AsyncMock(return_value=[])
    return store
