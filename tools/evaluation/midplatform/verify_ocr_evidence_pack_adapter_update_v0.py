#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for OCR Evidence Pack Adapter Update v0."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, List


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


def _is_false(v: Any) -> bool:
    return v is False


def main() -> int:
    _find_ws_root()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []
    checks_passed = 0

    def ok(cond: bool, name: str) -> None:
        nonlocal checks_passed
        if cond:
            checks_passed += 1
        else:
            blockers.append(name)

    paths = {
        "summary": root / "ocr_evidence_pack_adapter_update_summary.json",
        "poster": root / "ocr_evidence_pack_adapter_poster_collection.json",
        "rv": root / "ocr_evidence_pack_adapter_realvideo_collection.json",
        "unified": root / "ocr_evidence_pack_adapter_unified_index.json",
        "field_matrix": root / "ocr_evidence_pack_adapter_field_completeness_matrix.json",
        "coord": root / "ocr_evidence_pack_adapter_coordinate_attachment_report.json",
        "chain": root / "ocr_evidence_pack_adapter_source_chain_preservation_report.json",
        "raw": root / "ocr_evidence_pack_adapter_raw_ocr_preservation_report.json",
        "empty_guard": root / "ocr_evidence_pack_adapter_empty_text_guard_report.json",
        "readability": root / "ocr_evidence_pack_adapter_readability_quality_report.json",
        "sem": root / "ocr_evidence_pack_adapter_semantic_placeholder_report.json",
        "wm": root / "ocr_evidence_pack_adapter_world_model_attach_placeholder_report.json",
        "compliance": root / "ocr_evidence_pack_adapter_contract_compliance_report.json",
        "metrics": root / "ocr_evidence_pack_adapter_metrics_candidate_report.json",
        "benchmark": root / "ocr_evidence_pack_adapter_benchmark_link_report.json",
        "health": root / "ocr_evidence_pack_adapter_system_health_link_report.json",
        "boundary": root / "ocr_evidence_pack_adapter_no_write_boundary_report.json",
        "sim": root / "ocr_evidence_pack_adapter_simulation_context_report.json",
        "non_claims": root / "ocr_evidence_pack_adapter_non_claims_report.json",
        "followups": root / "ocr_evidence_pack_adapter_open_followups.json",
        "audit": root / "ocr_evidence_pack_adapter_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        _write_json(
            root / "ocr_evidence_pack_adapter_verifier_report.json",
            {"verdict": "NO_GO", "blockers": blockers, "checks_passed": 0},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    poster = _read_json(paths["poster"])
    rv = _read_json(paths["rv"])
    unified = _read_json(paths["unified"])
    field_matrix = _read_json(paths["field_matrix"])
    coord = _read_json(paths["coord"])
    chain = _read_json(paths["chain"])
    raw = _read_json(paths["raw"])
    empty_guard = _read_json(paths["empty_guard"])
    readability = _read_json(paths["readability"])
    sem = _read_json(paths["sem"])
    wm = _read_json(paths["wm"])
    compliance = _read_json(paths["compliance"])
    metrics = _read_json(paths["metrics"])
    benchmark = _read_json(paths["benchmark"])
    health = _read_json(paths["health"])
    boundary = _read_json(paths["boundary"])
    sim = _read_json(paths["sim"])
    non_claims = _read_json(paths["non_claims"])
    followups = _read_json(paths["followups"])
    audit = _read_json(paths["audit"])

    ok(summary.get("adapter_scope") == "adapter_update_only", "adapter_scope")
    ok(summary.get("based_on_contract") is True, "based_on_contract")
    ok(summary.get("poster_pack_count") == 4, "poster_pack_count")
    ok(summary.get("realvideo_pack_count") == 10, "realvideo_pack_count")
    ok(summary.get("total_pack_count") == 14, "total_pack_count")
    ok(summary.get("raw_ocr_text_preserved") is True, "raw_ocr_text_preserved")
    ok(summary.get("source_chain_preserved") is True, "source_chain_preserved")
    ok(_is_false(summary.get("semantic_model_invoked")), "summary_semantic_model")
    ok(_is_false(summary.get("world_model_attach_executed")), "summary_wm_attach")

    ok(poster.get("pack_count") == 4, "poster_pack_count_collection")
    poster_packs = poster.get("packs") if isinstance(poster.get("packs"), list) else []
    for p in poster_packs:
        if not isinstance(p, dict):
            blockers.append("poster_pack_invalid")
            break
        es = p.get("evidence_status") if isinstance(p.get("evidence_status"), dict) else {}
        if es.get("fact_status") != "not_fact":
            blockers.append(f"poster_fact_status:{p.get('evidence_id')}")
            break
    else:
        checks_passed += 1

    ok(rv.get("pack_count") == 10, "rv_pack_count")
    rv_packs = rv.get("packs") if isinstance(rv.get("packs"), list) else []
    for p in rv_packs:
        if not isinstance(p, dict):
            blockers.append("rv_pack_invalid")
            break
        ro = p.get("raw_ocr") if isinstance(p.get("raw_ocr"), dict) else {}
        if ro.get("empty_text") is not True:
            blockers.append(f"rv_empty_text:{p.get('evidence_id')}")
            break
    else:
        checks_passed += 1

    ok(unified.get("total_pack_count") == 14, "unified_total")
    ok(unified.get("empty_text_count") == 10, "empty_text_count")
    ok(unified.get("non_empty_text_count") == 4, "non_empty_text_count")

    rows = field_matrix.get("rows") if isinstance(field_matrix.get("rows"), list) else []
    ok(len(rows) == 14, "field_matrix_rows")
    for row in rows:
        if not isinstance(row, dict):
            blockers.append("field_matrix_row_invalid")
            break
        if row.get("missing_required_fields") != []:
            blockers.append(f"missing_fields:{row.get('evidence_id')}")
            break
    else:
        checks_passed += 1

    ok(coord.get("image_coordinate_field_present_count") == 14, "image_coord_present")
    ok(coord.get("temporal_coordinate_field_present_count") == 14, "temporal_coord_present")
    ok(coord.get("spatial_coordinate_field_present_count") == 14, "spatial_coord_present")
    ok(coord.get("coordinate_fabrication_detected") is False, "coord_fabrication")

    ok(chain.get("source_chain_preserved") is True, "source_chain_preserved")
    ok(raw.get("raw_output_mutated") is False, "raw_output_mutated")
    ok(empty_guard.get("empty_text_is_not_no_text_fact") is True, "empty_text_guard")
    ok(readability.get("grade_fabrication_detected") is False, "grade_fabrication")
    ok(sem.get("placeholder_count") == 14, "sem_placeholder_count")
    ok(_is_false(sem.get("semantic_model_invoked")), "sem_model_invoked")
    ok(wm.get("placeholder_count") == 14, "wm_placeholder_count")
    ok(wm.get("world_model_write_allowed") is False, "wm_write_allowed")
    ok(compliance.get("contract_compliance_status") == "pass", "contract_compliance")
    ok(metrics.get("raw_text_preservation_rate") == 1.0, "raw_preservation_rate")
    ok(metrics.get("field_completeness_rate") == 1.0, "field_completeness_rate")
    ok(benchmark.get("benchmark_score_generated") is False, "benchmark_score")
    ok(health.get("provider_health_runtime_checked") is False, "provider_health_runtime")
    ok(boundary.get("boundary_ok") is True, "boundary_ok")
    ok(boundary.get("violations") == [], "boundary_violations")
    ok(sim.get("simulation_profile_id") == "developer_full", "sim_profile")
    ok(non_claims.get("no_semantic_model_execution") is True, "non_claims_semantic")
    ok(non_claims.get("no_real_world_model_attach") is True, "non_claims_wm")
    ok(isinstance(followups.get("items"), list) and len(followups.get("items", [])) >= 8, "followups")
    ok(audit.get("ocr_evidence_pack_adapter_update_executed") is True, "audit_executed")
    ok(_is_false(audit.get("ocr_reinvoked")), "audit_ocr_reinvoked")
    ok(_is_false(audit.get("rapidocr_reinvoked")), "audit_rapidocr")
    ok(_is_false(audit.get("semantic_model_invoked")), "audit_semantic")
    ok(_is_false(audit.get("world_model_attach_executed")), "audit_wm_attach")
    ok(_is_false(audit.get("scene_delta_candidate_generated")), "audit_scene_delta")
    ok(_is_false(audit.get("midplatform_fact_written")), "audit_midplatform")
    ok(_is_false(audit.get("world_model_written")), "audit_world_model")
    ok(_is_false(audit.get("navigation_decision_invoked")), "audit_navigation")
    ok(_is_false(audit.get("runtime_routing_changed")), "audit_routing")

    provider_dist = unified.get("provider_distribution") if isinstance(unified.get("provider_distribution"), dict) else {}
    if "rapidocr_candidate" not in provider_dist:
        blockers.append("provider_distribution_rapidocr")
    else:
        checks_passed += 1

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "schema_version": "ocr_evidence_pack_adapter_verifier_report_v0",
        "verdict": verdict,
        "blockers": blockers,
        "checks_passed": checks_passed,
        "smoke_root": str(root),
    }
    _write_json(root / "ocr_evidence_pack_adapter_verifier_report.json", report)
    print(json.dumps({"verdict": verdict, "blockers": blockers, "checks_passed": checks_passed}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
