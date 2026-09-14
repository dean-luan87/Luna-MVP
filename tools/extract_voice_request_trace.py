#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最小语音请求抽链 CLI：按 request_id / trace_id 从 JSONL/JSON 日志聚合一条 RequestTraceChain。

不改主链；无 UI、无存储。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from capabilities.voice.observations.request_trace_extractor import extract_trace_from_paths


def _default_log_paths() -> List[Path]:
    """仓库内默认探测路径（存在则参与；否则依赖用户 --log）。"""
    logs = ROOT / "logs"
    candidates = [
        logs / "voice_stage22_observations.jsonl",
        logs / "voice_stage22_validation_results.json",
        ROOT / "docs" / "architecture" / "voice" / "fixtures" / "min_trace_samples.jsonl",
    ]
    return [p for p in candidates if p.exists()]


def _print_text(chain) -> None:
    d = chain.to_dict()
    print(f"request_id: {d['request_id']}")
    print(f"trace_id: {d['trace_id']}")
    print(f"chain_type: {d['chain_type']}")
    print(f"final_execution_mode: {d['final_execution_mode']}")
    print(f"provider_name: {d['provider_name']}")
    print(f"status: {d['status']}")
    print("stages:")
    for s in d["stages"]:
        print(f"  - {s['stage_name']}: {s['status']} | {s.get('source_observation_type', '')}")
        if s.get("key_fields"):
            print(f"      {s['key_fields']}")
    if d["errors"]:
        print("errors:")
        for e in d["errors"]:
            print(f"  - {e['stage_name']}: {e['error_type']} | {e['error_reason']}")
    if d["notes"]:
        print("notes:")
        for n in d["notes"]:
            print(f"  - {n}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract one voice request trace from JSONL/JSON logs.")
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--request-id", dest="request_id", help="SpeechRequest / observation request_id")
    g.add_argument("--trace-id", dest="trace_id", help="Optional trace_id (if logged)")
    parser.add_argument(
        "--log",
        dest="logs",
        action="append",
        help="JSONL or JSON file path (repeatable). Default: logs/* + fixtures if present.",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    paths: List[Path]
    if args.logs:
        paths = [Path(p).resolve() for p in args.logs]
    else:
        paths = _default_log_paths()
        if not paths:
            print(
                "No default log files found. Pass --log path/to/file.jsonl",
                file=sys.stderr,
            )
            return 2

    chain = extract_trace_from_paths(
        paths,
        request_id=args.request_id,
        trace_id=args.trace_id,
    )

    if args.format == "json":
        print(json.dumps(chain.to_dict(), ensure_ascii=False, indent=2))
    else:
        _print_text(chain)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
