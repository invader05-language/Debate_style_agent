"""
WebSocket connection manager for real-time communication.
"""

import json
import logging
from typing import Dict, Set
from fastapi import WebSocket

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections for real-time updates."""

    def __init__(self):
        # task_id -> set of websocket connections
        self._connections: Dict[str, Set[WebSocket]] = {}
        # Global connections (for notifications, dashboard updates)
        self._global: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket, task_id: str = None):
        """Accept and register a WebSocket connection."""
        await websocket.accept()
        if task_id:
            if task_id not in self._connections:
                self._connections[task_id] = set()
            self._connections[task_id].add(websocket)
        else:
            self._global.add(websocket)

    def disconnect(self, websocket: WebSocket, task_id: str = None):
        """Remove a WebSocket connection."""
        if task_id and task_id in self._connections:
            self._connections[task_id].discard(websocket)
            if not self._connections[task_id]:
                del self._connections[task_id]
        else:
            self._global.discard(websocket)

    async def broadcast_to_task(self, task_id: str, message: dict):
        """Broadcast a message to all connections for a specific task."""
        connections = self._connections.get(task_id, set())
        dead = set()
        for ws in connections:
            try:
                await ws.send_json(message)
            except Exception:
                dead.add(ws)
        for ws in dead:
            connections.discard(ws)

    async def broadcast_global(self, message: dict):
        """Broadcast a message to all global connections."""
        dead = set()
        for ws in self._global:
            try:
                await ws.send_json(message)
            except Exception:
                dead.add(ws)
        for ws in dead:
            self._global.discard(ws)

    @property
    def active_connections(self) -> int:
        total = len(self._global)
        for conns in self._connections.values():
            total += len(conns)
        return total


# Singleton instance
manager = ConnectionManager()
