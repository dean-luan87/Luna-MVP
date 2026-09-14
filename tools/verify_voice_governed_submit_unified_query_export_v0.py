# -*- coding: utf-8 -*-
"""
Phase-Voice-OutputGovernance-009
Verifier for governed submit unified query/export integration.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Set


GATE_POSITIONS = {"_maybe_submit_real_output_v1_pre", "VoiceOutputPlane.submit_entry"}
ALLOWED_RESULTS = {
    "submit_allowed_shadow",
    "submit_blocked_shadow",
    "submit_expired_shadow",
    "submit_cancelled_shadow",
    "submit_fallback_candidate_shadow",
}


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _non_empty_file(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def _require(cond: bool, msg: str, errors: List[str]) -> None:
    if not cond:
        errors.append(msg)


def verify(input_root: Path, query_output_root: Path, export_output_root: Path) -> Dict[str, Any]:
    errors: List[str] = []
    warnings: List[str] = []

    _require(input_root.exists() and input_root.is_dir(), f"input root not readable: {input_root}", errors)
    _require(query_output_root.exists() and query_output_root.is_dir(), f"query output root not readable: {query_output_root}", errors)
    _require(export_output_root.exists() and export_output_root.is_dir(), f"export output root not readable: {export_output_root}", errors)

    chains_path = input_root / "voice_governed_submit_enhanced_request_chains.json"
    _require(chains_path.exists(), "enhanced chains missing", errors)

    # Query outputs
    q_summary = query_output_root / "voice_governed_submit_unified_query_summary.json"
    q_results_json = query_output_root / "voice_governed_submit_unified_query_results.json"
    q_results_jsonl = query_output_root / "voice_governed_submit_unified_query_results.jsonl"
    q_report = query_output_root / "voice_governed_submit_unified_query_report.md"
    for p in (q_summary, q_results_json, q_results_jsonl, q_report):
        _require(p.exists(), f"missing query output: {p.name}", errors)
    _require(_non_empty_file(q_results_jsonl), "query results jsonl empty", errors)

    # Export outputs
    e_summary = export_output_root / "voice_governed_submit_unified_export_summary.json"
    pos_table_p = export_output_root / "voice_governed_submit_gate_position_table.json"
    res_table_p = export_output_root / "voice_governed_submit_result_table.json"
    ha_table_p = export_output_root / "voice_governed_submit_hard_audit_table.json"
    req_matrix_p = export_output_root / "voice_governed_submit_request_matrix.json"
    mapping_p = export_output_root / "voice_governed_submit_field_mapping_report.json"
    md_p = export_output_root / "voice_governed_submit_unified_export_report.md"
    for p in (e_summary, pos_table_p, res_table_p, ha_table_p, req_matrix_p, mapping_p, md_p):
        _require(p.exists(), f"missing export output: {p.name}", errors)

    if errors:
        return {"verdict": "NO_GO", "errors": errors, "warnings": warnings}

    # Structural checks
    pos_table = _read_json(pos_table_p)
    _require(isinstance(pos_table, list) and len(pos_table) > 0, "gate position table empty", errors)
    seen_pos: Set[str] = set()
    seen_results: Set[str] = set()
    for r in pos_table if isinstance(pos_table, list) else []:
        if not isinstance(r, dict):
            continue
        rp = r.get("submit_gate_position")
        rr = r.get("submit_shadow_result")
        if isinstance(rp, str):
            seen_pos.add(rp)
        if isinstance(rr, str):
            seen_results.add(rr)
        _require(bool(r.get("request_id")), "gate position table missing request_id", errors)
        _require("source_submit_shadow_decision_id" in r, "gate position table missing source_submit_shadow_decision_id", errors)
        _require("source_governance_decision_id" in r, "gate position table missing source_governance_decision_id", errors)

    _require(GATE_POSITIONS.issubset(seen_pos), f"gate position table missing positions: {GATE_POSITIONS - seen_pos}", errors)

    res_table = _read_json(res_table_p)
    _require(isinstance(res_table, list) and len(res_table) > 0, "result table empty", errors)
    for r in res_table if isinstance(res_table, list) else []:
        if not isinstance(r, dict):
            continue
        s = r.get("submit_shadow_result")
        if isinstance(s, str):
            _require(s in ALLOWED_RESULTS, f"unexpected submit_shadow_result: {s}", errors)

    # request matrix checks
    req_matrix = _read_json(req_matrix_p)
    _require(isinstance(req_matrix, list) and len(req_matrix) > 0, "request matrix empty", errors)
    for r in req_matrix if isinstance(req_matrix, list) else []:
        if not isinstance(r, dict):
            continue
        _require(bool(r.get("request_id")), "request matrix missing request_id", errors)
        _require("positions_consistent" in r, "request matrix missing positions_consistent", errors)

    # Hard audit invariants (sample check)
    ha_table = _read_json(ha_table_p)
    _require(isinstance(ha_table, list) and len(ha_table) > 0, "hard audit table empty", errors)
    for r in (ha_table[:50] if isinstance(ha_table, list) else []):
        if not isinstance(r, dict):
            continue
        ha = r.get("hard_audit")
        _require(isinstance(ha, dict), "hard_audit missing/not dict", errors)
        if isinstance(ha, dict):
            _require(ha.get("real_submit_invoked") in (False, None), "real_submit_invoked must be false", errors)
            _require(ha.get("real_tts_invoked") is False, "real_tts_invoked must be false", errors)
            _require(ha.get("playback_invoked") is False, "playback_invoked must be false", errors)
            _require(ha.get("provider_invoked") is False, "provider_invoked must be false", errors)
            _require(ha.get("navigation_action") in (None, ""), "navigation_action must be null", errors)
            _require(ha.get("downstream_invocation_count") in (0, None), "downstream_invocation_count must be 0", errors)

    # Mapping report exists and has required keys
    mapping = _read_json(mapping_p)
    _require(isinstance(mapping, list) and len(mapping) > 0, "field mapping report empty", errors)
    req_keys = {"source_file", "source_field", "unified_field", "mapping_status", "notes"}
    for r in (mapping[:30] if isinstance(mapping, list) else []):
        if not isinstance(r, dict):
            continue
        missing = [k for k in req_keys if k not in r]
        if missing:
            errors.append(f"mapping row missing keys {missing}")

    verdict = "GO" if not errors else "NO_GO"
    return {"verdict": verdict, "errors": errors, "warnings": warnings}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-root", required=True)
    ap.add_argument("--query-output-root", required=True)
    ap.add_argument("--export-output-root", required=True)
    args = ap.parse_args()

    report = verify(Path(args.input_root), Path(args.query_output_root), Path(args.export_output_root))
    out_path = Path(args.export_output_root) / "voice_governed_submit_unified_query_export_verify_report.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if report["verdict"] == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

