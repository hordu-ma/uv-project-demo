#!/bin/bash

# uv Python 项目开发环境一键脚本
# 基于最佳实践的自动化开发工作流

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 检查是否在项目根目录
check_project_root() {
    if [[ ! -f "pyproject.toml" ]]; then
        log_error "pyproject.toml not found. Please run this script from the project root directory."
        exit 1
    fi
}

# 显示帮助信息
show_help() {
    cat << EOF
uv Python 项目开发脚本

用法: ./dev.sh [选项]

选项:
    setup       完整环境设置（同步依赖 + 质量检查）
    test        运行测试套件
    test-cov    运行测试并显示覆盖率
    format      格式化代码
    lint        代码风格检查
    check       完整质量检查（格式化 + 检查 + 测试）
    clean       清理环境和缓存
    info        显示项目信息
    deps        管理依赖
    build       构建项目
    help        显示此帮助信息

示例:
    ./dev.sh setup      # 设置开发环境
    ./dev.sh check      # 运行所有质量检查
    ./dev.sh test-cov   # 运行测试并查看覆盖率

EOF
}

# 环境设置
setup_environment() {
    log_info "设置开发环境..."

    log_info "同步依赖..."
    uv sync

    log_info "验证 Python 环境..."
    PYTHON_VERSION=$(uv run python --version)
    log_success "Python 环境: $PYTHON_VERSION"

    log_info "验证关键依赖..."
    uv run python -c "import pytest, black" || {
        log_error "关键开发依赖缺失，正在安装..."
        uv add pytest black flake8 pytest-cov --dev
    }

    log_success "开发环境设置完成!"
}

# 运行测试
run_tests() {
    log_info "运行测试套件..."
    if uv run pytest -v; then
        log_success "所有测试通过!"
    else
        log_error "测试失败!"
        exit 1
    fi
}

# 运行测试并显示覆盖率
run_tests_with_coverage() {
    log_info "运行测试并显示覆盖率..."
    if uv run pytest --cov=src --cov-report=term-missing; then
        log_success "测试和覆盖率检查完成!"
    else
        log_error "测试或覆盖率检查失败!"
        exit 1
    fi
}

# 格式化代码
format_code() {
    log_info "格式化代码..."
    uv run black src/ tests/ main.py
    log_success "代码格式化完成!"
}

# 代码风格检查
lint_code() {
    log_info "进行代码风格检查..."
    if uv run flake8 src/ tests/ main.py; then
        log_success "代码风格检查通过!"
    else
        log_error "代码风格检查失败!"
        exit 1
    fi
}

# 完整质量检查
quality_check() {
    log_info "开始完整质量检查..."

    # 1. 格式化代码
    log_info "1/3 格式化代码..."
    uv run black src/ tests/ main.py

    # 2. 代码风格检查
    log_info "2/3 代码风格检查..."
    if ! uv run flake8 src/ tests/ main.py; then
        log_error "代码风格检查失败!"
        exit 1
    fi

    # 3. 运行测试
    log_info "3/3 运行测试套件..."
    if ! uv run pytest --cov=src --cov-fail-under=80; then
        log_error "测试失败或覆盖率不足!"
        exit 1
    fi

    log_success "所有质量检查通过! 🎉"
}

# 清理环境
clean_environment() {
    log_info "清理环境和缓存..."

    # 清理 uv 缓存
    uv clean

    # 清理测试缓存
    rm -rf .pytest_cache/
    rm -rf htmlcov/
    rm -rf .coverage

    # 清理 Python 缓存
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true

    log_success "环境清理完成!"
}

# 显示项目信息
show_info() {
    log_info "项目信息:"

    echo "📦 项目名称: $(grep '^name =' pyproject.toml | cut -d'"' -f2)"
    echo "🏷️  版本: $(grep '^version =' pyproject.toml | cut -d'"' -f2)"
    echo "🐍 Python: $(uv run python --version)"
    echo "📍 位置: $(pwd)"

    if [[ -f "uv.lock" ]]; then
        echo "🔒 依赖锁定文件存在"
    else
        log_warning "依赖锁定文件不存在"
    fi

    echo ""
    log_info "依赖统计:"
    uv tree --depth 1 2>/dev/null || echo "无法获取依赖信息"
}

# 依赖管理
manage_dependencies() {
    log_info "依赖管理选项:"
    echo "1. 查看依赖树 (uv tree)"
    echo "2. 更新所有依赖 (uv sync --upgrade)"
    echo "3. 导出依赖 (requirements.txt)"
    echo "4. 返回"

    read -p "请选择操作 [1-4]: " choice

    case $choice in
        1)
            log_info "依赖树:"
            uv tree
            ;;
        2)
            log_info "更新所有依赖..."
            uv sync --upgrade
            log_success "依赖更新完成!"
            ;;
        3)
            log_info "导出依赖到 requirements.txt..."
            uv export --format requirements-txt --output-file requirements.txt
            log_success "依赖已导出到 requirements.txt"
            ;;
        4)
            return
            ;;
        *)
            log_error "无效选择"
            ;;
    esac
}

# 构建项目
build_project() {
    log_info "构建项目..."

    # 先进行质量检查
    log_info "构建前质量检查..."
    if ! uv run pytest --cov=src --cov-fail-under=80 -q; then
        log_error "质量检查失败，取消构建"
        exit 1
    fi

    # 构建
    uv build

    if [[ -d "dist" ]]; then
        log_success "项目构建完成!"
        log_info "构建产物:"
        ls -la dist/
    else
        log_error "构建失败!"
        exit 1
    fi
}

# 主函数
main() {
    # 检查项目根目录
    check_project_root

    # 如果没有参数，显示帮助
    if [[ $# -eq 0 ]]; then
        show_help
        exit 0
    fi

    # 处理命令行参数
    case $1 in
        setup)
            setup_environment
            ;;
        test)
            run_tests
            ;;
        test-cov)
            run_tests_with_coverage
            ;;
        format)
            format_code
            ;;
        lint)
            lint_code
            ;;
        check)
            quality_check
            ;;
        clean)
            clean_environment
            ;;
        info)
            show_info
            ;;
        deps)
            manage_dependencies
            ;;
        build)
            build_project
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "未知选项: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"
