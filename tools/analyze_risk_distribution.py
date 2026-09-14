#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
量纲审计 Step 2：读 logs/risk_debug.jsonl，输出 weighted_sum 与各 feature 的分布（mean, p50, p90, p95, p99, max）。
用于判定 risk_score 真实物理尺度（0~1 还是 0~0.2）。
"""
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _quantile(x: List[float], q: float) -> float:
    if not x:
        return 0.0
    s = sorted(x)
    i = min(int(len(s) * q), len(s) - 1)
    return float(s[i])


def main() -> int:
    import argparse
    p = argparse.ArgumentParser(description="Analyze risk_debug.jsonl: weighted_sum and feature distributions")
    p.add_argument("--input", default="logs/risk_debug.jsonl", help="risk_debug.jsonl path")
    args = p.parse_args()

    path = args.input
    if not os.path.isabs(path):
        path = os.path.join(ROOT, path)
    if not os.path.isfile(path):
        print("ERROR: not found:", path, file=sys.stderr)
        return 2

    rows: List[Dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    if not rows:
        print("ERROR: no rows in", path, file=sys.stderr)
        return 2

    n = len(rows)
    ws = [float(r.get("weighted_sum_before_clamp", 0)) for r in rows]
    mean_ws = sum(ws) / n
    p50 = _quantile(ws, 0.5)
    p90 = _quantile(ws, 0.9)
    p95 = _quantile(ws, 0.95)
    p99 = _quantile(ws, 0.99)
    max_ws = max(ws)
    n_above_03 = sum(1 for x in ws if x > 0.3)
    n_above_04 = sum(1 for x in ws if x > 0.4)

    feature_keys = ["risk_density", "redline_hit", "path_instability", "motion_instability", "occlusion_ratio", "roi_load"]

    print("input:", path)
    print("rows:", n)
    print()
    print("--- weighted_sum_before_clamp ---")
    print("  mean   ", round(mean_ws, 4))
    print("  p50    ", round(p50, 4))
    print("  p90    ", round(p90, 4))
    print("  p95    ", round(p95, 4))
    print("  p99    ", round(p99, 4))
    print("  max    ", round(max_ws, 4))
    print("  frames > 0.3:", n_above_03)
    print("  frames > 0.4:", n_above_04)
    print()
    print("--- each feature (p95 / max) ---")
    for k in feature_keys:
        vals = [float(r.get(k, 0)) for r in rows]
        mx = max(vals) if vals else 0.0
        print(f"  {k}: p95={_quantile(vals, 0.95):.4f}  max={mx:.4f}")
    print()

    # 判定
    print("--- 量纲判定 ---")
    if max_ws > 0.6:
        print("  raw_max > 0.6：风险尺度可达 0~1；若 ema_max 仍很低，则 EMA 或后续缩放压扁。")
    elif max_ws > 0.3:
        print("  raw_max > 0.3：存在中高段风险帧；阈值可基于 raw_p95 校准。")
    elif max_ws < 0.25:
        print("  raw_max < 0.25：当前 risk_score 实际量纲 0~0.2；阈值 0.38 为空中楼阁。")
        print("  建议：safe_to_caution = raw_p95 * 1.1，或重标定 feature / 高压 Golden。")
    else:
        print("  raw_max 在 0.25~0.3：边界区；建议用 raw_p95 做 calibration。")

    return 0


if __name__ == "__main__":
    sys.exit(main())
