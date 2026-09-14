# examples/b2_v04_sanity_check.py
from __future__ import annotations
import json
import os
import numpy as np
from typing import Dict, List

# -----------------------------
# utils
# -----------------------------

def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_jsonl(path: str):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)

def warn(msg: str):
    print(f"[WARN] {msg}")

def fail(msg: str):
    print(f"[FAIL] {msg}")

def ok(msg: str):
    print(f"[OK] {msg}")

# -----------------------------
# A. Evidence coverage
# -----------------------------

def check_evidence_coverage(b2_events: List[Dict]) -> bool:
    missing = [e for e in b2_events if not e.get("evidence_ref")]
    if missing:
        fail(f"Evidence missing for {len(missing)} decisions")
        return False
    ok("All decisions have evidence_ref")
    return True

# -----------------------------
# B. Param stability
# -----------------------------

def check_param_stability(evidence_paths: List[str]) -> bool:
    series: Dict[str, List[float]] = {}

    for p in evidence_paths:
        ev = load_json(p)
        pv = ev.get("param_vector") or {}
        for k, v in pv.items():
            series.setdefault(k, []).append(float(v))

    unstable = []
    for k, vals in series.items():
        if len(vals) < 5:
            continue
        std = float(np.std(vals))
        if std > 0.25:   # v0.4 人工设定阈值
            unstable.append((k, std))

    if unstable:
        warn("Unstable params detected:")
        for k, std in unstable:
            warn(f"  {k} std={std:.3f}")
        return False

    ok("Param stability within acceptable range")
    return True

# -----------------------------
# C. Alignment quality
# -----------------------------

def check_alignment(report_csv: str) -> bool:
    import csv

    if not os.path.exists(report_csv):
        fail("Alignment report CSV not found")
        return False

    ok_cnt = late_cnt = miss_cnt = 0
    with open(report_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r["result"] == "OK":
                ok_cnt += 1
            elif r["result"] == "LATE":
                late_cnt += 1
            elif r["result"] == "MISS":
                miss_cnt += 1

    total = ok_cnt + late_cnt + miss_cnt
    if total == 0:
        fail("No alignment records")
        return False

    miss_ratio = miss_cnt / total
    if miss_ratio > 0.15:
        fail(f"MISS ratio too high: {miss_ratio:.2%}")
        return False

    warn(f"LATE={late_cnt}, MISS={miss_cnt}")
    ok("Alignment quality acceptable")
    return True

# -----------------------------
# D. Session continuity
# -----------------------------

def check_session_continuity(session_dir: str) -> bool:
    timeline = os.path.join(session_dir, "timeline.md")
    if not os.path.exists(timeline):
        fail("Session timeline.md missing")
        return False

    with open(timeline, "r", encoding="utf-8") as f:
        lines = [l for l in f.readlines() if "–" in l]

    if len(lines) < 3:
        warn("Too few decisions in session, continuity not meaningful")
        return False

    ok("Session continuity file exists and readable")
    return True

# -----------------------------
# main
# -----------------------------

def main():
    b2_events = list(load_jsonl("b2_v03_timeline.jsonl"))
    evidence_paths = [e["evidence_ref"] for e in b2_events if e.get("evidence_ref")]

    status = True

    status &= check_evidence_coverage(b2_events)
    status &= check_param_stability(evidence_paths)
    status &= check_alignment("reports/b2_v03_alignment.csv")
    status &= check_session_continuity("reports/b2_v03_review/sessions/session_001")

    print("-------------------------------------------------")
    if status:
        ok("B2 v0.4 SANITY CHECK: PASS")
    else:
        fail("B2 v0.4 SANITY CHECK: FAIL")

if __name__ == "__main__":
    main()

