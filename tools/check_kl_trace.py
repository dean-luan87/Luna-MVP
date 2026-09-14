#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 a3_trace.jsonl 中提取含 arbitration 且带 k/l/m 的记录，用于 K/L/M 验收。
用法: python3 tools/check_kl_trace.py [logs/a3_trace.jsonl]
"""

import json
import sys
from pathlib import Path

_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else _root / "logs" / "a3_trace.jsonl"
    path = Path(path)
    if not path.exists():
        print(f"文件不存在: {path}")
        sys.exit(1)

    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    arb = [r for r in rows if "arbitration" in r]
    with_k = [r for r in arb if r.get("k")]
    with_l = [r for r in arb if r.get("l")]
    with_m = [r for r in arb if r.get("m")]
    with_kl = [r for r in arb if r.get("k") and r.get("l")]

    print("=== K/L/M 验收 (a3_trace.jsonl) ===")
    print(f"总行数: {len(rows)}")
    print(f"arbitration 条数: {len(arb)}")
    print(f"含 k: {len(with_k)} | 含 l: {len(with_l)} | 含 m: {len(with_m)} | 同时含 k+l: {len(with_kl)}")
    apply_now_any = sum(1 for r in with_m if r.get("m", {}).get("apply_now") is True)
    if with_m and apply_now_any > 0:
        print(f"  ⚠ M 层 shadow-only 违规: apply_now=true 条数={apply_now_any} (应为 0)")
    elif with_m:
        print("  ✓ M 层 apply_now 全为 false (shadow-only)")
    if not with_kl:
        print("\n未发现同时带 k 与 l 的 arbitration 记录，请确认已进 ENGAGED 且使用 run_active_video_test.py + 高复杂度视频。")
        return

    print("\n--- 最近 5 条 含 k+l 的 arbitration ---")
    for r in with_kl[-5:]:
        ts = r.get("ts", "")
        arb_ = r.get("arbitration", {})
        k_ = r.get("k", {})
        l_ = r.get("l", {})
        m_ = r.get("m", {})
        print(f"  ts={ts}")
        print(f"    arbitration: winner={arb_.get('winner')}, winner_type={arb_.get('winner_type')}")
        print(f"    k: {k_}")
        print(f"    l: {l_}")
        if m_:
            print(f"    m: {m_}")
        print()


if __name__ == "__main__":
    main()
