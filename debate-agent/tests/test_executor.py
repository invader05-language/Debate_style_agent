"""
Tests for code executor — covers both legacy and new integrated flow.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from execution.executor import CodeExecutor
from execution.sandbox import ExecutionResult, TestResult, FallbackSandbox
from execution.code_generator import GeneratedCode


# ── Legacy ExecutionResult (from sandbox module) ─────────────────

class TestExecutionResult:
    def test_creation(self):
        r = ExecutionResult(
            success=True, output="Hello", error="",
            exit_code=0, execution_time=0.5
        )
        assert r.success is True
        assert r.output == "Hello"
        assert r.exit_code == 0
        assert r.execution_time == 0.5

    def test_to_dict(self):
        r = ExecutionResult(
            success=True, output="Test", error="Err",
            exit_code=0, execution_time=1.0
        )
        d = r.to_dict()
        assert d["success"] is True
        assert d["output"] == "Test"
        assert d["error"] == "Err"
        assert d["execution_time"] == 1.0

    def test_failure(self):
        r = ExecutionResult(success=False, output="", error="crash", exit_code=1)
        assert r.success is False
        assert r.error == "crash"


# ── CodeExecutor basics ──────────────────────────────────────────

class TestCodeExecutorBasic:

    def test_init_with_sandbox_false(self):
        """use_sandbox=False should create FallbackSandbox."""
        executor = CodeExecutor(use_sandbox=False)
        assert isinstance(executor.sandbox, FallbackSandbox)

    def test_init_defaults(self):
        """Default init should have timeout and memory_limit."""
        executor = CodeExecutor(use_sandbox=False)
        assert executor.timeout > 0
        assert executor.memory_limit is not None

    @pytest.mark.asyncio
    async def test_execute_python_success(self):
        """execute() should delegate to sandbox."""
        executor = CodeExecutor(use_sandbox=False)

        expected = ExecutionResult(success=True, output="hello\n", exit_code=0)
        with patch.object(executor.sandbox, 'execute', return_value=expected):
            result = await executor.execute("print('hello')", "python")

        assert result.success is True
        assert "hello" in result.output

    @pytest.mark.asyncio
    async def test_execute_python_error(self):
        """execute() should return error from sandbox."""
        executor = CodeExecutor(use_sandbox=False)

        expected = ExecutionResult(success=False, error="NameError", exit_code=1)
        with patch.object(executor.sandbox, 'execute', return_value=expected):
            result = await executor.execute("bad()", "python")

        assert result.success is False
        assert "NameError" in result.error

    @pytest.mark.asyncio
    async def test_execute_python_alias(self):
        """execute_python() should call execute() with 'python'."""
        executor = CodeExecutor(use_sandbox=False)

        with patch.object(executor, 'execute', return_value=ExecutionResult(True)) as mock_exec:
            await executor.execute_python("x=1")
            mock_exec.assert_called_once_with("x=1", "python")

    @pytest.mark.asyncio
    async def test_execute_javascript_alias(self):
        """execute_javascript() should call execute() with 'javascript'."""
        executor = CodeExecutor(use_sandbox=False)

        with patch.object(executor, 'execute', return_value=ExecutionResult(True)) as mock_exec:
            await executor.execute_javascript("let x=1")
            mock_exec.assert_called_once_with("let x=1", "javascript")


# ── generate_code ────────────────────────────────────────────────

class TestGenerateCode:

    @pytest.fixture
    def mock_agent(self):
        agent = AsyncMock()
        agent.chat = AsyncMock(return_value='{"main_code": "x=1", "test_code": "assert x==1", "dependencies": []}')
        return agent

    @pytest.mark.asyncio
    async def test_generate_code_creates_generator(self, mock_agent):
        """generate_code() should lazy-init CodeGenerator."""
        executor = CodeExecutor(use_sandbox=False, agent=mock_agent)
        result = await executor.generate_code(["Step 1"])
        assert isinstance(result, GeneratedCode)
        assert "x=1" in result.main_code

    @pytest.mark.asyncio
    async def test_generate_code_uses_default_agent(self):
        """generate_code() should create MIMOAgent if no agent provided."""
        executor = CodeExecutor(use_sandbox=False)

        with patch("agents.mimo_agent.MIMOAgent") as MockMIMO:
            mock_agent = AsyncMock()
            mock_agent.chat = AsyncMock(return_value='{"main_code": "y=2", "test_code": "", "dependencies": []}')
            MockMIMO.return_value = mock_agent

            result = await executor.generate_code(["Do something"])
            assert "y=2" in result.main_code


# ── generate_and_execute ─────────────────────────────────────────

class TestGenerateAndExecute:

    @pytest.mark.asyncio
    async def test_success_first_attempt(self):
        """Should return on first successful execution."""
        mock_agent = AsyncMock()
        mock_agent.chat = AsyncMock(return_value='{"main_code": "print(1)", "test_code": "", "dependencies": []}')

        executor = CodeExecutor(use_sandbox=False, agent=mock_agent)

        success_result = ExecutionResult(success=True, output="1\n", exit_code=0)
        with patch.object(executor.sandbox, 'execute', return_value=success_result):
            result = await executor.generate_and_execute(
                action_plan=["Print 1"], language="python", max_retries=3
            )

        assert result.success is True
        assert "1" in result.output

    @pytest.mark.asyncio
    async def test_retry_on_failure_then_success(self):
        """Should retry with AI fix when execution fails."""
        mock_agent = AsyncMock()
        # First generate → broken code, refine → fixed code
        mock_agent.chat = AsyncMock(side_effect=[
            '{"main_code": "print(bad)", "test_code": "", "dependencies": []}',  # generate
            '{"main_code": "print(42)", "test_code": "", "dependencies": []}',   # refine
        ])

        executor = CodeExecutor(use_sandbox=False, agent=mock_agent)

        fail_result = ExecutionResult(success=False, error="NameError", exit_code=1)
        success_result = ExecutionResult(success=True, output="42\n", exit_code=0)

        call_count = 0
        async def mock_execute(code, language="python"):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return fail_result
            return success_result

        with patch.object(executor.sandbox, 'execute', side_effect=mock_execute):
            result = await executor.generate_and_execute(
                action_plan=["Print 42"], max_retries=3
            )

        assert result.success is True
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_all_retries_exhausted(self):
        """Should return last failure after all retries exhausted."""
        mock_agent = AsyncMock()
        mock_agent.chat = AsyncMock(side_effect=[
            '{"main_code": "bad1()", "test_code": "", "dependencies": []}',  # generate
            '{"main_code": "bad2()", "test_code": "", "dependencies": []}',  # refine 1
            '{"main_code": "bad3()", "test_code": "", "dependencies": []}',  # refine 2
        ])

        executor = CodeExecutor(use_sandbox=False, agent=mock_agent)

        fail_result = ExecutionResult(success=False, error="still broken", exit_code=1)
        with patch.object(executor.sandbox, 'execute', return_value=fail_result):
            result = await executor.generate_and_execute(
                action_plan=["Do thing"], max_retries=3
            )

        assert result.success is False
        assert "still broken" in result.error

    @pytest.mark.asyncio
    async def test_empty_code_generation(self):
        """Should fail fast if code generation produces empty output."""
        mock_agent = AsyncMock()
        mock_agent.chat = AsyncMock(return_value='{"main_code": "", "test_code": "", "dependencies": []}')

        executor = CodeExecutor(use_sandbox=False, agent=mock_agent)
        result = await executor.generate_and_execute(action_plan=["Step 1"])

        assert result.success is False
        assert "empty" in result.error.lower()


# ── run_tests ────────────────────────────────────────────────────

class TestRunTests:

    @pytest.mark.asyncio
    async def test_run_tests_delegates_to_sandbox(self):
        """run_tests() should call sandbox.execute_with_tests()."""
        executor = CodeExecutor(use_sandbox=False)

        expected = TestResult(passed=2, failed=0, errors=0, output="2 passed")
        with patch.object(executor.sandbox, 'execute_with_tests', return_value=expected) as mock:
            result = await executor.run_tests("code", "tests", "python")

        mock.assert_called_once_with("code", "tests", "python")
        assert result.passed == 2
