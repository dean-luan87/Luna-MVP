#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 unified_env_shadow_snapshot envelope JSONL 转为 analyze_unified_env_shadow_v1.py 期望的 flat 行。

输入每行: {"type": "unified_env_shadow_snapshot", "data": {...}}
输出每行: {"id", "event_timestamp", "metadata"}（与 _load_jsonl 契约一致）

不做统计、不改语义；仅重排字段。
"""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from pathlib import Path
from typing import Any, Dict


def _flatten_line(obj: Dict[str, Any], line_no: int) -> Dict[str, Any] | None:
    if obj.get("type") != "unified_env_shadow_snapshot":
        return None
    data = obj.get("data")
    if not isinstance(data, dict):
        return None
    md = data.get("metadata")
    if not isinstance(md, dict):
        return None
    ets = data.get("event_timestamp")
    rid = data.get("related_request_id")
    fid = str(rid).strip() if rid else f"snapshot_line_{line_no}_{uuid.uuid4().hex[:8]}"
    try:
        ts = float(ets) if ets is not None else 0.0
    except (TypeError, ValueError):
        ts = 0.0
    return {"id": fid, "event_timestamp": ts, "metadata": md}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input_jsonl", type=Path, help="snapshot envelope JSONL")
    ap.add_argument("output_jsonl", type=Path, help="flat JSONL for shadow analyzer")
    args = ap.parse_args()

    text = args.input_jsonl.read_text(encoding="utf-8")
    out_lines: list[str] = []
    for i, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"{args.input_jsonl}:{i}: JSON error: {e}", file=sys.stderr)
            return 1
        if not isinstance(obj, dict):
            continue
        flat = _flatten_line(obj, i)
        if flat is None:
            continue
        out_lines.append(json.dumps(flat, ensure_ascii=False))

    args.output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    args.output_jsonl.write_text("\n".join(out_lines) + ("\n" if out_lines else ""), encoding="utf-8")
    print(f"Wrote {len(out_lines)} lines -> {args.output_jsonl}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
