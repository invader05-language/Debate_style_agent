"""
WebSocket 测试 for Multi-AI Debate Agent.
"""

import pytest
import json
from unittest.mock import AsyncMock, MagicMock
from backend.websocket.debate_ws import ConnectionManager


class TestConnectionManager:
    """ConnectionManager 测试."""

    @pytest.fixture
    def manager(self):
        return ConnectionManager()

    @pytest.fixture
    def mock_websocket(self):
        ws = AsyncMock()
        ws.send_json = AsyncMock()
        ws.send_text = AsyncMock()
        return ws

    @pytest.mark.asyncio
    async def test_connect(self, manager, mock_websocket):
        """测试连接成功."""
        await manager.connect(mock_websocket, "debate-1")

        assert "debate-1" in manager.active_connections
        assert mock_websocket in manager.active_connections["debate-1"]

    @pytest.mark.asyncio
    async def test_connect_multiple(self, manager):
        """测试多客户端连接."""
        ws1 = AsyncMock()
        ws2 = AsyncMock()

        await manager.connect(ws1, "debate-1")
        await manager.connect(ws2, "debate-1")

        assert len(manager.active_connections["debate-1"]) == 2

    def test_disconnect(self, manager, mock_websocket):
        """测试断开连接."""
        manager.active_connections["debate-1"] = {mock_websocket}

        manager.disconnect(mock_websocket, "debate-1")

        assert "debate-1" not in manager.active_connections

    def test_disconnect_partial(self, manager):
        """测试部分断开连接."""
        ws1 = MagicMock()
        ws2 = MagicMock()
        manager.active_connections["debate-1"] = {ws1, ws2}

        manager.disconnect(ws1, "debate-1")

        assert "debate-1" in manager.active_connections
        assert ws2 in manager.active_connections["debate-1"]

    @pytest.mark.asyncio
    async def test_broadcast(self, manager, mock_websocket):
        """测试消息广播."""
        manager.active_connections["debate-1"] = {mock_websocket}

        message = {"type": "test", "content": "hello"}
        await manager.broadcast("debate-1", message)

        mock_websocket.send_json.assert_called_once_with(message)

    @pytest.mark.asyncio
    async def test_broadcast_no_connections(self, manager):
        """测试无连接时广播."""
        # Should not raise
        await manager.broadcast("non-existent", {"type": "test"})

    @pytest.mark.asyncio
    async def test_broadcast_removes_broken(self, manager):
        """测试广播时移除断开的连接."""
        good_ws = AsyncMock()
        bad_ws = AsyncMock()
        bad_ws.send_json.side_effect = Exception("Connection closed")

        manager.active_connections["debate-1"] = {good_ws, bad_ws}

        await manager.broadcast("debate-1", {"type": "test"})

        # Bad connection should be removed
        assert good_ws in manager.active_connections["debate-1"]
        assert bad_ws not in manager.active_connections["debate-1"]


class TestBroadcastHelpers:
    """广播辅助函数测试."""

    @pytest.mark.asyncio
    async def test_broadcast_debate_message(self):
        """测试辩论消息广播."""
        from backend.websocket.debate_ws import broadcast_debate_message, manager

        mock_ws = AsyncMock()
        manager.active_connections["test-debate"] = {mock_ws}

        await broadcast_debate_message(
            debate_id="test-debate",
            role="pro",
            content="测试内容",
            round_number=1,
            model_used="mimo"
        )

        call_args = mock_ws.send_json.call_args[0][0]
        assert call_args["type"] == "debate_message"
        assert call_args["role"] == "pro"
        assert call_args["content"] == "测试内容"
        assert call_args["round_number"] == 1

        # Cleanup
        manager.active_connections.clear()

    @pytest.mark.asyncio
    async def test_broadcast_debate_status(self):
        """测试状态广播."""
        from backend.websocket.debate_ws import broadcast_debate_status, manager

        mock_ws = AsyncMock()
        manager.active_connections["test-debate"] = {mock_ws}

        await broadcast_debate_status(
            debate_id="test-debate",
            status="completed",
            message="辩论完成"
        )

        call_args = mock_ws.send_json.call_args[0][0]
        assert call_args["type"] == "status_update"
        assert call_args["status"] == "completed"

        manager.active_connections.clear()

    @pytest.mark.asyncio
    async def test_broadcast_debate_verdict(self):
        """测试裁决广播."""
        from backend.websocket.debate_ws import broadcast_debate_verdict, manager

        mock_ws = AsyncMock()
        manager.active_connections["test-debate"] = {mock_ws}

        verdict = {"recommendation": "建议", "winner": "pro"}
        await broadcast_debate_verdict("test-debate", verdict)

        call_args = mock_ws.send_json.call_args[0][0]
        assert call_args["type"] == "verdict"
        assert call_args["verdict"]["recommendation"] == "建议"

        manager.active_connections.clear()
