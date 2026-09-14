# -*- coding: utf-8 -*-
"""
Phase-CoreCapability-TRW-Unified-004
Verifier: Unified Query / Filter / Export View v0.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Set


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _non_empty_file(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def _require(cond: bool, msg: str, errors: List[str]) -> None:
    if not cond:
        errors.append(msg)


def _capabilities_from_table(table: List[Dict[str, Any]]) -> Set[str]:
    out: Set[str] = set()
    for r in table:
        if isinstance(r, dict) and isinstance(r.get("capability"), str):
            out.add(r["capability"])
    return out


def _check_field_level_mapping_rows(rows: List[Dict[str, Any]], errors: List[str]) -> None:
    required_keys = {"capability", "source_file", "source_field", "unified_field", "stage_name", "mapping_status", "notes"}
    _require(isinstance(rows, list) and len(rows) > 0, "field-level mapping report empty", errors)
    if not isinstance(rows, list):
        return
    for i, r in enumerate(rows[:50]):  # sample check
        if not isinstance(r, dict):
            errors.append(f"field-level mapping row not dict at index {i}")
            continue
        missing = [k for k in required_keys if k not in r]
        if missing:
            errors.append(f"field-level mapping row missing keys {missing} at index {i}")


def _check_query_results_preserve_refs(results: List[Dict[str, Any]], errors: List[str]) -> None:
    for i, r in enumerate(results[:100]):  # sample check
        if not isinstance(r, dict):
            continue
        _require("source_root" in r, f"query result missing source_root at index {i}", errors)
        _require("source_refs" in r, f"query result missing source_refs at index {i}", errors)
        _require("stage_name" in r, f"query result missing original_stage_name(stage_name) at index {i}", errors)
        _require("hard_audit" in r, f"query result missing hard_audit at index {i}", errors)
        _require("missing_fields" in r, f"query result missing missing_fields at index {i}", errors)


def verify(
    *,
    input_root: Path,
    query_output_root: Path,
    export_output_root: Path,
) -> Dict[str, Any]:
    errors: List[str] = []
    warnings: List[str] = []

    _require(input_root.exists() and input_root.is_dir(), f"input root not readable: {input_root}", errors)
    _require(query_output_root.exists() and query_output_root.is_dir(), f"query output root not readable: {query_output_root}", errors)
    _require(export_output_root.exists() and export_output_root.is_dir(), f"export output root not readable: {export_output_root}", errors)

    # Query outputs
    q_summary = query_output_root / "core_capability_unified_query_summary.json"
    q_results_json = query_output_root / "core_capability_unified_query_results.json"
    q_results_jsonl = query_output_root / "core_capability_unified_query_results.jsonl"
    q_report = query_output_root / "core_capability_unified_query_report.md"

    for p in (q_summary, q_results_json, q_results_jsonl, q_report):
        _require(p.exists(), f"missing query output: {p.name}", errors)
    _require(_non_empty_file(q_results_jsonl), "query results jsonl empty", errors)

    # Export outputs
    e_summary = export_output_root / "core_capability_unified_export_summary.json"
    cap_table = export_output_root / "core_capability_unified_capability_table.json"
    stage_table = export_output_root / "core_capability_unified_stage_table.json"
    ha_table = export_output_root / "core_capability_unified_hard_audit_table.json"
    mf_table = export_output_root / "core_capability_unified_missing_fields_table.json"
    map_report = export_output_root / "core_capability_unified_field_level_mapping_report.json"
    e_report = export_output_root / "core_capability_unified_export_report.md"

    for p in (e_summary, cap_table, stage_table, ha_table, mf_table, map_report, e_report):
        _require(p.exists(), f"missing export output: {p.name}", errors)

    # Structural checks
    cap_rows = _read_json(cap_table) if cap_table.exists() else []
    _require(isinstance(cap_rows, list) and len(cap_rows) > 0, "capability table empty", errors)
    caps = _capabilities_from_table(cap_rows) if isinstance(cap_rows, list) else set()
    _require("yolo" in caps, "capability table missing yolo", errors)
    _require("ocr" in caps, "capability table missing ocr", errors)
    _require("voice" in caps, "capability table missing voice", errors)

    st_rows = _read_json(stage_table) if stage_table.exists() else []
    _require(isinstance(st_rows, list) and len(st_rows) > 0, "stage table empty", errors)

    ha_rows = _read_json(ha_table) if ha_table.exists() else []
    _require(isinstance(ha_rows, list) and len(ha_rows) > 0, "hard audit table empty", errors)

    mf_rows = _read_json(mf_table) if mf_table.exists() else []
    _require(isinstance(mf_rows, list) and len(mf_rows) > 0, "missing fields table empty", errors)

    mapping_rows = _read_json(map_report) if map_report.exists() else []
    if isinstance(mapping_rows, list):
        _check_field_level_mapping_rows(mapping_rows, errors)
    else:
        errors.append("field-level mapping report invalid")

    # Query results should preserve refs (sample)
    q_rows = _read_json(q_results_json) if q_results_json.exists() else []
    if isinstance(q_rows, list):
        _check_query_results_preserve_refs(q_rows, errors)
    else:
        errors.append("query results json invalid")

    verdict = "GO" if not errors else "NO_GO"
    return {"verdict": verdict, "errors": errors, "warnings": warnings}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-root", required=True)
    ap.add_argument("--query-output-root", required=True)
    ap.add_argument("--export-output-root", required=True)
    args = ap.parse_args()

    report = verify(
        input_root=Path(args.input_root),
        query_output_root=Path(args.query_output_root),
        export_output_root=Path(args.export_output_root),
    )
    out_path = Path(args.export_output_root) / "core_capability_unified_query_export_verify_report.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if report["verdict"] == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

