"""
Demonstration of the "Delegate to Coding Agent" functionality

This module shows how to use Copilot to delegate tasks to specialized
coding agents for improved efficiency and accuracy.
"""

from .copilot import Copilot, TaskRequest
from .agents import CodeGenerationAgent, UnitTestGenerationAgent, CodeAnalysisAgent


def demonstrate_delegation():
    """
    Demonstrate the complete delegation workflow.

    展示完整的任务委托工作流程。
    """
    print("🤖 Copilot Delegation Demo")
    print("=" * 50)

    # Initialize Copilot and register agents
    copilot = Copilot()

    print("\n📝 Registering coding agents...")
    code_agent = CodeGenerationAgent()
    test_agent = UnitTestGenerationAgent()
    analysis_agent = CodeAnalysisAgent()

    copilot.register_agent(code_agent)
    copilot.register_agent(test_agent)
    copilot.register_agent(analysis_agent)

    print(f"✅ Registered {len(copilot.agents)} agents")

    # List available agents
    print("\n🔍 Available agents and capabilities:")
    agents_info = copilot.list_agents()
    for name, capabilities in agents_info.items():
        print(f"  • {name}: {', '.join(capabilities)}")

    print("\n" + "=" * 50)
    print("🎯 Task Delegation Examples")
    print("=" * 50)

    # Example 1: Code Generation
    print("\n1️⃣ Code Generation Task")
    print("-" * 25)

    code_task = TaskRequest(
        task_type="function",
        description="Create a function to calculate factorial",
        context={
            "name": "calculate_factorial",
            "parameters": ["n: int"],
            "return_type": "int",
        },
        language="python",
        difficulty="medium",
    )

    print(f"Task: {code_task.description}")
    result = copilot.delegate_task(code_task)

    if result.success:
        print(f"✅ Success! Handled by: {result.metadata['handled_by']}")
        print("Generated code:")
        print("-" * 40)
        print(result.result)
        print("-" * 40)
    else:
        print(f"❌ Failed: {result.message}")

    # Example 2: Test Generation
    print("\n2️⃣ Test Generation Task")
    print("-" * 25)

    test_task = TaskRequest(
        task_type="test",
        description="Create unit tests for the factorial function",
        context={"target": "calculate_factorial", "test_class": "TestFactorial"},
        language="python",
    )

    print(f"Task: {test_task.description}")
    result = copilot.delegate_task(test_task)

    if result.success:
        print(f"✅ Success! Handled by: {result.metadata['handled_by']}")
        print(f"Test framework: {result.metadata['test_framework']}")
        print(f"Test methods generated: {result.metadata['test_methods']}")
        print("Generated tests:")
        print("-" * 40)
        print(
            result.result[:300] + "..." if len(result.result) > 300 else result.result
        )
        print("-" * 40)
    else:
        print(f"❌ Failed: {result.message}")

    # Example 3: Code Analysis
    print("\n3️⃣ Code Analysis Task")
    print("-" * 25)

    sample_code = """def factorial(n):
    # TODO: Add input validation
    if n == 0:
        return 1
    return n * factorial(n - 1)

def another_long_function():
    # This function is getting quite long
    pass
    pass
    pass
    pass
    pass"""

    analysis_task = TaskRequest(
        task_type="analysis",
        description="Analyze the factorial implementation for issues",
        context={"code": sample_code},
        language="python",
    )

    print(f"Task: {analysis_task.description}")
    result = copilot.delegate_task(analysis_task)

    if result.success:
        print(f"✅ Success! Handled by: {result.metadata['handled_by']}")
        print(f"Lines analyzed: {result.metadata['lines_analyzed']}")
        print(f"Issues found: {result.metadata['issues_found']}")

        analysis = result.result
        print("\nAnalysis Results:")
        print("-" * 40)

        if analysis["issues"]:
            print("🔴 Issues found:")
            for issue in analysis["issues"]:
                print(f"  • {issue}")

        if analysis["suggestions"]:
            print("\n💡 Suggestions:")
            for suggestion in analysis["suggestions"]:
                print(f"  • {suggestion}")

        print("-" * 40)
    else:
        print(f"❌ Failed: {result.message}")

    # Example 4: Unsupported Task
    print("\n4️⃣ Unsupported Task (Error Handling)")
    print("-" * 40)

    unsupported_task = TaskRequest(
        task_type="database_design",
        description="Design a database schema",
        context={},
        difficulty="hard",
    )

    print(f"Task: {unsupported_task.description}")
    result = copilot.delegate_task(unsupported_task)

    if result.success:
        print(f"✅ Success! Handled by: {result.metadata['handled_by']}")
    else:
        print(f"❌ Expected failure: {result.message}")

    print("\n" + "=" * 50)
    print("🎉 Delegation Demo Complete!")
    print("\nKey Benefits Demonstrated:")
    print("  • 分工明确: Each agent specializes in specific tasks")
    print("  • 提升效率: Tasks routed to the most suitable agent")
    print("  • 可扩展性: Easy to add new agent types")
    print("  • 错误处理: Graceful handling of unsupported tasks")
    print("=" * 50)


def interactive_demo():
    """
    Interactive demonstration allowing user to input tasks.

    交互式演示，允许用户输入任务。
    """
    print("🤖 Interactive Copilot Demo")
    print("=" * 30)

    copilot = Copilot()

    # Register all agents
    copilot.register_agent(CodeGenerationAgent())
    copilot.register_agent(UnitTestGenerationAgent())
    copilot.register_agent(CodeAnalysisAgent())

    print(f"✅ Registered {len(copilot.agents)} agents")
    print("\nAvailable task types:")
    print("  • function, class, snippet (Code Generation)")
    print("  • test, unit_test, pytest (Test Generation)")
    print("  • analysis, review, quality (Code Analysis)")
    print("  • Type 'quit' to exit")

    while True:
        print("\n" + "-" * 30)
        task_type = input("Enter task type: ").strip()

        if task_type.lower() == "quit":
            break

        description = input("Enter task description: ").strip()

        if not task_type or not description:
            print("❌ Please provide both task type and description")
            continue

        task = TaskRequest(task_type=task_type, description=description, context={})

        print(f"\n🔄 Delegating task: {task_type}")
        result = copilot.delegate_task(task)

        if result.success:
            print(f"✅ Success! Handled by: {result.metadata['handled_by']}")
            print(f"Result: {result.message}")

            # Show result preview for non-analysis tasks
            if task_type != "analysis":
                preview = (
                    result.result[:200] + "..."
                    if len(str(result.result)) > 200
                    else str(result.result)
                )
                print(f"Preview: {preview}")
        else:
            print(f"❌ Failed: {result.message}")

    print("\n👋 Thanks for trying the Copilot delegation system!")


if __name__ == "__main__":
    # Run the demonstration
    demonstrate_delegation()

    # Uncomment the line below for interactive demo
    # interactive_demo()
