#!/bin/bash
# Luna Badge v1.4.1 自动化 QA 测试入口（完整版）

set -e

echo "=========================================="
echo "Luna Badge v1.4.1 自动化 QA 测试"
echo "（核心 + FailSafe + 压力 + 内存 + TTS）"
echo "=========================================="
echo ""

# 检查 pytest 是否安装
if ! command -v pytest &> /dev/null; then
    echo "❌ pytest 未安装，请运行: pip install pytest"
    exit 1
fi

# 进入项目根目录
cd "$(dirname "$0")/.."

# 运行完整 QA 测试套件
echo "运行完整 QA 测试套件..."
pytest tests/qa_1_4_1/ -s -v

echo ""
echo "=========================================="
echo "✅ QA 测试完成"
echo "=========================================="

