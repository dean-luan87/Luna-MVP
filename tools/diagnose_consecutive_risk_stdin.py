#!/usr/bin/env python3
"""从 stdin 读 replay_output.jsonl 路径（每行一个），输出 GLOBAL MAX consecutive >=0.55。
   用法: find ... -name replay_output.jsonl | python3 tools/diagnose_consecutive_risk_stdin.py"""
import json
import sys
from pathlib import Path

global_max = 0
risk_global_max = 0.0
first_keys = None
n_files = 0

for line in sys.stdin:
    path = Path(line.strip())
    if not path.is_file():
        continue
    n_files += 1
    with open(path) as f:
        current = 0
        for ln in f:
            rec = json.loads(ln)
            if first_keys is None:
                first_keys = sorted(rec.keys())
            r = rec.get("risk_used_for_decision", 0)
            try:
                r = float(r)
            except (TypeError, ValueError):
                r = 0.0
            risk_global_max = max(risk_global_max, r)
            if r >= 0.55:
                current += 1
                global_max = max(global_max, current)
            else:
                current = 0

print("GLOBAL MAX consecutive >=0.55:", global_max)
print("risk_used_for_decision global max:", risk_global_max)
print("first record keys:", first_keys)
print("files scanned:", n_files)
