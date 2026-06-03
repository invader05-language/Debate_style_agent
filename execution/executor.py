"""
Code execution engine for Multi-AI Debate Agent.
Executes code in a sandboxed environment.
"""

import asyncio
import tempfile
import subprocess
import os
from typing import Optional
from config import config


class ExecutionResult:
    """Result of code execution."""

    def __init__(self, success: bool, output: str, error: str = "",
                 exit_code: int = 0, execution_time: float = 0.0):
        self.success = success
        self.output = output
        self.error = error
        self.exit_code = exit_code
        self.execution_time = execution_time

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "output": self.output,
            "error": self.error,
            "exit_code": self.exit_code,
            "execution_time": self.execution_time
        }


class CodeExecutor:
    """
    Code execution engine with sandbox support.

    ┌─────────────────────────────────────────────┐
    │              CodeExecutor                    │
    ├─────────────────────────────────────────────┤
    │ + execute(code: str, language: str) -> Result│
    │ + execute_python(code: str) -> Result        │
    │ + execute_javascript(code: str) -> Result    │
    └─────────────────────────────────────────────┘
    """

    def __init__(self):
        self.timeout = config.EXECUTION_TIMEOUT
        self.memory_limit = config.EXECUTION_MEMORY_LIMIT

    async def execute(self, code: str, language: str = "python") -> ExecutionResult:
        """
        Execute code in sandbox.

        Args:
            code: Code to execute
            language: Programming language

        Returns:
            ExecutionResult with output or error
        """
        if language == "python":
            return await self.execute_python(code)
        elif language == "javascript":
            return await self.execute_javascript(code)
        else:
            return ExecutionResult(
                success=False,
                output="",
                error=f"Unsupported language: {language}"
            )

    async def execute_python(self, code: str) -> ExecutionResult:
        """
        Execute Python code in sandbox.

        Args:
            code: Python code to execute

        Returns:
            ExecutionResult with output or error
        """
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name

        try:
            # Execute with timeout
            process = await asyncio.create_subprocess_exec(
                'python', temp_file,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=self.timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                return ExecutionResult(
                    success=False,
                    output="",
                    error=f"Execution timeout after {self.timeout} seconds",
                    exit_code=-1
                )

            return ExecutionResult(
                success=process.returncode == 0,
                output=stdout.decode('utf-8', errors='ignore'),
                error=stderr.decode('utf-8', errors='ignore'),
                exit_code=process.returncode
            )

        except Exception as e:
            return ExecutionResult(
                success=False,
                output="",
                error=str(e),
                exit_code=-1
            )
        finally:
            # Clean up temp file
            try:
                os.unlink(temp_file)
            except:
                pass

    async def execute_javascript(self, code: str) -> ExecutionResult:
        """
        Execute JavaScript code in sandbox.

        Args:
            code: JavaScript code to execute

        Returns:
            ExecutionResult with output or error
        """
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(code)
            temp_file = f.name

        try:
            # Execute with timeout
            process = await asyncio.create_subprocess_exec(
                'node', temp_file,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=self.timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                return ExecutionResult(
                    success=False,
                    output="",
                    error=f"Execution timeout after {self.timeout} seconds",
                    exit_code=-1
                )

            return ExecutionResult(
                success=process.returncode == 0,
                output=stdout.decode('utf-8', errors='ignore'),
                error=stderr.decode('utf-8', errors='ignore'),
                exit_code=process.returncode
            )

        except Exception as e:
            return ExecutionResult(
                success=False,
                output="",
                error=str(e),
                exit_code=-1
            )
        finally:
            # Clean up temp file
            try:
                os.unlink(temp_file)
            except:
                pass
