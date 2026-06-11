"""
Role definitions for Multi-AI Debate Agent.
Defines the behavior and prompts for each debate role.
"""

from typing import List, Optional
from debate.protocol import Role, Message


class RolePrompt:
    """Base class for role prompts."""

    def __init__(self, role: Role, model_name: str):
        self.role = role
        self.model_name = model_name

    def get_system_prompt(self, topic: str, memories: Optional[List[dict]] = None) -> str:
        """Get system prompt for the role."""
        raise NotImplementedError

    def get_debate_prompt(self, topic: str, round_number: int,
                         previous_messages: List[Message],
                         memories: Optional[List[dict]] = None) -> str:
        """Get debate prompt for the role."""
        raise NotImplementedError


class ProRole(RolePrompt):
    """Pro (正方) role - supports the topic."""

    def __init__(self, model_name: str = "mimo"):
        super().__init__(Role.PRO, model_name)

    def get_system_prompt(self, topic: str, memories: Optional[List[dict]] = None) -> str:
        memory_context = ""
        if memories:
            memory_context = "\n\n相关历史经验:\n"
            for mem in memories:
                memory_context += f"- {mem.get('topic', '')}: {mem.get('debate_summary', '')}\n"

        return f"""你是一个辩论中的正方（Pro），你的任务是支持和论证给定的主题。

主题: {topic}

你的职责:
1. 提出支持主题的论点和证据
2. 反驳反方的质疑
3. 用具体例子和数据支持你的观点
4. 保持逻辑清晰，论证有力
{memory_context}

请用中文回答，保持专业和有说服力的语气。"""

    def get_debate_prompt(self, topic: str, round_number: int,
                         previous_messages: List[Message],
                         memories: Optional[List[dict]] = None) -> str:
        if round_number == 1:
            return f"""请作为正方，针对以下主题提出你的初始论点：

主题: {topic}

请提出 2-3 个核心论点，每个论点都要有具体的理由和例子支持。"""

        # Include previous messages for context
        context = "\n辩论历史:\n"
        for msg in previous_messages[-3:]:  # Last 3 messages
            role_name = "正方" if msg.role == Role.PRO else "反方" if msg.role == Role.CON else "裁判"
            context += f"{role_name}: {msg.content[:200]}...\n"

        return f"""请作为正方，回应反方的质疑并强化你的立场：

主题: {topic}
轮次: {round_number}
{context}

请：
1. 回应反方的具体质疑点
2. 补充新的论据
3. 总结你的立场"""


class ConRole(RolePrompt):
    """Con (反方) role - challenges the topic."""

    def __init__(self, model_name: str = "deepseek"):
        super().__init__(Role.CON, model_name)

    def get_system_prompt(self, topic: str, memories: Optional[List[dict]] = None) -> str:
        memory_context = ""
        if memories:
            memory_context = "\n\n相关历史经验:\n"
            for mem in memories:
                memory_context += f"- {mem.get('topic', '')}: {mem.get('debate_summary', '')}\n"

        return f"""你是一个辩论中的反方（Con），你的任务是质疑和挑战给定的主题。

主题: {topic}

你的职责:
1. 找出主题的潜在问题和风险
2. 提出替代方案
3. 用具体例子和数据反驳正方观点
4. 保持逻辑清晰，质疑有力
{memory_context}

请用中文回答，保持专业和批判性的语气。"""

    def get_debate_prompt(self, topic: str, round_number: int,
                         previous_messages: List[Message],
                         memories: Optional[List[dict]] = None) -> str:
        if round_number == 1:
            return f"""请作为反方，针对以下主题提出你的质疑：

主题: {topic}

请：
1. 指出主题的潜在问题和风险
2. 提出 2-3 个具体的质疑点
3. 提出可能的替代方案"""

        # Include previous messages for context
        context = "\n辩论历史:\n"
        for msg in previous_messages[-3:]:  # Last 3 messages
            role_name = "正方" if msg.role == Role.PRO else "反方" if msg.role == Role.CON else "裁判"
            context += f"{role_name}: {msg.content[:200]}...\n"

        return f"""请作为反方，回应正方的论点并强化你的质疑：

主题: {topic}
轮次: {round_number}
{context}

请：
1. 回应正方的具体论点
2. 补充新的质疑
3. 提出你的替代方案"""


class JudgeRole(RolePrompt):
    """Judge (裁判) role - summarizes and makes final decision."""

    def __init__(self, model_name: str = "mimo"):
        super().__init__(Role.JUDGE, model_name)

    def get_system_prompt(self, topic: str, memories: Optional[List[dict]] = None) -> str:
        memory_context = ""
        if memories:
            memory_context = "\n\n相关历史经验:\n"
            for mem in memories:
                memory_context += f"- {mem.get('topic', '')}: {mem.get('debate_summary', '')}\n"

        return f"""你是一个辩论中的裁判（Judge），你的任务是综合双方观点，给出最终建议。

主题: {topic}

你的职责:
1. 公正地评估双方的论点
2. 找出双方的共识点和分歧点
3. 给出最终的建议和执行计划
4. 保持客观和专业的判断
{memory_context}

请用中文回答，保持客观和专业的语气。"""

    def get_verdict_prompt(self, topic: str, all_messages: List[Message],
                          memories: Optional[List[dict]] = None) -> str:
        # Build debate summary
        debate_summary = "\n辩论总结:\n"
        current_round = 0
        for msg in all_messages:
            if msg.round_number != current_round:
                current_round = msg.round_number
                debate_summary += f"\n--- 第 {current_round} 轮 ---\n"
            role_name = "正方" if msg.role == Role.PRO else "反方" if msg.role == Role.CON else "裁判"
            debate_summary += f"{role_name}: {msg.content[:300]}...\n"

        return f"""请作为裁判，根据以下辩论内容给出最终判决：

主题: {topic}
{debate_summary}

请以 JSON 格式输出判决结果：
{{
    "recommendation": "你的最终建议",
    "winner": "pro 或 con 或 draw",
    "confidence": 0.85,
    "action_plan": ["步骤1", "步骤2", "步骤3"]
}}

请确保输出是有效的 JSON 格式。"""


def get_role(role: Role, model_name: Optional[str] = None) -> RolePrompt:
    """Factory function to get role instance."""
    if role == Role.PRO:
        return ProRole(model_name or "mimo")
    elif role == Role.CON:
        return ConRole(model_name or "deepseek")
    elif role == Role.JUDGE:
        return JudgeRole(model_name or "mimo")
    else:
        raise ValueError(f"Unknown role: {role}")
