#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
校验 golden_stress_v2_powerclips 级统计：episodes_count、risk_used_max/high_risk_frames 分位、点火率 100%。
"""
import json
import sys
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parents[1]


def _p95(vals: List[float]) -> float:
    if not vals:
        return 0.0
    s = sorted(vals)
    i = max(0, int(len(s) * 0.95) - 1)
    return s[i]


def main() -> int:
    import argparse
    p = argparse.ArgumentParser(description="Validate powerclips suite stats (ignition rate must be 100%)")
    p.add_argument("--suite", default="library_store/v1.1/golden_stress_v2_powerclips",
                   help="Path to suite dir (under ROOT or absolute)")
    args = p.parse_args()

    suite = ROOT / args.suite.strip().strip("/") if not Path(args.suite).is_absolute() else Path(args.suite)
    if not suite.is_dir():
        print("ERROR: suite dir not found:", suite, file=sys.stderr)
        return 2

    risk_max_list: List[float] = []
    high_risk_list: List[int] = []
    episodes_count = 0
    ignited = 0

    for ep_dir in sorted(suite.iterdir()):
        if not ep_dir.is_dir():
            continue
        meta_path = ep_dir / "meta.json"
        if not meta_path.is_file():
            continue
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        episodes_count += 1
        risk_max = meta.get("risk_used_max")
        high_risk_frames = meta.get("high_risk_frames", 0)
        if isinstance(risk_max, (int, float)):
            risk_max_list.append(float(risk_max))
        if isinstance(high_risk_frames, (int, float)):
            high_risk_list.append(int(high_risk_frames))
        if high_risk_frames and int(high_risk_frames) > 0:
            ignited += 1

    ignition_rate = (ignited / episodes_count * 100.0) if episodes_count else 0.0
    print("episodes_count:", episodes_count)
    if risk_max_list:
        s_risk = sorted(risk_max_list)
        mid = len(s_risk) // 2
        med = (s_risk[mid - 1] + s_risk[mid]) / 2.0 if len(s_risk) > 1 else (s_risk[0] if s_risk else 0)
        print("risk_used_max: min=%.4f median=%.4f p95=%.4f" % (min(risk_max_list), med, _p95(risk_max_list)))
    if high_risk_list:
        s_hr = sorted(high_risk_list)
        mid = len(s_hr) // 2
        med_hr = (s_hr[mid - 1] + s_hr[mid]) // 2 if len(s_hr) > 1 else (s_hr[0] if s_hr else 0)
        print("high_risk_frames: min=%d median=%d p95=%d" % (min(high_risk_list), med_hr, int(_p95([float(x) for x in high_risk_list]))))
    print("ignition_rate (high_risk_frames>0): %.1f%% (%d/%d)" % (ignition_rate, ignited, episodes_count))

    if episodes_count and ignition_rate < 100.0:
        print("FAIL: ignition rate must be 100%", file=sys.stderr)
        return 2
    if episodes_count == 0:
        print("FAIL: no episodes in suite", file=sys.stderr)
        return 2
    print("PASS: powerclips suite valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
