"""
主要应用逻辑模块

包含应用的核心功能实现。
"""

from typing import Optional
import sys


def greet(name: Optional[str] = None) -> str:
    """
    生成问候消息

    Args:
        name: 可选的用户名

    Returns:
        str: 格式化的问候消息
    """
    if name:
        return f"Hello {name} from uv-project-demo!"
    return "Hello from uv-project-demo!"


def main() -> None:
    """
    应用主入口函数

    处理命令行参数并执行主要逻辑。
    """
    try:
        # 简单的命令行参数处理
        if len(sys.argv) > 1:
            name = sys.argv[1]
            message = greet(name)
        else:
            message = greet()

        print(message)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
