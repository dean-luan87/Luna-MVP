#!/bin/bash
# Luna Badge v1.4.1 QA 测试套件运行脚本

set -e

echo "=========================================="
echo "Luna Badge v1.4.1 QA 测试套件"
echo "=========================================="
echo ""

# 检查 pytest 是否安装
if ! command -v pytest &> /dev/null; then
    echo "❌ pytest 未安装，请运行: pip install pytest pytest-html"
    exit 1
fi

# 进入项目根目录
cd "$(dirname "$0")/../.."

# 运行所有测试
echo "运行所有 QA 测试..."
pytest tests/qa_1_4_1/ -v --tb=short

echo ""
echo "=========================================="
echo "✅ 所有测试完成"
echo "=========================================="
















