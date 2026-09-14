#!/usr/bin/env bash
# 量纲审计：录 Golden(含 6m42s 切片) risk_debug → 分析 weighted_sum / feature 分布。
# 在项目根目录执行： bash tools/run_risk_audit.sh

set -e
cd "$(dirname "$0")/.."
mkdir -p logs

echo "=== Step 1: 录制 risk_debug.jsonl (full Golden Suite) ==="
python3 tools/record_risk_debug.py --golden --out logs/risk_debug.jsonl

echo ""
echo "=== Step 2: 统计分布 ==="
python3 tools/analyze_risk_distribution.py --input logs/risk_debug.jsonl
