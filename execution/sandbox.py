"""
Docker 沙箱执行器 for Multi-AI Debate Agent.
在隔离的 Docker 容器中安全执行代码.
"""

import asyncio
import logging
import tempfile
import os
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class ExecutionResult:
    """执行结果."""
    success: bool
    output: str = ""
    error: str = ""
    exit_code: int = 0
    execution_time: float = 0.0

    def to_dict(self):
        return {
            "success": self.success,
            "output": self.output,
            "error": self.error,
            "exit_code": self.exit_code,
            "execution_time": self.execution_time
        }


@dataclass
class TestResult:
    """测试结果."""
    passed: int = 0
    failed: int = 0
    errors: int = 0
    output: str = ""

    def to_dict(self):
        return {
            "passed": self.passed,
            "failed": self.failed,
            "errors": self.errors,
            "output": self.output
        }


class DockerSandbox:
    """Docker 容器沙箱执行器."""

    IMAGES = {
        "python": "python:3.11-slim",
        "javascript": "node:20-slim",
    }

    def __init__(self, timeout: int = 30, memory_limit: str = "256m",
                 cpu_limit: float = 0.5):
        self.timeout = timeout
        self.memory_limit = memory_limit
        self.cpu_limit = cpu_limit

    async def execute(self, code: str, language: str = "python") -> ExecutionResult:
        """在 Docker 容器中执行代码."""
        import time
        start_time = time.time()

        image = self.IMAGES.get(language)
        if not image:
            return ExecutionResult(
                success=False,
                error=f"Unsupported language: {language}",
                exit_code=1
            )

        # Write code to temp file
        ext = "py" if language == "python" else "js"
        with tempfile.NamedTemporaryFile(mode='w', suffix=f'.{ext}', delete=False) as f:
            f.write(code)
            code_file = f.name

        try:
            # Build docker run command
            cmd = [
                "docker", "run", "--rm",
                "--network", "none",
                "--memory", self.memory_limit,
                "--cpus", str(self.cpu_limit),
                "--read-only",
                "--tmpfs", "/tmp:rw,noexec,nosuid,size=64m",
                "-v", f"{code_file}:/app/code.{ext}:ro",
                image,
                "timeout", str(self.timeout),
                language if language == "python" else "node",
                f"/app/code.{ext}"
            ]

            # Execute
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    proc.communicate(),
                    timeout=self.timeout + 5
                )
            except asyncio.TimeoutError:
                proc.kill()
                return ExecutionResult(
                    success=False,
                    error=f"Execution timed out after {self.timeout}s",
                    exit_code=-1,
                    execution_time=time.time() - start_time
                )

            execution_time = time.time() - start_time
            success = proc.returncode == 0

            return ExecutionResult(
                success=success,
                output=stdout.decode('utf-8', errors='replace'),
                error=stderr.decode('utf-8', errors='replace'),
                exit_code=proc.returncode,
                execution_time=execution_time
            )

        except FileNotFoundError:
            return ExecutionResult(
                success=False,
                error="Docker not found. Please install Docker.",
                exit_code=-1,
                execution_time=time.time() - start_time
            )
        except Exception as e:
            return ExecutionResult(
                success=False,
                error=str(e),
                exit_code=-1,
                execution_time=time.time() - start_time
            )
        finally:
            os.unlink(code_file)

    async def execute_with_tests(self, code: str, test_code: str,
                                  language: str = "python") -> TestResult:
        """执行代码并运行测试."""
        # First execute main code
        result = await self.execute(code, language)
        if not result.success:
            return TestResult(
                failed=1,
                output=f"Main code execution failed:\n{result.error}"
            )

        # Then execute tests
        test_result = await self.execute(test_code, language)

        # Parse test output
        passed = 0
        failed = 0
        errors = 0

        if "PASSED" in test_result.output:
            passed = test_result.output.count("PASSED")
        if "FAILED" in test_result.output:
            failed = test_result.output.count("FAILED")
        if "ERROR" in test_result.output:
            errors = test_result.output.count("ERROR")

        if test_result.success and passed == 0:
            passed = 1

        return TestResult(
            passed=passed,
            failed=failed,
            errors=errors,
            output=test_result.output
        )


class FallbackSandbox:
    """本地执行器 (无 Docker 时的降级方案)."""

    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    async def execute(self, code: str, language: str = "python") -> ExecutionResult:
        """在本地执行代码 (无隔离，仅用于开发环境)."""
        import time
        start_time = time.time()

        ext = "py" if language == "python" else "js"
        cmd = ["python" if language == "python" else "node"]

        with tempfile.NamedTemporaryFile(mode='w', suffix=f'.{ext}', delete=False) as f:
            f.write(code)
            code_file = f.name

        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd, code_file,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    proc.communicate(),
                    timeout=self.timeout
                )
            except asyncio.TimeoutError:
                proc.kill()
                return ExecutionResult(
                    success=False,
                    error=f"Execution timed out after {self.timeout}s",
                    exit_code=-1,
                    execution_time=time.time() - start_time
                )

            return ExecutionResult(
                success=proc.returncode == 0,
                output=stdout.decode('utf-8', errors='replace'),
                error=stderr.decode('utf-8', errors='replace'),
                exit_code=proc.returncode,
                execution_time=time.time() - start_time
            )

        except Exception as e:
            return ExecutionResult(
                success=False,
                error=str(e),
                exit_code=-1,
                execution_time=time.time() - start_time
            )
        finally:
            os.unlink(code_file)
