#!/bin/bash
# V1.8 冻结门禁脚本
# 在 CI 或本地提交前运行此脚本进行审计检查

set -e

echo "🔍 Running V1.8 Full Engineering Audit (Freeze Gate)..."
echo ""

python3 tools/v18_full_audit.py --ci

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo ""
    echo "✅ Audit passed - Freeze gate open"
    echo ""
    echo "🔍 Running C Gate validation..."
    python3 - <<'PY'
from runtime.main_loop import MainLoop

loop = MainLoop("runs/trace_c_gate.jsonl")
loop.run_for_seconds(1)
PY
    python3 tools/validate_c_gate.py --trace runs/trace_c_gate.jsonl --out runs/c_gate_report.json
    c_exit=$?
    if [ $c_exit -ne 0 ]; then
        echo ""
        echo "❌ C Gate failed - blocking"
        exit $c_exit
    fi
    echo "✅ C Gate passed"
    exit 0
elif [ $exit_code -eq 1 ]; then
    echo ""
    echo "❌ Audit failed - RISK detected (blocked in CI mode)"
    echo "   Review the audit report: docs/V1_8_AUDIT_REPORT.md"
    exit 1
elif [ $exit_code -eq 2 ]; then
    echo ""
    echo "🚨 Audit failed - VIOLATION detected (must fix)"
    echo "   Review the audit report: docs/V1_8_AUDIT_REPORT.md"
    exit 2
else
    echo ""
    echo "⚠️  Audit completed with exit code: $exit_code"
    exit $exit_code
fi


