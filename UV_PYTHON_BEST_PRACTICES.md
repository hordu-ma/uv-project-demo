# uv Python 项目最佳实践指南

> 基于 Unix 哲学和 Python 之禅的现代 Python 项目管理工作流

## 📋 目录

- [第一部分：新建项目的最佳实践](#第一部分新建项目的最佳实践)
- [第二部分：项目维护标准规程](#第二部分项目维护标准规程)
- [附录：常用命令速查](#附录常用命令速查)

---

## 第一部分：新建项目的最佳实践

### 🚀 1. 项目初始化

#### 1.1 创建项目目录和初始化
```bash
# 在项目根目录下创建新项目
cd ~/my-devs/python
uv init my-project-name
cd my-project-name

# 设置 Python 版本（推荐 3.12+）
uv python pin 3.12
```

#### 1.2 配置基础依赖
```bash
# 添加开发工具依赖
uv add black flake8 pytest pytest-cov --dev

# 如果需要类型检查
uv add mypy --dev

# 根据项目需要添加运行时依赖
uv add requests fastapi pandas  # 示例
```

### 🏗️ 2. 项目结构搭建

#### 2.1 创建标准 src 布局
```bash
# 创建目录结构
mkdir -p src/$(echo ${PWD##*/} | tr '-' '_')
mkdir -p tests
mkdir -p docs

# 创建包初始化文件
touch src/$(echo ${PWD##*/} | tr '-' '_')/__init__.py
touch tests/__init__.py
```

#### 2.2 标准项目结构
```
my-project-name/
├── src/
│   └── my_project_name/          # 包名（连字符转下划线）
│       ├── __init__.py
│       ├── main.py               # 主要逻辑
│       ├── config.py             # 配置管理
│       ├── utils.py              # 工具函数
│       ├── models/               # 数据模型
│       │   └── __init__.py
│       └── services/             # 业务逻辑
│           └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   ├── test_utils.py
│   └── fixtures/                 # 测试数据
├── docs/                         # 文档
├── main.py                       # 项目入口点
├── pyproject.toml               # 项目配置
├── README.md
├── .gitignore
└── uv.lock
```

### ⚙️ 3. 配置文件优化

#### 3.1 优化 `pyproject.toml`
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-project-name"
version = "0.1.0"
description = "项目简要描述"
readme = "README.md"
requires-python = ">=3.12"
authors = [{ name = "Your Name", email = "your.email@example.com" }]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.12",
]
dependencies = [
    # 运行时依赖
]

[project.urls]
Homepage = "https://github.com/yourusername/my-project-name"
Repository = "https://github.com/yourusername/my-project-name"

[project.scripts]
my-project-name = "my_project_name.main:main"

[tool.hatch.build.targets.wheel]
packages = ["src/my_project_name"]

# pytest 配置
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "-v",
    "--strict-markers",
    "--strict-config",
    "--cov=src/my_project_name",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-fail-under=80",
]

# Black 格式化配置
[tool.black]
line-length = 88
target-version = ["py312"]
include = '\.pyi?$'
extend-exclude = '''
/(
  \.eggs
  | \.git
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''

# Flake8 配置（需要单独的 .flake8 文件）
[tool.flake8]
max-line-length = 88
extend-ignore = ["E203", "W503"]
exclude = [".git", "__pycache__", "build", "dist", ".venv"]
```

#### 3.2 创建 `.flake8` 配置文件
```ini
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = .git,__pycache__,build,dist,.venv
```

### 📝 4. 核心文件模板

#### 4.1 入口文件 `main.py`
```python
#!/usr/bin/env python3
"""
项目入口点

保持根目录简洁，便于项目的部署和执行。
"""

from src.my_project_name.main import main

if __name__ == "__main__":
    main()
```

#### 4.2 主逻辑 `src/my_project_name/main.py`
```python
"""
主要应用逻辑模块

包含应用的核心功能实现。
"""

from typing import Optional
import sys


def main() -> None:
    """
    应用主入口函数

    遵循单一职责原则，长度不超过 60 行。
    """
    try:
        print("Hello from my-project-name!")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
```

#### 4.3 包初始化 `src/my_project_name/__init__.py`
```python
"""
my-project-name: Python 项目模板

遵循 Unix 哲学和 Python 之禅的最佳实践。
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# 导出主要功能
from .main import main

__all__ = ["main"]
```

### 🧪 5. 测试框架搭建

#### 5.1 基础测试模板 `tests/test_main.py`
```python
"""
主模块测试用例

遵循 pytest 最佳实践，覆盖正常和边界情况。
"""

import pytest
from src.my_project_name.main import main


class TestMainFunction:
    """测试 main 函数的各种场景"""

    def test_main_execution(self):
        """测试主函数执行"""
        # 这里应该包含具体的测试逻辑
        assert callable(main)

    def test_integration(self):
        """集成测试"""
        # 测试模块导入
        from src.my_project_name.main import main
        assert callable(main)


# 参数化测试示例
@pytest.mark.parametrize("input_value,expected", [
    ("test1", "expected1"),
    ("test2", "expected2"),
])
def test_parametrized_example(input_value, expected):
    """参数化测试示例"""
    # 具体的测试逻辑
    pass
```

### 📄 6. 文档和版本控制

#### 6.1 优化 `README.md`
```markdown
# Project Name

项目简要描述

## 安装

```bash
# 克隆项目
git clone <repository-url>
cd my-project-name

# 使用 uv 安装依赖
uv sync
```

## 使用方法

```bash
# 运行项目
python main.py

# 或者使用 uv
uv run python main.py
```

## 开发

```bash
# 运行测试
uv run pytest

# 代码格式化
uv run black src/ tests/

# 代码检查
uv run flake8 src/ tests/
```
```

#### 6.2 `.gitignore` 配置
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.venv/
.env

# Testing
.coverage
htmlcov/
.pytest_cache/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# macOS
.DS_Store
```

---

## 第二部分：项目维护标准规程

### 🔄 1. 进入项目工作流

#### 1.1 环境激活和依赖同步
```bash
# 进入项目目录
cd ~/my-devs/python/my-project-name

# 同步依赖（确保环境一致）
uv sync

# 验证环境
uv run python --version
uv run python -c "import sys; print(sys.executable)"
```

#### 1.2 项目健康检查
```bash
# 运行测试确保代码正常
uv run pytest -x  # 遇到第一个失败就停止

# 检查代码覆盖率
uv run pytest --cov-report=term

# 快速语法检查
uv run flake8 src/ tests/ --count
```

### 🛠️ 2. 日常开发工作流

#### 2.1 代码开发循环
```bash
# 1. 创建功能分支（如果使用 Git）
git checkout -b feature/new-feature

# 2. 开发代码
# 编辑 src/my_project_name/ 下的文件

# 3. 运行测试（TDD 方式）
uv run pytest tests/test_specific.py -v

# 4. 代码格式化
uv run black src/ tests/

# 5. 代码检查
uv run flake8 src/ tests/

# 6. 运行完整测试套件
uv run pytest
```

#### 2.2 依赖管理
```bash
# 添加新的运行时依赖
uv add package-name

# 添加开发依赖
uv add package-name --dev

# 更新依赖
uv sync --upgrade

# 移除依赖
uv remove package-name

# 查看依赖树
uv tree
```

### 🧪 3. 测试和质量保证

#### 3.1 测试策略
```bash
# 运行所有测试
uv run pytest

# 运行特定测试文件
uv run pytest tests/test_main.py

# 运行特定测试类
uv run pytest tests/test_main.py::TestMainFunction

# 运行特定测试方法
uv run pytest tests/test_main.py::TestMainFunction::test_specific

# 显示测试覆盖率
uv run pytest --cov=src --cov-report=html

# 只运行失败的测试
uv run pytest --lf
```

#### 3.2 代码质量检查
```bash
# 格式化代码
uv run black src/ tests/ main.py

# 检查代码风格
uv run flake8 src/ tests/ main.py

# 类型检查（如果配置了 mypy）
uv run mypy src/

# 一键质量检查脚本
cat > check.sh << 'EOF'
#!/bin/bash
echo "🔍 Running code quality checks..."
echo "1. Black formatting..."
uv run black --check src/ tests/ main.py
echo "2. Flake8 linting..."
uv run flake8 src/ tests/ main.py
echo "3. Running tests..."
uv run pytest --cov=src --cov-fail-under=80
echo "✅ All checks passed!"
EOF
chmod +x check.sh
```

### 📦 4. 项目构建和部署

#### 4.1 构建项目
```bash
# 构建 wheel 包
uv build

# 验证构建结果
ls -la dist/

# 测试安装
uv pip install dist/*.whl
```

#### 4.2 环境管理
```bash
# 导出依赖列表
uv export --format requirements-txt --output-file requirements.txt

# 创建生产环境锁文件
uv export --format requirements-txt --no-dev --output-file requirements-prod.txt

# 清理环境
uv clean
```

### 🔧 5. 故障排除和维护

#### 5.1 常见问题解决
```bash
# 依赖冲突解决
uv sync --refresh

# 重建虚拟环境
rm -rf .venv
uv sync

# 查看环境信息
uv info

# 检查过期依赖
uv tree --outdated
```

#### 5.2 性能和内存监控
```bash
# 使用 memory_profiler 监控内存使用
uv add memory-profiler line-profiler --dev

# 在代码中添加性能监控装饰器
@profile
def expensive_function():
    # 函数实现
    pass

# 运行内存分析
uv run python -m memory_profiler main.py
```

### 📊 6. 项目维护检查清单

#### 6.1 每日检查清单
- [ ] `uv sync` 同步依赖
- [ ] `uv run pytest -x` 快速测试
- [ ] `uv run black src/ tests/` 代码格式化
- [ ] `uv run flake8 src/ tests/` 代码检查

#### 6.2 每周维护清单
- [ ] `uv sync --upgrade` 更新依赖
- [ ] `uv run pytest --cov=src` 完整测试和覆盖率
- [ ] 审查和更新 TODO 注释
- [ ] 检查安全漏洞（如果有安全扫描工具）

#### 6.3 发版前检查清单
- [ ] 所有测试通过且覆盖率 ≥ 80%
- [ ] 代码风格检查通过
- [ ] 更新版本号（`pyproject.toml`）
- [ ] 更新 CHANGELOG.md
- [ ] 构建测试 `uv build`
- [ ] Git 标签和发布

---

## 附录：常用命令速查

### 🎯 uv 核心命令
```bash
# 项目管理
uv init project-name          # 创建新项目
uv sync                       # 同步依赖
uv sync --upgrade             # 更新依赖
uv clean                      # 清理缓存

# 依赖管理
uv add package                # 添加依赖
uv add package --dev          # 添加开发依赖
uv remove package             # 移除依赖
uv tree                       # 查看依赖树

# 运行命令
uv run python script.py       # 运行 Python 脚本
uv run pytest                # 运行测试
uv run black .                # 格式化代码

# 环境管理
uv python pin 3.12           # 锁定 Python 版本
uv info                       # 查看环境信息
uv export                     # 导出依赖
```

### 🧪 测试命令
```bash
# 基础测试
uv run pytest                      # 运行所有测试
uv run pytest -v                   # 详细输出
uv run pytest -x                   # 失败时停止
uv run pytest --lf                 # 只运行上次失败的测试

# 覆盖率测试
uv run pytest --cov=src            # 显示覆盖率
uv run pytest --cov-report=html    # 生成 HTML 报告
uv run pytest --cov-fail-under=80  # 覆盖率阈值

# 特定测试
uv run pytest tests/test_main.py                    # 运行特定文件
uv run pytest tests/test_main.py::TestClass         # 运行特定类
uv run pytest tests/test_main.py::test_function     # 运行特定函数
```

### 🎨 代码质量命令
```bash
# Black 格式化
uv run black .                    # 格式化所有文件
uv run black --check .            # 检查格式（不修改）
uv run black --diff .             # 显示需要的更改

# Flake8 检查
uv run flake8 src/ tests/         # 检查指定目录
uv run flake8 --count             # 显示错误数量
uv run flake8 --statistics        # 显示错误统计
```

### 🚀 开发工作流一键脚本

创建 `dev.sh` 快速开发脚本：
```bash
#!/bin/bash
# 开发环境一键设置脚本

set -e

echo "🔧 Setting up development environment..."

# 同步依赖
echo "📦 Syncing dependencies..."
uv sync

# 运行测试
echo "🧪 Running tests..."
uv run pytest -x

# 代码格式化
echo "🎨 Formatting code..."
uv run black src/ tests/ main.py

# 代码检查
echo "🔍 Linting code..."
uv run flake8 src/ tests/ main.py

echo "✅ Development environment ready!"
echo "💡 You can now start coding in src/$(basename $(pwd) | tr '-' '_')/"
```

---

## 🎯 最佳实践总结

### 核心原则
1. **遵循 Unix 哲学**：专一、简洁、组合
2. **遵循 Python 之禅**：简洁胜于复杂，可读性很重要
3. **显式胜于隐式**：明确的错误处理和类型注解
4. **测试驱动**：确保 80%+ 代码覆盖率
5. **自动化**：使用脚本自动化重复性任务

### 项目结构原则
- 使用 `src` 布局避免导入冲突
- 保持根目录简洁
- 明确分离源码、测试、文档
- 遵循 Python 包命名规范（下划线）

### 开发工作流原则
- 每次开发前先 `uv sync`
- 频繁运行测试（TDD）
- 及时格式化和检查代码
- 定期更新依赖
- 使用语义化版本控制

通过遵循这些最佳实践，你将能够构建高质量、可维护的 Python 项目，形成高效的开发工作流。
