#!/usr/bin/env python3
"""最小诊断：replay 里真实的连续 risk >= 0.55 的最大连续帧数。只输出一个数字。"""
import json
from pathlib import Path

suite_path = Path("outputs/d1_runs/phase4_seed_sweep/lam_0.40/seed_42")

global_max = 0

for p in suite_path.rglob("replay_output.jsonl"):
    with open(p) as f:
        current = 0
        for line in f:
            r = json.loads(line).get("risk_used_for_decision", 0)
            if r >= 0.55:
                current += 1
                global_max = max(global_max, current)
            else:
                current = 0

print("GLOBAL MAX consecutive >=0.55:", global_max)
