#!/usr/bin/env python3
"""
P layer v0 verification script

Verifies:
1. Distribution of ACTION_EXECUTED / NO_ACTION / ACTION_FAILED
2. Every EXECUTED/BLOCKED/FAILED has a valid reason (no UNKNOWN)
3. apply_now is always False in outcome (shadow-only invariant)
4. P only executes SAY actions (implicit via reason set)
"""

import json
import sys
from collections import Counter

FROZEN_OUTCOME_TYPES = {
    "ACTION_EXECUTED",
    "NO_ACTION",
    "ACTION_FAILED",
}

FROZEN_REASONS = {
    # EXECUTED
    "SAY_OK",

    # BLOCKED
    "APPLY_NOW_FALSE",
    "ACTION_NOT_ALLOWED_IN_V0",
    "BLOCKED_COOLDOWN",
    "BLOCKED_ARBITRATION",

    # FAILED
    "EMPTY_TEXT",
    # allow prefix match for TTS errors
}


def is_valid_reason(reason: str) -> bool:
    if reason in FROZEN_REASONS:
        return True
    if reason.startswith("TTS_ERROR"):
        return True
    return False


def main(trace_path: str):
    outcome_count = 0
    type_counter = Counter()
    reason_counter = Counter()

    invalid_type = 0
    invalid_reason = 0
    apply_now_violation = 0

    with open(trace_path, "r") as f:
        for line in f:
            rec = json.loads(line)

            # only arbitration records have outcome
            outcome = rec.get("outcome")
            if not outcome:
                continue

            outcome_count += 1

            otype = outcome.get("outcome_type")
            reason = outcome.get("reason")
            apply_now = outcome.get("apply_now")

            # type check
            if otype not in FROZEN_OUTCOME_TYPES:
                invalid_type += 1
            else:
                type_counter[otype] += 1

            # reason check
            if not reason or not is_valid_reason(reason):
                invalid_reason += 1
            else:
                reason_counter[reason] += 1

            # apply_now invariant
            if apply_now is not False:
                apply_now_violation += 1

    print("\n=== P layer v0 verification ===\n")

    print(f"Outcome records: {outcome_count}")
    print("\n--- Outcome type distribution ---")
    for k, v in type_counter.items():
        print(f"  {k}: {v}")

    print("\n--- Reason distribution ---")
    for k, v in reason_counter.items():
        print(f"  {k}: {v}")

    print("\n--- Invariant checks ---")

    if invalid_type == 0:
        print("[PASS] No invalid outcome_type")
    else:
        print(f"[FAIL] Invalid outcome_type count: {invalid_type}")

    if invalid_reason == 0:
        print("[PASS] No invalid reason")
    else:
        print(f"[FAIL] Invalid reason count: {invalid_reason}")

    if apply_now_violation == 0:
        print("[PASS] apply_now always False (shadow-only)")
    else:
        print(f"[FAIL] apply_now violation count: {apply_now_violation}")

    if invalid_type == 0 and invalid_reason == 0 and apply_now_violation == 0:
        print("\n=== Final verdict ===")
        print("✅ P layer v0 PASSED — execution is controlled, observable, and explainable.")
    else:
        print("\n=== Final verdict ===")
        print("❌ P layer v0 FAILED — invariant violation detected.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        trace_path = "logs/a3_trace.jsonl"
    else:
        trace_path = sys.argv[1]

    try:
        main(trace_path)
    except FileNotFoundError:
        print(f"[FAIL] trace not found: {trace_path}")
        sys.exit(1)
