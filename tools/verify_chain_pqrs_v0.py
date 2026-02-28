#!/usr/bin/env python3
# tools/verify_chain_pqrs_v0.py
# 整链验收：P→Q→R→S 全链路（真实视频 trace 离线分析）

import sys
import json
from collections import Counter

TRACE_PATH = sys.argv[1] if len(sys.argv) > 1 else "logs/a3_trace.jsonl"


def load_trace(path):
    rows = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except Exception:
                    pass
    except FileNotFoundError:
        return None, path
    return rows, path


def main():
    rows, path = load_trace(TRACE_PATH)
    if rows is None:
        print(f"[FAIL] trace not found: {path}")
        sys.exit(1)
    if not rows:
        print(f"[FAIL] trace empty: {path}")
        sys.exit(1)

    # ----------------------------
    # P / Q / R / S 收集器
    # ----------------------------

    p_outcomes = []
    q_records = []
    r_records = []
    s_records = []

    for r in rows:
        if "outcome" in r:
            p_outcomes.append(r["outcome"])
        if "q" in r:
            q_records.append(r["q"])
        if "r" in r:
            r_records.append(r["r"])
        if "s" in r:
            s_records.append(r["s"])

    print("\n=== PQRS Chain Verification (v0) ===\n")

    # ----------------------------
    # P 层验证
    # ----------------------------

    print("[P] Outcome layer")

    if not p_outcomes:
        print("  ❌ FAIL: no outcome records found")
        print("  提示: outcome 仅在 ENGAGED (L1/L2/L3) 时写入。请用以下命令重新跑主流程后再验收:")
        print("    rm -f logs/a3_trace.jsonl")
        print("    python3 main.py --video test_video_complex_6m42s.mp4 --force-engaged-test")
        print("    python3 tools/verify_chain_pqrs_v0.py")
        sys.exit(1)

    p_type_dist = Counter(o.get("outcome_type") for o in p_outcomes)
    p_reason_dist = Counter(o.get("reason") for o in p_outcomes)

    print(f"  outcome_type distribution: {dict(p_type_dist)}")
    print(f"  reason distribution:       {dict(p_reason_dist)}")

    print("  ✅ PASS: P layer observable\n")

    # ----------------------------
    # Q 层验证
    # ----------------------------

    print("[Q] Attribution layer")

    if not q_records:
        print("  ❌ FAIL: no Q attribution records found")
        sys.exit(1)

    # Q v0：ack_state=UNKNOWN 为设计态；校验结构完整（ack_state + meta.reason/executed）
    has_structure = all(
        q.get("ack_state") is not None and isinstance(q.get("meta"), dict)
        for q in q_records
    )
    if not has_structure:
        print("  ❌ FAIL: Q records missing ack_state or meta")
        sys.exit(1)

    ack_dist = Counter(q.get("ack_state") for q in q_records)
    print(f"  total Q records: {len(q_records)}")
    print(f"  ack_state distribution: {dict(ack_dist)} (UNKNOWN valid in v0)")

    print("  ✅ PASS: Q layer attribution complete\n")

    # ----------------------------
    # R 层验证
    # ----------------------------

    print("[R] Rolling statistics layer")

    if not r_records:
        print("  ❌ FAIL: no R records found")
        sys.exit(1)

    blocked_ratios = []
    executed_counts = []

    for rec in r_records:
        snap = rec.get("snapshot", {})
        if "blocked_ratio" in snap:
            blocked_ratios.append(snap["blocked_ratio"])
        if "executed" in snap:
            executed_counts.append(snap["executed"])

    print(f"  R samples: {len(r_records)}")
    if blocked_ratios:
        print(f"  blocked_ratio avg: {sum(blocked_ratios) / len(blocked_ratios):.3f}")
    if executed_counts:
        print(f"  executed avg:      {sum(executed_counts) / len(executed_counts):.3f}")

    print("  ✅ PASS: R layer statistics present\n")

    # ----------------------------
    # S 层验证
    # ----------------------------

    print("[S] Stress observer layer")

    if not s_records:
        print("  ❌ FAIL: no S stress records found")
        sys.exit(1)

    stress_dist = Counter(s.get("stress_level") for s in s_records)
    reason_dist = Counter(s.get("reason") for s in s_records)

    print(f"  stress_level distribution: {dict(stress_dist)}")
    print(f"  reason distribution:       {dict(reason_dist)}")

    print("  ✅ PASS: S layer observable\n")

    # ----------------------------
    # Final verdict
    # ----------------------------

    print("=== FINAL VERDICT ===")
    print("✅ PQRS chain v0 PASSED on real video trace\n")


if __name__ == "__main__":
    main()
