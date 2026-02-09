# -*- coding: utf-8 -*-
"""
Determinism Guard：测试级护栏。输入完全一致时，验证 decision 序列完全一致。
不读 wall clock / 不依赖 logger 行数 / 不用 pipeline / 不比较浮点。
只认 seq + decision.safety_level + decision.control_mode。
"""
import json
import sys
from typing import Dict, List, Tuple


DECISION_KEYS = ("safety_level", "control_mode")


def load_decisions(trace_path: str) -> Dict[int, Tuple]:
    """
    读取 trace 文件，提取 sampled=True 的 decision，
    返回 { seq: (safety_level, control_mode) }
    """
    decisions = {}

    with open(trace_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue

            # 只认 v1 observation 行
            if "obs" not in obj:
                continue
            if not obj.get("sampled", False):
                continue

            seq = obj.get("seq")
            decision = obj.get("decision", {})

            if seq is None:
                continue

            decisions[seq] = tuple(decision.get(k) for k in DECISION_KEYS)

    return decisions


def diff_decisions(
    a: Dict[int, Tuple], b: Dict[int, Tuple]
) -> List[str]:
    """
    返回差异列表，空列表表示完全一致
    """
    diffs = []

    all_seqs = sorted(set(a.keys()) | set(b.keys()))
    for seq in all_seqs:
        da = a.get(seq)
        db = b.get(seq)

        if da != db:
            diffs.append(
                f"seq={seq}: run1={da}, run2={db}"
            )

    return diffs


def main():
    if len(sys.argv) != 3:
        print("Usage: python determinism_guard.py trace_run1.jsonl trace_run2.jsonl")
        sys.exit(2)

    trace1, trace2 = sys.argv[1], sys.argv[2]

    d1 = load_decisions(trace1)
    d2 = load_decisions(trace2)

    diffs = diff_decisions(d1, d2)

    if diffs:
        print("❌ Determinism violation detected:")
        for d in diffs[:10]:
            print(" ", d)
        if len(diffs) > 10:
            print(f"... ({len(diffs)} diffs total)")
        sys.exit(1)

    print("✅ Determinism check passed.")
    print(f"Compared {len(d1)} sampled decisions.")


if __name__ == "__main__":
    main()
