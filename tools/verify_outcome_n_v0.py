#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
N layer v0 automatic verification
- read a3_trace.jsonl
- validate Outcome completeness, distribution, and consistency
- 目标：验证 Outcome 是否「可统计、可解释、可冻结」
"""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


TRACE_PATH = "logs/a3_trace.jsonl"

# v0 冻结：outcome_type 与 reason 枚举
VALID_OUTCOME_TYPES = frozenset({"ACTION", "NO_ACTION"})
VALID_REASONS = frozenset({
    "ACTION_EXECUTED",
    "BLOCKED_COOLDOWN",
    "BLOCKED_RHYTHM",
    "BLOCKED_ARBITRATION",
    "BLOCKED_UNKNOWN",
    "NOT_ATTEMPTED",
})


def load_trace(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return rows


def main():
    path = Path(TRACE_PATH)
    if len(sys.argv) >= 2:
        path = Path(sys.argv[1])
    if not path.exists():
        print(f"[FAIL] trace not found: {path}")
        sys.exit(1)

    rows = load_trace(path)

    # ENGAGED 相关：带 rhythm.state==ENGAGED 的行（timeseries）
    engaged_ticks = [r for r in rows if r.get("rhythm", {}).get("state") == "ENGAGED"]
    # 带 engaged_signal 的行（J 产出）；这些行应同时带 outcome（N 产出）
    engaged_signal_rows = [r for r in rows if "engaged_signal" in r]
    outcome_rows = [r for r in rows if "outcome" in r]

    total_engaged_ticks = len(engaged_ticks)
    total_engaged_signal = len(engaged_signal_rows)
    total_outcome = len(outcome_rows)

    print("\n=== N layer v0 verification ===\n")
    print(f"ENGAGED ticks (rhythm=ENGAGED): {total_engaged_ticks}")
    print(f"Engaged_signal records (J):     {total_engaged_signal}")
    print(f"Outcome records (N):           {total_outcome}")

    # 1️⃣ Completeness：每条 engaged_signal 必须有 outcome
    missing_outcome = 0
    for r in engaged_signal_rows:
        if "outcome" not in r or not r.get("outcome"):
            missing_outcome += 1

    if missing_outcome > 0:
        print(f"\n[FAIL] Missing outcome: {missing_outcome} row(s) have engaged_signal but no outcome")
    else:
        print("\n[PASS] Outcome completeness OK (every engaged_signal has outcome)")

    # 2️⃣ Outcome distribution + apply_now（v0 必须全为 false）
    outcome_type_counter = Counter()
    reason_counter = Counter()
    unknown_outcome_type = 0
    unknown_reason = 0
    apply_now_not_false = 0

    for r in outcome_rows:
        o = r.get("outcome") or {}
        otype = o.get("outcome_type") or "UNKNOWN"
        reason = o.get("reason") or "UNKNOWN"
        apply_now = o.get("apply_now", True)  # 缺省视为违规

        if otype not in VALID_OUTCOME_TYPES:
            unknown_outcome_type += 1
        if reason not in VALID_REASONS:
            unknown_reason += 1
        if apply_now is not False:
            apply_now_not_false += 1

        outcome_type_counter[otype] += 1
        reason_counter[reason] += 1

    print("\n--- Outcome type distribution ---")
    for k, v in sorted(outcome_type_counter.items(), key=lambda x: (-x[1], x[0])):
        print(f"  {k:20s}: {v}")

    print("\n--- Reason distribution (BLOCKED / NOT_ATTEMPTED / ACTION_EXECUTED) ---")
    if reason_counter:
        for k, v in sorted(reason_counter.items(), key=lambda x: (-x[1], x[0])):
            print(f"  {k:25s}: {v}")
    else:
        print("  (none)")

    # 3️⃣ Consistency：engaged_signal 条数 ≈ outcome 条数（同条写入应一致）
    consistency_ok = total_engaged_signal == total_outcome and missing_outcome == 0
    if not consistency_ok:
        print(f"\n[WARN] Consistency: engaged_signal={total_engaged_signal}, outcome={total_outcome}, missing={missing_outcome}")
    else:
        print("\n[PASS] Consistency OK (engaged_signal count == outcome count)")

    # 4️⃣ 无结构性异常：无 UNKNOWN、BLOCKED 原因在已定义枚举内
    unknown_outcomes = unknown_outcome_type + unknown_reason
    if unknown_outcomes > 0:
        print(f"\n[WARN] UNKNOWN or invalid: outcome_type={unknown_outcome_type}, reason={unknown_reason}")
    else:
        print("\n[PASS] No UNKNOWN outcome type or reason (frozen enum only)")

    # 4b apply_now 必须全为 false（shadow-only）
    if outcome_rows and apply_now_not_false > 0:
        print(f"\n[FAIL] apply_now must be false for all outcomes (got {apply_now_not_false} not false)")
    elif outcome_rows:
        print("\n[PASS] apply_now all false (shadow-only)")

    # 5️⃣ Final verdict（封板判据：无缺失、无 UNKNOWN、一致、apply_now 全 false）
    print("\n=== Final verdict ===")
    apply_ok = apply_now_not_false == 0
    if missing_outcome == 0 and unknown_outcomes == 0 and consistency_ok and apply_ok:
        print("✅ N layer v0 PASSED — outcome is observable, consistent, and explainable.")
    else:
        print("❌ N layer v0 FAILED — see warnings above.")


if __name__ == "__main__":
    main()
