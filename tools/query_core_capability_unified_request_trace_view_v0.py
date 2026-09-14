# -*- coding: utf-8 -*-
"""
Phase-CoreCapability-TRW-Unified-004
Offline query tool for Phase-CoreCapability-TRW-Unified-003 unified shadow view.

Supports filtering by:
- capability (yolo/ocr/voice/all)
- stage_name
- missing_field
- hard_audit_only (anomaly: any forbidden flag not in allowed values)
- request_id

Exports:
- JSON (list)
- JSONL (stage records)
- Markdown report
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _iter_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            if isinstance(obj, dict):
                yield obj


def _write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def _allowed_capability(c: str) -> bool:
    return c in ("yolo", "ocr", "voice", "all")


def _hard_audit_is_anomalous(row: Dict[str, Any]) -> bool:
    ha = row.get("hard_audit")
    if not isinstance(ha, dict):
        return True
    cap = row.get("capability")
    # Common forbidden values
    if ha.get("real_tts_invoked") not in (False, None):
        return True
    if ha.get("navigation_action") not in (None, ""):
        return True
    if ha.get("downstream_invocation_count") not in (0, None):
        return True
    if cap == "yolo":
        if ha.get("runtime_invoked") not in (False, None):
            return True
    if cap == "ocr":
        if ha.get("semantic_interpretation_enabled") not in (False, None):
            return True
        if ha.get("allows_execute_now") not in (False, None):
            return True
    if cap == "voice":
        if ha.get("provider_invoked") not in (False, None):
            return True
        if ha.get("playback_invoked") not in (False, None):
            return True
    return False


def _matches_filters(
    row: Dict[str, Any],
    *,
    capability: str,
    stage_name: Optional[str],
    missing_field: Optional[str],
    request_id: Optional[str],
    hard_audit_only: bool,
) -> bool:
    if capability != "all":
        if row.get("capability") != capability:
            return False
    if stage_name:
        if row.get("stage_name") != stage_name:
            return False
    if request_id:
        if row.get("request_id") != request_id:
            return False
    if missing_field:
        mf = row.get("missing_fields")
        if not (isinstance(mf, list) and missing_field in mf):
            return False
    if hard_audit_only:
        if not _hard_audit_is_anomalous(row):
            return False
    return True


def _load_stage_records(input_root: Path) -> List[Dict[str, Any]]:
    # Primary data: unified trace jsonl contains the unified stage records.
    trace_jsonl = input_root / "core_capability_unified_trace.jsonl"
    if not trace_jsonl.exists():
        raise FileNotFoundError(f"missing unified jsonl: {trace_jsonl}")
    return list(_iter_jsonl(trace_jsonl))


def _mk_out_root(p: Optional[str]) -> Path:
    if p:
        out = Path(p)
    else:
        out = Path("logs") / f"core_capability_unified_query_004_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    if not out.is_absolute():
        out = Path.cwd() / out
    out.mkdir(parents=True, exist_ok=True)
    return out


def _build_md_report(summary: Dict[str, Any], sample: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Core Capability Unified Query Report (v0)")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("```json")
    lines.append(json.dumps(summary, ensure_ascii=False, indent=2))
    lines.append("```")
    lines.append("")
    lines.append("## Sample Results (first 10)")
    lines.append("")
    for i, r in enumerate(sample[:10], start=1):
        lines.append(f"### Result {i}")
        lines.append("")
        # keep compact fields for readability
        compact = {
            "capability": r.get("capability"),
            "request_id": r.get("request_id"),
            "stage_name": r.get("stage_name"),
            "stage_order": r.get("stage_order"),
            "stage_namespace": r.get("stage_namespace"),
            "source_root": r.get("source_root"),
            "hard_audit": r.get("hard_audit"),
            "missing_fields": r.get("missing_fields"),
        }
        lines.append("```json")
        lines.append(json.dumps(compact, ensure_ascii=False, indent=2))
        lines.append("```")
        lines.append("")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-root", required=True)
    ap.add_argument("--capability", default="all")
    ap.add_argument("--stage-name", default=None)
    ap.add_argument("--missing-field", default=None)
    ap.add_argument("--hard-audit-only", action="store_true")
    ap.add_argument("--request-id", default=None)
    ap.add_argument("--export-format", default="json", choices=("json", "jsonl", "md"))
    ap.add_argument("--output-root", default=None)
    args = ap.parse_args()

    if not _allowed_capability(args.capability):
        raise SystemExit(f"invalid --capability: {args.capability}")

    input_root = Path(args.input_root)
    if not input_root.exists() or not input_root.is_dir():
        raise SystemExit(f"input root not readable: {args.input_root}")

    out_root = _mk_out_root(args.output_root)

    rows = _load_stage_records(input_root)
    filtered = [
        r
        for r in rows
        if _matches_filters(
            r,
            capability=args.capability,
            stage_name=args.stage_name,
            missing_field=args.missing_field,
            request_id=args.request_id,
            hard_audit_only=args.hard_audit_only,
        )
    ]

    summary = {
        "phase": "Phase-CoreCapability-TRW-Unified-004",
        "tool": "query_core_capability_unified_request_trace_view_v0.py",
        "input_root": str(input_root),
        "filters": {
            "capability": args.capability,
            "stage_name": args.stage_name,
            "missing_field": args.missing_field,
            "hard_audit_only": bool(args.hard_audit_only),
            "request_id": args.request_id,
        },
        "counts": {"total_stage_records": len(rows), "matched_stage_records": len(filtered)},
        "notes": [
            "offline/shadow query only",
            "does not claim cross-capability linkage",
        ],
    }

    _write_json(out_root / "core_capability_unified_query_summary.json", summary)
    _write_json(out_root / "core_capability_unified_query_results.json", filtered)
    _write_jsonl(out_root / "core_capability_unified_query_results.jsonl", filtered)
    (out_root / "core_capability_unified_query_report.md").write_text(
        _build_md_report(summary, filtered), encoding="utf-8"
    )

    # Also print output root for convenience.
    print(str(out_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

