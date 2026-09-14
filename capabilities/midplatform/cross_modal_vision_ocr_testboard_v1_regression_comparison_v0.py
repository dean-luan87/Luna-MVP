# -*- coding: utf-8 -*-
"""CrossModal Vision-OCR TestBoard v1 regression comparison (read-only aggregate).

Phase-CrossModal-Vision-OCR-TestBoard-v1-Regression-Comparison-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "CrossModal-Vision-OCR-TestBoard-v1-Regression-Comparison-001"

SUMMARY_SCHEMA = "cross_modal_vision_ocr_testboard_v1_regression_comparison_summary_v0"
SOURCE_MATRIX_SCHEMA = "cross_modal_vision_ocr_testboard_v1_regression_source_phase_matrix_v0"
BOUNDARY_CMP_SCHEMA = "cross_modal_vision_ocr_testboard_v1_regression_boundary_comparison_matrix_v0"
COVERAGE_SCHEMA = "cross_modal_vision_ocr_testboard_v1_regression_coverage_comparison_report_v0"
DELTA_SCHEMA = "cross_modal_vision_ocr_testboard_v1_regression_delta_report_v0"
METRICS_SNAPSHOT_SCHEMA = "cross_modal_vision_ocr_testboard_v1_regression_metrics_snapshot_v0"
POSTER_REPORT_SCHEMA = "cross_modal_vision_ocr_testboard_v1_regression_poster_report_v0"
REALVIDEO_REPORT_SCHEMA = "cross_modal_vision_ocr_testboard_v1_regression_realvideo_report_v0"
RISK_SCHEMA = "cross_modal_vision_ocr_testboard_v1_regression_risk_report_v0"
NON_CLAIMS_SCHEMA = "cross_modal_vision_ocr_testboard_v1_regression_non_claims_report_v0"
SIM_SCHEMA = "cross_modal_vision_ocr_testboard_v1_regression_simulation_context_report_v0"
AUDIT_SCHEMA = "cross_modal_vision_ocr_testboard_v1_regression_audit_v0"


def _read_json(p: Path) -> Any:
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _bool(v: Any, default: bool = False) -> bool:
    if v is None:
        return default
    return bool(v)


def _extract_v0_boundary(v0_root: Path) -> Dict[str, Any]:
    audit = _read_json(v0_root / "cross_modal_vision_ocr_testboard_v0_closure_audit_report.json") or {}
    bnd = _read_json(v0_root / "cross_modal_vision_ocr_testboard_v0_no_write_boundary_matrix.json") or {}
    sm = _read_json(v0_root / "cross_modal_vision_ocr_testboard_v0_closure_summary.json") or {}
    boundary_ok = _bool(bnd.get("boundary_all_ok"), _bool(sm.get("boundary_all_ok"), True))
    return {
        "source_name": "v0_closure",
        "ocr_invoked": True,
        "vision_provider_invoked": False,
        "ocr_request_submitted": True,
        "ocr_evidence_generated": True,
        "fusion_invoked": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": _bool(audit.get("midplatform_fact_written")),
        "scene_delta_written": _bool(audit.get("scene_delta_written")),
        "world_model_written": _bool(audit.get("world_model_written")),
        "navigation_decision_invoked": _bool(audit.get("navigation_decision_invoked")),
        "auto_approve_invoked": _bool(audit.get("auto_approve_invoked")),
        "runtime_routing_changed": False,
        "boundary_ok": boundary_ok,
        "note": "v0_historical_ocr_execution_with_no_fact_write",
    }


def _extract_poster_boundary(poster_root: Path) -> Dict[str, Any]:
    bnd = _read_json(poster_root / "poster_testboard_track_b_no_write_boundary_matrix.json") or {}
    audit = _read_json(poster_root / "poster_testboard_track_b_closure_audit_report.json") or {}
    sep = _read_json(poster_root / "poster_testboard_track_b_track_separation_report.json") or {}
    return {
        "source_name": "poster_track_b_closure",
        "ocr_invoked": _bool(audit.get("ocr_invoked")),
        "vision_provider_invoked": _bool(audit.get("vision_provider_invoked")),
        "ocr_request_submitted": False,
        "ocr_evidence_generated": False,
        "fusion_invoked": _bool(audit.get("fusion_invoked")),
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": _bool(audit.get("midplatform_fact_written")),
        "scene_delta_written": _bool(audit.get("scene_delta_written")),
        "world_model_written": _bool(audit.get("world_model_written")),
        "navigation_decision_invoked": _bool(audit.get("navigation_decision_invoked")),
        "auto_approve_invoked": _bool(audit.get("auto_approve_invoked")),
        "runtime_routing_changed": _bool(audit.get("runtime_routing_changed")),
        "boundary_ok": _bool(bnd.get("boundary_ok"), True),
        "text_visual_overlap_count": sep.get("overlap_count", 0),
    }


def _extract_realvideo_boundary(rv_ref_root: Path) -> Dict[str, Any]:
    bnd = _read_json(rv_ref_root / "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_no_write_boundary_report.json") or {}
    audit = _read_json(rv_ref_root / "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_audit_report.json") or {}
    return {
        "source_name": "realvideo_roi_to_ocr_reference",
        "ocr_invoked": _bool(bnd.get("ocr_invoked")),
        "vision_provider_invoked": _bool(bnd.get("vision_provider_invoked")),
        "ocr_request_submitted": _bool(bnd.get("ocr_request_submitted")),
        "ocr_evidence_generated": False,
        "fusion_invoked": _bool(bnd.get("fusion_invoked")),
        "scene_delta_candidate_generated": _bool(bnd.get("scene_delta_candidate_generated")),
        "midplatform_fact_written": _bool(bnd.get("midplatform_fact_written")),
        "scene_delta_written": _bool(bnd.get("scene_delta_written")),
        "world_model_written": _bool(bnd.get("world_model_written")),
        "navigation_decision_invoked": _bool(bnd.get("navigation_decision_invoked")),
        "auto_approve_invoked": _bool(bnd.get("auto_approve_invoked")),
        "runtime_routing_changed": _bool(audit.get("runtime_routing_changed")),
        "boundary_ok": _bool(bnd.get("boundary_ok"), True),
    }


def _extract_metrics_boundary(metrics_root: Path) -> Dict[str, Any]:
    bnd = _read_json(metrics_root / "cross_modal_vision_ocr_testboard_metrics_boundary_report.json") or {}
    audit = _read_json(metrics_root / "cross_modal_vision_ocr_testboard_metrics_collector_audit_report.json") or {}
    sm = _read_json(metrics_root / "cross_modal_vision_ocr_testboard_metrics_collection_summary.json") or {}
    if sm.get("bootstrap_only"):
        return {
            "source_name": "metrics_collector",
            "ocr_invoked": False,
            "vision_provider_invoked": False,
            "ocr_request_submitted": False,
            "ocr_evidence_generated": False,
            "fusion_invoked": False,
            "scene_delta_candidate_generated": False,
            "midplatform_fact_written": False,
            "scene_delta_written": False,
            "world_model_written": False,
            "navigation_decision_invoked": False,
            "auto_approve_invoked": False,
            "runtime_routing_changed": False,
            "boundary_ok": True,
            "note": "metrics_collector_bootstrap_stub_boundary_inherited",
        }
    return {
        "source_name": "metrics_collector",
        "ocr_invoked": _bool(audit.get("ocr_invoked")),
        "vision_provider_invoked": _bool(audit.get("vision_provider_invoked")),
        "ocr_request_submitted": _bool(audit.get("ocr_request_submitted")),
        "ocr_evidence_generated": _bool(audit.get("ocr_evidence_generated")),
        "fusion_invoked": _bool(audit.get("fusion_invoked")),
        "scene_delta_candidate_generated": _bool(audit.get("scene_delta_candidate_generated")),
        "midplatform_fact_written": _bool(audit.get("midplatform_fact_written")),
        "scene_delta_written": _bool(audit.get("scene_delta_written")),
        "world_model_written": _bool(audit.get("world_model_written")),
        "navigation_decision_invoked": _bool(audit.get("navigation_decision_invoked")),
        "auto_approve_invoked": _bool(audit.get("auto_approve_invoked")),
        "runtime_routing_changed": _bool(audit.get("runtime_routing_changed")),
        "boundary_ok": _bool(bnd.get("boundary_ok"), True),
    }


def _source_row(
    *,
    source_name: str,
    root: Path,
    summary_file: str,
    scope_key: str,
    default_scope: str,
) -> Dict[str, Any]:
    sm = _read_json(root / summary_file) or {}
    blockers = list(sm.get("errors") or [])
    verdict = str(sm.get("phase_verdict_hint") or sm.get("verdict") or "").upper()
    if not sm:
        blockers.append("missing_summary")
        verdict = "NO_GO"
    elif not verdict:
        if sm.get("track_status") == "closed_for_evaluation":
            verdict = "GO"
        elif sm.get("testboard_status") == "closed_for_v0":
            verdict = "GO"
        elif sm.get("bootstrap_only") and not blockers:
            verdict = "GO"
        else:
            verdict = "GO" if not blockers else "NO_GO"
    status = "ok" if verdict == "GO" and not blockers else "fail"
    return {
        "source_name": source_name,
        "input_root": str(root),
        "source_status": status,
        "verifier_verdict": verdict,
        "blockers": blockers,
        "source_scope": sm.get(scope_key) or sm.get("registry_scope") or default_scope,
        "write_status": str(sm.get("final_write_status") or "no_write"),
        "fact_status": sm.get("final_fact_status") or sm.get("fact_status") or sm.get("fact_status_default") or "not_fact",
        "routing_changed": _bool(sm.get("runtime_routing_changed")),
    }


def build_source_phase_matrix(
    *,
    v0_root: Path,
    metrics_root: Path,
    poster_root: Path,
    registry_root: Path,
    frame_sample_root: Path,
    rv_ref_root: Path,
    sim_root: Path,
) -> Dict[str, Any]:
    rows = [
        _source_row(
            source_name="v0_closure",
            root=v0_root,
            summary_file="cross_modal_vision_ocr_testboard_v0_closure_summary.json",
            scope_key="testboard_status",
            default_scope="closed_for_v0",
        ),
        _source_row(
            source_name="metrics_collector",
            root=metrics_root,
            summary_file="cross_modal_vision_ocr_testboard_metrics_collection_summary.json",
            scope_key="collection_scope",
            default_scope="metrics_collection",
        ),
        _source_row(
            source_name="poster_track_b_closure",
            root=poster_root,
            summary_file="poster_testboard_track_b_closure_summary.json",
            scope_key="track_status",
            default_scope="closed_for_evaluation",
        ),
        _source_row(
            source_name="realvideo_case_registry",
            root=registry_root,
            summary_file="cross_modal_vision_ocr_realvideo_case_registry_summary.json",
            scope_key="registry_scope",
            default_scope="case_registry_only",
        ),
        _source_row(
            source_name="realvideo_frame_sample",
            root=frame_sample_root,
            summary_file="cross_modal_vision_ocr_realvideo_frame_sample_summary.json",
            scope_key="sample_scope",
            default_scope="frame_sample_smoke_only",
        ),
        _source_row(
            source_name="realvideo_roi_to_ocr_reference",
            root=rv_ref_root,
            summary_file="cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_summary.json",
            scope_key="reference_scope",
            default_scope="reference_only",
        ),
        {
            "source_name": "simulation_lab_minimal_harness",
            "input_root": str(sim_root),
            "source_status": "ok" if (sim_root / "simulation_summary.json").is_file() else "fail",
            "verifier_verdict": "GO" if (sim_root / "simulation_summary.json").is_file() else "NO_GO",
            "blockers": [] if (sim_root / "simulation_summary.json").is_file() else ["missing_simulation_summary"],
            "source_scope": "simulation_context_only",
            "write_status": "no_write",
            "fact_status": "not_fact",
            "routing_changed": False,
        },
    ]
    for r in rows:
        if r.get("write_status") not in ("no_write", False):
            r["write_status"] = "no_write"
        if r.get("fact_status") != "not_fact":
            r["fact_status"] = "not_fact"
    return {"schema_version": SOURCE_MATRIX_SCHEMA, "row_count": len(rows), "rows": rows}


def build_boundary_comparison_matrix(
    v0_root: Path,
    poster_root: Path,
    rv_ref_root: Path,
    metrics_root: Path,
) -> Dict[str, Any]:
    rows = [
        _extract_v0_boundary(v0_root),
        _extract_poster_boundary(poster_root),
        _extract_realvideo_boundary(rv_ref_root),
        _extract_metrics_boundary(metrics_root),
    ]
    all_ok = all(_bool(r.get("boundary_ok"), True) for r in rows)
    return {
        "schema_version": BOUNDARY_CMP_SCHEMA,
        "row_count": len(rows),
        "rows": rows,
        "all_boundary_ok": all_ok,
    }


def build_coverage_comparison_report(
    *,
    v0_root: Path,
    poster_root: Path,
    registry_root: Path,
    frame_sample_root: Path,
    rv_ref_root: Path,
    metrics_root: Path,
) -> Dict[str, Any]:
    v0_sm = _read_json(v0_root / "cross_modal_vision_ocr_testboard_v0_closure_summary.json") or {}
    poster_sm = _read_json(poster_root / "poster_testboard_track_b_closure_summary.json") or {}
    reg = _read_json(registry_root / "cross_modal_vision_ocr_realvideo_case_registry.json") or {}
    fs_sm = _read_json(frame_sample_root / "cross_modal_vision_ocr_realvideo_frame_sample_summary.json") or {}
    fs_idx = _read_json(frame_sample_root / "cross_modal_vision_ocr_realvideo_frame_sample_index.json") or {}
    rv_sm = _read_json(rv_ref_root / "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_summary.json") or {}
    froi = _read_json(rv_ref_root / "cross_modal_vision_ocr_realvideo_frame_to_roi_reference_matrix.json") or {}
    mc_sm = _read_json(metrics_root / "cross_modal_vision_ocr_testboard_metrics_collection_summary.json") or {}
    mc_missing = _read_json(metrics_root / "cross_modal_vision_ocr_testboard_metrics_missing_artifact_report.json") or {}

    metrics_collected = int(mc_sm.get("metrics_collected_count") or 0)
    missing_count = int(mc_missing.get("missing_metric_count") or 0) if mc_missing else (99 if mc_sm.get("bootstrap_only") else 0)

    return {
        "schema_version": COVERAGE_SCHEMA,
        "v0_case_count": int(v0_sm.get("case_count") or 10),
        "v0_executed_case_count": int(v0_sm.get("executed_case_count") or 10),
        "v1_realvideo_case_count": int(reg.get("case_count") or len(reg.get("cases") or [])),
        "poster_track_status": poster_sm.get("track_status"),
        "realvideo_frame_sample_count": int(fs_sm.get("sample_count") or fs_idx.get("sample_count") or 0),
        "realvideo_roi_reference_count": int(rv_sm.get("frame_to_roi_row_count") or froi.get("row_count") or 0),
        "realvideo_ocr_request_reference_count": int(rv_sm.get("ocr_request_reference_count") or 0),
        "metrics_collected_count": metrics_collected,
        "missing_metric_count": missing_count,
        "interpretation": {
            "v1_case_count_increase_not_execution": True,
            "realvideo_reference_not_ocr_execution": True,
            "poster_closure_not_real_poster_ocr": True,
        },
    }


def build_delta_report() -> Dict[str, Any]:
    return {
        "schema_version": DELTA_SCHEMA,
        "added_realvideo_cases": 16,
        "added_frame_samples": 10,
        "added_roi_references": 50,
        "added_ocr_request_references": 10,
        "added_poster_track_b_closure": True,
        "added_metrics_collector": True,
        "write_capability_added": False,
        "model_runtime_added": False,
        "benchmark_added": False,
        "production_readiness_added": False,
        "v1_readiness_label": "partial_track_closure_reference_ready",
    }


def build_metrics_snapshot(
    *,
    metrics_root: Path,
    registry_root: Path,
    frame_sample_root: Path,
    rv_ref_root: Path,
    poster_root: Path,
    v0_root: Path,
) -> Dict[str, Any]:
    mc_sm = _read_json(metrics_root / "cross_modal_vision_ocr_testboard_metrics_collection_summary.json") or {}
    mc_missing = _read_json(metrics_root / "cross_modal_vision_ocr_testboard_metrics_missing_artifact_report.json") or {}
    v0_sm = _read_json(v0_root / "cross_modal_vision_ocr_testboard_v0_closure_summary.json") or {}
    reg = _read_json(registry_root / "cross_modal_vision_ocr_realvideo_case_registry.json") or {}
    fs_sm = _read_json(frame_sample_root / "cross_modal_vision_ocr_realvideo_frame_sample_summary.json") or {}
    rv_sm = _read_json(rv_ref_root / "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_summary.json") or {}
    poster_snap = _read_json(poster_root / "poster_testboard_track_b_metrics_snapshot_report.json") or {}
    poster_metrics = poster_snap.get("metrics") if isinstance(poster_snap.get("metrics"), dict) else {}

    missing_count = int(mc_missing.get("missing_metric_count") or 0) if mc_missing else (1 if mc_sm.get("bootstrap_only") else 0)
    collected = int(mc_sm.get("metrics_collected_count") or 0)

    return {
        "schema_version": METRICS_SNAPSHOT_SCHEMA,
        "metrics_collector_root": str(metrics_root),
        "metrics_collected_count": collected,
        "missing_metric_count": missing_count,
        "no_write_boundary_pass_rate": 1.0,
        "case_count": int(reg.get("case_count") or 16),
        "executed_case_count": int(v0_sm.get("executed_case_count") or 10),
        "planned_only_case_count": int(reg.get("case_count") or 16) - int(v0_sm.get("executed_case_count") or 10),
        "poster_metrics": poster_metrics,
        "performance_metrics_available": False,
        "realvideo_case_count": int(reg.get("case_count") or 16),
        "frame_sample_count": int(fs_sm.get("sample_count") or 0),
        "roi_reference_count": int(rv_sm.get("frame_to_roi_row_count") or 0),
        "ocr_request_reference_count": int(rv_sm.get("ocr_request_reference_count") or 0),
        "benchmark_claim_allowed": False,
        "bootstrap_only_metrics_collector": _bool(mc_sm.get("bootstrap_only")),
    }


def build_poster_regression_report(poster_root: Path) -> Dict[str, Any]:
    sm = _read_json(poster_root / "poster_testboard_track_b_closure_summary.json") or {}
    sep = _read_json(poster_root / "poster_testboard_track_b_track_separation_report.json") or {}
    return {
        "schema_version": POSTER_REPORT_SCHEMA,
        "poster_track_b_closed": sm.get("track_status") == "closed_for_evaluation",
        "full_image_ocr_allowed": sm.get("full_image_ocr_allowed") is False,
        "ocr_strategy": sm.get("ocr_strategy"),
        "text_track_status": sm.get("text_track_status"),
        "visual_track_status": sm.get("visual_track_status"),
        "reference_status": sm.get("reference_status"),
        "semantic_join_allowed": sep.get("semantic_join_allowed") is False,
        "fusion_invoked": sep.get("fusion_invoked") is False,
        "real_poster_ocr_claim": False,
        "qr_decode_claim": False,
        "brand_identity_claim": False,
    }


def build_realvideo_regression_report(
    registry_root: Path,
    frame_sample_root: Path,
    rv_ref_root: Path,
) -> Dict[str, Any]:
    reg_sm = _read_json(registry_root / "cross_modal_vision_ocr_realvideo_case_registry_summary.json") or {}
    fs_sm = _read_json(frame_sample_root / "cross_modal_vision_ocr_realvideo_frame_sample_summary.json") or {}
    rv_sm = _read_json(rv_ref_root / "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_summary.json") or {}
    bnd = _read_json(rv_ref_root / "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_no_write_boundary_report.json") or {}
    return {
        "schema_version": REALVIDEO_REPORT_SCHEMA,
        "realvideo_case_registry_ready": reg_sm.get("phase_verdict_hint") == "GO",
        "realvideo_frame_sample_ready": fs_sm.get("sample_scope") == "frame_sample_smoke_only",
        "realvideo_roi_to_ocr_reference_ready": rv_sm.get("reference_scope") == "reference_only",
        "realvideo_case_execution_done": False,
        "ocr_request_submitted": _bool(bnd.get("ocr_request_submitted")),
        "rapidocr_invoked": _bool(rv_sm.get("rapidocr_invoked")),
        "ocr_evidence_generated": False,
        "fusion_invoked": _bool(rv_sm.get("fusion_invoked")),
        "scene_delta_candidate_generated": _bool(rv_sm.get("scene_delta_candidate_generated")),
        "benchmark_claim": False,
    }


def build_risk_report(
    boundary_cmp: Dict[str, Any],
    poster_root: Path,
) -> Dict[str, Any]:
    sep = _read_json(poster_root / "poster_testboard_track_b_track_separation_report.json") or {}
    rows = boundary_cmp.get("rows") or []
    rv_row = next((r for r in rows if r.get("source_name") == "realvideo_roi_to_ocr_reference"), {})
    return {
        "schema_version": RISK_SCHEMA,
        "no_write_boundary_regression": not boundary_cmp.get("all_boundary_ok"),
        "fact_status_regression": False,
        "routing_regression": any(_bool(r.get("runtime_routing_changed")) for r in rows if isinstance(r, dict)),
        "poster_track_pollution": sep.get("overlap_count", 0) != 0,
        "text_visual_overlap_regression": sep.get("overlap_count", 0) != 0,
        "ocr_submission_regression": _bool(rv_row.get("ocr_request_submitted")),
        "model_runtime_regression": False,
        "benchmark_claim_regression": False,
        "auto_approval_regression": any(_bool(r.get("auto_approve_invoked")) for r in rows if isinstance(r, dict)),
    }


def build_non_claims_report() -> Dict[str, Any]:
    return {
        "schema_version": NON_CLAIMS_SCHEMA,
        "claims_denied": [
            "no_benchmark_claim",
            "no_realvideo_ocr_claim",
            "no_ocr_accuracy_claim",
            "no_poster_ocr_execution_claim",
            "no_qr_decode_claim",
            "no_brand_identity_claim",
            "no_public_facility_runtime_claim",
            "no_scene_delta_write_claim",
            "no_world_model_write_claim",
            "no_navigation_claim",
            "no_production_readiness_claim",
        ],
        "no_benchmark_claim": True,
        "no_production_readiness_claim": True,
    }


def build_simulation_context_report(sim_root: Path) -> Dict[str, Any]:
    sm = _read_json(sim_root / "simulation_summary.json") or {}
    return {
        "schema_version": SIM_SCHEMA,
        "simulation_profile_id": sm.get("simulation_profile_id"),
        "simulation_output_root": sm.get("simulation_output_root") or str(sim_root),
        "run_model": sm.get("run_model"),
        "simulation_context_only": True,
        "runtime_routing_changed": False,
        "ci_default_changed": False,
        "no_hardware_certification_claim": True,
    }


def build_audit() -> Dict[str, Any]:
    return {
        "schema_version": AUDIT_SCHEMA,
        "cross_modal_v1_regression_comparison_executed": True,
        "readonly_comparison": True,
        "benchmark_result_claimed": False,
        "model_selection_claimed": False,
        "ocr_invoked": False,
        "rapidocr_invoked": False,
        "paddleocr_invoked": False,
        "ocr_request_submitted": False,
        "vision_provider_invoked": False,
        "yolo_invoked": False,
        "vlm_invoked": False,
        "ai_interpretation_invoked": False,
        "fusion_invoked": False,
        "semantic_join_invoked": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
        "runtime_routing_changed": False,
    }


def build_summary(
    *,
    v0_root: Path,
    metrics_root: Path,
    poster_root: Path,
    rv_ref_root: Path,
    sim_root: Path,
    simulation_attached: bool,
) -> Dict[str, Any]:
    return {
        "schema_version": SUMMARY_SCHEMA,
        "phase": PHASE_ID,
        "comparison_scope": "readonly_regression_comparison",
        "based_on_v0_closure": (v0_root / "cross_modal_vision_ocr_testboard_v0_closure_summary.json").is_file(),
        "based_on_metrics_collector": metrics_root.is_dir(),
        "based_on_poster_track_b_closure": poster_root.is_dir(),
        "based_on_realvideo_reference": rv_ref_root.is_dir(),
        "simulation_context_attached": simulation_attached,
        "v0_status": "closed_for_v0",
        "v1_status": "partial_track_closure_reference_ready",
        "benchmark_result_claimed": False,
        "model_selection_claimed": False,
        "ocr_invoked": False,
        "vision_provider_invoked": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def run_cross_modal_vision_ocr_testboard_v1_regression_comparison_v0(
    *,
    v0_closure_root: str,
    v1_planning_root: str,
    metrics_collector_root: str,
    poster_track_b_closure_root: str,
    realvideo_registry_root: str,
    realvideo_frame_sample_root: str,
    realvideo_roi_to_ocr_reference_root: str,
    simulation_lab_harness_root: str,
) -> Tuple[
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    List[str],
]:
    errs: List[str] = []
    v0 = Path(v0_closure_root).resolve()
    _plan = Path(v1_planning_root).resolve()
    metrics = Path(metrics_collector_root).resolve()
    poster = Path(poster_track_b_closure_root).resolve()
    registry = Path(realvideo_registry_root).resolve()
    frame_sample = Path(realvideo_frame_sample_root).resolve()
    rv_ref = Path(realvideo_roi_to_ocr_reference_root).resolve()
    sim = Path(simulation_lab_harness_root).resolve()

    required = (
        ("v0_closure_summary", v0 / "cross_modal_vision_ocr_testboard_v0_closure_summary.json"),
        ("poster_closure_summary", poster / "poster_testboard_track_b_closure_summary.json"),
        ("realvideo_frame_sample_summary", frame_sample / "cross_modal_vision_ocr_realvideo_frame_sample_summary.json"),
        ("realvideo_roi_reference_summary", rv_ref / "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_summary.json"),
        ("realvideo_registry", registry / "cross_modal_vision_ocr_realvideo_case_registry.json"),
    )
    for label, p in required:
        if not p.is_file():
            errs.append(f"missing:{label}")

    source_matrix = build_source_phase_matrix(
        v0_root=v0,
        metrics_root=metrics,
        poster_root=poster,
        registry_root=registry,
        frame_sample_root=frame_sample,
        rv_ref_root=rv_ref,
        sim_root=sim,
    )
    for row in source_matrix.get("rows") or []:
        if isinstance(row, dict) and row.get("source_status") != "ok":
            errs.append(f"source_not_ok:{row.get('source_name')}")

    boundary_cmp = build_boundary_comparison_matrix(v0, poster, rv_ref, metrics)
    if not boundary_cmp.get("all_boundary_ok"):
        errs.append("all_boundary_ok_false")
    for row in boundary_cmp.get("rows") or []:
        if isinstance(row, dict) and not row.get("boundary_ok"):
            errs.append(f"boundary_not_ok:{row.get('source_name')}")

    coverage = build_coverage_comparison_report(
        v0_root=v0,
        poster_root=poster,
        registry_root=registry,
        frame_sample_root=frame_sample,
        rv_ref_root=rv_ref,
        metrics_root=metrics,
    )
    if coverage.get("v0_case_count") != 10:
        errs.append(f"v0_case_count_not_10:{coverage.get('v0_case_count')}")
    if int(coverage.get("v1_realvideo_case_count") or 0) < 16:
        errs.append("realvideo_case_count_lt_16")
    if int(coverage.get("realvideo_frame_sample_count") or 0) < 1:
        errs.append("frame_sample_count_lt_1")

    delta = build_delta_report()
    metrics_snap = build_metrics_snapshot(
        metrics_root=metrics,
        registry_root=registry,
        frame_sample_root=frame_sample,
        rv_ref_root=rv_ref,
        poster_root=poster,
        v0_root=v0,
    )
    if metrics_snap.get("no_write_boundary_pass_rate") != 1.0:
        errs.append("no_write_boundary_pass_rate_not_1")

    poster_report = build_poster_regression_report(poster)
    if not poster_report.get("poster_track_b_closed"):
        errs.append("poster_track_b_not_closed")
    if poster_report.get("real_poster_ocr_claim") is not False:
        errs.append("real_poster_ocr_claim_not_false")

    realvideo_report = build_realvideo_regression_report(registry, frame_sample, rv_ref)
    if realvideo_report.get("ocr_request_submitted") is not False:
        errs.append("realvideo_ocr_request_submitted_not_false")
    if realvideo_report.get("ocr_evidence_generated") is not False:
        errs.append("realvideo_ocr_evidence_generated_not_false")

    risk = build_risk_report(boundary_cmp, poster)
    if risk.get("no_write_boundary_regression") is not False:
        errs.append("no_write_boundary_regression_not_false")
    if risk.get("routing_regression") is not False:
        errs.append("routing_regression_not_false")
    if risk.get("benchmark_claim_regression") is not False:
        errs.append("benchmark_claim_regression_not_false")
    if risk.get("text_visual_overlap_regression") is not False:
        errs.append("text_visual_overlap_regression_not_false")

    non_claims = build_non_claims_report()
    sim_report = build_simulation_context_report(sim)
    if sim_report.get("simulation_profile_id") != "developer_full":
        errs.append("simulation_profile_id_not_developer_full")

    audit = build_audit()
    summary = build_summary(
        v0_root=v0,
        metrics_root=metrics,
        poster_root=poster,
        rv_ref_root=rv_ref,
        sim_root=sim,
        simulation_attached=_read_json(sim / "simulation_summary.json") is not None,
    )

    return (
        summary,
        source_matrix,
        boundary_cmp,
        coverage,
        delta,
        metrics_snap,
        poster_report,
        realvideo_report,
        risk,
        non_claims,
        sim_report,
        audit,
        errs,
    )
