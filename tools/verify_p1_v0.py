# tools/verify_p1_v0.py
import sys
import json
from collections import Counter

TRACE = sys.argv[1] if len(sys.argv) > 1 else "logs/a3_trace.jsonl"


def load_rows(path):
    rows = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    rows.append(json.loads(line))
                except Exception:
                    pass
    except FileNotFoundError:
        return None, path
    return rows, path


rows, _ = load_rows(TRACE)
if rows is None:
    print(f"[FAIL] trace not found: {TRACE}")
    sys.exit(1)

# 我们约定：P1 outcome 会写在 trace 行的 outcome 字段里（和 PQRS 兼容）
outcomes = [r["outcome"] for r in rows if isinstance(r, dict) and "outcome" in r]

print("\n=== P1 verification (v0) ===")
print(f"Trace: {TRACE}")
print(f"Outcome records: {len(outcomes)}")

if not outcomes:
    print("[FAIL] no outcome records found")
    sys.exit(1)

type_dist = Counter(o.get("outcome_type") for o in outcomes)
reason_dist = Counter(o.get("reason") for o in outcomes)
exec_count = sum(
    1 for o in outcomes
    if o.get("outcome_type") == "ACTION_EXECUTED" and o.get("executed") is True
)

blocked = 0
failed = 0
for o in outcomes:
    rs = (o.get("reason") or "")
    if rs.startswith("BLOCKED"):
        blocked += 1
    if rs.startswith("FAILED"):
        failed += 1

print("\n--- outcome_type distribution ---")
for k, v in type_dist.most_common():
    print(f"  {k}: {v}")

print("\n--- reason distribution (top 15) ---")
for k, v in reason_dist.most_common(15):
    print(f"  {k}: {v}")

print("\n--- summary ---")
print(f"  EXECUTED: {exec_count}")
print(f"  BLOCKED:  {blocked}")
print(f"  FAILED:   {failed}")

# 冻结判据（v0）：必须可观测；若 EXECUTED=0 仍可 PASS（取决于你是否在 force-engaged 场景）
unknown_reasons = [o for o in outcomes if (o.get("reason") or "").startswith("UNKNOWN")]
if unknown_reasons:
    print(f"[FAIL] UNKNOWN reasons present: {len(unknown_reasons)}")
    sys.exit(1)

print("\n[PASS] P1 outcome is observable and explainable (no UNKNOWN)")
print("=== Final verdict ===")
print("✅ P1 verification PASSED")
