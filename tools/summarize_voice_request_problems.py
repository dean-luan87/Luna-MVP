#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对已导出的 RequestTraceChain JSON 做问题提炼与优先级排序（无 DB、无 LLM）。

数据流：chain JSON → analyze_request_trace_issue → extract_problem_summary → prioritize_problems。
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

from capabilities.voice.observations.request_trace_chain import RequestTraceChain  # noqa: E402
from capabilities.voice.observations.request_trace_issue_analyzer import analyze_request_trace_issue  # noqa: E402
from capabilities.voice.observations.request_trace_problem_extractor import extract_problem_summary  # noqa: E402
from capabilities.voice.observations.request_trace_problem_prioritizer import prioritize_problems  # noqa: E402
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
    return chains


def main() -> int:
    p = argparse.ArgumentParser(
        description="Build prioritized RequestTraceProblemSummary list from chain JSON files."
    )
    p.add_argument("--input-dir", help="Directory of *.json chain files")
    p.add_argument("--input-file", action="append", dest="input_files", help="Chain JSON (repeatable)")
    p.add_argument("--glob", default="*.json", help="Glob under input-dir")
    p.add_argument("--top-k", dest="top_k", type=int, default=0, help="Only output first K after sort (0=all)")
    p.add_argument("--format", choices=("json", "text"), default="json")
    args = p.parse_args()

    if not args.input_dir and not args.input_files:
        print("Need --input-dir and/or --input-file", file=sys.stderr)
        return 2

    chains = _load_chains(args)
    summaries = []
    for c in chains:
        issue, diag = analyze_request_trace_issue(c)
        summaries.append(extract_problem_summary(c, issue, diag))

    ranked = prioritize_problems(summaries)
    if args.top_k and args.top_k > 0:
        ranked = ranked[: args.top_k]

    if args.format == "json":
        print(json.dumps([x.to_dict() for x in ranked], ensure_ascii=False, indent=2))
    else:
        for x in ranked:
            d = x.to_dict()
            print(
                f"{d['priority_score']}\t{d['alert_level']}\t{d['request_id']}\t"
                f"{d['primary_issue_type']}\t{d['summary_text'][:80]}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
