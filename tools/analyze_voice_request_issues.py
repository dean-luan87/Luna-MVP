#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对已导出的 RequestTraceChain JSON 做链级问题分析与诊断摘要（规则化，无自动修复、无 LLM）。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from capabilities.voice.observations.request_trace_chain import RequestTraceChain  # noqa: E402
from capabilities.voice.observations.request_trace_issue_analyzer import (  # noqa: E402
    analyze_request_trace_issue,
)
from capabilities.voice.observations.request_trace_query import (  # noqa: E402
    load_chains_from_directory,
    load_chains_from_json_files,
)


def _load_chains(args: argparse.Namespace) -> List[RequestTraceChain]:
    chains: List[RequestTraceChain] = []
    if args.input_dir:
        chains.extend(load_chains_from_directory(args.input_dir, args.glob))
    if args.input_files:
        chains.extend(load_chains_from_json_files(args.input_files))
    if args.request_id:
        chains = [c for c in chains if c.request_id == args.request_id]
    return chains


def main() -> int:
    p = argparse.ArgumentParser(description="Analyze voice request trace issues from chain JSON.")
    p.add_argument("--input-dir", help="Directory of chain JSON files")
    p.add_argument("--input-file", action="append", dest="input_files", help="Chain JSON file (repeatable)")
    p.add_argument("--glob", default="*.json")
    p.add_argument("--request-id", dest="request_id", help="Analyze only this request_id")
    p.add_argument("--format", choices=("json", "text"), default="text")
    args = p.parse_args()

    if not args.input_dir and not args.input_files:
        print("Need --input-dir and/or --input-file", file=sys.stderr)
        return 2

    chains = _load_chains(args)
    if not chains:
        print("No chains loaded", file=sys.stderr)
        return 2

    out: List[Dict[str, Any]] = []
    for c in chains:
        issue, diag = analyze_request_trace_issue(c)
        out.append(
            {
                "issue": issue.to_dict(),
                "diagnostic_summary": diag.to_dict(),
            }
        )

    if args.format == "json":
        print(json.dumps(out if len(out) > 1 else out[0], ensure_ascii=False, indent=2))
    else:
        for item in out:
            d = item["diagnostic_summary"]
            print("---")
            print(f"request_id: {d['request_id']}")
            print(f"severity: {d['severity']}")
            print(f"final_status: {d['final_status']}")
            print(f"primary_issue_type: {d['primary_issue_type']}")
            print(f"summary_text: {d['summary_text']}")
            print("checkpoints:")
            for cp in d["recommended_checkpoints"]:
                print(f"  - {cp}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
