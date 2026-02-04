#!/bin/bash
# BC Architecture Guard CI 入口脚本
# 用途：CI Pipeline 统一入口

set -e  # 遇到错误立即退出

echo "=========================================="
echo "BC Architecture Guard CI Pipeline"
echo "=========================================="

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 未找到"
    exit 1
fi

# Step 1: Architecture Guard Check（硬拦截）
echo ""
echo "Step 1: Architecture Guard Check"
echo "----------------------------------------"
python3 .ci/run_arch_guard.py \
    --guard .ci/bc_architecture_guard.yaml \
    --dcs .ci/dcs_rules.yaml \
    --scan vision_pipeline

GUARD_EXIT_CODE=$?

if [ $GUARD_EXIT_CODE -ne 0 ]; then
    echo ""
    echo "❌ CI FAIL: Architecture Guard 检查失败"
    exit $GUARD_EXIT_CODE
fi

# Step 2: DCS Judgment（红黄绿）
echo ""
echo "Step 2: DCS Judgment"
echo "----------------------------------------"
# DCS 检查已包含在 run_arch_guard.py 中
# 这里可以单独运行 DCS 分析（如果需要）

# Step 3: Violation Test Suite（反例回归）
echo ""
echo "Step 3: Violation Test Suite"
echo "----------------------------------------"
python3 -m pytest .ci/violation_cases.py -v

TEST_EXIT_CODE=$?

if [ $TEST_EXIT_CODE -ne 0 ]; then
    echo ""
    echo "❌ CI FAIL: 反例测试集失败"
    exit $TEST_EXIT_CODE
fi

echo ""
echo "=========================================="
echo "✅ CI PASS: 所有检查通过"
echo "=========================================="
exit 0
