#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最小本地归档写入器：把抽链 / issue / diagnostic 落到 whitebox_archive。

本脚本不做服务器、不做 UI、不做数据库、不改主链。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from capabilities.voice.observations.request_trace_archive import (  # noqa: E402
    archive_request_trace,
    default_archive_root,
    load_diagnostic_from_dict,
    load_issue_from_dict,
    make_chain_id,
)
from capabilities.voice.observations.request_trace_chain import RequestTraceChain  # noqa: E402
from capabilities.voice.observations.request_trace_query import (  # noqa: E402
    load_chains_from_directory,
)


def _load_json_if_exists(path: Path) -> Optional[Dict[str, Any]]:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def main() -> int:
    p = argparse.ArgumentParser(description="Archive RequestTraceChain into local whitebox_archive.")
    p.add_argument("--input-dir", required=True, help="Directory containing exported RequestTraceChain JSON files.")
    p.add_argument("--glob", default="*.json", help="Glob under input-dir (default: *.json)")

    p.add_argument("--input-issues-dir", help="Optional: issues sidecar dir with matching <chain_id>.json")
    p.add_argument("--input-diagnostics-dir", help="Optional: diagnostics sidecar dir with matching <chain_id>.json")

    p.add_argument("--archive-root", help="Default: ./whitebox_archive")
    p.add_argument("--archive-date", help="YYYY-MM-DD (default: today)")
    args = p.parse_args()

    archive_root = Path(args.archive_root) if args.archive_root else default_archive_root()
    input_dir = Path(args.input_dir)

    if not input_dir.is_dir():
        print(f"input-dir not found: {input_dir}", file=sys.stderr)
        return 2

    issues_dir = Path(args.input_issues_dir) if args.input_issues_dir else None
    diagnostics_dir = Path(args.input_diagnostics_dir) if args.input_diagnostics_dir else None

    chains: List[RequestTraceChain] = load_chains_from_directory(str(input_dir), args.glob)
    if not chains:
        print("No chains loaded. Check --input-dir/--glob.")
        return 3

    written = 0
    for c in chains:
        cid = make_chain_id(c)

        issue = None
        if issues_dir:
            d = _load_json_if_exists(issues_dir / f"{cid}.json")
            if isinstance(d, dict):
                issue = load_issue_from_dict(d)

        diagnostic = None
        if diagnostics_dir:
            d = _load_json_if_exists(diagnostics_dir / f"{cid}.json")
            if isinstance(d, dict):
                diagnostic = load_diagnostic_from_dict(d)

        res = archive_request_trace(
            chain=c,
            issue=issue,
            diagnostic=diagnostic,
            archive_root=archive_root,
            archive_date=args.archive_date,
        )
        written += 1
        # 最小摘要输出（可用来验证写入是否落盘）
        print(
            f"archived {cid} -> {res.chain_path} (tier={res.manifest_path})"
        )

    print(f"OK: wrote {written} chains into {archive_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

