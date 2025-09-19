"""
uv-project-demo: A Python project managed by uv.

This package provides the core functionality for the uv-project-demo
application, including the "delegate to coding agent" framework.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# 导出主要功能
from .main import main

# 导出 Copilot 代理功能
from .copilot import Copilot, CodingAgent, TaskRequest, TaskResult
from .agents import CodeGenerationAgent, UnitTestGenerationAgent, CodeAnalysisAgent

__all__ = [
    "main",
    "Copilot",
    "CodingAgent",
    "TaskRequest",
    "TaskResult",
    "CodeGenerationAgent",
    "UnitTestGenerationAgent",
    "CodeAnalysisAgent",
]
