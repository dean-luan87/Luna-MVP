# tools/verify_p2_v0.py
"""
P2 v0 自动验收：P2 仅产出 OK_CONTENT / BLOCKED_LOW_VALUE，无 UNKNOWN。
约定：P2 写在 arbitration 行或 outcome.debug.p2 / outcome.p2
"""
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
        return None
    return rows


rows = load_rows(TRACE)
if rows is None:
    print(f"[FAIL] trace not found: {TRACE}")
    sys.exit(1)

# 约定：P2 outcome 写在 arbitration 行或 outcome.debug.p2
p2_rows = []
for r in rows:
    if not isinstance(r, dict):
        continue
    p2 = None
    if "p2" in r:
        p2 = r["p2"]
    elif "outcome" in r and isinstance(r["outcome"], dict):
        # outcome.p2（main 写入）或 outcome.evidence.p2
        p2 = r["outcome"].get("p2")
        if p2 is None and "evidence" in r["outcome"]:
            ev = r["outcome"]["evidence"]
            if isinstance(ev, dict) and "p2" in ev:
                p2 = ev["p2"].get("p2") if isinstance(ev.get("p2"), dict) else ev["p2"]
    if isinstance(p2, dict):
        p2_rows.append(p2)

print("\n=== P2 verification (v0) ===")
print(f"Trace: {TRACE}")
print(f"P2 records: {len(p2_rows)}")

if not p2_rows:
    print("[FAIL] no P2 records found")
    sys.exit(1)

allow_cnt = sum(1 for p in p2_rows if p.get("allow") is True)
deny_cnt = sum(1 for p in p2_rows if p.get("allow") is False)
# 兼容 allowed 字段
if allow_cnt == 0 and deny_cnt == 0:
    allow_cnt = sum(1 for p in p2_rows if p.get("allowed") is True)
    deny_cnt = sum(1 for p in p2_rows if p.get("allowed") is False)
reason_dist = Counter(p.get("reason") for p in p2_rows)

print("\n--- allow/deny ---")
print(f"  allow: {allow_cnt}")
print(f"  deny:  {deny_cnt}")

print("\n--- reason distribution ---")
for k, v in reason_dist.most_common():
    print(f"  {k}: {v}")

# 冻结判据
unknown = [p for p in p2_rows if (p.get("reason") or "").startswith("UNKNOWN")]
if unknown:
    print(f"[FAIL] UNKNOWN reasons present: {len(unknown)}")
    sys.exit(1)

print("\n[PASS] P2 content gate is observable and explainable")
print("=== Final verdict ===")
print("✅ P2 verification PASSED")
