#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速检查：当前 golden suite 的 replay 里 risk_used_for_decision 最大值。
若接近 0.1 说明「无应力」；需用 golden_stress_v2_powerclips + base_patch 才有 early_gain。
用法：python3 tools/verify_golden_stress_level.py [suite_dir]
默认：library_store/v1.1/golden_stress_v2
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
suite = ROOT / (sys.argv[1].strip().strip("/") if len(sys.argv) > 1 else "library_store/v1.1/golden_stress_v2")
mx = 0.0
cnt = 0
replay_files = list(suite.rglob("replay_output.jsonl"))
for p in replay_files:
    for line in p.read_text(encoding="utf-8").strip().splitlines():
        if not line:
            continue
        r = json.loads(line)
        v = r.get("risk_used_for_decision")
        if v is None:
            continue
        mx = max(mx, float(v))
        cnt += 1
print("replay frames scanned:", cnt)
print("max risk_used_for_decision:", mx)
if not replay_files and suite.is_dir():
    print("(no replay_output.jsonl under suite; run recompute or use golden_stress_v2_powerclips)")
