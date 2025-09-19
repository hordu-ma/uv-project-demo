"""
Tests for specialized coding agents

Tests the concrete implementations of coding agents that handle
specific types of programming tasks.
"""

import pytest

from src.uv_project_demo.copilot import TaskRequest, TaskResult
from src.uv_project_demo.agents import (
    CodeGenerationAgent,
    UnitTestGenerationAgent,
    CodeAnalysisAgent,
)


class TestCodeGenerationAgent:
    """Test CodeGenerationAgent functionality."""

    def test_initialization(self):
        """Test CodeGenerationAgent initialization."""
        agent = CodeGenerationAgent()

        assert agent.name == "CodeGenerationAgent"
        assert "code_generation" in agent.capabilities
        assert "function_creation" in agent.capabilities
        assert "class_creation" in agent.capabilities

    def test_can_handle_supported_tasks(self):
        """Test can_handle method for supported task types."""
        agent = CodeGenerationAgent()

        supported_tasks = [
            TaskRequest("code_generation", "Generate code", {}),
            TaskRequest("function", "Create function", {}),
            TaskRequest("class", "Create class", {}),
            TaskRequest("snippet", "Create snippet", {}),
        ]

        for task in supported_tasks:
            assert agent.can_handle(task) is True

    def test_can_handle_unsupported_tasks(self):
        """Test can_handle method for unsupported task types."""
        agent = CodeGenerationAgent()

        unsupported_tasks = [
            TaskRequest("test", "Create test", {}),
            TaskRequest("analysis", "Analyze code", {}),
            TaskRequest("review", "Review code", {}),
        ]

        for task in unsupported_tasks:
            assert agent.can_handle(task) is False

    def test_execute_function_generation(self):
        """Test generating a function."""
        agent = CodeGenerationAgent()

        task = TaskRequest(
            task_type="function",
            description="Create a greeting function",
            context={
                "name": "greet_user",
                "parameters": ["name: str", "age: int"],
                "return_type": "str",
            },
        )

        result = agent.execute(task)

        assert result.success is True
        assert "def greet_user(name: str, age: int) -> str:" in result.result
        assert "Create a greeting function" in result.result
        assert result.metadata["lines_generated"] > 0

    def test_execute_class_generation(self):
        """Test generating a class."""
        agent = CodeGenerationAgent()

        task = TaskRequest(
            task_type="class",
            description="Create a user management class",
            context={"name": "UserManager"},
        )

        result = agent.execute(task)

        assert result.success is True
        assert "class UserManager:" in result.result
        assert "Create a user management class" in result.result
        assert "def __init__(self):" in result.result

    def test_execute_snippet_generation(self):
        """Test generating a code snippet."""
        agent = CodeGenerationAgent()

        task = TaskRequest(
            task_type="snippet", description="Create file reading logic", context={}
        )

        result = agent.execute(task)

        assert result.success is True
        assert "Create file reading logic" in result.result
        assert "pass" in result.result

    def test_execute_with_defaults(self):
        """Test execution with minimal context."""
        agent = CodeGenerationAgent()

        task = TaskRequest(
            task_type="function", description="Simple function", context={}
        )

        result = agent.execute(task)

        assert result.success is True
        assert "def generated_function() -> None:" in result.result


class TestUnitTestGenerationAgent:
    """Test UnitTestGenerationAgent functionality."""

    def test_initialization(self):
        """Test UnitTestGenerationAgent initialization."""
        agent = UnitTestGenerationAgent()

        assert agent.name == "UnitTestGenerationAgent"
        assert "test_generation" in agent.capabilities
        assert "unit_tests" in agent.capabilities
        assert "pytest" in agent.capabilities

    def test_can_handle_supported_tasks(self):
        """Test can_handle method for supported task types."""
        agent = UnitTestGenerationAgent()

        supported_tasks = [
            TaskRequest("test", "Create test", {}),
            TaskRequest("unit_test", "Create unit test", {}),
            TaskRequest("test_generation", "Generate tests", {}),
            TaskRequest("pytest", "Create pytest", {}),
        ]

        for task in supported_tasks:
            assert agent.can_handle(task) is True

    def test_can_handle_unsupported_tasks(self):
        """Test can_handle method for unsupported task types."""
        agent = UnitTestGenerationAgent()

        unsupported_tasks = [
            TaskRequest("function", "Create function", {}),
            TaskRequest("analysis", "Analyze code", {}),
            TaskRequest("class", "Create class", {}),
        ]

        for task in unsupported_tasks:
            assert agent.can_handle(task) is False

    def test_execute_test_generation(self):
        """Test generating unit tests."""
        agent = UnitTestGenerationAgent()

        task = TaskRequest(
            task_type="test",
            description="Create tests for user authentication",
            context={"target": "authenticate_user", "test_class": "TestAuthentication"},
        )

        result = agent.execute(task)

        assert result.success is True
        assert "class TestAuthentication:" in result.result
        assert "def test_authenticate_user_basic(self):" in result.result
        assert "def test_authenticate_user_edge_cases(self):" in result.result
        assert "def test_authenticate_user_error_handling(self):" in result.result
        assert "import pytest" in result.result
        assert result.metadata["test_framework"] == "pytest"
        assert result.metadata["test_methods"] == 3

    def test_execute_with_defaults(self):
        """Test execution with minimal context."""
        agent = UnitTestGenerationAgent()

        task = TaskRequest(task_type="test", description="Basic test", context={})

        result = agent.execute(task)

        assert result.success is True
        assert "class TestFunction:" in result.result
        assert "def test_function_to_test_basic(self):" in result.result


class TestCodeAnalysisAgent:
    """Test CodeAnalysisAgent functionality."""

    def test_initialization(self):
        """Test CodeAnalysisAgent initialization."""
        agent = CodeAnalysisAgent()

        assert agent.name == "CodeAnalysisAgent"
        assert "code_analysis" in agent.capabilities
        assert "code_review" in agent.capabilities
        assert "quality_check" in agent.capabilities

    def test_can_handle_supported_tasks(self):
        """Test can_handle method for supported task types."""
        agent = CodeAnalysisAgent()

        supported_tasks = [
            TaskRequest("analysis", "Analyze code", {}),
            TaskRequest("review", "Review code", {}),
            TaskRequest("quality", "Check quality", {}),
            TaskRequest("lint", "Lint code", {}),
        ]

        for task in supported_tasks:
            assert agent.can_handle(task) is True

    def test_can_handle_unsupported_tasks(self):
        """Test can_handle method for unsupported task types."""
        agent = CodeAnalysisAgent()

        unsupported_tasks = [
            TaskRequest("function", "Create function", {}),
            TaskRequest("test", "Create test", {}),
            TaskRequest("class", "Create class", {}),
        ]

        for task in unsupported_tasks:
            assert agent.can_handle(task) is False

    def test_execute_code_analysis(self):
        """Test analyzing code."""
        agent = CodeAnalysisAgent()

        test_code = '''def example_function():
    # TODO: Implement this
    pass

class ExampleClass:
    def method(self):
        return "example"'''

        task = TaskRequest(
            task_type="analysis",
            description="Analyze example code",
            context={"code": test_code},
        )

        result = agent.execute(task)

        assert result.success is True
        assert isinstance(result.result, dict)
        assert "description" in result.result
        assert "summary" in result.result
        assert "issues" in result.result
        assert "suggestions" in result.result
        assert result.result["line_count"] == 7
        assert result.metadata["lines_analyzed"] == 7
        assert result.metadata["issues_found"] >= 0

    def test_execute_analysis_with_issues(self):
        """Test analysis that finds issues."""
        agent = CodeAnalysisAgent()

        test_code = (
            """def long_function():
    # TODO: This needs implementation
    pass
"""
            * 20
        )  # Create a long function

        task = TaskRequest(
            task_type="analysis",
            description="Analyze problematic code",
            context={"code": test_code},
        )

        result = agent.execute(task)

        assert result.success is True
        analysis = result.result

        # Should find TODO issues
        todo_issues = [issue for issue in analysis["issues"] if "TODO" in issue]
        assert len(todo_issues) > 0

        # Should suggest breaking down long functions
        long_func_suggestions = [
            sugg for sugg in analysis["suggestions"] if "breaking down" in sugg
        ]
        assert len(long_func_suggestions) > 0

    def test_execute_empty_code_analysis(self):
        """Test analyzing empty code."""
        agent = CodeAnalysisAgent()

        task = TaskRequest(
            task_type="analysis", description="Analyze empty code", context={"code": ""}
        )

        result = agent.execute(task)

        assert result.success is True
        analysis = result.result
        assert "No code provided for analysis" in analysis["issues"]
        assert result.metadata["lines_analyzed"] == 0

    def test_execute_no_code_provided(self):
        """Test analysis when no code is in context."""
        agent = CodeAnalysisAgent()

        task = TaskRequest(task_type="analysis", description="Analyze code", context={})

        result = agent.execute(task)

        assert result.success is True
        analysis = result.result
        assert "No code provided for analysis" in analysis["issues"]


# Integration tests
class TestAgentsIntegration:
    """Integration tests for all agents working together."""

    def test_agents_compatibility(self):
        """Test that all agents are compatible with the base framework."""
        agents = [CodeGenerationAgent(), UnitTestGenerationAgent(), CodeAnalysisAgent()]

        for agent in agents:
            # Each agent should have a unique name
            assert isinstance(agent.name, str)
            assert len(agent.name) > 0

            # Each agent should have capabilities
            assert isinstance(agent.capabilities, list)
            assert len(agent.capabilities) > 0

            # Each agent should be able to report capabilities
            caps = agent.get_capabilities()
            assert isinstance(caps, list)
            assert caps == agent.capabilities

    def test_task_type_coverage(self):
        """Test that different agents handle different task types."""
        agents = [CodeGenerationAgent(), UnitTestGenerationAgent(), CodeAnalysisAgent()]

        test_tasks = [
            TaskRequest("function", "Create function", {}),
            TaskRequest("test", "Create test", {}),
            TaskRequest("analysis", "Analyze code", {}),
        ]

        # Each task should be handled by exactly one agent type
        for task in test_tasks:
            handlers = [agent for agent in agents if agent.can_handle(task)]
            assert (
                len(handlers) == 1
            ), f"Task {task.task_type} handled by {len(handlers)} agents"

    @pytest.mark.parametrize(
        "agent_class,task_type",
        [
            (CodeGenerationAgent, "function"),
            (UnitTestGenerationAgent, "test"),
            (CodeAnalysisAgent, "analysis"),
        ],
    )
    def test_agent_execution_success(self, agent_class, task_type):
        """Test that each agent can successfully execute its primary task type."""
        agent = agent_class()
        task = TaskRequest(task_type, "Test task", {})

        assert agent.can_handle(task) is True

        result = agent.execute(task)
        assert isinstance(result, TaskResult)
        assert result.success is True
        assert result.result is not None
        assert isinstance(result.message, str)
