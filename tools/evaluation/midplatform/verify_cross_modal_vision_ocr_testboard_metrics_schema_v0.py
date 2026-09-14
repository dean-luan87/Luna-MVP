#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for CrossModal Vision OCR TestBoard metrics schema v0."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


REQUIRED_GROUPS = (
    "A_OCR_Output_Metrics",
    "B_Case_Outcome_Metrics",
    "C_Risk_Coverage_Metrics",
    "D_Boundary_Metrics",
    "E_Poster_Layout_Metrics",
    "F_Reference_Fusion_Metrics",
    "G_Performance_Placeholder_Metrics",
)


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
            if str(parent) not in sys.path:
                sys.path.insert(0, str(parent))
            return parent
    return here.parents[3]


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _matrix_row(matrix: Dict[str, Any], metric_name: str) -> Dict[str, Any] | None:
    rows = matrix.get("rows") if isinstance(matrix.get("rows"), list) else []
    for r in rows:
        if isinstance(r, dict) and r.get("metric_name") == metric_name:
            return r
    return None


def main() -> int:
    _find_ws_root()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []

    paths = {
        "summary": root / "cross_modal_vision_ocr_testboard_metrics_schema_summary.json",
        "schema": root / "cross_modal_vision_ocr_testboard_metrics_schema.json",
        "matrix": root / "cross_modal_vision_ocr_testboard_metrics_definition_matrix.json",
        "source_map": root / "cross_modal_vision_ocr_testboard_metrics_source_map.json",
        "gate": root / "cross_modal_vision_ocr_testboard_metrics_gate_policy.json",
        "non_claims": root / "cross_modal_vision_ocr_testboard_metrics_non_claims_report.json",
        "collector": root / "cross_modal_vision_ocr_testboard_metrics_collector_contract_stub.json",
        "audit": root / "cross_modal_vision_ocr_testboard_metrics_schema_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        rep = {
            "schema": "cross_modal_vision_ocr_testboard_metrics_schema_verifier_report_v0",
            "phase": "CrossModal-Vision-OCR-TestBoard-Metrics-Schema-001",
            "smoke_root": str(root),
            "verdict": "NO_GO",
            "blockers": blockers,
        }
        _write_json(root / "cross_modal_vision_ocr_testboard_metrics_schema_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    schema = _read_json(paths["schema"])
    matrix = _read_json(paths["matrix"])
    source_map = _read_json(paths["source_map"])
    gate = _read_json(paths["gate"])
    non_claims = _read_json(paths["non_claims"])
    collector = _read_json(paths["collector"])
    aud = _read_json(paths["audit"])

    if summary.get("metrics_scope") != "schema_only":
        blockers.append("metrics_scope_not_schema_only")
    if summary.get("runtime_execution") is not False:
        blockers.append("runtime_execution_true")

    groups = schema.get("metric_groups") if isinstance(schema.get("metric_groups"), dict) else {}
    for g in REQUIRED_GROUPS:
        if g not in groups:
            blockers.append(f"missing_group:{g}")

    empty_row = _matrix_row(matrix, "ocr_empty_text_count")
    if not empty_row:
        blockers.append("matrix_missing_ocr_empty_text_count")
    elif "case_type_dependent" not in str(empty_row.get("interpretation_rule", "")):
        blockers.append("ocr_empty_text_interpretation")

    nw_row = _matrix_row(matrix, "no_write_boundary_pass_rate")
    if not nw_row:
        blockers.append("matrix_missing_no_write_boundary_pass_rate")
    elif "must_equal_1_for_go" not in str(nw_row.get("interpretation_rule", "")):
        blockers.append("no_write_boundary_interpretation")

    sources = source_map.get("sources") if isinstance(source_map.get("sources"), list) else []
    poster_src = next((s for s in sources if isinstance(s, dict) and s.get("source_id") == "poster_layout_governance"), None)
    if not poster_src:
        blockers.append("source_map_missing_poster")

    if gate.get("benchmark_claim_allowed") is not False:
        blockers.append("benchmark_claim_allowed")
    if gate.get("performance_claim_allowed") is not False:
        blockers.append("performance_claim_allowed")
    if gate.get("model_selection_claim_allowed") is not False:
        blockers.append("model_selection_claim_allowed")

    if not isinstance(non_claims.get("explicit_non_claims"), list) or len(non_claims.get("explicit_non_claims", [])) < 3:
        blockers.append("non_claims_incomplete")

    if collector.get("implementation_status") != "stub_only":
        blockers.append("collector_not_stub")

    if summary.get("ocr_invoked") is not False:
        blockers.append("summary_ocr_invoked")

    audit_checks = (
        ("ocr_invoked", False),
        ("vision_provider_invoked", False),
        ("midplatform_fact_written", False),
        ("scene_delta_written", False),
        ("world_model_written", False),
        ("navigation_decision_invoked", False),
        ("auto_approve_invoked", False),
    )
    for key, expected in audit_checks:
        if aud.get(key) != expected:
            blockers.append(f"audit_{key}")

    verdict = "GO" if not blockers else "NO_GO"
    rep: Dict[str, Any] = {
        "schema": "cross_modal_vision_ocr_testboard_metrics_schema_verifier_report_v0",
        "phase": "CrossModal-Vision-OCR-TestBoard-Metrics-Schema-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
    }
    _write_json(root / "cross_modal_vision_ocr_testboard_metrics_schema_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
