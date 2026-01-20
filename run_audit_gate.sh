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


