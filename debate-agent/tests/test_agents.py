"""
Agent 单元测试 for Multi-AI Debate Agent.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from agents.mimo_agent import MIMOAgent
from agents.deepseek_agent import DeepSeekAgent


class TestMIMOAgent:
    """MIMO Agent 测试."""

    @pytest.mark.asyncio
    async def test_chat_success(self, mock_agent):
        """测试 chat 成功调用."""
        agent = MIMOAgent()
        with patch.object(agent, 'chat', return_value="测试回复"):
            result = await agent.chat(
                system_prompt="你是一个测试助手",
                user_message="你好"
            )
            assert result == "测试回复"

    @pytest.mark.asyncio
    async def test_chat_returns_string(self, mock_agent):
        """测试 chat 返回字符串."""
        agent = MIMOAgent()
        with patch.object(agent, 'chat', return_value="回复内容"):
            result = await agent.chat(
                system_prompt="系统提示",
                user_message="用户消息"
            )
            assert isinstance(result, str)
            assert len(result) > 0

    @pytest.mark.asyncio
    async def test_get_embedding(self):
        """测试 get_embedding."""
        agent = MIMOAgent()
        with patch.object(agent, 'get_embedding', return_value=[0.1, 0.2, 0.3]):
            result = await agent.get_embedding("测试文本")
            assert isinstance(result, list)
            assert len(result) == 3


class TestDeepSeekAgent:
    """DeepSeek Agent 测试."""

    @pytest.mark.asyncio
    async def test_chat_success(self, mock_agent):
        """测试 chat 成功调用."""
        agent = DeepSeekAgent()
        with patch.object(agent, 'chat', return_value="DeepSeek 回复"):
            result = await agent.chat(
                system_prompt="你是一个测试助手",
                user_message="你好"
            )
            assert result == "DeepSeek 回复"

    @pytest.mark.asyncio
    async def test_chat_returns_string(self, mock_agent):
        """测试 chat 返回字符串."""
        agent = DeepSeekAgent()
        with patch.object(agent, 'chat', return_value="回复内容"):
            result = await agent.chat(
                system_prompt="系统提示",
                user_message="用户消息"
            )
            assert isinstance(result, str)
            assert len(result) > 0


class TestAgentBuildMessages:
    """Agent 消息构建测试."""

    def test_build_messages_format(self):
        """测试消息构建格式."""
        from agents.base_agent import BaseAgent

        class TestAgent(BaseAgent):
            async def chat(self, **kwargs):
                return "test"
            async def get_embedding(self, text):
                return [0.1]

        agent = TestAgent(model_name="test-model")
        messages = agent._build_messages(
            system_prompt="系统提示",
            user_message="用户消息",
            context=[]
        )

        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"
        assert messages[0]["content"] == "系统提示"
        assert messages[1]["content"] == "用户消息"

    def test_build_messages_with_context(self):
        """测试带上下文的消息构建."""
        from agents.base_agent import BaseAgent
        from debate.protocol import Message, Role

        class TestAgent(BaseAgent):
            async def chat(self, **kwargs):
                return "test"
            async def get_embedding(self, text):
                return [0.1]

        agent = TestAgent(model_name="test-model")
        context = [
            Message(
                debate_id="test",
                round_number=1,
                role=Role.PRO,
                content="上下文消息",
                model_used="mimo",
                confidence=0.8
            )
        ]

        messages = agent._build_messages(
            system_prompt="系统提示",
            user_message="用户消息",
            context=context
        )

        assert len(messages) == 3
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "assistant"
        assert messages[2]["role"] == "user"
