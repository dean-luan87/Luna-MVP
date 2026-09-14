#!/usr/bin/env bash
# 路径 1 校准全流程（最短落地）：stress 从 golden 选 → 三档阈值跑四指标 → 三候选对撞。
# 在项目根目录执行： bash tools/run_calib_full.sh

set -e
cd "$(dirname "$0")/.."

echo "=== 1) 从 Golden 选 10~15 条 stress 到 golden_stress ==="
python3 tools/populate_stress_from_golden.py --top-n 15

echo ""
echo "=== 2) 三档 calib 阈值跑 stress suite，输出四指标 ==="
python3 tools/run_calib_stress_suite.py --base-dir library_store --version-tag v1.1

echo ""
echo "=== 3) 用选定档(0.195)跑三候选 (baseline / aggressive / conservative) ==="
python3 tools/run_calib_three_candidates.py --calib-patch patches/calib_threshold_0195.json

echo ""
echo "完成。三档四指标见 outputs/v1.1/calib_v1/calib_three_tiers.json；三候选见 calib_three_candidates.json。"
