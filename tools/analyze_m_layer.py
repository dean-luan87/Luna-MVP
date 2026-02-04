#!/usr/bin/env python3
"""
Analyze M layer (ActionPlan) distribution from arbitration trace.

Usage:
    python3 tools/analyze_m_layer.py logs/a3_trace.jsonl
"""

import json
import sys
from collections import Counter, defaultdict


def load_arbitration_records(path):
    """Load trace lines that contain arbitration; each record is full row (arbitration + k + l + m)."""
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                j = json.loads(line)
            except Exception:
                continue
            if "arbitration" in j:
                records.append(j)
    return records


def analyze_m(records):
    total = len(records)

    action_type = Counter()
    modality = Counter()
    urgency = Counter()
    apply_now = Counter()
    by_winner = defaultdict(Counter)

    missing_m = 0

    for r in records:
        m = r.get("m")
        arb = r.get("arbitration", {})
        winner = arb.get("winner_type") if arb.get("winner_type") is not None else arb.get("winner")
        if winner is None:
            winner = "NONE"

        if not m:
            missing_m += 1
            continue

        action_type[m.get("action_type")] += 1
        modality[m.get("modality")] += 1
        urgency[m.get("urgency")] += 1
        apply_now[m.get("apply_now")] += 1

        by_winner[winner][m.get("action_type")] += 1

    return {
        "total_arbitrations": total,
        "missing_m": missing_m,
        "action_type": action_type,
        "modality": modality,
        "urgency": urgency,
        "apply_now": apply_now,
        "by_winner": dict(by_winner),
    }


def print_report(stats):
    print("\n=== M Layer v0 Analysis ===\n")

    print(f"Total arbitration records : {stats['total_arbitrations']}")
    print(f"Missing m field           : {stats['missing_m']}")

    print("\n-- ActionType distribution --")
    for k, v in stats["action_type"].items():
        print(f"  {k or 'None':10s}: {v}")

    print("\n-- Modality distribution --")
    for k, v in stats["modality"].items():
        print(f"  {k or 'None':10s}: {v}")

    print("\n-- Urgency distribution --")
    for k, v in stats["urgency"].items():
        print(f"  {k or 'None':10s}: {v}")

    print("\n-- apply_now (must all be False in v0) --")
    for k, v in stats["apply_now"].items():
        print(f"  {k}: {v}")

    print("\n-- ActionType by Winner --")
    for winner, cnt in sorted(stats["by_winner"].items(), key=lambda x: str(x[0])):
        print(f"\n  Winner = {winner}")
        for action, v in cnt.items():
            print(f"    {action or 'None':10s}: {v}")

    # ---- v0 invariants ----
    print("\n=== v0 Invariant Checks ===")

    ok = True

    if stats["missing_m"] != 0:
        print("✗ FAIL: Some arbitration records missing `m`")
        ok = False
    else:
        print("✓ All arbitration records contain `m`")

    if list(stats["apply_now"].keys()) != [False]:
        print("✗ FAIL: apply_now is not always False")
        ok = False
    else:
        print("✓ apply_now is always False (shadow-only)")

    # WARN 只允许出现在 winner_type == SAFETY
    warn_ok = True
    for winner, cnt in stats["by_winner"].items():
        if "WARN" in cnt and winner != "SAFETY":
            warn_ok = False
            break
    if not warn_ok:
        print("✗ FAIL: WARN appears for non-SAFETY winner")
        ok = False
    else:
        print("✓ WARN only appears under SAFETY winner")

    if ok:
        print("\n✅ M layer v0 PASSED all invariant checks")
    else:
        print("\n❌ M layer v0 FAILED one or more invariant checks")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 tools/analyze_m_layer.py <a3_trace.jsonl>")
        sys.exit(1)

    path = sys.argv[1]
    records = load_arbitration_records(path)

    if not records:
        print("No arbitration records found.")
        sys.exit(0)

    stats = analyze_m(records)
    print_report(stats)


if __name__ == "__main__":
    main()
