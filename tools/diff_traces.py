#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stage 2 首次分叉定位：比较两遍 replay 的 trace，找到第一个 diff 的 ts/seq，输出前后 5 行上下文。

用法:
  python3 tools/diff_traces.py <trace1.jsonl> <trace2.jsonl>
  python3 tools/diff_traces.py <trace1.jsonl> <trace2.jsonl> --keys decision,ts,seq,advice_rhythm,advice_rhythm_record

默认：按行索引逐行比较完整 JSON；--keys 时仅比较指定键（用于决策路径 + advice_rhythm 差异定位）。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _extract(obj: dict, keys: list[str]) -> dict:
    out = {}
    for k in keys:
        if k in obj:
            out[k] = obj[k]
    return out


def _load_lines(path: Path) -> list[dict]:
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                out.append({"_raw": line, "_parse_error": True})
    return out


def _same(a: dict, b: dict, keys: list[str] | None) -> bool:
    if keys is None:
        return a == b
    return _extract(a, keys) == _extract(b, keys)


def main() -> None:
    ap = argparse.ArgumentParser(description="定位两遍 replay trace 的首次分叉")
    ap.add_argument("trace1", type=Path, help="trace 文件 1")
    ap.add_argument("trace2", type=Path, help="trace 文件 2")
    ap.add_argument(
        "--keys",
        type=str,
        default=None,
        help="仅比较这些键（逗号分隔），如: decision,ts,seq,advice_rhythm,advice_rhythm_record",
    )
    ap.add_argument(
        "--context",
        type=int,
        default=5,
        help="前后上下文行数（默认 5）",
    )
    args = ap.parse_args()

    if not args.trace1.exists():
        print(f"文件不存在: {args.trace1}", file=sys.stderr)
        sys.exit(1)
    if not args.trace2.exists():
        print(f"文件不存在: {args.trace2}", file=sys.stderr)
        sys.exit(1)

    lines1 = _load_lines(args.trace1)
    lines2 = _load_lines(args.trace2)
    keys = [k.strip() for k in args.keys.split(",")] if args.keys else None
    ctx = args.context

    n1, n2 = len(lines1), len(lines2)
    n = min(n1, n2)
    if n1 != n2:
        print(f"行数不一致: trace1={n1}, trace2={n2}，比较前 {n} 行", file=sys.stderr)

    first_diff_idx = None
    for i in range(n):
        if not _same(lines1[i], lines2[i], keys):
            first_diff_idx = i
            break

    if first_diff_idx is None:
        if n1 == n2:
            print("两遍 trace 完全一致")
        else:
            print(f"前 {n} 行一致，trace2 多 {n2 - n} 行")
        return

    i = first_diff_idx
    ts1 = lines1[i].get("ts")
    ts2 = lines2[i].get("ts")
    seq1 = lines1[i].get("seq")
    seq2 = lines2[i].get("seq")
    print(f"首次分叉 @ 行索引 {i}")
    if ts1 is not None or ts2 is not None:
        print(f"  ts:  run1={ts1}, run2={ts2}")
    if seq1 is not None or seq2 is not None:
        print(f"  seq: run1={seq1}, run2={seq2}")
    print()
    print("--- trace1 上下文 ---")
    for j in range(max(0, i - ctx), min(n1, i + ctx + 1)):
        prefix = ">>> " if j == i else "    "
        print(f"{prefix}[{j}] {json.dumps(lines1[j], ensure_ascii=False)[:200]}{'...' if len(json.dumps(lines1[j])) > 200 else ''}")
    print()
    print("--- trace2 上下文 ---")
    for j in range(max(0, i - ctx), min(n2, i + ctx + 1)):
        prefix = ">>> " if j == i else "    "
        print(f"{prefix}[{j}] {json.dumps(lines2[j], ensure_ascii=False)[:200]}{'...' if len(json.dumps(lines2[j])) > 200 else ''}")
    sys.exit(1)


if __name__ == "__main__":
    main()
