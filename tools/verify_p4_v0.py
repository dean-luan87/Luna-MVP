# tools/verify_p4_v0.py
"""
P4 v0 自动验收：style 分布 + 不变式（SAFETY 必 ONE_LINER、style 仅三种）。
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

p4_rows = []
for r in rows:
    if not isinstance(r, dict):
        continue
    p4 = r.get("p4") or (r.get("outcome") or {}).get("p4")
    if isinstance(p4, dict):
        p4_rows.append(r)

print("\n=== P4 verification (v0) ===")
print(f"Trace: {TRACE}")
print(f"P4 records: {len(p4_rows)}")
if not p4_rows:
    print("[FAIL] no P4 records found")
    sys.exit(1)


def _p4(r):
    return r.get("p4") or (r.get("outcome") or {}).get("p4") or {}


style_dist = Counter(_p4(r).get("style") for r in p4_rows)
reason_dist = Counter(_p4(r).get("reason") for r in p4_rows)

print("\n--- style distribution ---")
for k, v in style_dist.most_common():
    print(f"  {k}: {v}")

print("\n--- reason distribution ---")
for k, v in reason_dist.most_common():
    print(f"  {k}: {v}")

# v0 不变式：style 仅三种
allowed_styles = {"ONE_LINER", "TWO_STEP", "ASK_CONFIRM"}
bad_unknown = [r for r in p4_rows if _p4(r).get("style") not in allowed_styles]
if bad_unknown:
    print(f"[FAIL] unknown style found: {len(bad_unknown)}")
    sys.exit(1)

# SAFETY 必须 ONE_LINER（从 g 或 arbitration 取 winner_type）
viol_safety = []
for r in p4_rows:
    g = r.get("g") or {}
    wt = g.get("winner_type") or r.get("arbitration", {}).get("winner_type") or "NONE"
    wt = (wt or "NONE").upper() if isinstance(wt, str) else "NONE"
    if wt == "SAFETY" and _p4(r).get("style") != "ONE_LINER":
        viol_safety.append(r)
if viol_safety:
    print(f"[FAIL] SAFETY not ONE_LINER: {len(viol_safety)}")
    sys.exit(1)

print("\n[PASS] P4 is observable, explainable, and invariants hold")
print("=== Final verdict ===")
print("✅ P4 verification PASSED")
