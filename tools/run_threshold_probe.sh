#!/usr/bin/env bash
# 路径 A 最小扰动验证：仅降阈值（threshold_probe_30down），同一条 episode。
# 验收：看 ema 是否靠近新阈值 0.266；看 diff_frames 是否 > 0。
# 在项目根目录执行： bash tools/run_threshold_probe.sh

set -e
cd "$(dirname "$0")/.."
EP="slice_EPISODE_6M42S_control_mode_switch_2_2"
PATCH="patches/threshold_probe_30down.json"

echo "=== A) 风险分布诊断（看 ema 是否接近新阈值 0.266）==="
python3 tools/diagnose_a3_risk_score.py \
  --base-dir library_store --version-tag v1.1 \
  --episode-id "$EP" \
  --patch "$PATCH"

echo ""
echo "=== B) 决策分叉验证（baseline 无 patch vs candidate 阈值 probe）==="
python3 tools/diff_recompute_single_episode.py \
  --base-dir library_store --version-tag v1.1 \
  --patch "$PATCH" \
  --episode-id "$EP" \
  --max-print 25

echo ""
echo "验收：若 diff_frames > 0 → 阈值真空区确认，权重是有效旋钮；若仍 = 0 → 需查 risk_score 尺度链路。"
