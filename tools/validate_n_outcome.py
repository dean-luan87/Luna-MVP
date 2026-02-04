#!/usr/bin/env python3
"""
N 层 Outcome v0 自动验收脚本（J→N 严丝合缝版）。

验收标准：
  1. 存在性：100% engaged_signal 记录包含 outcome
  2. outcome_type 仅 ACTION / NO_ACTION
  3. reason 仅使用冻结枚举（无 FAIL / ERROR）
  4. confidence 在 0.0–1.0

Usage:
    python3 tools/validate_n_outcome.py logs/a3_trace.jsonl
"""

import json
import sys
from collections import Counter

# v0 冻结 reason 枚举
VALID_REASONS = frozenset({
    "ACTION_EXECUTED",
    "BLOCKED_COOLDOWN",
    "BLOCKED_RHYTHM",
    "BLOCKED_ARBITRATION",
    "BLOCKED_UNKNOWN",
    "NOT_ATTEMPTED",
})
VALID_OUTCOME_TYPES = frozenset({"ACTION", "NO_ACTION"})


def load_engaged_signal_records(path):
    """Load trace lines that contain engaged_signal."""
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
            if "engaged_signal" in j:
                records.append(j)
    return records


def analyze_outcome(records):
    total = len(records)
    missing_outcome = 0
    outcome_type_dist = Counter()
    reason_dist = Counter()
    invalid_reason = 0
    invalid_outcome_type = 0
    invalid_confidence = 0

    for r in records:
        out = r.get("outcome")
        if not out:
            missing_outcome += 1
            continue

        ot = out.get("outcome_type")
        reason = out.get("reason")
        conf = out.get("confidence")

        if ot not in VALID_OUTCOME_TYPES:
            invalid_outcome_type += 1
        if reason not in VALID_REASONS:
            invalid_reason += 1
        if not isinstance(conf, (int, float)) or conf < 0.0 or conf > 1.0:
            invalid_confidence += 1

        outcome_type_dist[ot] += 1
        reason_dist[reason] += 1

    return {
        "total_engaged_signal": total,
        "missing_outcome": missing_outcome,
        "outcome_type_dist": outcome_type_dist,
        "reason_dist": reason_dist,
        "invalid_reason": invalid_reason,
        "invalid_outcome_type": invalid_outcome_type,
        "invalid_confidence": invalid_confidence,
    }


def print_report(stats):
    print("\n=== N Layer Outcome v0 (J→N) Analysis ===\n")

    print(f"Total engaged_signal records : {stats['total_engaged_signal']}")
    print(f"Missing outcome field        : {stats['missing_outcome']}")

    print("\n-- outcome_type distribution --")
    for k, v in sorted(stats["outcome_type_dist"].items(), key=lambda x: (-x[1], str(x[0]))):
        print(f"  {k or 'None':25s}: {v}")

    print("\n-- reason distribution --")
    for k, v in sorted(stats["reason_dist"].items(), key=lambda x: (-x[1], str(x[0]))):
        print(f"  {k or 'None':25s}: {v}")

    # ---- v0 验收 ----
    print("\n=== N v0 Acceptance Criteria ===")

    ok = True

    if stats["total_engaged_signal"] == 0:
        print("○ No engaged_signal records in trace (nothing to validate)")
        return

    if stats["missing_outcome"] != 0:
        print("✗ FAIL: Not all engaged_signal records contain `outcome`")
        ok = False
    else:
        print("✓ 1. Existence: 100% engaged_signal records contain `outcome`")

    if stats["invalid_outcome_type"] != 0:
        print("✗ FAIL: outcome_type must be ACTION or NO_ACTION only")
        ok = False
    else:
        print("✓ 2. outcome_type: only ACTION / NO_ACTION")

    if stats["invalid_reason"] != 0:
        print("✗ FAIL: reason must use frozen enum (no FAIL/ERROR)")
        ok = False
    else:
        print("✓ 3. reason: frozen enum only")

    if stats["invalid_confidence"] != 0:
        print("✗ FAIL: confidence must be in [0.0, 1.0]")
        ok = False
    else:
        print("✓ 4. confidence: in range")

    if ok:
        print("\n✅ N layer Outcome v0 PASSED all acceptance criteria")
    else:
        print("\n❌ N layer Outcome v0 FAILED one or more criteria")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 tools/validate_n_outcome.py <a3_trace.jsonl>")
        sys.exit(1)

    path = sys.argv[1]
    records = load_engaged_signal_records(path)

    if not records:
        print("No engaged_signal records found.")
        sys.exit(0)

    stats = analyze_outcome(records)
    print_report(stats)


if __name__ == "__main__":
    main()
