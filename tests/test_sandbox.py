"""
Tests for sandbox execution (DockerSandbox + FallbackSandbox).
"""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from execution.sandbox import (
    DockerSandbox, FallbackSandbox,
    ExecutionResult, TestResult
)


# ── Data classes ─────────────────────────────────────────────────

class TestExecutionResult:
    def test_creation(self):
        r = ExecutionResult(success=True, output="ok", error="", exit_code=0, execution_time=0.5)
        assert r.success is True
        assert r.output == "ok"
        assert r.exit_code == 0

    def test_to_dict(self):
        r = ExecutionResult(success=False, output="", error="fail", exit_code=1, execution_time=1.0)
        d = r.to_dict()
        assert d["success"] is False
        assert d["error"] == "fail"
        assert d["execution_time"] == 1.0


class TestTestResult:
    def test_creation(self):
        t = TestResult(passed=3, failed=1, errors=0, output="3 passed, 1 failed")
        assert t.passed == 3
        assert t.failed == 1

    def test_to_dict(self):
        t = TestResult(passed=5, failed=0, errors=0, output="all good")
        d = t.to_dict()
        assert d["passed"] == 5


# ── DockerSandbox ────────────────────────────────────────────────

class TestDockerSandbox:
    def test_init_defaults(self):
        s = DockerSandbox()
        assert s.timeout == 30
        assert s.memory_limit == "256m"
        assert s.cpu_limit == 0.5

    def test_custom_params(self):
        s = DockerSandbox(timeout=60, memory_limit="512m", cpu_limit=1.0)
        assert s.timeout == 60
        assert s.memory_limit == "512m"
        assert s.cpu_limit == 1.0

    def test_images_defined(self):
        assert "python" in DockerSandbox.IMAGES
        assert "javascript" in DockerSandbox.IMAGES

    @pytest.mark.asyncio
    async def test_unsupported_language(self):
        s = DockerSandbox()
        result = await s.execute("code", language="ruby")
        assert result.success is False
        assert "Unsupported language" in result.error

    @pytest.mark.asyncio
    async def test_execute_success(self):
        """Mock docker run to simulate successful execution."""
        s = DockerSandbox()

        mock_proc = AsyncMock()
        mock_proc.returncode = 0
        mock_proc.communicate = AsyncMock(return_value=(b"hello\n", b""))

        with patch("asyncio.create_subprocess_exec", return_value=mock_proc):
            result = await s.execute("print('hello')", "python")

        assert result.success is True
        assert "hello" in result.output
        assert result.exit_code == 0

    @pytest.mark.asyncio
    async def test_execute_failure(self):
        """Mock docker run to simulate failed execution."""
        s = DockerSandbox()

        mock_proc = AsyncMock()
        mock_proc.returncode = 1
        mock_proc.communicate = AsyncMock(return_value=(b"", b"SyntaxError"))

        with patch("asyncio.create_subprocess_exec", return_value=mock_proc):
            result = await s.execute("bad code", "python")

        assert result.success is False
        assert "SyntaxError" in result.error
        assert result.exit_code == 1

    @pytest.mark.asyncio
    async def test_execute_docker_not_found(self):
        """Should return error when docker binary not found."""
        s = DockerSandbox()

        with patch("asyncio.create_subprocess_exec", side_effect=FileNotFoundError):
            result = await s.execute("print(1)", "python")

        assert result.success is False
        assert "Docker not found" in result.error

    @pytest.mark.asyncio
    async def test_execute_with_tests_success(self):
        """execute_with_tests should parse PASSED/FAILED from output."""
        s = DockerSandbox()

        # First call: main code succeeds
        main_proc = AsyncMock()
        main_proc.returncode = 0
        main_proc.communicate = AsyncMock(return_value=(b"ok", b""))

        # Second call: test output with PASSED
        test_proc = AsyncMock()
        test_proc.returncode = 0
        test_proc.communicate = AsyncMock(return_value=(b"2 PASSED", b""))

        call_count = 0
        original_execute = s.execute

        async def mock_execute(code, language="python"):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return ExecutionResult(success=True, output="ok")
            else:
                return ExecutionResult(success=True, output="2 PASSED")

        with patch.object(s, 'execute', side_effect=mock_execute):
            result = await s.execute_with_tests("code", "test_code", "python")

        assert result.passed >= 1

    @pytest.mark.asyncio
    async def test_execute_with_tests_main_fails(self):
        """execute_with_tests should fail fast if main code fails."""
        s = DockerSandbox()

        async def mock_execute(code, language="python"):
            return ExecutionResult(success=False, error="main code broke")

        with patch.object(s, 'execute', side_effect=mock_execute):
            result = await s.execute_with_tests("bad", "test", "python")

        assert result.failed >= 1


# ── FallbackSandbox ──────────────────────────────────────────────

class TestFallbackSandbox:
    def test_init(self):
        s = FallbackSandbox(timeout=15)
        assert s.timeout == 15

    @pytest.mark.asyncio
    async def test_execute_python_success(self):
        """Should execute Python code via subprocess."""
        s = FallbackSandbox(timeout=10)

        mock_proc = AsyncMock()
        mock_proc.returncode = 0
        mock_proc.communicate = AsyncMock(return_value=(b"hello\n", b""))

        with patch("asyncio.create_subprocess_exec", return_value=mock_proc):
            result = await s.execute("print('hello')", "python")

        assert result.success is True
        assert "hello" in result.output

    @pytest.mark.asyncio
    async def test_execute_js_success(self):
        """Should execute JavaScript code via subprocess."""
        s = FallbackSandbox(timeout=10)

        mock_proc = AsyncMock()
        mock_proc.returncode = 0
        mock_proc.communicate = AsyncMock(return_value=(b"42\n", b""))

        with patch("asyncio.create_subprocess_exec", return_value=mock_proc):
            result = await s.execute("console.log(42)", "javascript")

        assert result.success is True
        assert "42" in result.output

    @pytest.mark.asyncio
    async def test_execute_error(self):
        """Should capture stderr on failure."""
        s = FallbackSandbox(timeout=10)

        mock_proc = AsyncMock()
        mock_proc.returncode = 1
        mock_proc.communicate = AsyncMock(return_value=(b"", b"NameError"))

        with patch("asyncio.create_subprocess_exec", return_value=mock_proc):
            result = await s.execute("bad_code()", "python")

        assert result.success is False
        assert "NameError" in result.error

    @pytest.mark.asyncio
    async def test_execute_unsupported_language(self):
        """Unsupported language should return error (no image match)."""
        # FallbackSandbox doesn't have IMAGES dict like DockerSandbox,
        # it uses python/node directly. Let's verify it handles the command.
        s = FallbackSandbox(timeout=10)
        # This will try to run 'ruby' command which won't exist,
        # but the sandbox doesn't validate language upfront
        mock_proc = AsyncMock()
        mock_proc.returncode = 1
        mock_proc.communicate = AsyncMock(return_value=(b"", b"command not found"))

        with patch("asyncio.create_subprocess_exec", return_value=mock_proc):
            result = await s.execute("puts 'hi'", "ruby")

        assert result.success is False
