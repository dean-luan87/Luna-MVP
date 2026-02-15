#!/usr/bin/env bash
# A3 risk_score vs 阈值诊断（单 episode，baseline + risk_density 3x 各跑一次）
# 在项目根目录执行： bash tools/run_diagnose_a3_risk.sh

cd "$(dirname "$0")/.."
echo "=== baseline ==="
python3 tools/diagnose_a3_risk_score.py --episode-id slice_EPISODE_6M42S_control_mode_switch_2_2
echo ""
echo "=== risk_density 3x ==="
python3 tools/diagnose_a3_risk_score.py --episode-id slice_EPISODE_6M42S_control_mode_switch_2_2 --patch tools/patches_extreme/risk_density_3x.json
