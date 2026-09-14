#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v1.1 确定性验证：比较两次运行的 decision 序列是否一致。
只比较 v1 Observation 行（含 seq / decision），按 seq 对齐。
用法: python3 tools/compare_trace_determinism.py logs/a3_trace_run1.jsonl logs/a3_trace_run2.jsonl
"""

import json
import sys
from pathlib import Path


def is_v1_observation(line: dict) -> bool:
    return isinstance(line, dict) and "seq" in line and "decision" in line and "obs" in line


def decision_key(d: dict) -> tuple:
    """可比较的 decision 主键（离散字段，避免浮点噪声）。"""
    if not d:
        return ()
    return (d.get("safety_level"), d.get("control_mode"))


def load_v1_sequence(path: Path) -> list[tuple[int, float, tuple]]:
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not is_v1_observation(row):
                continue
            seq = row.get("seq")
            ts = row.get("ts")
            dec = row.get("decision") or {}
            out.append((seq, ts, decision_key(dec)))
    return out


def main():
    if len(sys.argv) < 3:
        print("用法: python3 compare_trace_determinism.py <trace1.jsonl> <trace2.jsonl>")
        sys.exit(2)
    p1, p2 = Path(sys.argv[1]), Path(sys.argv[2])
    if not p1.exists() or not p2.exists():
        print("文件不存在")
        sys.exit(1)

    s1 = load_v1_sequence(p1)
    s2 = load_v1_sequence(p2)

    if len(s1) != len(s2):
        print(f"seq 数量不一致: run1={len(s1)}, run2={len(s2)}")
        # 仍比到最短长度
        n = min(len(s1), len(s2))
    else:
        n = len(s1)

    for i in range(n):
        seq1, ts1, k1 = s1[i]
        seq2, ts2, k2 = s2[i]
        if seq1 != seq2:
            print(f"不一致 @ 索引 {i}: seq run1={seq1} run2={seq2}")
            sys.exit(1)
        if k1 != k2:
            print(f"不一致 @ seq={seq1} ts≈{ts1:.3f}s: decision 不同")
            print(f"  run1: {k1}")
            print(f"  run2: {k2}")
            sys.exit(1)

    print("两次 decision 序列一致")
    print(f"  v1 行数: {n}")


if __name__ == "__main__":
    main()
