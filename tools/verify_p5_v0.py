# tools/verify_p5_v0.py
"""
P5 v0 自动验收：结构正确性、shadow-only、枚举冻结、无 UNKNOWN。
P5 不改变 outcome_type / apply_now，只写同条 arbitration 的 p5 字段。
"""
import sys
import json
from collections import Counter

TRACE = sys.argv[1] if len(sys.argv) > 1 else "logs/a3_trace.jsonl"

LENGTH_ENUM = {"SHORT", "MEDIUM", "LONG"}
FORM_ENUM = {"STATEMENT", "QUESTION", "SUGGESTION", "WARNING"}
DENSITY_ENUM = {"LOW", "NORMAL", "HIGH"}


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

# 约定：与 m/p4 同条的 arbitration 行（含 outcome 且含 p4 或 arbitration）必须含 p5；J 路径的 engaged_signal 行无 p4 不要求 p5
outcome_rows = [r for r in rows if isinstance(r, dict) and r.get("outcome") is not None]
arb_rows = [r for r in outcome_rows if r.get("p4") is not None or r.get("arbitration") is not None]
p5_rows = [r for r in rows if isinstance(r, dict) and r.get("p5") is not None]

print("\n=== P5 verification (v0) ===")
print(f"Trace: {TRACE}")
print(f"Arbitration rows (outcome + p4/arbitration): {len(arb_rows)}")
print(f"P5 records: {len(p5_rows)}")

if not arb_rows:
    print("[FAIL] no arbitration rows (with p4/arbitration) to attach P5")
    sys.exit(1)

# 100% 含 p5
missing = [r for r in arb_rows if r.get("p5") is None]
if missing:
    print(f"[FAIL] {len(missing)} arbitration row(s) missing p5")
    sys.exit(1)

if not p5_rows:
    print("[FAIL] no P5 records found")
    sys.exit(1)


def _p5(r):
    return r.get("p5") or {}


# 枚举与 shadow_only
bad_shadow = [r for r in p5_rows if _p5(r).get("shadow_only") is not True]
if bad_shadow:
    print(f"[FAIL] shadow_only != true: {len(bad_shadow)}")
    sys.exit(1)

bad_length = [r for r in p5_rows if _p5(r).get("length") not in LENGTH_ENUM]
bad_form = [r for r in p5_rows if _p5(r).get("form") not in FORM_ENUM]
bad_density = [r for r in p5_rows if _p5(r).get("density") not in DENSITY_ENUM]
if bad_length or bad_form or bad_density:
    print(f"[FAIL] enum violation: length={len(bad_length)}, form={len(bad_form)}, density={len(bad_density)}")
    sys.exit(1)

# reason != UNKNOWN
unknown_reasons = [r for r in p5_rows if (str(_p5(r).get("reason", "") or "").upper().startswith("UNKNOWN"))]
if unknown_reasons:
    print(f"[FAIL] UNKNOWN reason present: {len(unknown_reasons)}")
    sys.exit(1)

# 分布输出
length_dist = Counter(_p5(r).get("length") for r in p5_rows)
form_dist = Counter(_p5(r).get("form") for r in p5_rows)
density_dist = Counter(_p5(r).get("density") for r in p5_rows)
reason_dist = Counter(_p5(r).get("reason") for r in p5_rows)

print("\n--- length distribution ---")
for k, v in length_dist.most_common():
    print(f"  {k}: {v}")
print("\n--- form distribution ---")
for k, v in form_dist.most_common():
    print(f"  {k}: {v}")
print("\n--- density distribution ---")
for k, v in density_dist.most_common():
    print(f"  {k}: {v}")
print("\n--- reason distribution (top 10) ---")
for k, v in reason_dist.most_common(10):
    print(f"  {k}: {v}")

print("\n[PASS] P5 v0 structure and invariants hold (shadow-only, enums frozen, no UNKNOWN)")
print("=== Final verdict ===")
print("✅ P5 verification PASSED")
