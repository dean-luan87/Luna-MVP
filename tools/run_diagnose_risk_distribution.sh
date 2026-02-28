#!/usr/bin/env bash
# risk_score 尺度诊断：单 episode + 全 Golden 各跑一次，输出 raw 分布与 component 分布。
# 在项目根目录执行： bash tools/run_diagnose_risk_distribution.sh

set -e
cd "$(dirname "$0")/.."
EP="slice_EPISODE_6M42S_control_mode_switch_2_2"
OUT="outputs/v1.1"
mkdir -p "$OUT"

echo "=== 单 episode (slice_EPISODE_6M42S_control_mode_switch_2_2) ==="
python3 tools/diagnose_risk_score_distribution.py --episode-id "$EP" --out-json "$OUT/risk_score_distribution.json"

echo ""
echo "=== 全 Golden Suite ==="
python3 tools/diagnose_risk_score_distribution.py --golden --out-json "$OUT/risk_score_distribution_golden.json"
