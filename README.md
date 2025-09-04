# uv-project-demo

> 基于 uv 的 Python 项目最佳实践示例

这个项目展示了如何使用 `uv` 构建和管理现代 Python 项目，遵循 Unix 哲学和 Python 之禅的最佳实践。

## 🚀 特性

- ✅ **标准 src 布局**：避免导入冲突，符合 Python 打包标准
- ✅ **完整测试套件**：使用 pytest，包含覆盖率检测（96%+）
- ✅ **自动化工具链**：Black 格式化 + Flake8 检查
- ✅ **类型注解支持**：完整的类型提示和检查
- ✅ **一键开发脚本**：自动化所有开发工作流
- ✅ **详细文档**：包含最佳实践指南

## 📦 快速开始

### 安装依赖

```bash
# 克隆项目
git clone <repository-url>
cd uv-project-demo

# 使用 uv 同步依赖
uv sync
```

### 运行项目

```bash
# 直接运行
python main.py

# 或使用 uv
uv run python main.py

# 带参数运行
python main.py "你的名字"
```

## 🛠️ 开发

### 使用一键开发脚本

```bash
# 设置开发环境
./dev.sh setup

# 完整质量检查（推荐）
./dev.sh check

# 运行测试
./dev.sh test

# 查看项目信息
./dev.sh info

# 查看所有选项
./dev.sh help
```

### 手动开发命令

```bash
# 运行测试
uv run pytest

# 测试覆盖率
uv run pytest --cov=src

# 代码格式化
uv run black src/ tests/

# 代码检查
uv run flake8 src/ tests/
```

## 📁 项目结构

```
uv-project-demo/
├── src/uv_project_demo/          # 主要源代码
│   ├── __init__.py               # 包初始化
│   └── main.py                   # 核心逻辑
├── tests/                        # 测试代码
│   ├── __init__.py
│   └── test_main.py              # 测试用例
├── main.py                       # 项目入口点
├── dev.sh                        # 开发工具脚本
├── pyproject.toml                # 项目配置
├── .flake8                       # Flake8 配置
└── uv.lock                       # 依赖锁定文件
```

## 📚 最佳实践文档

本项目包含完整的最佳实践指南：

- **[UV_PYTHON_BEST_PRACTICES.md](./UV_PYTHON_BEST_PRACTICES.md)** - 完整的 uv Python 项目最佳实践指南
- **[QUICK_REFERENCE.md](./QUICK_REFERENCE.md)** - 快速参考卡片

这些文档涵盖：

- 新建项目的标准流程
- 日常开发工作流
- 测试和质量保证
- 依赖管理
- 故障排除

## 🎯 质量标准

本项目遵循严格的质量标准：

- ✅ 测试覆盖率 ≥ 80%（当前：96%）
- ✅ 所有测试必须通过
- ✅ Black 代码格式化
- ✅ Flake8 代码检查无错误
- ✅ 函数长度 < 60 行
- ✅ 完整的类型注解
- ✅ 显式异常处理

## 🔧 开发工具

### 核心依赖

- **uv** - 现代 Python 包管理器
- **black** - 代码格式化工具
- **flake8** - 代码风格检查
- **pytest** - 测试框架
- **pytest-cov** - 覆盖率测试

### 配置文件

- `pyproject.toml` - 项目元数据和工具配置
- `.flake8` - Flake8 特定配置
- `uv.lock` - 依赖版本锁定

## 📋 开发检查清单

### 每日开发

- [ ] `uv sync` 同步依赖
- [ ] `./dev.sh check` 质量检查
- [ ] 编写测试用例
- [ ] 保持函数简洁（< 60 行）

### 提交前

- [ ] 所有测试通过
- [ ] 代码覆盖率 ≥ 80%
- [ ] 代码格式化完成
- [ ] 无 Flake8 错误

### 发版前

- [ ] 更新版本号
- [ ] 更新文档
- [ ] `uv build` 构建成功
- [ ] Git 标签创建

## 🌟 为什么选择这种结构？

1. **src 布局**：防止测试时的导入冲突，符合现代 Python 项目标准
2. **自动化脚本**：减少重复性工作，确保一致的开发体验
3. **完整测试**：保证代码质量，便于重构和维护
4. **清晰文档**：新团队成员能快速上手
5. **标准化配置**：所有工具使用统一配置，避免冲突

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！在提交代码前，请确保：

1. 运行 `./dev.sh check` 通过所有检查
2. 添加适当的测试用例
3. 更新相关文档

## 📄 许可证

MIT License - 详见 LICENSE 文件

---

**💡 提示**：这个项目可以作为新 Python 项目的模板。复制整个结构，根据需要修改包名和配置即可快速启动新项目！
