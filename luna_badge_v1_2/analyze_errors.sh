#!/bin/bash
# 文件：analyze_errors.sh
# 说明：自动分析测试结果，计算错误率，输出失败模块

echo "============================================"
echo "🔍 Luna 测试结果分析"
echo "============================================"

# 统计单元测试失败次数
DET_FAIL=$(grep -c "FAILED" test_reports/test_detection.log 2>/dev/null | head -1 || echo "0")
FUS_FAIL=$(grep -c "FAILED" test_reports/test_fusion.log 2>/dev/null | head -1 || echo "0")
PATH_FAIL=$(grep -c "FAILED" test_reports/test_path_detector.log 2>/dev/null | head -1 || echo "0")
AZ_FAIL=$(grep -c "FAILED\|failed" test_reports/test_AZ.log 2>/dev/null | head -1 || echo "0")

# 统计单元测试通过次数
DET_PASS=$(grep -c "PASSED" test_reports/test_detection.log 2>/dev/null | head -1 || echo "0")
FUS_PASS=$(grep -c "PASSED" test_reports/test_fusion.log 2>/dev/null | head -1 || echo "0")
PATH_PASS=$(grep -c "PASSED" test_reports/test_path_detector.log 2>/dev/null | head -1 || echo "0")

# 从压力测试 JSON 读取结果
if [ -f "test_reports/stress_report.json" ]; then
    STRESS_FAIL=$(python3 -c "import json; d=json.load(open('test_reports/stress_report.json')); print(d.get('error_count', 0))" 2>/dev/null || echo "0")
    STRESS_TOTAL=$(python3 -c "import json; d=json.load(open('test_reports/stress_report.json')); print(d.get('test_count', 0))" 2>/dev/null || echo "0")
    STRESS_SUCCESS=$(python3 -c "import json; d=json.load(open('test_reports/stress_report.json')); print(d.get('success_count', 0))" 2>/dev/null || echo "0")
else
    STRESS_FAIL=0
    STRESS_TOTAL=0
    STRESS_SUCCESS=0
fi

# 从 LNB 评分读取
if [ -f "test_reports/lnb_score_nav.json" ]; then
    LNB_SCORE=$(python3 -c "import json; d=json.load(open('test_reports/lnb_score_nav.json')); print(d.get('total_score', 0))" 2>/dev/null || echo "0")
    KPI7=$(python3 -c "import json; d=json.load(open('test_reports/lnb_score_nav.json')); print(d.get('kpi_scores', {}).get('KPI7', 0))" 2>/dev/null || echo "0")
else
    LNB_SCORE=0
    KPI7=0
fi

echo ""
echo "📊 单元测试结果:"
echo "  detection:      通过 $DET_PASS, 失败 $DET_FAIL"
echo "  fusion:         通过 $FUS_PASS, 失败 $FUS_FAIL"
echo "  path_detector:  通过 $PATH_PASS, 失败 $PATH_FAIL"
echo "  A-Z:            失败 $AZ_FAIL"

echo ""
echo "🔥 压力测试结果:"
echo "  总测试数: $STRESS_TOTAL"
echo "  成功: $STRESS_SUCCESS"
echo "  失败: $STRESS_FAIL"

# 计算错误率
if [ "$STRESS_TOTAL" -gt 0 ]; then
    ERR_RATE=$(python3 -c "print(f'{100*$STRESS_FAIL/$STRESS_TOTAL:.2f}')" 2>/dev/null || echo "0.00")
else
    ERR_RATE="0.00"
fi

echo ""
echo "📈 错误率: ${ERR_RATE}%"

# 计算总失败数（确保是数字）
DET_FAIL_NUM=${DET_FAIL:-0}
FUS_FAIL_NUM=${FUS_FAIL:-0}
PATH_FAIL_NUM=${PATH_FAIL:-0}
STRESS_FAIL_NUM=${STRESS_FAIL:-0}
TOTAL_FAIL=$((DET_FAIL_NUM + FUS_FAIL_NUM + PATH_FAIL_NUM + STRESS_FAIL_NUM))

echo ""
echo "============================================"
if (( $(echo "$ERR_RATE == 0" | bc -l 2>/dev/null || echo "1") )); then
    if [ "$ERR_RATE" = "0.00" ] && [ "$TOTAL_FAIL" -eq 0 ]; then
        echo "🎉🎉🎉 测试通过：错误率 = 0%"
        echo "✅ 所有测试模块通过"
    else
        echo "⚠️  需修复剩余错误，才能达到 0%。"
        echo "   总失败数: $TOTAL_FAIL"
    fi
else
    echo "⚠️  需修复剩余错误，才能达到 0%。"
    echo "   总失败数: $TOTAL_FAIL"
fi

echo ""
echo "⭐ LNB v1.1 评分:"
echo "  总分: $LNB_SCORE / 100"
echo "  KPI7 (压力测试): $KPI7 分"

echo ""
echo "📋 失败模块详情:"
if [ "$DET_FAIL_NUM" -gt 0 ]; then
    echo "  ❌ test_detection.py: $DET_FAIL_NUM 次失败"
fi
if [ "$FUS_FAIL_NUM" -gt 0 ]; then
    echo "  ❌ test_fusion.py: $FUS_FAIL_NUM 次失败"
fi
if [ "$PATH_FAIL_NUM" -gt 0 ]; then
    echo "  ❌ test_path_detector.py: $PATH_FAIL_NUM 次失败"
fi
if [ "$STRESS_FAIL_NUM" -gt 0 ]; then
    echo "  ❌ 压力测试: $STRESS_FAIL_NUM 次失败"
fi

if [ "$TOTAL_FAIL" -eq 0 ]; then
    echo "  ✅ 无失败模块"
fi

echo "============================================"

