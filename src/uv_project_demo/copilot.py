"""
Coding Agent Framework

This module implements the "delegate to coding agent" functionality for Copilot.
It provides a base architecture for specialized coding agents that can handle
different types of programming tasks.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class TaskRequest:
    """Represents a coding task request."""

    task_type: str
    description: str
    context: Dict[str, Any]
    language: Optional[str] = None
    difficulty: Optional[str] = "medium"


@dataclass
class TaskResult:
    """Represents the result of a coding task."""

    success: bool
    result: Any
    message: str
    metadata: Optional[Dict[str, Any]] = None


class CodingAgent(ABC):
    """
    Abstract base class for coding agents.

    每个编码代理专注于特定类型的编程任务，提升效率和准确性。
    """

    def __init__(self, name: str, capabilities: List[str]):
        self.name = name
        self.capabilities = capabilities

    @abstractmethod
    def can_handle(self, task: TaskRequest) -> bool:
        """Check if this agent can handle the given task."""
        pass

    @abstractmethod
    def execute(self, task: TaskRequest) -> TaskResult:
        """Execute the coding task."""
        pass

    def get_capabilities(self) -> List[str]:
        """Get the list of capabilities this agent supports."""
        return self.capabilities.copy()


class Copilot:
    """
    Main Copilot class that delegates tasks to appropriate coding agents.

    主 Copilot 负责理解用户意图和上下文，将具体任务委托给专门的编码代理。
    """

    def __init__(self):
        self.agents: Dict[str, CodingAgent] = {}

    def register_agent(self, agent: CodingAgent) -> None:
        """Register a coding agent with the Copilot."""
        self.agents[agent.name] = agent

    def delegate_task(self, task: TaskRequest) -> TaskResult:
        """
        Delegate a task to the most appropriate coding agent.

        将某些编程任务委托给专门的"编码代理"来完成。
        """
        # Find suitable agents
        suitable_agents = [
            agent for agent in self.agents.values() if agent.can_handle(task)
        ]

        if not suitable_agents:
            return TaskResult(
                success=False,
                result=None,
                message=f"No agent found to handle task type: {task.task_type}",
            )

        # Select the first suitable agent (in a real implementation,
        # this could be more sophisticated selection logic)
        selected_agent = suitable_agents[0]

        try:
            result = selected_agent.execute(task)
            result.metadata = result.metadata or {}
            result.metadata["handled_by"] = selected_agent.name
            return result
        except Exception as e:
            return TaskResult(
                success=False,
                result=None,
                message=f"Agent {selected_agent.name} failed to execute task: {str(e)}",
                metadata={"handled_by": selected_agent.name, "error": str(e)},
            )

    def list_agents(self) -> Dict[str, List[str]]:
        """List all registered agents and their capabilities."""
        return {name: agent.get_capabilities() for name, agent in self.agents.items()}
