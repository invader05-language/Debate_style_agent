"""
Debate engine core logic for Multi-AI Debate Agent.
Orchestrates the debate process between multiple AI agents.
"""

import json
import asyncio
from typing import List, Optional, Callable, TYPE_CHECKING
from datetime import datetime
from debate.protocol import (
    DebateStatus, Role, Message, Round, Verdict,
    DebateResult, DebateConfig
)
from debate.roles import get_role, RolePrompt
from config import config

if TYPE_CHECKING:
    from memory.store import MemoryStore
    from agents.base_agent import BaseAgent
    from agents.mimo_agent import MIMOAgent
    from agents.deepseek_agent import DeepSeekAgent


class DebateEngine:
    """
    Core debate engine that orchestrates the debate process.

    ┌─────────────────────────────────────────────┐
    │              DebateEngine                    │
    ├─────────────────────────────────────────────┤
    │ + start_debate(topic: str) -> DebateResult  │
    │ + run_round(pro, con, judge) -> Round       │
    │ + check_termination(rounds) -> bool         │
    │ + format_output(result) -> JSON             │
    └─────────────────────────────────────────────┘
    """

    def __init__(self, memory_store: Optional['MemoryStore'] = None):
        # Lazy imports to avoid circular dependency
        from agents.mimo_agent import MIMOAgent
        from agents.deepseek_agent import DeepSeekAgent

        self.memory_store = memory_store
        self.agents = {
            "mimo": MIMOAgent(),
            "deepseek": DeepSeekAgent()
        }
        self.on_message_callback: Optional[Callable] = None

    def set_on_message_callback(self, callback: Callable):
        """Set callback for real-time message updates (WebSocket)."""
        self.on_message_callback = callback

    async def _notify_message(self, message: Message):
        """Notify about new message (for WebSocket)."""
        if self.on_message_callback:
            await self.on_message_callback(message)

    async def start_debate(self, config: DebateConfig) -> DebateResult:
        """
        Start a new debate.

        Args:
            config: Debate configuration

        Returns:
            DebateResult with the debate outcome
        """
        # Create debate result
        result = DebateResult(
            topic=config.topic,
            status=DebateStatus.RUNNING,
            rounds=[]
        )

        # Get relevant memories
        memories = []
        if self.memory_store:
            memories = await self.memory_store.get_relevant(config.topic)

        # Run debate rounds
        for round_num in range(1, config.max_rounds + 1):
            try:
                round_result = await self._run_round(
                    config=config,
                    round_number=round_num,
                    previous_messages=self._get_all_messages(result),
                    memories=memories
                )
                result.rounds.append(round_result)

                # Check for early termination (consensus)
                if await self._check_consensus(round_result):
                    break

            except Exception as e:
                result.status = DebateStatus.FAILED
                raise e

        # Get judge verdict
        try:
            verdict = await self._get_verdict(
                config=config,
                all_messages=self._get_all_messages(result),
                memories=memories
            )
            result.verdict = verdict
            result.status = DebateStatus.COMPLETED
            result.completed_at = datetime.now()

            # Save to memory
            if self.memory_store:
                await self._save_to_memory(result)

        except Exception as e:
            result.status = DebateStatus.FAILED
            raise e

        return result

    async def _run_round(self, config: DebateConfig, round_number: int,
                        previous_messages: List[Message],
                        memories: List[dict]) -> Round:
        """
        Run a single debate round.

        Args:
            config: Debate configuration
            round_number: Current round number
            previous_messages: Messages from previous rounds
            memories: Relevant memories

        Returns:
            Round with pro, con, and judge messages
        """
        # Get roles
        pro_role = get_role(Role.PRO, config.models.get("pro", "mimo"))
        con_role = get_role(Role.CON, config.models.get("con", "deepseek"))
        judge_role = get_role(Role.JUDGE, config.models.get("judge", "mimo"))

        # Get agents
        pro_agent = self.agents[pro_role.model_name]
        con_agent = self.agents[con_role.model_name]
        judge_agent = self.agents[judge_role.model_name]

        # Get prompts
        pro_system = pro_role.get_system_prompt(config.topic, memories)
        pro_prompt = pro_role.get_debate_prompt(
            config.topic, round_number, previous_messages, memories
        )

        con_system = con_role.get_system_prompt(config.topic, memories)
        con_prompt = con_role.get_debate_prompt(
            config.topic, round_number, previous_messages, memories
        )

        # Run pro
        pro_response = await pro_agent.chat(
            system_prompt=pro_system,
            user_message=pro_prompt,
            context=previous_messages[-5:] if previous_messages else []
        )
        pro_message = Message(
            debate_id="",  # Will be set by caller
            round_number=round_number,
            role=Role.PRO,
            content=pro_response,
            model_used=pro_role.model_name,
            confidence=0.8
        )
        await self._notify_message(pro_message)

        # Run con
        con_response = await con_agent.chat(
            system_prompt=con_system,
            user_message=con_prompt,
            context=previous_messages[-5:] + [pro_message]
        )
        con_message = Message(
            debate_id="",
            round_number=round_number,
            role=Role.CON,
            content=con_response,
            model_used=con_role.model_name,
            confidence=0.8
        )
        await self._notify_message(con_message)

        # Run judge (summary for this round)
        judge_system = judge_role.get_system_prompt(config.topic, memories)
        judge_prompt = f"""请作为裁判，对第 {round_number} 轮辩论进行简要总结：

正方观点: {pro_response[:500]}
反方观点: {con_response[:500]}

请指出双方的主要分歧点和共识点。"""

        judge_response = await judge_agent.chat(
            system_prompt=judge_system,
            user_message=judge_prompt,
            context=[]
        )
        judge_message = Message(
            debate_id="",
            round_number=round_number,
            role=Role.JUDGE,
            content=judge_response,
            model_used=judge_role.model_name,
            confidence=0.9
        )
        await self._notify_message(judge_message)

        return Round(
            round_number=round_number,
            pro_message=pro_message,
            con_message=con_message,
            judge_message=judge_message
        )

    async def _get_verdict(self, config: DebateConfig,
                          all_messages: List[Message],
                          memories: List[dict]) -> Verdict:
        """
        Get final verdict from judge.

        Args:
            config: Debate configuration
            all_messages: All debate messages
            memories: Relevant memories

        Returns:
            Verdict with recommendation and action plan
        """
        judge_role = get_role(Role.JUDGE, config.models.get("judge", "mimo"))
        judge_agent = self.agents[judge_role.model_name]

        judge_system = judge_role.get_system_prompt(config.topic, memories)
        judge_prompt = judge_role.get_verdict_prompt(
            config.topic, all_messages, memories
        )

        response = await judge_agent.chat(
            system_prompt=judge_system,
            user_message=judge_prompt,
            context=[]
        )

        # Parse JSON response
        try:
            # Try to extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                verdict_data = json.loads(json_str)
                return Verdict(
                    recommendation=verdict_data.get("recommendation", response),
                    winner=verdict_data.get("winner", "draw"),
                    confidence=verdict_data.get("confidence", 0.8),
                    action_plan=verdict_data.get("action_plan", [])
                )
        except json.JSONDecodeError:
            pass

        # Fallback: create verdict from response text
        return Verdict(
            recommendation=response,
            winner="draw",
            confidence=0.7,
            action_plan=["请根据裁判建议执行"]
        )

    async def _check_consensus(self, round_result: Round) -> bool:
        """
        Check if there's consensus between pro and con.

        Args:
            round_result: Current round result

        Returns:
            True if consensus reached
        """
        # Simple heuristic: if both sides mention similar keywords
        pro_content = round_result.pro_message.content.lower()
        con_content = round_result.con_message.content.lower()

        # Check for explicit consensus indicators
        consensus_indicators = ["同意", "赞同", "共识", "一致", "有道理"]
        for indicator in consensus_indicators:
            if indicator in con_content and indicator in pro_content:
                return True

        return False

    def _get_all_messages(self, result: DebateResult) -> List[Message]:
        """Extract all messages from debate result."""
        messages = []
        for round in result.rounds:
            messages.append(round.pro_message)
            messages.append(round.con_message)
            if round.judge_message:
                messages.append(round.judge_message)
        return messages

    async def _save_to_memory(self, result: DebateResult):
        """Save debate result to memory."""
        if not self.memory_store:
            return

        # Create memory entry
        memory = {
            "topic": result.topic,
            "debate_summary": self._generate_summary(result),
            "outcome": result.verdict.recommendation if result.verdict else "",
            "confidence": result.verdict.confidence if result.verdict else 0.5,
            "tags": self._extract_tags(result),
            "lessons_learned": self._extract_lessons(result)
        }

        await self.memory_store.save(memory)

    def _generate_summary(self, result: DebateResult) -> str:
        """Generate debate summary."""
        summary_parts = []
        for round in result.rounds:
            summary_parts.append(
                f"第{round.round_number}轮: "
                f"正方建议{round.pro_message.content[:100]}..., "
                f"反方质疑{round.con_message.content[:100]}..."
            )
        return "\n".join(summary_parts)

    def _extract_tags(self, result: DebateResult) -> List[str]:
        """Extract tags from debate."""
        tags = []
        # Extract from topic
        topic_words = result.topic.split()
        tags.extend(topic_words[:3])

        # Extract from verdict
        if result.verdict:
            recommendation = result.verdict.recommendation.lower()
            if "jwt" in recommendation:
                tags.append("JWT")
            if "数据库" in recommendation or "database" in recommendation:
                tags.append("数据库")
            if "安全" in recommendation:
                tags.append("安全")

        return list(set(tags))

    def _extract_lessons(self, result: DebateResult) -> List[str]:
        """Extract lessons learned from debate."""
        lessons = []
        if result.verdict:
            lessons.append(result.verdict.recommendation[:200])
        return lessons
