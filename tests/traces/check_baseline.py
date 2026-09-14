#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基线校验：对比 trace_report 与 tests/traces/baselines/<label>.json，四指标在约束内则 PASS。

用法：
  python3 tests/traces/check_baseline.py tests/traces/baselines/medium_long_01.json logs/trace_report_6m42s.json
  python3 tests/traces/check_baseline.py tests/traces/baselines/medium_long_01.json logs/trace_report.json --label medium_long_01

可与 pytest 或 CI 集成：失败时 exit 1。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description="校验 trace 报告是否满足基线约束")
    ap.add_argument("baseline", help="基线 JSON 路径，如 tests/traces/baselines/medium_long_01.json")
    ap.add_argument("report", help="trace_report 路径，如 logs/trace_report_6m42s.json")
    ap.add_argument("--label", default=None, help="报告中的视频 label，默认用 baseline 里的 label")
    args = ap.parse_args()

    with open(args.baseline, "r", encoding="utf-8") as f:
        baseline = json.load(f)
    with open(args.report, "r", encoding="utf-8") as f:
        report = json.load(f)

    label = args.label or baseline.get("label")
    if not label or label not in report.get("videos", {}):
        print(f"FAIL: label '{label}' 不在 report.videos 中", file=sys.stderr)
        return 1

    current = report["videos"][label]
    constraints = baseline.get("constraints", {})
    if not constraints:
        print("PASS: 无约束（仅做占位）", file=sys.stderr)
        return 0

    fails = []
    # mode_switch_total <= max
    if "mode_switch_total_max" in constraints:
        v = current.get("mode_switch_total")
        if v is not None and v > constraints["mode_switch_total_max"]:
            fails.append(f"mode_switch_total {v} > {constraints['mode_switch_total_max']}")

    if "CAUTION_ratio_min" in constraints:
        v = current.get("CAUTION_ratio")
        if v is not None and v < constraints["CAUTION_ratio_min"]:
            fails.append(f"CAUTION_ratio {v} < {constraints['CAUTION_ratio_min']}")
    if "CAUTION_ratio_max" in constraints:
        v = current.get("CAUTION_ratio")
        if v is not None and v > constraints["CAUTION_ratio_max"]:
            fails.append(f"CAUTION_ratio {v} > {constraints['CAUTION_ratio_max']}")

    if "SAFE_EDGE_duration_mean_sec_min" in constraints:
        v = current.get("SAFE_EDGE_duration_mean_sec")
        if v is not None and v < constraints["SAFE_EDGE_duration_mean_sec_min"]:
            fails.append(f"SAFE_EDGE_duration_mean_sec {v} < {constraints['SAFE_EDGE_duration_mean_sec_min']}")
    if "SAFE_EDGE_duration_mean_sec_max" in constraints:
        v = current.get("SAFE_EDGE_duration_mean_sec")
        if v is not None and v > constraints["SAFE_EDGE_duration_mean_sec_max"]:
            fails.append(f"SAFE_EDGE_duration_mean_sec {v} > {constraints['SAFE_EDGE_duration_mean_sec_max']}")

    if "SAFE_EDGE_to_CAUTION_ratio_min" in constraints:
        v = current.get("SAFE_EDGE_to_CAUTION_ratio")
        if v is not None and v < constraints["SAFE_EDGE_to_CAUTION_ratio_min"]:
            fails.append(f"SAFE_EDGE_to_CAUTION_ratio {v} < {constraints['SAFE_EDGE_to_CAUTION_ratio_min']}")
    if "SAFE_EDGE_to_CAUTION_ratio_max" in constraints:
        v = current.get("SAFE_EDGE_to_CAUTION_ratio")
        if v is not None and v > constraints["SAFE_EDGE_to_CAUTION_ratio_max"]:
            fails.append(f"SAFE_EDGE_to_CAUTION_ratio {v} > {constraints['SAFE_EDGE_to_CAUTION_ratio_max']}")

    # 抖动压力样本约束（stress_oscillate_01）
    if "short_caution_run_ratio_max" in constraints:
        v = current.get("short_caution_run_ratio")
        if v is not None and v > constraints["short_caution_run_ratio_max"]:
            fails.append(f"short_caution_run_ratio {v} > {constraints['short_caution_run_ratio_max']}")
    if "switch_per_min_max" in constraints:
        v = current.get("switch_per_min")
        if v is not None and v > constraints["switch_per_min_max"]:
            fails.append(f"switch_per_min {v} > {constraints['switch_per_min_max']}")

    if fails:
        for msg in fails:
            print("FAIL:", msg, file=sys.stderr)
        return 1
    print(f"PASS: {label} 满足基线约束", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
