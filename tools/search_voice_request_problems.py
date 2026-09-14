#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
问题导向检索：从归档目录或本地 chain JSON 目录加载链，输出 concise 结果（JSON/text）。

无全文检索、无 DB；结构化过滤见 request_trace_search_query。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from capabilities.voice.observations.request_trace_chain import RequestTraceChain  # noqa: E402
from capabilities.voice.observations.request_trace_search_entry import RequestTraceSearchEntry  # noqa: E402
from capabilities.voice.observations.request_trace_search_query import search_chains_to_results  # noqa: E402
from capabilities.voice.observations.request_trace_query import (  # noqa: E402
    load_chains_from_archive_directory,
    load_chains_from_directory,
    load_chains_from_json_files,
)


def _bool_arg(s: str) -> bool:
    return s.strip().lower() in ("1", "true", "yes", "y")


def _load_chains(args: argparse.Namespace) -> List[RequestTraceChain]:
    chains: List[RequestTraceChain] = []
    if args.input_dir:
        chains.extend(load_chains_from_directory(args.input_dir, args.glob))
    if args.input_files:
        chains.extend(load_chains_from_json_files(args.input_files))
    if args.archive_dir:
        chains.extend(load_chains_from_archive_directory(args.archive_dir, args.glob))
    return chains


def _build_entry(args: argparse.Namespace) -> RequestTraceSearchEntry:
    def opt_str(name: str) -> Optional[str]:
        v = getattr(args, name, None)
        if v is None or v == "":
            return None
        return str(v)

    def opt_bool(name: str) -> Optional[bool]:
        if not hasattr(args, name):
            return None
        v = getattr(args, name)
        if v is None:
            return None
        return _bool_arg(v)

    def opt_int(name: str) -> Optional[int]:
        v = getattr(args, name, None)
        if v is None:
            return None
        return int(v)

    return RequestTraceSearchEntry(
        request_id=opt_str("request_id"),
        trace_id=opt_str("trace_id"),
        chain_type=opt_str("chain_type"),
        provider_name=opt_str("provider_name"),
        final_execution_mode=opt_str("final_execution_mode"),
        status=opt_str("status"),
        failure_type=opt_str("failure_type"),
        failure_signature=opt_str("failure_signature"),
        primary_issue_type=opt_str("primary_issue_type"),
        alert_level=opt_str("alert_level"),
        presentation_semantic=opt_str("presentation_semantic"),
        has_fallback=opt_bool("has_fallback"),
        has_rollback=opt_bool("has_rollback"),
        archive_tier=opt_str("archive_tier"),
        start_after=getattr(args, "start_after", None),
        start_before=getattr(args, "start_before", None),
        is_action_required=opt_bool("is_action_required"),
        priority_min=opt_int("priority_min") if getattr(args, "priority_min", None) is not None else None,
        only_main_provider_related=opt_bool("only_main_provider_related"),
        problem_focus=opt_str("problem_focus"),
    )


def main() -> int:
    p = argparse.ArgumentParser(description="Problem-oriented search over RequestTraceChain JSON (concise results).")
    p.add_argument("--input-dir", help="Directory of *.json chain files")
    p.add_argument("--input-file", action="append", dest="input_files", help="Chain JSON (repeatable)")
    p.add_argument("--archive-dir", help="whitebox_archive/voice/... or day dir with chains/")
    p.add_argument("--glob", default="*.json", help="Glob pattern")
    p.add_argument("--request-id", dest="request_id")
    p.add_argument("--trace-id", dest="trace_id")
    p.add_argument("--chain-type", dest="chain_type")
    p.add_argument("--provider-name", dest="provider_name")
    p.add_argument("--final-execution-mode", dest="final_execution_mode")
    p.add_argument("--status")
    p.add_argument("--failure-type", dest="failure_type")
    p.add_argument("--failure-signature", dest="failure_signature")
    p.add_argument("--primary-issue-type", dest="primary_issue_type")
    p.add_argument("--alert-level", dest="alert_level", help="e.g. critical or high_risk|critical")
    p.add_argument("--presentation-semantic", dest="presentation_semantic", help="e.g. danger or warning|danger")
    p.add_argument("--has-fallback", dest="has_fallback", choices=("true", "false"))
    p.add_argument("--has-rollback", dest="has_rollback", choices=("true", "false"))
    p.add_argument("--archive-tier", dest="archive_tier", help="requires manifest map; else no hits")
    p.add_argument("--start-after", dest="start_after", type=float)
    p.add_argument("--start-before", dest="start_before", type=float)
    p.add_argument("--is-action-required", dest="is_action_required", choices=("true", "false"))
    p.add_argument("--priority-min", dest="priority_min", type=int)
    p.add_argument("--only-main-provider-related", dest="only_main_provider_related", choices=("true", "false"))
    p.add_argument(
        "--problem-focus",
        dest="problem_focus",
        help="shortcut: rollback|fallback|high_risk|main_provider|action_required",
    )
    p.add_argument("--format", choices=("json", "text"), default="json")
    args = p.parse_args()

    if not args.input_dir and not args.input_files and not args.archive_dir:
        print("Need --input-dir, --input-file and/or --archive-dir", file=sys.stderr)
        return 2

    chains = _load_chains(args)
    entry = _build_entry(args)
    results = search_chains_to_results(chains, entry)

    if args.format == "json":
        print(json.dumps([r.to_dict() for r in results], ensure_ascii=False, indent=2))
    else:
        for r in results:
            d = r.to_dict()
            print(
                f"{d['request_id']}\t{d.get('provider_name')}\t{d['chain_type']}\t"
                f"{d['alert_level']}\t{d['presentation_semantic']}\t{d['priority_score']}\t"
                f"{d['primary_issue_type']}\t{(d.get('summary_text') or '')[:100]}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
