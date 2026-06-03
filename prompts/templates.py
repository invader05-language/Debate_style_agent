"""
Prompt templates for Multi-AI Debate Agent.
Provides reusable prompt templates for different debate scenarios.
"""

from typing import List, Optional


class PromptTemplates:
    """
    Prompt templates for debate agents.

    Provides standardized prompts for:
    - Pro (正方) arguments
    - Con (反方) arguments
    - Judge (裁判) verdicts
    - Memory integration
    """

    @staticmethod
    def get_pro_system_prompt(topic: str, memories: Optional[List[dict]] = None) -> str:
        """Get system prompt for pro agent."""
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

    @staticmethod
    def get_con_system_prompt(topic: str, memories: Optional[List[dict]] = None) -> str:
        """Get system prompt for con agent."""
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

    @staticmethod
    def get_judge_system_prompt(topic: str, memories: Optional[List[dict]] = None) -> str:
        """Get system prompt for judge agent."""
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

    @staticmethod
    def get_pro_initial_prompt(topic: str) -> str:
        """Get initial prompt for pro agent."""
        return f"""请作为正方，针对以下主题提出你的初始论点：

主题: {topic}

请提出 2-3 个核心论点，每个论点都要有具体的理由和例子支持。"""

    @staticmethod
    def get_con_initial_prompt(topic: str) -> str:
        """Get initial prompt for con agent."""
        return f"""请作为反方，针对以下主题提出你的质疑：

主题: {topic}

请：
1. 指出主题的潜在问题和风险
2. 提出 2-3 个具体的质疑点
3. 提出可能的替代方案"""

    @staticmethod
    def get_pro_response_prompt(topic: str, round_number: int,
                               pro_argument: str, con_argument: str) -> str:
        """Get response prompt for pro agent."""
        return f"""请作为正方，回应反方的质疑并强化你的立场：

主题: {topic}
轮次: {round_number}

正方论点: {pro_argument[:500]}
反方质疑: {con_argument[:500]}

请：
1. 回应反方的具体质疑点
2. 补充新的论据
3. 总结你的立场"""

    @staticmethod
    def get_con_response_prompt(topic: str, round_number: int,
                               pro_argument: str, con_argument: str) -> str:
        """Get response prompt for con agent."""
        return f"""请作为反方，回应正方的论点并强化你的质疑：

主题: {topic}
轮次: {round_number}

正方论点: {pro_argument[:500]}
反方质疑: {con_argument[:500]}

请：
1. 回应正方的具体论点
2. 补充新的质疑
3. 提出你的替代方案"""

    @staticmethod
    def get_judge_round_summary_prompt(topic: str, round_number: int,
                                      pro_argument: str, con_argument: str) -> str:
        """Get round summary prompt for judge agent."""
        return f"""请作为裁判，对第 {round_number} 轮辩论进行简要总结：

主题: {topic}

正方观点: {pro_argument[:500]}
反方观点: {con_argument[:500]}

请指出双方的主要分歧点和共识点。"""

    @staticmethod
    def get_judge_verdict_prompt(topic: str, debate_summary: str) -> str:
        """Get verdict prompt for judge agent."""
        return f"""请作为裁判，根据以下辩论内容给出最终判决：

主题: {topic}

辩论总结:
{debate_summary}

请以 JSON 格式输出判决结果：
{{
    "recommendation": "你的最终建议",
    "winner": "pro 或 con 或 draw",
    "confidence": 0.85,
    "action_plan": ["步骤1", "步骤2", "步骤3"]
}}

请确保输出是有效的 JSON 格式。"""
