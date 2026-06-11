"""
Tests for AI code generator.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from execution.code_generator import CodeGenerator, GeneratedCode


class TestGeneratedCode:
    """GeneratedCode dataclass tests."""

    def test_creation(self):
        code = GeneratedCode(
            main_code="print('hello')",
            test_code="assert True",
            dependencies=["requests"],
            language="python"
        )
        assert code.main_code == "print('hello')"
        assert code.test_code == "assert True"
        assert code.dependencies == ["requests"]
        assert code.language == "python"

    def test_defaults(self):
        code = GeneratedCode(main_code="x = 1")
        assert code.test_code == ""
        assert code.dependencies == []
        assert code.language == "python"


class TestCodeGenerator:
    """CodeGenerator tests."""

    @pytest.fixture
    def mock_agent(self):
        agent = AsyncMock()
        return agent

    @pytest.fixture
    def generator(self, mock_agent):
        return CodeGenerator(agent=mock_agent)

    @pytest.mark.asyncio
    async def test_generate_parses_json(self, generator, mock_agent):
        """generate() should parse JSON response from AI."""
        mock_agent.chat.return_value = '''
        {
            "main_code": "print('hello')",
            "test_code": "assert 1 == 1",
            "dependencies": ["requests"]
        }
        '''
        result = await generator.generate(
            action_plan=["Step 1: print hello"],
            language="python"
        )
        assert isinstance(result, GeneratedCode)
        assert "print('hello')" in result.main_code
        assert "assert 1 == 1" in result.test_code
        assert "requests" in result.dependencies

    @pytest.mark.asyncio
    async def test_generate_handles_non_json(self, generator, mock_agent):
        """generate() should fallback when AI returns non-JSON."""
        mock_agent.chat.return_value = "Here is your code:\nprint('hello')"
        result = await generator.generate(
            action_plan=["Step 1"],
            language="python"
        )
        assert isinstance(result, GeneratedCode)
        assert "print('hello')" in result.main_code
        assert result.test_code == ""

    @pytest.mark.asyncio
    async def test_generate_handles_agent_error(self, generator, mock_agent):
        """generate() should return error comment on agent failure."""
        mock_agent.chat.side_effect = Exception("API timeout")
        result = await generator.generate(
            action_plan=["Step 1"],
            language="python"
        )
        assert isinstance(result, GeneratedCode)
        assert "Code generation failed" in result.main_code

    @pytest.mark.asyncio
    async def test_generate_passes_language(self, generator, mock_agent):
        """generate() should include language in the prompt."""
        mock_agent.chat.return_value = '{"main_code": "console.log(1)", "test_code": "", "dependencies": []}'
        await generator.generate(
            action_plan=["Step 1"],
            language="javascript"
        )
        call_args = mock_agent.chat.call_args
        assert "javascript" in call_args.kwargs.get("system_prompt", call_args[1].get("system_prompt", ""))

    @pytest.mark.asyncio
    async def test_generate_includes_action_plan(self, generator, mock_agent):
        """generate() should include action plan in user prompt."""
        mock_agent.chat.return_value = '{"main_code": "x=1", "test_code": "", "dependencies": []}'
        plan = ["Create database", "Add API endpoint", "Write tests"]
        await generator.generate(action_plan=plan)
        call_args = mock_agent.chat.call_args
        user_msg = call_args.kwargs.get("user_message", call_args[1].get("user_message", ""))
        assert "Create database" in user_msg
        assert "Add API endpoint" in user_msg

    @pytest.mark.asyncio
    async def test_refine_parses_json(self, generator, mock_agent):
        """refine() should parse fixed code from AI response."""
        mock_agent.chat.return_value = '''
        {
            "main_code": "print('fixed')",
            "test_code": "assert True",
            "dependencies": []
        }
        '''
        original = GeneratedCode(main_code="print(broken)")
        result = await generator.refine(
            code=original,
            error="NameError: name 'broken' is not defined"
        )
        assert "print('fixed')" in result.main_code
        assert result.language == original.language

    @pytest.mark.asyncio
    async def test_refine_preserves_original_on_failure(self, generator, mock_agent):
        """refine() should return original code if AI fails."""
        mock_agent.chat.side_effect = Exception("API error")
        original = GeneratedCode(main_code="original_code", language="python")
        result = await generator.refine(code=original, error="some error")
        assert result is original
        assert result.main_code == "original_code"

    @pytest.mark.asyncio
    async def test_refine_includes_error_in_prompt(self, generator, mock_agent):
        """refine() should send the error message to AI."""
        mock_agent.chat.return_value = '{"main_code": "fixed", "test_code": "", "dependencies": []}'
        original = GeneratedCode(main_code="broken")
        error_msg = "TypeError: unsupported operand"
        await generator.refine(code=original, error=error_msg)
        call_args = mock_agent.chat.call_args
        user_msg = call_args.kwargs.get("user_message", call_args[1].get("user_message", ""))
        assert error_msg in user_msg

    @pytest.mark.asyncio
    async def test_generate_partial_json(self, generator, mock_agent):
        """generate() should handle partial JSON (missing fields)."""
        mock_agent.chat.return_value = '{"main_code": "x = 1"}'
        result = await generator.generate(action_plan=["Step 1"])
        assert result.main_code == "x = 1"
        assert result.test_code == ""
        assert result.dependencies == []
