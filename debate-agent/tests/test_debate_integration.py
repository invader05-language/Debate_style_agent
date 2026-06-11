"""
辩论集成测试 for Multi-AI Debate Agent.
使用 mock agents 测试完整辩论流程.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from debate.engine import DebateEngine
from debate.protocol import (
    DebateStatus, Role, Message, Round, Verdict,
    DebateResult, DebateConfig
)


class TestDebateIntegration:
    """辩论集成测试."""

    @pytest.mark.asyncio
    async def test_full_debate_flow(self, sample_debate_config, mock_memory_store):
        """测试完整辩论流程."""
        engine = DebateEngine(memory_store=mock_memory_store)

        # Mock agents responses
        mock_pro_response = "JWT 支持跨域认证，无状态性更好"
        mock_con_response = "Session cookies 更安全，实现更简单"
        mock_judge_response = "双方各有优势，需要根据场景选择"
        mock_verdict_response = '''
        {
            "recommendation": "建议使用 JWT 结合 refresh token",
            "winner": "pro",
            "confidence": 0.85,
            "action_plan": ["实现 JWT 中间件", "添加 token 刷新"]
        }
        '''

        with patch.object(engine.agents["mimo"], 'chat') as mock_mimo_chat, \
             patch.object(engine.agents["deepseek"], 'chat') as mock_deepseek_chat:

            # Setup mock responses
            mock_mimo_chat.side_effect = [
                mock_pro_response,    # Round 1 pro
                mock_judge_response,  # Round 1 judge summary
                mock_pro_response,    # Round 2 pro
                mock_judge_response,  # Round 2 judge summary
                mock_verdict_response # Final verdict
            ]
            mock_deepseek_chat.side_effect = [
                mock_con_response,    # Round 1 con
                mock_con_response,    # Round 2 con
            ]

            result = await engine.start_debate(sample_debate_config)

            assert result.status == DebateStatus.COMPLETED
            assert len(result.rounds) == sample_debate_config.max_rounds
            assert result.verdict is not None
            assert result.verdict.winner in ["pro", "con", "draw"]

    @pytest.mark.asyncio
    async def test_debate_early_consensus(self, mock_memory_store):
        """测试共识提前终止."""
        config = DebateConfig(
            topic="测试主题",
            max_rounds=3,
            models={"pro": "mimo", "con": "deepseek", "judge": "mimo"}
        )

        engine = DebateEngine(memory_store=mock_memory_store)

        # Both sides agree
        consensus_response = "我同意对方的观点，这确实是一个好的方案。我赞同这个建议。"

        with patch.object(engine.agents["mimo"], 'chat') as mock_mimo_chat, \
             patch.object(engine.agents["deepseek"], 'chat') as mock_deepseek_chat:

            mock_mimo_chat.side_effect = [
                consensus_response,  # Round 1 pro - agrees
                "共识已达成",        # Round 1 judge
                '{"recommendation": "达成共识", "winner": "draw", "confidence": 0.9, "action_plan": ["执行共识方案"]}'
            ]
            mock_deepseek_chat.side_effect = [
                consensus_response,  # Round 1 con - agrees
            ]

            result = await engine.start_debate(config)

            # Should terminate early due to consensus
            assert len(result.rounds) < config.max_rounds

    @pytest.mark.asyncio
    async def test_debate_agent_failure_recovery(self, sample_debate_config, mock_memory_store):
        """测试 agent 失败时的恢复."""
        engine = DebateEngine(memory_store=mock_memory_store)

        with patch.object(engine.agents["mimo"], 'chat') as mock_mimo_chat, \
             patch.object(engine.agents["deepseek"], 'chat') as mock_deepseek_chat:

            # First call fails, second succeeds
            mock_mimo_chat.side_effect = [
                Exception("API 超时"),
                "恢复后的回复",
                "裁判总结",
                '{"recommendation": "建议", "winner": "pro", "confidence": 0.7, "action_plan": ["步骤1"]}'
            ]
            mock_deepseek_chat.return_value = "反方观点"

            # Should raise exception (no retry in engine itself)
            with pytest.raises(Exception):
                await engine.start_debate(sample_debate_config)

    @pytest.mark.asyncio
    async def test_debate_round_progression(self, sample_debate_config, mock_memory_store):
        """测试多轮辩论的消息累积."""
        engine = DebateEngine(memory_store=mock_memory_store)

        with patch.object(engine.agents["mimo"], 'chat') as mock_mimo_chat, \
             patch.object(engine.agents["deepseek"], 'chat') as mock_deepseek_chat:

            mock_mimo_chat.side_effect = [
                "第1轮正方观点", "第1轮裁判总结",
                "第2轮正方观点", "第2轮裁判总结",
                '{"recommendation": "最终建议", "winner": "pro", "confidence": 0.8, "action_plan": ["步骤1"]}'
            ]
            mock_deepseek_chat.side_effect = [
                "第1轮反方观点",
                "第2轮反方观点",
            ]

            result = await engine.start_debate(sample_debate_config)

            assert len(result.rounds) == 2
            # Check messages accumulate
            all_messages = engine._get_all_messages(result)
            assert len(all_messages) == 6  # 2 rounds * 3 messages each

    @pytest.mark.asyncio
    async def test_debate_verdict_json_parsing(self, mock_memory_store):
        """测试裁决 JSON 解析."""
        config = DebateConfig(
            topic="测试主题",
            max_rounds=1,
            models={"pro": "mimo", "con": "deepseek", "judge": "mimo"}
        )

        engine = DebateEngine(memory_store=mock_memory_store)

        verdict_json = '''
        {
            "recommendation": "使用 JWT 认证",
            "winner": "pro",
            "confidence": 0.9,
            "action_plan": ["步骤1", "步骤2"]
        }
        '''

        with patch.object(engine.agents["mimo"], 'chat') as mock_mimo_chat, \
             patch.object(engine.agents["deepseek"], 'chat') as mock_deepseek_chat:

            mock_mimo_chat.side_effect = [
                "正方观点", "裁判总结", verdict_json
            ]
            mock_deepseek_chat.return_value = "反方观点"

            result = await engine.start_debate(config)

            assert result.verdict is not None
            assert result.verdict.winner == "pro"
            assert result.verdict.confidence == 0.9
            assert len(result.verdict.action_plan) == 2

    @pytest.mark.asyncio
    async def test_debate_verdict_fallback(self, mock_memory_store):
        """测试裁决解析失败时的降级."""
        config = DebateConfig(
            topic="测试主题",
            max_rounds=1,
            models={"pro": "mimo", "con": "deepseek", "judge": "mimo"}
        )

        engine = DebateEngine(memory_store=mock_memory_store)

        with patch.object(engine.agents["mimo"], 'chat') as mock_mimo_chat, \
             patch.object(engine.agents["deepseek"], 'chat') as mock_deepseek_chat:

            mock_mimo_chat.side_effect = [
                "正方观点", "裁判总结", "这不是有效的 JSON 裁决"
            ]
            mock_deepseek_chat.return_value = "反方观点"

            result = await engine.start_debate(config)

            # Should use fallback verdict
            assert result.verdict is not None
            assert result.verdict.winner == "draw"
            assert result.verdict.confidence == 0.7
