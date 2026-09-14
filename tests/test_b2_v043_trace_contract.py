#!/usr/bin/env python3
"""
B2 v0.4.3 Trace Contract Test

用途：
- 验证每帧必有 trace
- Gate / NO_OP / READ_ONLY 行为是否符合冻结规则
- 防止未来回退成"只看结果、不看过程"

不依赖 OCR / 真实视觉：
- 只依赖 trace JSONL
- 可用模拟 perception 或已有跑过一次的 trace

使用方式：
  # 1️⃣ 先跑一次 B2（任意方式），生成 trace
  python3 tests/test_b2_v041_gate_behavior_standalone.py

  # 2️⃣ 再跑 trace 合同验收
  python3 tests/test_b2_v043_trace_contract.py \
    --trace traces/b2_trace_v043.jsonl \
    --fps 30

CI 规则：
  - ❌ 有 ERROR → exit 2（直接拦）
  - ⚠️ 只有 WARNING → exit 1（黄）
  - ✅ 全部通过 → exit 0
"""

from __future__ import annotations
import argparse
import json
import sys
from typing import Dict, Any, List

# -------------------------------------------------
# Helpers
# -------------------------------------------------

def die(code: int):
    sys.exit(code)

def load_trace(path: str) -> List[Dict[str, Any]]:
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception as e:
                print(f"❌ JSON parse error @ line {ln}: {e}")
                die(2)
    return rows

def has(d: Dict[str, Any], *keys) -> bool:
    cur = d
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return False
        cur = cur[k]
    return True

# -------------------------------------------------
# Contract Checks
# -------------------------------------------------

ERRORS: List[str] = []
WARNINGS: List[str] = []

def error(msg: str):
    ERRORS.append(msg)

def warn(msg: str):
    WARNINGS.append(msg)

def check_required_fields(r: Dict[str, Any], idx: int):
    """检查必需字段是否存在"""
    # Top-level invariants
    if r.get("schema_version") != "b2.trace.v0.4.3":
        error(f"[{idx}] schema_version missing or incorrect")

    for path in [
        ("time",),
        ("runtime",),
        ("gate",),
        ("factors",),
        ("impact",),
        ("to_c",),
        ("writeback",),
        ("dcs",),
    ]:
        if not has(r, *path):
            error(f"[{idx}] missing field: {'.'.join(path)}")

def check_time_semantics(r: Dict[str, Any], idx: int):
    """检查时间语义"""
    if not has(r, "time", "t_video_s"):
        error(f"[{idx}] missing time.t_video_s")
    if not has(r, "time", "t_str"):
        warn(f"[{idx}] missing time.t_str (human readable)")
    if not has(r, "time", "frame_id"):
        warn(f"[{idx}] missing time.frame_id")

def check_gate_rules(r: Dict[str, Any], idx: int):
    """检查 Gate 规则"""
    gate = r["gate"]
    to_c = r["to_c"]
    writeback = r["writeback"]

    mode = gate.get("mode")

    if mode == "SUSPENDED":
        if to_c.get("send"):
            error(f"[{idx}] gate=SUSPENDED but to_c.send=true")
        for k, v in writeback.items():
            if v:
                error(f"[{idx}] gate=SUSPENDED but writeback.{k}=true")

    if mode == "READ_ONLY":
        for k, v in writeback.items():
            if v:
                error(f"[{idx}] gate=READ_ONLY but writeback.{k}=true")

def check_impact_rules(r: Dict[str, Any], idx: int):
    """检查 Impact 规则"""
    impact = r["impact"]
    to_c = r["to_c"]
    writeback = r["writeback"]

    if impact.get("advisory_only") is not True:
        error(f"[{idx}] advisory_only must be true")

    if impact.get("impact") == "NO_OP":
        if to_c.get("send"):
            error(f"[{idx}] impact=NO_OP but to_c.send=true")
        if writeback.get("timeline"):
            error(f"[{idx}] impact=NO_OP but timeline written")

def check_consistency(r: Dict[str, Any], idx: int):
    """检查一致性（禁止确认性风险语义）"""
    # B must not confirm risk
    forbidden_words = ["确认", "必然", "已经发生", "confirmed"]
    notes = json.dumps(r, ensure_ascii=False)
    for w in forbidden_words:
        if w in notes:
            warn(f"[{idx}] suspicious confirm-like wording: {w}")

# -------------------------------------------------
# Main
# -------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="B2 v0.4.3 Trace Contract Test")
    ap.add_argument("--trace", required=True, help="Path to trace JSONL file")
    ap.add_argument("--fps", type=float, default=30.0, help="FPS (for validation)")
    args = ap.parse_args()

    rows = load_trace(args.trace)
    if not rows:
        error("trace file is empty")

    print("============================================================")
    print("B2 v0.4.3 Trace Contract Test")
    print("============================================================")
    print(f"Trace file: {args.trace}")
    print(f"Frames: {len(rows)}")
    print("------------------------------------------------------------")

    for idx, r in enumerate(rows):
        check_required_fields(r, idx)
        check_time_semantics(r, idx)
        check_gate_rules(r, idx)
        check_impact_rules(r, idx)
        check_consistency(r, idx)

    print("------------------------------------------------------------")
    print(f"Errors: {len(ERRORS)}")
    print(f"Warnings: {len(WARNINGS)}")

    if ERRORS:
        print("\n❌ ERRORS:")
        for e in ERRORS[:20]:
            print("  -", e)
        if len(ERRORS) > 20:
            print(f"  ... and {len(ERRORS) - 20} more errors")
        die(2)

    if WARNINGS:
        print("\n⚠️ WARNINGS:")
        for w in WARNINGS[:20]:
            print("  -", w)
        if len(WARNINGS) > 20:
            print(f"  ... and {len(WARNINGS) - 20} more warnings")
        die(1)

    print("\n✅ Trace contract PASSED")
    die(0)

if __name__ == "__main__":
    main()
