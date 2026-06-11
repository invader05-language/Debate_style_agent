"""
AI 代码生成器 for Multi-AI Debate Agent.
将辩论的 action_plan 转化为可执行代码.
"""

import json
import logging
from dataclasses import dataclass, field
from typing import List, Optional

from agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)


@dataclass
class GeneratedCode:
    """生成的代码结构."""
    main_code: str
    test_code: str = ""
    dependencies: List[str] = field(default_factory=list)
    language: str = "python"


class CodeGenerator:
    """将辩论的 action_plan 转化为可执行代码."""

    def __init__(self, agent: BaseAgent):
        self.agent = agent

    async def generate(self, action_plan: List[str],
                       language: str = "python") -> GeneratedCode:
        """根据 action_plan 生成代码和测试."""
        plan_text = "\n".join(f"- {step}" for step in action_plan)

        system_prompt = f"""你是一个代码生成专家。根据给定的行动方案，生成可执行的 {language} 代码和单元测试。

要求：
1. 代码必须完整、可直接运行
2. 包含必要的 import 语句
3. 包含错误处理
4. 生成对应的单元测试
5. 列出需要安装的依赖包

请以 JSON 格式输出：
{{
    "main_code": "完整的主代码",
    "test_code": "完整的测试代码",
    "dependencies": ["依赖包1", "依赖包2"]
}}"""

        user_prompt = f"""请根据以下行动方案生成 {language} 代码：

{plan_text}

请确保代码可以直接运行，并包含完整的错误处理。"""

        try:
            response = await self.agent.chat(
                system_prompt=system_prompt,
                user_message=user_prompt
            )

            # Parse JSON response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                data = json.loads(json_str)

                return GeneratedCode(
                    main_code=data.get("main_code", ""),
                    test_code=data.get("test_code", ""),
                    dependencies=data.get("dependencies", []),
                    language=language
                )

            # Fallback: use response as main code
            return GeneratedCode(
                main_code=response,
                language=language
            )

        except Exception as e:
            logger.error(f"Code generation failed: {e}")
            return GeneratedCode(
                main_code=f"# Code generation failed: {e}\n# Action plan:\n# {plan_text}",
                language=language
            )

    async def refine(self, code: GeneratedCode,
                     error: str) -> GeneratedCode:
        """根据执行错误修复代码."""
        system_prompt = """你是一个代码修复专家。根据错误信息修复代码中的问题。

请以 JSON 格式输出：
{
    "main_code": "修复后的完整代码",
    "test_code": "修复后的完整测试代码",
    "dependencies": ["依赖包列表"]
}"""

        user_prompt = f"""请修复以下代码中的错误：

错误信息：
{error}

当前代码：
{code.main_code}

请分析错误原因并提供修复后的完整代码。"""

        try:
            response = await self.agent.chat(
                system_prompt=system_prompt,
                user_message=user_prompt
            )

            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                data = json.loads(json_str)

                return GeneratedCode(
                    main_code=data.get("main_code", code.main_code),
                    test_code=data.get("test_code", code.test_code),
                    dependencies=data.get("dependencies", code.dependencies),
                    language=code.language
                )

            return code

        except Exception as e:
            logger.error(f"Code refinement failed: {e}")
            return code
