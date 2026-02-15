#!/usr/bin/env bash
# 单 episode 差异检查：用极端权重 patch，长 episode，只打前 20 行。
# 在项目根目录执行： bash tools/run_diff_recompute.sh

cd "$(dirname "$0")/.."
python3 tools/diff_recompute_single_episode.py \
  --patch tools/patches_extreme/risk_density_3x.json \
  --episode-id slice_EPISODE_6M42S_control_mode_switch_2_2 \
  --max-print 20
