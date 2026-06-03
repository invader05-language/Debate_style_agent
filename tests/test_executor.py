"""
Tests for code executor.
"""

import pytest
from execution.executor import CodeExecutor, ExecutionResult


class TestExecutionResult:
    """Test execution result."""

    def test_execution_result_creation(self):
        """Test execution result creation."""
        result = ExecutionResult(
            success=True,
            output="Hello, World!",
            error="",
            exit_code=0,
            execution_time=0.5
        )
        assert result.success is True
        assert result.output == "Hello, World!"
        assert result.error == ""
        assert result.exit_code == 0
        assert result.execution_time == 0.5

    def test_execution_result_to_dict(self):
        """Test execution result to dict conversion."""
        result = ExecutionResult(
            success=True,
            output="Test output",
            error="Test error",
            exit_code=0,
            execution_time=1.0
        )
        result_dict = result.to_dict()
        assert result_dict["success"] is True
        assert result_dict["output"] == "Test output"
        assert result_dict["error"] == "Test error"
        assert result_dict["exit_code"] == 0
        assert result_dict["execution_time"] == 1.0


class TestCodeExecutor:
    """Test code executor."""

    def test_executor_initialization(self):
        """Test executor initialization."""
        executor = CodeExecutor()
        assert executor.timeout > 0
        assert executor.memory_limit is not None

    @pytest.mark.asyncio
    async def test_execute_python_hello_world(self):
        """Test executing simple Python code."""
        executor = CodeExecutor()
        code = 'print("Hello, World!")'
        result = await executor.execute_python(code)
        assert result.success is True
        assert "Hello, World!" in result.output
        assert result.exit_code == 0

    @pytest.mark.asyncio
    async def test_execute_python_error(self):
        """Test executing Python code with error."""
        executor = CodeExecutor()
        code = 'print(undefined_variable)'
        result = await executor.execute_python(code)
        assert result.success is False
        assert result.exit_code != 0
        assert len(result.error) > 0

    @pytest.mark.asyncio
    async def test_execute_unsupported_language(self):
        """Test executing code with unsupported language."""
        executor = CodeExecutor()
        code = 'console.log("Hello")'
        result = await executor.execute(code, language="ruby")
        assert result.success is False
        assert "Unsupported language" in result.error
