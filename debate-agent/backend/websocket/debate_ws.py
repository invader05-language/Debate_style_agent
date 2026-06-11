"""
WebSocket handler for Multi-AI Debate Agent.
Handles real-time debate updates.
"""

import json
from typing import Dict, Set
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from datetime import datetime

router = APIRouter()


class ConnectionManager:
    """Manages WebSocket connections."""

    def __init__(self):
        # debate_id -> set of websockets
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, debate_id: str):
        """Connect to a debate room."""
        await websocket.accept()

        if debate_id not in self.active_connections:
            self.active_connections[debate_id] = set()

        self.active_connections[debate_id].add(websocket)

    def disconnect(self, websocket: WebSocket, debate_id: str):
        """Disconnect from a debate room."""
        if debate_id in self.active_connections:
            self.active_connections[debate_id].discard(websocket)
            if not self.active_connections[debate_id]:
                del self.active_connections[debate_id]

    async def broadcast(self, debate_id: str, message: dict):
        """Broadcast message to all connections in a debate room."""
        if debate_id in self.active_connections:
            broken = set()
            for connection in list(self.active_connections[debate_id]):
                try:
                    await connection.send_json(message)
                except Exception:
                    broken.add(connection)
            self.active_connections[debate_id] -= broken


# Global connection manager
manager = ConnectionManager()


@router.websocket("/ws/debate/{debate_id}")
async def websocket_debate(websocket: WebSocket, debate_id: str):
    """
    WebSocket endpoint for real-time debate updates.

    Connect to receive real-time updates during a debate.
    """
    await manager.connect(websocket, debate_id)

    try:
        # Send welcome message
        await websocket.send_json({
            "type": "connected",
            "debate_id": debate_id,
            "message": "Connected to debate room",
            "timestamp": datetime.utcnow().isoformat()
        })

        # Keep connection alive and handle messages
        while True:
            try:
                # Receive message from client
                data = await websocket.receive_text()
                message = json.loads(data)

                # Handle different message types
                if message.get("type") == "ping":
                    await websocket.send_json({
                        "type": "pong",
                        "timestamp": datetime.utcnow().isoformat()
                    })

            except WebSocketDisconnect:
                break
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid JSON format"
                })

    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(websocket, debate_id)


async def broadcast_debate_message(debate_id: str, role: str, content: str,
                                   round_number: int, model_used: str):
    """
    Broadcast a debate message to all connected clients.

    Args:
        debate_id: Debate ID
        role: Role (pro/con/judge)
        content: Message content
        round_number: Round number
        model_used: Model used
    """
    await manager.broadcast(debate_id, {
        "type": "debate_message",
        "debate_id": debate_id,
        "role": role,
        "content": content,
        "round_number": round_number,
        "model_used": model_used,
        "timestamp": datetime.utcnow().isoformat()
    })


async def broadcast_debate_status(debate_id: str, status: str, message: str = ""):
    """
    Broadcast debate status update.

    Args:
        debate_id: Debate ID
        status: New status
        message: Status message
    """
    await manager.broadcast(debate_id, {
        "type": "status_update",
        "debate_id": debate_id,
        "status": status,
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    })


async def broadcast_debate_verdict(debate_id: str, verdict: dict):
    """
    Broadcast debate verdict.

    Args:
        debate_id: Debate ID
        verdict: Verdict data
    """
    await manager.broadcast(debate_id, {
        "type": "verdict",
        "debate_id": debate_id,
        "verdict": verdict,
        "timestamp": datetime.utcnow().isoformat()
    })
