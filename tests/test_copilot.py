"""
Tests for the Copilot delegation framework

Tests the core functionality of delegating tasks to coding agents.
"""

from unittest.mock import Mock

from src.uv_project_demo.copilot import Copilot, CodingAgent, TaskRequest, TaskResult


class MockCodingAgent(CodingAgent):
    """Mock coding agent for testing."""

    def __init__(self, name: str, capabilities: list, can_handle_types: list):
        super().__init__(name, capabilities)
        self.can_handle_types = can_handle_types
        self.execution_count = 0

    def can_handle(self, task: TaskRequest) -> bool:
        return task.task_type in self.can_handle_types

    def execute(self, task: TaskRequest) -> TaskResult:
        self.execution_count += 1
        return TaskResult(
            success=True,
            result=f"Mock result for {task.task_type}",
            message=f"Task executed by {self.name}",
        )


class TestTaskRequest:
    """Test TaskRequest dataclass."""

    def test_task_request_creation(self):
        """Test creating a TaskRequest."""
        task = TaskRequest(
            task_type="test",
            description="Test task",
            context={"key": "value"},
            language="python",
            difficulty="easy",
        )

        assert task.task_type == "test"
        assert task.description == "Test task"
        assert task.context == {"key": "value"}
        assert task.language == "python"
        assert task.difficulty == "easy"

    def test_task_request_defaults(self):
        """Test TaskRequest with default values."""
        task = TaskRequest(task_type="test", description="Test task", context={})

        assert task.language is None
        assert task.difficulty == "medium"


class TestTaskResult:
    """Test TaskResult dataclass."""

    def test_task_result_creation(self):
        """Test creating a TaskResult."""
        result = TaskResult(
            success=True,
            result="test result",
            message="Success",
            metadata={"info": "test"},
        )

        assert result.success is True
        assert result.result == "test result"
        assert result.message == "Success"
        assert result.metadata == {"info": "test"}

    def test_task_result_defaults(self):
        """Test TaskResult with default values."""
        result = TaskResult(success=False, result=None, message="Failed")

        assert result.metadata is None


class TestCodingAgent:
    """Test CodingAgent abstract base class."""

    def test_coding_agent_initialization(self):
        """Test CodingAgent initialization."""
        agent = MockCodingAgent("TestAgent", ["capability1", "capability2"], ["test"])

        assert agent.name == "TestAgent"
        assert agent.capabilities == ["capability1", "capability2"]

    def test_get_capabilities(self):
        """Test getting agent capabilities."""
        capabilities = ["cap1", "cap2", "cap3"]
        agent = MockCodingAgent("TestAgent", capabilities, ["test"])

        returned_caps = agent.get_capabilities()
        assert returned_caps == capabilities

        # Ensure it returns a copy, not the original list
        returned_caps.append("new_cap")
        assert agent.capabilities != returned_caps

    def test_can_handle(self):
        """Test agent can_handle method."""
        agent = MockCodingAgent("TestAgent", ["test"], ["function", "class"])

        task1 = TaskRequest("function", "Create function", {})
        task2 = TaskRequest("snippet", "Create snippet", {})

        assert agent.can_handle(task1) is True
        assert agent.can_handle(task2) is False

    def test_execute(self):
        """Test agent execute method."""
        agent = MockCodingAgent("TestAgent", ["test"], ["function"])

        task = TaskRequest("function", "Create function", {})
        result = agent.execute(task)

        assert result.success is True
        assert result.result == "Mock result for function"
        assert result.message == "Task executed by TestAgent"
        assert agent.execution_count == 1


class TestCopilot:
    """Test Copilot delegation functionality."""

    def test_copilot_initialization(self):
        """Test Copilot initialization."""
        copilot = Copilot()
        assert copilot.agents == {}

    def test_register_agent(self):
        """Test registering agents with Copilot."""
        copilot = Copilot()
        agent = MockCodingAgent("TestAgent", ["test"], ["function"])

        copilot.register_agent(agent)

        assert "TestAgent" in copilot.agents
        assert copilot.agents["TestAgent"] == agent

    def test_delegate_task_success(self):
        """Test successful task delegation."""
        copilot = Copilot()
        agent = MockCodingAgent("TestAgent", ["code_gen"], ["function"])
        copilot.register_agent(agent)

        task = TaskRequest("function", "Create a function", {})
        result = copilot.delegate_task(task)

        assert result.success is True
        assert result.result == "Mock result for function"
        assert result.metadata["handled_by"] == "TestAgent"
        assert agent.execution_count == 1

    def test_delegate_task_no_suitable_agent(self):
        """Test delegation when no suitable agent exists."""
        copilot = Copilot()
        agent = MockCodingAgent("TestAgent", ["test"], ["function"])
        copilot.register_agent(agent)

        task = TaskRequest("unsupported", "Unsupported task", {})
        result = copilot.delegate_task(task)

        assert result.success is False
        assert result.result is None
        assert "No agent found to handle task type: unsupported" in result.message

    def test_delegate_task_multiple_agents(self):
        """Test delegation with multiple suitable agents."""
        copilot = Copilot()

        agent1 = MockCodingAgent("Agent1", ["gen"], ["function"])
        agent2 = MockCodingAgent("Agent2", ["gen"], ["function"])

        copilot.register_agent(agent1)
        copilot.register_agent(agent2)

        task = TaskRequest("function", "Create function", {})
        result = copilot.delegate_task(task)

        assert result.success is True
        # Should use the first suitable agent found
        assert result.metadata["handled_by"] in ["Agent1", "Agent2"]

    def test_delegate_task_agent_exception(self):
        """Test delegation when agent throws exception."""
        copilot = Copilot()

        # Create a mock agent that raises an exception
        agent = Mock(spec=CodingAgent)
        agent.name = "ErrorAgent"
        agent.can_handle.return_value = True
        agent.execute.side_effect = ValueError("Test error")

        copilot.register_agent(agent)

        task = TaskRequest("test", "Test task", {})
        result = copilot.delegate_task(task)

        assert result.success is False
        assert result.result is None
        assert "ErrorAgent failed to execute task: Test error" in result.message
        assert result.metadata["handled_by"] == "ErrorAgent"
        assert result.metadata["error"] == "Test error"

    def test_list_agents(self):
        """Test listing registered agents and their capabilities."""
        copilot = Copilot()

        agent1 = MockCodingAgent("Agent1", ["cap1", "cap2"], ["function"])
        agent2 = MockCodingAgent("Agent2", ["cap3"], ["test"])

        copilot.register_agent(agent1)
        copilot.register_agent(agent2)

        agents_list = copilot.list_agents()

        expected = {"Agent1": ["cap1", "cap2"], "Agent2": ["cap3"]}

        assert agents_list == expected

    def test_empty_agents_list(self):
        """Test listing agents when none are registered."""
        copilot = Copilot()
        agents_list = copilot.list_agents()
        assert agents_list == {}


# Integration tests
class TestCopilotIntegration:
    """Integration tests for the Copilot system."""

    def test_complete_workflow(self):
        """Test a complete workflow from registration to execution."""
        # Setup
        copilot = Copilot()

        code_agent = MockCodingAgent(
            "CodeAgent", ["code_generation"], ["function", "class"]
        )
        test_agent = MockCodingAgent(
            "TestAgent", ["test_generation"], ["test", "unit_test"]
        )

        # Register agents
        copilot.register_agent(code_agent)
        copilot.register_agent(test_agent)

        # Test code generation task
        code_task = TaskRequest("function", "Create a greeting function", {})
        code_result = copilot.delegate_task(code_task)

        assert code_result.success is True
        assert code_result.metadata["handled_by"] == "CodeAgent"

        # Test test generation task
        test_task = TaskRequest("test", "Create unit tests", {})
        test_result = copilot.delegate_task(test_task)

        assert test_result.success is True
        assert test_result.metadata["handled_by"] == "TestAgent"

        # Verify agents were used
        assert code_agent.execution_count == 1
        assert test_agent.execution_count == 1

        # List all agents
        agents = copilot.list_agents()
        assert len(agents) == 2
        assert "CodeAgent" in agents
        assert "TestAgent" in agents
