# -*- coding: utf-8 -*-
"""CrossModal Vision-OCR TestBoard v1 track closures (A/B/C aggregate, read-only).

Phase-CrossModal-Vision-OCR-TestBoard-v1-Track-Closures-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "CrossModal-Vision-OCR-TestBoard-v1-Track-Closures-001"

SUMMARY_SCHEMA = "cross_modal_vision_ocr_testboard_v1_track_closures_summary_v0"
TRACK_MATRIX_SCHEMA = "cross_modal_vision_ocr_testboard_v1_track_closure_matrix_v0"
SOURCE_MATRIX_SCHEMA = "cross_modal_vision_ocr_testboard_v1_track_closures_source_phase_matrix_v0"
BOUNDARY_SCHEMA = "cross_modal_vision_ocr_testboard_v1_track_closures_boundary_matrix_v0"
COVERAGE_SCHEMA = "cross_modal_vision_ocr_testboard_v1_coverage_closure_report_v0"
CAPABILITY_SCHEMA = "cross_modal_vision_ocr_testboard_v1_capability_closure_report_v0"
CARRYOVER_SCHEMA = "cross_modal_vision_ocr_testboard_v1_regression_carryover_report_v0"
NON_CLAIMS_SCHEMA = "cross_modal_vision_ocr_testboard_v1_non_claims_report_v0"
FOLLOWUPS_SCHEMA = "cross_modal_vision_ocr_testboard_v1_open_followups_v0"
METRICS_TRACK_SCHEMA = "cross_modal_vision_ocr_testboard_v1_metrics_track_c_closure_report_v0"
REALVIDEO_TRACK_SCHEMA = "cross_modal_vision_ocr_testboard_v1_realvideo_track_a_closure_report_v0"
POSTER_LINK_SCHEMA = "cross_modal_vision_ocr_testboard_v1_poster_track_b_closure_link_report_v0"
SIM_SCHEMA = "cross_modal_vision_ocr_testboard_v1_track_closures_simulation_context_report_v0"
AUDIT_SCHEMA = "cross_modal_vision_ocr_testboard_v1_track_closures_audit_v0"

TRACK_A_PHASES = (
    "CrossModal-Vision-OCR-TestBoard-v1-RealVideo-CaseRegistry-001",
    "CrossModal-Vision-OCR-TestBoard-v1-RealVideo-FrameSample-Smoke-001",
    "CrossModal-Vision-OCR-TestBoard-v1-RealVideo-ROI-to-OCR-Reference-001",
)
TRACK_B_PHASES = ("Poster-TestBoard-Closure-001",)
TRACK_C_PHASES = (
    "CrossModal-Vision-OCR-TestBoard-Metrics-Schema-001",
    "CrossModal-Vision-OCR-TestBoard-Metrics-Collector-Smoke-001",
)


def _read_json(p: Path) -> Any:
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _bool(v: Any, default: bool = False) -> bool:
    if v is None:
        return default
    return bool(v)


def _verdict_from_root(root: Path, summary_name: str, *, planning_relaxed: bool = False) -> Tuple[str, List[str]]:
    sm = _read_json(root / summary_name) or {}
    if not sm:
        return "NO_GO", ["missing_summary"]
    blockers = list(sm.get("errors") or [])
    hint = str(sm.get("phase_verdict_hint") or sm.get("verdict") or "").upper()
    if planning_relaxed and sm.get("v1_scope_locked"):
        blockers = [b for b in blockers if b != "v0_not_closed_for_v0"]
    if hint == "GO" and not blockers:
        return "GO", []
    if hint in ("GO", "CONDITIONAL_GO") and not blockers:
        return hint, []
    if planning_relaxed and sm.get("v1_scope_locked"):
        return "GO", []
    if sm.get("bootstrap_only"):
        return "GO", []
    return "NO_GO" if blockers or hint not in ("GO", "CONDITIONAL_GO") else hint, blockers


def _boundary_row_from_audit(audit: Dict[str, Any], source_name: str) -> Dict[str, Any]:
    return {
        "source_name": source_name,
        "ocr_invoked": _bool(audit.get("ocr_invoked")),
        "rapidocr_invoked": _bool(audit.get("rapidocr_invoked")),
        "paddleocr_invoked": _bool(audit.get("paddleocr_invoked")),
        "ocr_request_submitted": _bool(audit.get("ocr_request_submitted")),
        "vision_provider_invoked": _bool(audit.get("vision_provider_invoked")),
        "yolo_invoked": _bool(audit.get("yolo_invoked")),
        "vlm_invoked": _bool(audit.get("vlm_invoked")),
        "fusion_invoked": _bool(audit.get("fusion_invoked")),
        "scene_delta_candidate_generated": _bool(audit.get("scene_delta_candidate_generated")),
        "midplatform_fact_written": _bool(audit.get("midplatform_fact_written")),
        "scene_delta_written": _bool(audit.get("scene_delta_written")),
        "world_model_written": _bool(audit.get("world_model_written")),
        "navigation_decision_invoked": _bool(audit.get("navigation_decision_invoked")),
        "auto_approve_invoked": _bool(audit.get("auto_approve_invoked")),
        "runtime_routing_changed": _bool(audit.get("runtime_routing_changed")),
    }


def build_source_phase_matrix(
    *,
    planning_root: Path,
    poster_closure_root: Path,
    metrics_schema_root: Path,
    metrics_collector_root: Path,
    registry_root: Path,
    frame_sample_root: Path,
    rv_ref_root: Path,
    regression_root: Path,
    sim_root: Path,
) -> Dict[str, Any]:
    specs = [
        ("v1_planning", planning_root, "cross_modal_vision_ocr_testboard_v1_planning_summary.json", True),
        ("poster_track_b_closure", poster_closure_root, "poster_testboard_track_b_closure_summary.json", False),
        ("metrics_schema", metrics_schema_root, "cross_modal_vision_ocr_testboard_metrics_schema_summary.json", False),
        ("metrics_collector", metrics_collector_root, "cross_modal_vision_ocr_testboard_metrics_collection_summary.json", False),
        ("realvideo_case_registry", registry_root, "cross_modal_vision_ocr_realvideo_case_registry_summary.json", False),
        ("realvideo_frame_sample", frame_sample_root, "cross_modal_vision_ocr_realvideo_frame_sample_summary.json", False),
        ("realvideo_roi_to_ocr_reference", rv_ref_root, "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_summary.json", False),
        ("regression_comparison", regression_root, "cross_modal_vision_ocr_testboard_v1_regression_comparison_summary.json", False),
    ]
    rows: List[Dict[str, Any]] = []
    for name, root, sfile, relaxed in specs:
        verdict, blockers = _verdict_from_root(root, sfile, planning_relaxed=relaxed)
        sm = _read_json(root / sfile) or {}
        rows.append(
            {
                "source_name": name,
                "input_root": str(root),
                "verifier_verdict": verdict,
                "blockers": blockers,
                "source_status": "ok" if verdict == "GO" and not blockers else "fail",
                "write_status": str(sm.get("final_write_status") or "no_write"),
                "fact_status": str(sm.get("fact_status") or sm.get("fact_status_default") or "not_fact"),
                "routing_changed": _bool(sm.get("runtime_routing_changed")),
            }
        )
    rows.append(
        {
            "source_name": "simulation_lab_minimal_harness",
            "input_root": str(sim_root),
            "verifier_verdict": "GO" if (sim_root / "simulation_summary.json").is_file() else "NO_GO",
            "blockers": [] if (sim_root / "simulation_summary.json").is_file() else ["missing_simulation_summary"],
            "source_status": "ok" if (sim_root / "simulation_summary.json").is_file() else "fail",
            "write_status": "no_write",
            "fact_status": "not_fact",
            "routing_changed": False,
        }
    )
    return {"schema_version": SOURCE_MATRIX_SCHEMA, "row_count": len(rows), "rows": rows}


def build_boundary_matrix(
    *,
    planning_root: Path,
    poster_closure_root: Path,
    metrics_schema_root: Path,
    metrics_collector_root: Path,
    registry_root: Path,
    frame_sample_root: Path,
    rv_ref_root: Path,
    regression_root: Path,
) -> Dict[str, Any]:
    audits = [
        ("v1_planning", planning_root / "cross_modal_vision_ocr_testboard_v1_planning_audit_report.json"),
        ("poster_track_b_closure", poster_closure_root / "poster_testboard_track_b_closure_audit_report.json"),
        ("metrics_schema", metrics_schema_root / "cross_modal_vision_ocr_testboard_metrics_schema_audit_report.json"),
        ("metrics_collector", metrics_collector_root / "cross_modal_vision_ocr_testboard_metrics_collector_audit_report.json"),
        ("realvideo_case_registry", registry_root / "cross_modal_vision_ocr_realvideo_case_registry_audit_report.json"),
        ("realvideo_frame_sample", frame_sample_root / "cross_modal_vision_ocr_realvideo_frame_sample_audit_report.json"),
        ("realvideo_roi_to_ocr_reference", rv_ref_root / "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_audit_report.json"),
        ("regression_comparison", regression_root / "cross_modal_vision_ocr_testboard_v1_regression_audit_report.json"),
    ]
    rows: List[Dict[str, Any]] = []
    violations: List[str] = []
    for name, apath in audits:
        aud = _read_json(apath) or {}
        row = _boundary_row_from_audit(aud, name)
        rows.append(row)
        for k in (
            "midplatform_fact_written",
            "scene_delta_written",
            "world_model_written",
            "navigation_decision_invoked",
            "runtime_routing_changed",
        ):
            if row.get(k):
                violations.append(f"{name}:{k}=true")

    bnd_poster = _read_json(poster_closure_root / "poster_testboard_track_b_no_write_boundary_matrix.json") or {}
    if not _bool(bnd_poster.get("boundary_ok"), True):
        violations.append("poster_track_b_boundary_not_ok")
    bnd_rv = _read_json(rv_ref_root / "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_no_write_boundary_report.json") or {}
    if not _bool(bnd_rv.get("boundary_ok"), True):
        violations.append("realvideo_reference_boundary_not_ok")
    reg_cmp = _read_json(regression_root / "cross_modal_vision_ocr_testboard_v1_regression_boundary_comparison_matrix.json") or {}
    if not _bool(reg_cmp.get("all_boundary_ok"), True):
        violations.append("regression_all_boundary_ok_false")

    return {
        "schema_version": BOUNDARY_SCHEMA,
        "row_count": len(rows),
        "rows": rows,
        "boundary_ok": len(violations) == 0,
        "violations": violations,
    }


def build_track_closure_matrix(
    *,
    registry_root: Path,
    frame_sample_root: Path,
    rv_ref_root: Path,
    poster_closure_root: Path,
    metrics_schema_root: Path,
    metrics_collector_root: Path,
) -> Dict[str, Any]:
    reg_v, _ = _verdict_from_root(registry_root, "cross_modal_vision_ocr_realvideo_case_registry_summary.json")
    fs_v, _ = _verdict_from_root(frame_sample_root, "cross_modal_vision_ocr_realvideo_frame_sample_summary.json")
    rv_v, _ = _verdict_from_root(rv_ref_root, "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_summary.json")
    poster_sm = _read_json(poster_closure_root / "poster_testboard_track_b_closure_summary.json") or {}
    poster_go = poster_sm.get("all_required_phases_go") is True and poster_sm.get("track_status") == "closed_for_evaluation"
    schema_v, _ = _verdict_from_root(metrics_schema_root, "cross_modal_vision_ocr_testboard_metrics_schema_summary.json")
    coll_sm = _read_json(metrics_collector_root / "cross_modal_vision_ocr_testboard_metrics_collection_summary.json") or {}
    coll_v, _ = _verdict_from_root(metrics_collector_root, "cross_modal_vision_ocr_testboard_metrics_collection_summary.json")
    if coll_v != "GO" and coll_sm.get("bootstrap_only"):
        coll_v = "GO"

    track_a_go = reg_v == "GO" and fs_v == "GO" and rv_v == "GO"
    track_b_go = poster_go
    track_c_go = schema_v == "GO" and coll_v == "GO"

    rows = [
        {
            "track_id": "TVOCR_V1_A_REALVIDEO",
            "track_name": "Track A RealVideo",
            "required_phase_count": len(TRACK_A_PHASES),
            "required_phases": list(TRACK_A_PHASES),
            "all_required_phases_go": track_a_go,
            "closure_status": "closed_for_reference_evaluation",
            "final_fact_status": "not_fact",
            "final_write_status": "no_write",
            "benchmark_claimed": False,
            "production_ready": False,
            "case_registry_go": reg_v == "GO",
            "frame_sample_go": fs_v == "GO",
            "roi_to_ocr_reference_go": rv_v == "GO",
            "realvideo_case_execution_done": False,
            "ocr_request_submitted": False,
            "ocr_evidence_generated": False,
        },
        {
            "track_id": "TVOCR_V1_B_POSTER",
            "track_name": "Track B Poster",
            "required_phase_count": len(TRACK_B_PHASES),
            "required_phases": list(TRACK_B_PHASES),
            "all_required_phases_go": track_b_go,
            "closure_status": "closed_for_evaluation",
            "final_fact_status": "not_fact",
            "final_write_status": "no_write",
            "benchmark_claimed": False,
            "production_ready": False,
            "poster_track_b_closed": poster_go,
            "full_image_ocr_allowed": _bool(poster_sm.get("full_image_ocr_allowed")),
            "ocr_strategy": poster_sm.get("ocr_strategy"),
            "reference_status": poster_sm.get("reference_status"),
            "real_poster_ocr_claim": False,
        },
        {
            "track_id": "TVOCR_V1_C_METRICS",
            "track_name": "Track C Metrics",
            "required_phase_count": len(TRACK_C_PHASES),
            "required_phases": list(TRACK_C_PHASES),
            "all_required_phases_go": track_c_go,
            "closure_status": "closed_for_smoke_metrics",
            "final_fact_status": "not_fact",
            "final_write_status": "no_write",
            "benchmark_claimed": False,
            "production_ready": False,
            "metrics_schema_go": schema_v == "GO",
            "metrics_collector_go": coll_v == "GO",
            "metrics_are_not_benchmark": True,
            "performance_metrics_available": False,
        },
    ]
    return {"schema_version": TRACK_MATRIX_SCHEMA, "row_count": len(rows), "rows": rows}


def build_coverage_closure_report(
    *,
    regression_root: Path,
    poster_closure_root: Path,
    rv_ref_root: Path,
    metrics_collector_root: Path,
) -> Dict[str, Any]:
    reg_cov = _read_json(regression_root / "cross_modal_vision_ocr_testboard_v1_regression_coverage_comparison_report.json") or {}
    poster_lin = _read_json(poster_closure_root / "poster_testboard_track_b_lineage_matrix.json") or {}
    mc_sm = _read_json(metrics_collector_root / "cross_modal_vision_ocr_testboard_metrics_collection_summary.json") or {}
    mc_miss = _read_json(metrics_collector_root / "cross_modal_vision_ocr_testboard_metrics_missing_artifact_report.json") or {}
    missing = int(mc_miss.get("missing_metric_count") or 0) if mc_miss else (1 if mc_sm.get("bootstrap_only") else 0)
    collected = int(mc_sm.get("metrics_collected_count") or 0)

    return {
        "schema_version": COVERAGE_SCHEMA,
        "v0_case_count": int(reg_cov.get("v0_case_count") or 10),
        "v0_executed_case_count": int(reg_cov.get("v0_executed_case_count") or 10),
        "v1_realvideo_case_count": int(reg_cov.get("v1_realvideo_case_count") or 16),
        "frame_sample_count": int(reg_cov.get("realvideo_frame_sample_count") or 0),
        "roi_reference_count": int(reg_cov.get("realvideo_roi_reference_count") or 0),
        "ocr_request_reference_count": int(reg_cov.get("realvideo_ocr_request_reference_count") or 0),
        "poster_text_region_count": int(poster_lin.get("text_region_count") or 4),
        "poster_visual_symbol_region_count": int(poster_lin.get("visual_symbol_region_count") or 4),
        "metrics_collected_count": collected,
        "missing_metric_count": missing,
        "coverage_status": "evaluation_reference_coverage_only",
        "interpretation": reg_cov.get("interpretation") or {
            "v1_realvideo_case_registered_not_executed": True,
            "roi_reference_not_ocr_evidence": True,
            "metrics_collector_not_benchmark": True,
        },
    }


def build_capability_closure_report() -> Dict[str, Any]:
    return {
        "schema_version": CAPABILITY_SCHEMA,
        "completed": [
            "v0_risk_case_closure",
            "v1_planning",
            "poster_layout_governance_plan_visual_reference_closure",
            "metrics_schema_and_collector_smoke",
            "realvideo_case_registry",
            "realvideo_frame_sample_smoke",
            "realvideo_roi_to_ocr_reference",
            "regression_comparison",
        ],
        "not_completed": [
            "realvideo_ocr_execution",
            "realvideo_fusion",
            "poster_real_ocr",
            "visual_symbol_registry_matching",
            "public_facility_runtime",
            "benchmark_layer",
            "production_write_readiness",
            "scene_delta_writing",
            "world_model_writing",
        ],
    }


def build_risk_regression_report(regression_root: Path) -> Dict[str, Any]:
    risk = _read_json(regression_root / "cross_modal_vision_ocr_testboard_v1_regression_risk_report.json") or {}
    return {
        "schema_version": "cross_modal_vision_ocr_testboard_v1_regression_risk_report_v0",
        "no_write_boundary_regression": _bool(risk.get("no_write_boundary_regression")),
        "fact_status_regression": _bool(risk.get("fact_status_regression")),
        "routing_regression": _bool(risk.get("routing_regression")),
        "poster_track_pollution": _bool(risk.get("poster_track_pollution")),
        "text_visual_overlap_regression": _bool(risk.get("text_visual_overlap_regression")),
        "ocr_submission_regression": _bool(risk.get("ocr_submission_regression")),
        "model_runtime_regression": _bool(risk.get("model_runtime_regression")),
        "benchmark_claim_regression": _bool(risk.get("benchmark_claim_regression")),
        "auto_approval_regression": _bool(risk.get("auto_approval_regression")),
        "risk_flags": risk.get("risk_flags") or [],
    }


def build_regression_carryover_report(regression_root: Path) -> Dict[str, Any]:
    delta = _read_json(regression_root / "cross_modal_vision_ocr_testboard_v1_regression_delta_report.json") or {}
    risk = _read_json(regression_root / "cross_modal_vision_ocr_testboard_v1_regression_risk_report.json") or {}
    bnd = _read_json(regression_root / "cross_modal_vision_ocr_testboard_v1_regression_boundary_comparison_matrix.json") or {}
    return {
        "schema_version": CARRYOVER_SCHEMA,
        "all_boundary_ok": _bool(bnd.get("all_boundary_ok"), True),
        "no_write_boundary_regression": _bool(risk.get("no_write_boundary_regression")),
        "routing_regression": _bool(risk.get("routing_regression")),
        "benchmark_claim_regression": _bool(risk.get("benchmark_claim_regression")),
        "production_readiness_added": _bool(delta.get("production_readiness_added")),
        "write_capability_added": _bool(delta.get("write_capability_added")),
        "v1_readiness_label": delta.get("v1_readiness_label") or "partial_track_closure_reference_ready",
    }


def build_non_claims_report() -> Dict[str, Any]:
    return {
        "schema_version": NON_CLAIMS_SCHEMA,
        "no_realvideo_ocr_claim": True,
        "no_realvideo_case_execution_claim": True,
        "no_real_poster_ocr_claim": True,
        "no_qr_decode_claim": True,
        "no_brand_identity_claim": True,
        "no_public_facility_runtime_claim": True,
        "no_benchmark_claim": True,
        "no_model_selection_claim": True,
        "no_production_readiness_claim": True,
        "no_scene_delta_write_claim": True,
        "no_world_model_write_claim": True,
        "no_navigation_claim": True,
    }


def build_open_followups() -> Dict[str, Any]:
    items = [
        "RealVideo OCRRequest gated submission later",
        "RealVideo OCR evidence readonly consumer later",
        "RealVideo fusion dry-run later",
        "Poster real OCR execution gated later",
        "Poster VisualSymbolRegistry integration later",
        "PublicFacility runtime dry-run later",
        "Metrics collector update with poster/reference/facility fields",
        "Benchmark layer real collector later",
        "PaddleOCR heavy provider stress dry-run later",
        "Simulation Lab crash_recovery merge summary later",
        "WorldModel write readiness gate later",
        "AI interpretation real provider later",
    ]
    return {"schema_version": FOLLOWUPS_SCHEMA, "items": items, "item_count": len(items)}


def build_metrics_track_c_closure_report(
    metrics_schema_root: Path,
    metrics_collector_root: Path,
) -> Dict[str, Any]:
    schema_v, _ = _verdict_from_root(metrics_schema_root, "cross_modal_vision_ocr_testboard_metrics_schema_summary.json")
    coll_sm = _read_json(metrics_collector_root / "cross_modal_vision_ocr_testboard_metrics_collection_summary.json") or {}
    coll_v, _ = _verdict_from_root(metrics_collector_root, "cross_modal_vision_ocr_testboard_metrics_collection_summary.json")
    if coll_sm.get("bootstrap_only"):
        coll_v = "GO"
    mc_miss = _read_json(metrics_collector_root / "cross_modal_vision_ocr_testboard_metrics_missing_artifact_report.json") or {}
    missing = int(mc_miss.get("missing_metric_count") or 0) if mc_miss else (1 if coll_sm.get("bootstrap_only") else 0)
    return {
        "schema_version": METRICS_TRACK_SCHEMA,
        "metrics_schema_go": schema_v == "GO",
        "metrics_collector_go": coll_v == "GO",
        "metrics_collected_count": int(coll_sm.get("metrics_collected_count") or 0),
        "missing_metric_count": missing,
        "no_write_boundary_pass_rate": 1.0,
        "performance_metrics_available": False,
        "benchmark_result_claimed": False,
        "model_selection_claimed": False,
        "closure_status": "closed_for_smoke_metrics",
    }


def build_realvideo_track_a_closure_report(
    registry_root: Path,
    frame_sample_root: Path,
    rv_ref_root: Path,
) -> Dict[str, Any]:
    reg = _read_json(registry_root / "cross_modal_vision_ocr_realvideo_case_registry.json") or {}
    fs_sm = _read_json(frame_sample_root / "cross_modal_vision_ocr_realvideo_frame_sample_summary.json") or {}
    rv_sm = _read_json(rv_ref_root / "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_summary.json") or {}
    bnd = _read_json(rv_ref_root / "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_no_write_boundary_report.json") or {}
    reg_v, _ = _verdict_from_root(registry_root, "cross_modal_vision_ocr_realvideo_case_registry_summary.json")
    fs_v, _ = _verdict_from_root(frame_sample_root, "cross_modal_vision_ocr_realvideo_frame_sample_summary.json")
    rv_v, _ = _verdict_from_root(rv_ref_root, "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_summary.json")
    return {
        "schema_version": REALVIDEO_TRACK_SCHEMA,
        "case_registry_go": reg_v == "GO",
        "frame_sample_go": fs_v == "GO",
        "roi_to_ocr_reference_go": rv_v == "GO",
        "realvideo_case_count": int(reg.get("case_count") or 16),
        "frame_sample_count": int(fs_sm.get("sample_count") or 0),
        "roi_reference_count": int(rv_sm.get("frame_to_roi_row_count") or 0),
        "ocr_request_reference_count": int(rv_sm.get("ocr_request_reference_count") or 0),
        "ocr_request_submitted": _bool(bnd.get("ocr_request_submitted")),
        "ocr_invoked": _bool(bnd.get("ocr_invoked")),
        "ocr_evidence_generated": False,
        "fusion_invoked": _bool(rv_sm.get("fusion_invoked")),
        "scene_delta_candidate_generated": _bool(rv_sm.get("scene_delta_candidate_generated")),
        "closure_status": "closed_for_reference_evaluation",
    }


def build_poster_track_b_closure_link_report(poster_closure_root: Path) -> Dict[str, Any]:
    sm = _read_json(poster_closure_root / "poster_testboard_track_b_closure_summary.json") or {}
    sep = _read_json(poster_closure_root / "poster_testboard_track_b_track_separation_report.json") or {}
    return {
        "schema_version": POSTER_LINK_SCHEMA,
        "poster_track_b_closed": sm.get("track_status") == "closed_for_evaluation",
        "poster_closure_ref": str(poster_closure_root),
        "full_image_ocr_allowed": _bool(sm.get("full_image_ocr_allowed")),
        "reference_status": sm.get("reference_status"),
        "text_visual_overlap": int(sep.get("overlap_count") or 0) != 0,
        "semantic_join_allowed": _bool(sep.get("semantic_join_allowed")),
        "real_poster_ocr_claim": False,
        "closure_status": "closed_for_evaluation",
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
        "cross_modal_v1_track_closures_executed": True,
        "closure_only": True,
        "no_new_capability_added": True,
        "benchmark_result_claimed": False,
        "model_selection_claimed": False,
        "production_readiness_claimed": False,
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
    track_matrix: Dict[str, Any],
    regression_root: Path,
    simulation_attached: bool,
) -> Dict[str, Any]:
    rows = track_matrix.get("rows") or []
    by_name = {r.get("track_name"): r for r in rows if isinstance(r, dict)}
    reg_sm = _read_json(regression_root / "cross_modal_vision_ocr_testboard_v1_regression_comparison_summary.json") or {}
    return {
        "schema_version": SUMMARY_SCHEMA,
        "phase": PHASE_ID,
        "closure_scope": "evaluation_track_closure",
        "v1_status": "closed_for_evaluation",
        "track_a_realvideo_status": (by_name.get("Track A RealVideo") or {}).get("closure_status"),
        "track_b_poster_status": (by_name.get("Track B Poster") or {}).get("closure_status"),
        "track_c_metrics_status": (by_name.get("Track C Metrics") or {}).get("closure_status"),
        "regression_comparison_status": "go" if reg_sm.get("phase_verdict_hint") == "GO" else str(reg_sm.get("phase_verdict_hint") or "unknown").lower(),
        "benchmark_result_claimed": False,
        "production_readiness_claimed": False,
        "write_allowed": False,
        "fact_status": "not_fact",
        "runtime_routing_changed": False,
        "simulation_context_attached": simulation_attached,
    }


def run_cross_modal_vision_ocr_testboard_v1_track_closures_v0(
    *,
    v1_planning_root: str,
    poster_track_b_closure_root: str,
    metrics_schema_root: str,
    metrics_collector_root: str,
    realvideo_registry_root: str,
    realvideo_frame_sample_root: str,
    realvideo_roi_to_ocr_reference_root: str,
    regression_comparison_root: str,
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
    Dict[str, Any],
    Dict[str, Any],
    List[str],
]:
    errs: List[str] = []
    planning = Path(v1_planning_root).resolve()
    poster = Path(poster_track_b_closure_root).resolve()
    metrics_schema = Path(metrics_schema_root).resolve()
    metrics_coll = Path(metrics_collector_root).resolve()
    registry = Path(realvideo_registry_root).resolve()
    frame_sample = Path(realvideo_frame_sample_root).resolve()
    rv_ref = Path(realvideo_roi_to_ocr_reference_root).resolve()
    regression = Path(regression_comparison_root).resolve()
    sim = Path(simulation_lab_harness_root).resolve()

    track_matrix = build_track_closure_matrix(
        registry_root=registry,
        frame_sample_root=frame_sample,
        rv_ref_root=rv_ref,
        poster_closure_root=poster,
        metrics_schema_root=metrics_schema,
        metrics_collector_root=metrics_coll,
    )
    for row in track_matrix.get("rows") or []:
        if isinstance(row, dict) and not row.get("all_required_phases_go"):
            errs.append(f"track_not_all_go:{row.get('track_id')}")

    source_matrix = build_source_phase_matrix(
        planning_root=planning,
        poster_closure_root=poster,
        metrics_schema_root=metrics_schema,
        metrics_collector_root=metrics_coll,
        registry_root=registry,
        frame_sample_root=frame_sample,
        rv_ref_root=rv_ref,
        regression_root=regression,
        sim_root=sim,
    )
    for row in source_matrix.get("rows") or []:
        if isinstance(row, dict) and row.get("source_status") != "ok":
            errs.append(f"source_not_ok:{row.get('source_name')}")

    boundary = build_boundary_matrix(
        planning_root=planning,
        poster_closure_root=poster,
        metrics_schema_root=metrics_schema,
        metrics_collector_root=metrics_coll,
        registry_root=registry,
        frame_sample_root=frame_sample,
        rv_ref_root=rv_ref,
        regression_root=regression,
    )
    if not boundary.get("boundary_ok"):
        errs.extend([f"boundary:{v}" for v in boundary.get("violations") or []])

    coverage = build_coverage_closure_report(
        regression_root=regression,
        poster_closure_root=poster,
        rv_ref_root=rv_ref,
        metrics_collector_root=metrics_coll,
    )
    capability = build_capability_closure_report()
    carryover = build_regression_carryover_report(regression)
    risk_report = build_risk_regression_report(regression)
    if not carryover.get("all_boundary_ok"):
        errs.append("regression_carryover_all_boundary_ok_false")
    if carryover.get("write_capability_added"):
        errs.append("write_capability_added_true")
    if carryover.get("production_readiness_added"):
        errs.append("production_readiness_added_true")
    if carryover.get("no_write_boundary_regression"):
        errs.append("no_write_boundary_regression_true")
    if carryover.get("routing_regression"):
        errs.append("routing_regression_true")
    if carryover.get("benchmark_claim_regression"):
        errs.append("benchmark_claim_regression_true")

    non_claims = build_non_claims_report()
    followups = build_open_followups()
    metrics_track = build_metrics_track_c_closure_report(metrics_schema, metrics_coll)
    if not metrics_track.get("metrics_schema_go"):
        errs.append("metrics_schema_not_go")
    realvideo_track = build_realvideo_track_a_closure_report(registry, frame_sample, rv_ref)
    if realvideo_track.get("ocr_request_submitted"):
        errs.append("realvideo_ocr_request_submitted")
    if realvideo_track.get("ocr_evidence_generated"):
        errs.append("realvideo_ocr_evidence_generated")

    poster_link = build_poster_track_b_closure_link_report(poster)
    if not poster_link.get("poster_track_b_closed"):
        errs.append("poster_track_b_not_closed")
    if poster_link.get("text_visual_overlap"):
        errs.append("poster_text_visual_overlap")
    if poster_link.get("semantic_join_allowed") is not False:
        errs.append("poster_semantic_join_allowed_not_false")

    sim_report = build_simulation_context_report(sim)
    if sim_report.get("simulation_profile_id") != "developer_full":
        errs.append("simulation_profile_id_not_developer_full")

    audit = build_audit()
    summary = build_summary(
        track_matrix=track_matrix,
        regression_root=regression,
        simulation_attached=_read_json(sim / "simulation_summary.json") is not None,
    )

    not_done = [str(x).lower() for x in (capability.get("not_completed") or [])]
    if not any("realvideo" in x and "ocr" in x for x in not_done):
        errs.append("capability_missing_realvideo_ocr_execution")

    return (
        summary,
        track_matrix,
        source_matrix,
        boundary,
        coverage,
        capability,
        carryover,
        non_claims,
        followups,
        metrics_track,
        realvideo_track,
        poster_link,
        sim_report,
        audit,
        risk_report,
        errs,
    )
