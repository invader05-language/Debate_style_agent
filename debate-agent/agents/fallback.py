"""
Agent 降级策略 for Multi-AI Debate Agent.
当首选 Agent 不可用时自动切换到备用 Agent.
"""

import logging
import time
from typing import Dict, Optional

from agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)


class AgentFallback:
    """Agent 降级策略."""

    def __init__(self, agents: Dict[str, BaseAgent]):
        self.agents = agents
        self.health_status: Dict[str, bool] = {name: True for name in agents}
        self.failure_counts: Dict[str, int] = {name: 0 for name in agents}
        self.last_failure: Dict[str, float] = {name: 0 for name in agents}
        self.max_failures = 3
        self.recovery_interval = 60  # seconds

    async def chat(self, preferred: str, fallback: str,
                   system_prompt: str, user_message: str,
                   context=None) -> str:
        """带降级的 chat 调用."""
        # Try preferred agent first
        if self._is_healthy(preferred):
            try:
                agent = self.agents[preferred]
                result = await agent.chat(
                    system_prompt=system_prompt,
                    user_message=user_message,
                    context=context
                )
                self._record_success(preferred)
                return result
            except Exception as e:
                self._record_failure(preferred, e)
                logger.warning(f"Agent {preferred} failed, falling back to {fallback}: {e}")

        # Fallback to backup agent
        if self._is_healthy(fallback):
            try:
                agent = self.agents[fallback]
                result = await agent.chat(
                    system_prompt=system_prompt,
                    user_message=user_message,
                    context=context
                )
                self._record_success(fallback)
                return result
            except Exception as e:
                self._record_failure(fallback, e)
                logger.error(f"Fallback agent {fallback} also failed: {e}")
                raise

        raise RuntimeError(f"Both agents {preferred} and {fallback} are unhealthy")

    def _is_healthy(self, agent_name: str) -> bool:
        """Check if agent is healthy. Auto-recover after interval."""
        if self.health_status.get(agent_name, False):
            return True

        # Check if recovery interval has passed
        last_fail = self.last_failure.get(agent_name, 0)
        if time.time() - last_fail > self.recovery_interval:
            self.health_status[agent_name] = True
            self.failure_counts[agent_name] = 0
            logger.info(f"Agent {agent_name} marked for recovery probe")
            return True

        return False

    def _record_failure(self, agent_name: str, error: Exception):
        """Record agent failure."""
        self.failure_counts[agent_name] = self.failure_counts.get(agent_name, 0) + 1
        self.last_failure[agent_name] = time.time()

        if self.failure_counts[agent_name] >= self.max_failures:
            self.health_status[agent_name] = False
            logger.warning(f"Agent {agent_name} marked unhealthy after {self.max_failures} failures")

    def _record_success(self, agent_name: str):
        """Record agent success."""
        self.failure_counts[agent_name] = 0
        self.health_status[agent_name] = True
