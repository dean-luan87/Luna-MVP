#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对已导出的 RequestTraceChain JSON 做最小结构化查询（无 DB、无全文检索）。

数据流：observation/log → 抽链 → RequestTraceChain JSON → 本脚本查询。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from capabilities.voice.observations.request_trace_query import (  # noqa: E402
    TraceQuery,
    filter_chains,
    filter_summaries,
    load_chains_from_directory,
    load_chains_from_json_files,
    load_chains_from_archive_directory,
)
from capabilities.voice.observations.request_trace_summary import build_request_trace_summary  # noqa: E402


def _bool_arg(s: str) -> bool:
    return s.strip().lower() in ("1", "true", "yes", "y")


def _print_summary_text(summaries: List[Any]) -> None:
    for s in summaries:
        d = s.to_dict()
        line = (
            f"{d['request_id']}\t{d['chain_type']}\t{d.get('provider_name')}\t"
            f"{d.get('final_execution_mode')}\t{d['status']}\t"
            f"{d.get('primary_error_type')}\t"
            f"fb={d['has_fallback']}\trb={d['has_rollback']}"
        )
        print(line)


def main() -> int:
    p = argparse.ArgumentParser(description="Query pre-extracted voice RequestTraceChain JSON files.")
    p.add_argument("--input-dir", help="Directory of *.json chain files (one chain per file)")
    p.add_argument("--input-file", action="append", dest="input_files", help="Chain JSON file (repeatable)")
    p.add_argument("--glob", default="*.json", help="Glob under input-dir (default: *.json)")
    p.add_argument("--archive-dir", dest="archive_dir", help="whitebox_archive/voice/... directory to query")
    p.add_argument("--request-id", dest="request_id")
    p.add_argument("--trace-id", dest="trace_id")
    p.add_argument("--chain-type", dest="chain_type", help="e.g. success, provider_fallback, legacy_rollback, or *_chain")
    p.add_argument("--provider-name", dest="provider_name", help="e.g. piper (current main sample)")
    p.add_argument("--final-execution-mode", dest="final_execution_mode")
    p.add_argument("--status", help="normalized: success|degraded_success|failed|suppressed|unknown or raw ok|failed")
    p.add_argument("--failure-type", dest="failure_type", help="matches primary_error_type / errors (substring)")
    p.add_argument("--has-fallback", dest="has_fallback", choices=("true", "false"))
    p.add_argument("--has-rollback", dest="has_rollback", choices=("true", "false"))
    p.add_argument("--start-after", dest="start_after", type=float)
    p.add_argument("--start-before", dest="start_before", type=float)
    p.add_argument("--mode", choices=("summary", "full"), default="summary")
    p.add_argument("--format", choices=("text", "json"), default="text")
    args = p.parse_args()

    if not args.input_dir and not args.input_files and not args.archive_dir:
        print("Need --input-dir and/or --input-file", file=sys.stderr)
        return 2

    chains = []
    if args.input_dir:
        chains.extend(load_chains_from_directory(args.input_dir, args.glob))
    if args.input_files:
        chains.extend(load_chains_from_json_files(args.input_files))
    if args.archive_dir:
        chains.extend(load_chains_from_archive_directory(args.archive_dir, args.glob))

    q = TraceQuery(
        request_id=args.request_id,
        trace_id=args.trace_id,
        chain_type=args.chain_type,
        provider_name=args.provider_name,
        final_execution_mode=args.final_execution_mode,
        status=args.status,
        failure_type=args.failure_type,
        has_fallback=_bool_arg(args.has_fallback) if args.has_fallback is not None else None,
        has_rollback=_bool_arg(args.has_rollback) if args.has_rollback is not None else None,
        start_after=args.start_after,
        start_before=args.start_before,
    )

    if args.mode == "summary":
        result = filter_summaries(chains, q)
        if args.format == "json":
            print(json.dumps([x.to_dict() for x in result], ensure_ascii=False, indent=2))
        else:
            print("# request_id\tchain_type\tprovider_name\tfinal_execution_mode\tstatus\tprimary_error\tfb\trb")
            _print_summary_text(result)
    else:
        result = filter_chains(chains, q)
        if args.format == "json":
            print(json.dumps([c.to_dict() for c in result], ensure_ascii=False, indent=2))
        else:
            for c in result:
                print(json.dumps(c.to_dict(), ensure_ascii=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
