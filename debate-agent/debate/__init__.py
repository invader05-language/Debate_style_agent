"""
Debate module for Multi-AI Debate Agent.
"""

from debate.protocol import (
    DebateStatus, Role, Message, Round, Verdict,
    DebateResult, DebateConfig
)
from debate.roles import get_role, RolePrompt
from debate.engine import DebateEngine

__all__ = [
    "DebateStatus", "Role", "Message", "Round", "Verdict",
    "DebateResult", "DebateConfig", "get_role", "RolePrompt",
    "DebateEngine"
]
