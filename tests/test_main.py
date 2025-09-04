"""
主模块测试用例

测试 src.uv_project_demo.main 模块的核心功能。
使用 pytest 框架进行单元测试。
"""

import pytest
from unittest.mock import patch
from io import StringIO

from src.uv_project_demo.main import greet, main


class TestGreetFunction:
    """测试 greet 函数的各种场景"""

    def test_greet_without_name(self):
        """测试无参数调用"""
        result = greet()
        assert result == "Hello from uv-project-demo!"
        assert isinstance(result, str)

    def test_greet_with_name(self):
        """测试带参数调用"""
        result = greet("Alice")
        assert result == "Hello Alice from uv-project-demo!"
        assert isinstance(result, str)

    def test_greet_with_empty_string(self):
        """测试空字符串参数"""
        result = greet("")
        assert result == "Hello from uv-project-demo!"

    def test_greet_with_none(self):
        """测试 None 参数"""
        result = greet(None)
        assert result == "Hello from uv-project-demo!"

    def test_greet_with_special_characters(self):
        """测试特殊字符参数"""
        result = greet("张三")
        assert result == "Hello 张三 from uv-project-demo!"

    @pytest.mark.parametrize(
        "name,expected",
        [
            ("Bob", "Hello Bob from uv-project-demo!"),
            ("123", "Hello 123 from uv-project-demo!"),
            ("test-user", "Hello test-user from uv-project-demo!"),
        ],
    )
    def test_greet_parametrized(self, name, expected):
        """参数化测试多种输入"""
        result = greet(name)
        assert result == expected


class TestMainFunction:
    """测试 main 函数的各种场景"""

    @patch("sys.stdout", new_callable=StringIO)
    @patch("sys.argv", ["script_name"])
    def test_main_without_args(self, mock_stdout):
        """测试无命令行参数时的执行"""
        main()
        output = mock_stdout.getvalue().strip()
        assert output == "Hello from uv-project-demo!"

    @patch("sys.stdout", new_callable=StringIO)
    @patch("sys.argv", ["script_name", "TestUser"])
    def test_main_with_args(self, mock_stdout):
        """测试带命令行参数时的执行"""
        main()
        output = mock_stdout.getvalue().strip()
        assert output == "Hello TestUser from uv-project-demo!"

    @patch("sys.stdout", new_callable=StringIO)
    @patch("sys.argv", ["script_name", "User1", "User2"])
    def test_main_with_multiple_args(self, mock_stdout):
        """测试多个命令行参数时只使用第一个"""
        main()
        output = mock_stdout.getvalue().strip()
        assert output == "Hello User1 from uv-project-demo!"

    @patch("sys.stderr", new_callable=StringIO)
    @patch("sys.stdout", new_callable=StringIO)
    @patch("src.uv_project_demo.main.greet")
    def test_main_exception_handling(self, mock_greet, mock_stdout, mock_stderr):
        """测试异常处理"""
        mock_greet.side_effect = Exception("Test error")

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        error_output = mock_stderr.getvalue().strip()
        assert "Error: Test error" in error_output


class TestIntegration:
    """集成测试"""

    def test_module_imports(self):
        """测试模块导入是否正常"""
        from src.uv_project_demo.main import greet, main

        assert callable(greet)
        assert callable(main)

    def test_function_types(self):
        """测试函数类型注解"""
        import inspect
        from src.uv_project_demo.main import greet, main

        # 检查 greet 函数签名
        greet_sig = inspect.signature(greet)
        assert "name" in greet_sig.parameters
        assert greet_sig.return_annotation == str

        # 检查 main 函数签名
        main_sig = inspect.signature(main)
        assert main_sig.return_annotation is None or main_sig.return_annotation is type(
            None
        )


# 如果直接运行此文件，执行测试
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
