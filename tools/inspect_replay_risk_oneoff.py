#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单次检查：指定 run_dir 下 replay_output.jsonl 的 risk 相关键与统计。
用法：python3 tools/inspect_replay_risk_oneoff.py [run_dir]
默认 run_dir = outputs/d1_runs/dev_smoke/20260214041011
"""
import json
from pathlib import Path
import sys

run_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("outputs/d1_runs/dev_smoke/20260214041011")
it = run_dir.rglob("replay_output.jsonl")
p = next(it, None)
print("replay:", p)
if not p:
    sys.exit(0)

lines = p.read_text(encoding="utf-8").strip().splitlines()
if not lines:
    print("empty replay")
    sys.exit(0)
first = json.loads(lines[0])
keys = [k for k in ["seq", "decision", "high_risk", "risk_used_for_decision", "threshold_safe_to_caution"] if k in first]
print("keys in first record:", keys)

hr = 0
mx = None
ths = set()
for ln in lines:
    r = json.loads(ln)
    if r.get("high_risk") is True:
        hr += 1
    v = r.get("risk_used_for_decision")
    if isinstance(v, (int, float)):
        mx = v if mx is None else max(mx, v)
    t = r.get("threshold_safe_to_caution")
    if isinstance(t, (int, float)):
        ths.add(t)

print("high_risk frames:", hr)
print("risk_used_max:", mx)
print("thresholds:", ths)
