#!/bin/bash
# Luna Badge v1.4.1 自动化 QA 测试入口

set -e

echo "=========================================="
echo "Luna Badge v1.4.1 自动化 QA 测试"
echo "=========================================="
echo ""

# 检查 pytest 是否安装
if ! command -v pytest &> /dev/null; then
    echo "❌ pytest 未安装，请运行: pip install pytest"
    exit 1
fi

# 进入项目根目录
cd "$(dirname "$0")/.."

# 运行 QA 测试
echo "运行自动化 QA 测试..."
pytest tests/qa_1_4_1/test_entry.py tests/qa_1_4_1/test_hooks.py -s -v

echo ""
echo "=========================================="
echo "✅ QA 测试完成"
echo "=========================================="

