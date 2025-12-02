#!/bin/bash
# 文件：run_full_test.sh
# 说明：Luna Badge v1.3.0 一键全测试脚本（单测 + 压测 + LNB 评分）

mkdir -p test_reports

echo "============================================"
echo "🚀 Luna Badge v1.3.0 一键测试开始"
echo "============================================"
sleep 1

# ---------------------------------------------
# 1. 运行 3 个关键模块单元测试
# ---------------------------------------------
echo ""
echo ">> [1/5] 运行关键单元测试 (3 modules)..."
python3 -m pytest tests/test_detection.py -vv --maxfail=1 --disable-warnings --log-cli-level=ERROR 2>&1 | tee test_reports/test_detection.log
python3 -m pytest tests/test_fusion.py -vv --maxfail=1 --disable-warnings --log-cli-level=ERROR 2>&1 | tee test_reports/test_fusion.log
python3 -m pytest tests/test_path_detector.py -vv --maxfail=1 --disable-warnings --log-cli-level=ERROR 2>&1 | tee test_reports/test_path_detector.log

echo ""
echo "✔ 单元测试完成，日志输出至 test_reports/*.log"

# ---------------------------------------------
# 2. 全量 A-Z 测试（模块级）
# ---------------------------------------------
echo ""
echo ">> [2/5] A-Z 全量模块测试 (可能需 1-3 分钟)..."
if [ -f "tests/test_all_AZ.py" ]; then
    python3 tests/test_all_AZ.py 2>&1 | tee test_reports/test_AZ.log
else
    echo "⚠️  test_all_AZ.py 不存在，跳过 A-Z 测试"
    echo "跳过 A-Z 测试" > test_reports/test_AZ.log
fi

# ---------------------------------------------
# 3. 压力测试
# ---------------------------------------------
echo ""
echo ">> [3/5] 运行压力测试（60秒，2线程）..."
python3 tests/stress_test_AZ.py --duration 60 --threads 2 2>&1 | tee test_reports/stress_test.log

# ---------------------------------------------
# 4. NAV_STUCK 监控 & 收集器
# ---------------------------------------------
echo ""
echo ">> [4/5] 检查 NAV_STUCK 事件..."
python3 tests/stress_nav_stuck_collector.py 2>&1 | tee test_reports/nav_stuck.log

# ---------------------------------------------
# 5. LNB v1.1 工程评分
# ---------------------------------------------
echo ""
echo ">> [5/5] 运行 LNB v1.1 工程评分..."
python3 tests/lnb_scorer_nav.py 2>&1 | tee test_reports/lnb_score.log

echo ""
echo "============================================"
echo "🎉 测试全部结束：结果请查看 test_reports/"
echo "============================================"

