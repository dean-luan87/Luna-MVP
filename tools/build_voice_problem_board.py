#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 RequestTraceChain JSON 构建简洁模式问题区（RequestTraceConciseProblemBoard），输出 JSON。

数据流：chain JSON → analyze_request_trace_issue → extract_problem_summary → build_concise_problem_board。
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
from capabilities.voice.observations.request_trace_concise_problem_board import build_concise_problem_board  # noqa: E402
from capabilities.voice.observations.request_trace_issue_analyzer import analyze_request_trace_issue  # noqa: E402
from capabilities.voice.observations.request_trace_problem_extractor import extract_problem_summary  # noqa: E402
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
    p = argparse.ArgumentParser(description="Build concise mode problem board JSON from chain files.")
    p.add_argument("--input-dir", help="Directory of *.json chain files")
    p.add_argument("--input-file", action="append", dest="input_files", help="Chain JSON (repeatable)")
    p.add_argument("--glob", default="*.json", help="Glob under input-dir")
    p.add_argument("--active-limit", type=int, default=5, help="Max active_problems rows (default 5)")
    args = p.parse_args()

    if not args.input_dir and not args.input_files:
        print("Need --input-dir and/or --input-file", file=sys.stderr)
        return 2

    chains = _load_chains(args)
    summaries = []
    for c in chains:
        issue, diag = analyze_request_trace_issue(c)
        summaries.append(extract_problem_summary(c, issue, diag))

    board = build_concise_problem_board(summaries, active_limit=args.active_limit)
    print(json.dumps(board.to_dict(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
