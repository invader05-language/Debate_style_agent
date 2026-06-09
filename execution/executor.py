"""
Code execution engine for Multi-AI Debate Agent.
Integrates CodeGenerator + DockerSandbox/FallbackSandbox.
"""

import logging
from typing import List, Optional

from config import config
from execution.sandbox import (
    DockerSandbox, FallbackSandbox,
    ExecutionResult, TestResult
)
from execution.code_generator import CodeGenerator, GeneratedCode
from agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)


class CodeExecutor:
    """
    Unified code execution engine.

    Flow: action_plan -> CodeGenerator -> Sandbox -> ExecutionResult

    ┌──────────────────────────────────────────────────────────┐
    │                     CodeExecutor                          │
    ├──────────────────────────────────────────────────────────┤
    │ + execute(code, language) -> ExecutionResult             │
    │ + generate_and_execute(plan, lang, retries) -> ExecResult│
    │ + run_tests(code, test_code, lang) -> TestResult         │
    │ + generate_code(plan, lang) -> GeneratedCode             │
    └──────────────────────────────────────────────────────────┘
    """

    def __init__(self, use_sandbox: bool = True,
                 agent: Optional[BaseAgent] = None):
        self.timeout = config.EXECUTION_TIMEOUT
        self.memory_limit = config.EXECUTION_MEMORY_LIMIT

        # Sandbox: prefer Docker, fallback to local subprocess
        if use_sandbox:
            try:
                self.sandbox = DockerSandbox(
                    timeout=self.timeout,
                    memory_limit=self.memory_limit
                )
                logger.info("Using DockerSandbox for code execution")
            except Exception as e:
                logger.warning(f"Docker unavailable, using FallbackSandbox: {e}")
                self.sandbox = FallbackSandbox(timeout=self.timeout)
        else:
            self.sandbox = FallbackSandbox(timeout=self.timeout)

        # Code generator (lazy init — needs an agent)
        self._agent = agent
        self._generator: Optional[CodeGenerator] = None

    def _get_generator(self) -> CodeGenerator:
        """Lazy-init CodeGenerator with a default agent."""
        if self._generator is None:
            if self._agent is None:
                from agents.mimo_agent import MIMOAgent
                self._agent = MIMOAgent()
            self._generator = CodeGenerator(agent=self._agent)
        return self._generator

    # ── Core execution ──────────────────────────────────────────

    async def execute(self, code: str,
                      language: str = "python") -> ExecutionResult:
        """
        Execute code in sandbox.

        Args:
            code: Source code to execute
            language: "python" or "javascript"

        Returns:
            ExecutionResult with output/error/exit_code
        """
        return await self.sandbox.execute(code, language)

    async def execute_python(self, code: str) -> ExecutionResult:
        """Execute Python code (convenience alias)."""
        return await self.execute(code, "python")

    async def execute_javascript(self, code: str) -> ExecutionResult:
        """Execute JavaScript code (convenience alias)."""
        return await self.execute(code, "javascript")

    # ── Generate + Execute pipeline ─────────────────────────────

    async def generate_code(self, action_plan: List[str],
                            language: str = "python") -> GeneratedCode:
        """
        Generate executable code from a debate action_plan.

        Args:
            action_plan: List of implementation steps from the verdict
            language: Target language

        Returns:
            GeneratedCode with main_code, test_code, dependencies
        """
        generator = self._get_generator()
        return await generator.generate(action_plan, language)

    async def generate_and_execute(
        self,
        action_plan: List[str],
        language: str = "python",
        max_retries: int = 3
    ) -> ExecutionResult:
        """
        Full pipeline: generate code from action_plan, execute it,
        auto-fix on failure up to max_retries.

        Args:
            action_plan: Steps from debate verdict
            language: Target language
            max_retries: Max fix-and-rerun attempts

        Returns:
            ExecutionResult of the final attempt
        """
        generator = self._get_generator()

        # Step 1: Generate initial code
        logger.info(f"Generating code from {len(action_plan)}-step action plan")
        generated = await generator.generate(action_plan, language)

        if not generated.main_code.strip():
            return ExecutionResult(
                success=False,
                error="Code generation produced empty output",
                exit_code=-1
            )

        # Step 2: Execute with retry loop
        for attempt in range(1, max_retries + 1):
            logger.info(f"Execution attempt {attempt}/{max_retries}")
            result = await self.sandbox.execute(generated.main_code, language)

            if result.success:
                logger.info(f"Execution succeeded on attempt {attempt}")
                return result

            logger.warning(
                f"Execution failed on attempt {attempt}: "
                f"{result.error[:200]}"
            )

            # Step 3: Ask AI to fix the code
            if attempt < max_retries:
                logger.info("Requesting code fix from AI")
                generated = await generator.refine(generated, result.error)

        logger.error(f"Execution failed after {max_retries} attempts")
        return result

    async def run_tests(self, code: str, test_code: str,
                        language: str = "python") -> TestResult:
        """
        Run code and its tests in sandbox.

        Args:
            code: Main source code
            test_code: Test code
            language: Language

        Returns:
            TestResult with passed/failed/errors counts
        """
        return await self.sandbox.execute_with_tests(code, test_code, language)
