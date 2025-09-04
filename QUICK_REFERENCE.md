# uv Python 项目快速参考卡片

> 🚀 一页纸掌握 uv Python 项目工作流

## 🎯 新项目快速启动（5分钟）

```bash
# 1. 创建项目
cd ~/my-devs/python
uv init my-project && cd my-project
uv python pin 3.12

# 2. 添加开发工具
uv add black flake8 pytest pytest-cov --dev

# 3. 创建 src 结构
mkdir -p src/$(echo ${PWD##*/} | tr '-' '_') tests
touch src/$(echo ${PWD##*/} | tr '-' '_')/__init__.py tests/__init__.py

# 4. 验证环境
uv run python --version && echo "✅ 项目就绪！"
```

## 💻 每日开发工作流（30秒）

```bash
# 进入项目
cd my-project && uv sync

# 开发循环（重复执行）
uv run pytest -x                    # 快速测试
# [编写代码...]
uv run black src/ tests/            # 格式化
uv run flake8 src/ tests/           # 检查
uv run pytest                       # 完整测试
```

## 🔧 核心命令速查

| 功能 | 命令 | 说明 |
|------|------|------|
| **项目管理** | `uv sync` | 同步依赖 |
| | `uv sync --upgrade` | 更新依赖 |
| | `uv clean` | 清理缓存 |
| **依赖管理** | `uv add package` | 添加运行依赖 |
| | `uv add package --dev` | 添加开发依赖 |
| | `uv remove package` | 移除依赖 |
| | `uv tree` | 查看依赖树 |
| **测试** | `uv run pytest` | 运行所有测试 |
| | `uv run pytest -x` | 失败时停止 |
| | `uv run pytest --cov=src` | 覆盖率测试 |
| **代码质量** | `uv run black .` | 格式化代码 |
| | `uv run flake8 .` | 代码检查 |

## 📁 标准项目结构

```
my-project/
├── src/my_project/          # 主代码（下划线命名）
│   ├── __init__.py
│   ├── main.py             # 核心逻辑
│   └── utils.py
├── tests/                   # 测试代码
│   ├── __init__.py
│   └── test_main.py
├── main.py                  # 项目入口
├── pyproject.toml          # 项目配置
├── README.md
└── uv.lock                 # 锁定文件
```

## ⚡ 一键脚本

**创建 `dev.sh`：**
```bash
#!/bin/bash
echo "🚀 Dev environment setup..."
uv sync && uv run pytest -x && uv run black . && uv run flake8 .
echo "✅ Ready to code!"
```

**使用：** `chmod +x dev.sh && ./dev.sh`

## 🎯 质量标准

- ✅ 测试覆盖率 ≥ 80%
- ✅ 所有测试通过
- ✅ Black 格式化
- ✅ Flake8 无错误
- ✅ 函数 < 60 行
- ✅ 类型注解完整

## 🔍 故障排除

| 问题 | 解决方案 |
|------|----------|
| 依赖冲突 | `uv sync --refresh` |
| 环境损坏 | `rm -rf .venv && uv sync` |
| 测试失败 | `uv run pytest --lf -v` |
| 导入错误 | 检查 `PYTHONPATH` 和 `src/` 结构 |

## 📋 发版检查清单

- [ ] `uv run pytest --cov=src --cov-fail-under=80` 通过
- [ ] `uv run black --check .` 通过
- [ ] `uv run flake8 .` 通过
- [ ] 更新版本号 `pyproject.toml`
- [ ] `uv build` 构建成功
- [ ] Git 提交和标签

---

**💡 提示：** 将此文件保存到每个项目根目录，随时查阅！
