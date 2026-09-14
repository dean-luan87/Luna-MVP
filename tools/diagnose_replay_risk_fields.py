#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定位 replay 是否包含 risk_used_for_decision / threshold_safe_to_caution / high_risk（顶层字段）。
用法：python3 tools/diagnose_replay_risk_fields.py [run_dir]
默认 run_dir = outputs/d1_runs/dev_smoke 下最新一次 run。
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main():
    if len(sys.argv) > 1:
        run_dir = Path(sys.argv[1])
        if not run_dir.is_dir():
            print("run_dir not found:", run_dir, file=sys.stderr)
            return 2
        latest = run_dir
    else:
        run_dir = ROOT / "outputs/d1_runs/dev_smoke"
        if not run_dir.is_dir():
            print("run_dir not found:", run_dir, file=sys.stderr)
            return 2
        subs = sorted(run_dir.iterdir(), key=lambda x: x.stat().st_mtime)
        latest = subs[-1] if subs else run_dir

    it = Path(latest).rglob("replay_output.jsonl")
    p = next(it, None)
    print("using:", p)
    if not p:
        print("no replay_output.jsonl under", latest, file=sys.stderr)
        return 1

    lines = p.read_text(encoding="utf-8").strip().splitlines()
    if not lines:
        print("empty replay", file=sys.stderr)
        return 1
    first = json.loads(lines[0])
    print("available keys:", list(first.keys()))
    keys = [k for k in ("seq", "decision", "high_risk", "risk_used_for_decision", "threshold_safe_to_caution") if k in first]
    print("risk-related keys in first record:", keys)

    n_hr = 0
    risk_max = None
    threshold_vals = set()
    for ln in lines:
        r = json.loads(ln)
        if r.get("high_risk") is True:
            n_hr += 1
        v = r.get("risk_used_for_decision")
        if isinstance(v, (int, float)):
            risk_max = v if risk_max is None else max(risk_max, v)
        t = r.get("threshold_safe_to_caution")
        if isinstance(t, (int, float)):
            threshold_vals.add(t)

    print("high_risk frames:", n_hr)
    print("risk_used_max:", risk_max)
    print("thresholds seen:", threshold_vals)
    return 0


if __name__ == "__main__":
    sys.exit(main())
