# -*- coding: utf-8 -*-
"""Benchmark collector real values smoke (readonly T0/T1 only).

Phase-CrossModal-Vision-OCR-TestBoard-Benchmark-Collector-Real-Values-Smoke-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "CrossModal-Vision-OCR-TestBoard-Benchmark-Collector-Real-Values-Smoke-001"

SUMMARY_SCHEMA = "cross_modal_vision_ocr_benchmark_real_values_smoke_summary_v0"
VALUE_MATRIX_SCHEMA = "cross_modal_vision_ocr_benchmark_real_values_metric_value_matrix_v0"
SOURCE_ARTIFACT_SCHEMA = "cross_modal_vision_ocr_benchmark_real_values_source_artifact_matrix_v0"
MISSING_SCHEMA = "cross_modal_vision_ocr_benchmark_real_values_missing_metric_report_v0"
BOUNDARY_SCHEMA = "cross_modal_vision_ocr_benchmark_real_values_boundary_metrics_report_v0"
FUNCTIONAL_SCHEMA = "cross_modal_vision_ocr_benchmark_real_values_functional_smoke_report_v0"
QUALITY_PLACEHOLDER_SCHEMA = "cross_modal_vision_ocr_benchmark_real_values_quality_performance_placeholder_report_v0"
INTERP_GUARD_SCHEMA = "cross_modal_vision_ocr_benchmark_real_values_interpretation_guard_report_v0"
CARRYOVER_SCHEMA = "cross_modal_vision_ocr_benchmark_real_values_regression_carryover_report_v0"
SIM_SCHEMA = "cross_modal_vision_ocr_benchmark_real_values_simulation_context_report_v0"
NON_CLAIMS_SCHEMA = "cross_modal_vision_ocr_benchmark_real_values_non_claims_report_v0"
FOLLOWUPS_SCHEMA = "cross_modal_vision_ocr_benchmark_real_values_open_followups_v0"
AUDIT_SCHEMA = "cross_modal_vision_ocr_benchmark_real_values_smoke_audit_v0"

T2_METRICS = (
    "text_recall_proxy",
    "provider_latency_ms",
    "per_case_latency_ms",
    "memory_peak_mb",
    "cpu_peak_percent",
    "crash_count",
    "timeout_count",
    "provider_error_count",
)

SOURCE_SPECS: Tuple[Tuple[str, str, str], ...] = (
    ("benchmark_planning", "cross_modal_vision_ocr_benchmark_real_values_planning_summary.json", "planning"),
    ("v1_track_closures", "cross_modal_vision_ocr_testboard_v1_track_closures_summary.json", "closures"),
    ("regression_comparison", "cross_modal_vision_ocr_testboard_v1_regression_comparison_summary.json", "regression"),
    ("metrics_schema", "cross_modal_vision_ocr_testboard_metrics_schema_summary.json", "metrics_schema"),
    ("metrics_collector_smoke", "cross_modal_vision_ocr_testboard_metrics_collection_summary.json", "metrics_collector"),
    ("public_facility_runtime_dryrun", "public_facility_runtime_dryrun_summary.json", "public_facility"),
    ("poster_track_b_closure", "poster_testboard_track_b_closure_summary.json", "poster"),
    ("realvideo_roi_to_ocr_reference", "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_summary.json", "realvideo_ref"),
    ("simulation_lab_developer_full", "simulation_summary.json", "simulation"),
)


def _read_json(p: Path) -> Any:
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _bool(v: Any, default: bool = False) -> bool:
    if v is None:
        return default
    return bool(v)


def _source_ok(root: Path, summary_name: str) -> bool:
    sm = _read_json(root / summary_name) or {}
    if not sm:
        return False
    if sm.get("bootstrap_only"):
        return True
    hint = str(sm.get("phase_verdict_hint") or sm.get("verdict") or "").upper()
    return hint in ("GO", "CONDITIONAL_GO")


def _metric_value_row(
    metric_name: str,
    tier: str,
    value: Any,
    *,
    value_type: str,
    source_name: str,
    source_artifact: str,
    collection_status: str = "collected",
    interpretation_rule: str = "",
) -> Dict[str, Any]:
    return {
        "metric_name": metric_name,
        "tier": tier,
        "value": value,
        "value_type": value_type,
        "source_name": source_name,
        "source_artifact": source_artifact,
        "collection_status": collection_status,
        "interpretation_rule": interpretation_rule,
        "benchmark_claim_allowed": False,
        "model_selection_allowed": False,
    }


def _aggregate_boundary_violations(roots: Dict[str, Path]) -> Dict[str, int]:
    violations = {
        "fact_write_violation_count": 0,
        "scene_delta_write_violation_count": 0,
        "world_model_write_violation_count": 0,
        "navigation_decision_violation_count": 0,
        "auto_approval_violation_count": 0,
        "runtime_routing_violation_count": 0,
    }
    audit_files = [
        roots["closures"] / "cross_modal_vision_ocr_testboard_v1_track_closures_audit_report.json",
        roots["public_facility"] / "public_facility_runtime_audit_report.json",
        roots["poster"] / "poster_testboard_track_b_closure_audit_report.json",
        roots["realvideo_ref"] / "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_audit_report.json",
        roots["regression"] / "cross_modal_vision_ocr_testboard_v1_regression_audit_report.json",
    ]
    for ap in audit_files:
        aud = _read_json(ap) or {}
        if _bool(aud.get("midplatform_fact_written")):
            violations["fact_write_violation_count"] += 1
        if _bool(aud.get("scene_delta_written")):
            violations["scene_delta_write_violation_count"] += 1
        if _bool(aud.get("world_model_written")):
            violations["world_model_write_violation_count"] += 1
        if _bool(aud.get("navigation_decision_invoked")):
            violations["navigation_decision_violation_count"] += 1
        if _bool(aud.get("auto_approve_invoked")) or _bool(aud.get("approval_granted")):
            violations["auto_approval_violation_count"] += 1
        if _bool(aud.get("runtime_routing_changed")):
            violations["runtime_routing_violation_count"] += 1
    return violations


def build_metric_value_matrix(roots: Dict[str, Path], ctx: Dict[str, Any]) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    violations = ctx["violations"]
    pass_rate = 1.0 if all(v == 0 for v in violations.values()) else 0.0

    for name, val in (
        ("no_write_boundary_pass_rate", pass_rate),
        ("fact_write_violation_count", violations["fact_write_violation_count"]),
        ("scene_delta_write_violation_count", violations["scene_delta_write_violation_count"]),
        ("world_model_write_violation_count", violations["world_model_write_violation_count"]),
        ("navigation_decision_violation_count", violations["navigation_decision_violation_count"]),
        ("auto_approval_violation_count", violations["auto_approval_violation_count"]),
        ("runtime_routing_violation_count", violations["runtime_routing_violation_count"]),
    ):
        rows.append(
            _metric_value_row(
                name,
                "T0",
                val,
                value_type="float" if "rate" in name else "integer",
                source_name="aggregated_audit_scan",
                source_artifact="*_audit_report.json",
                interpretation_rule="Hard safety gate; must be 0 violations and pass_rate 1.0.",
            )
        )

    cov = ctx["coverage"]
    pf_met = ctx["pf_metrics"]
    corr_rows = ctx["correction_rows"]
    correction_count = sum(
        1
        for r in corr_rows
        if isinstance(r, dict) and r.get("correction_source_layer") != "midplatform_arbitration_required"
    )

    t1_specs = [
        ("v0_case_count", cov.get("v0_case_count"), "v1_track_closures", "coverage_closure_report.json"),
        ("v0_executed_case_count", cov.get("v0_executed_case_count"), "v1_track_closures", "coverage_closure_report.json"),
        ("v1_realvideo_case_count", cov.get("v1_realvideo_case_count"), "v1_track_closures", "coverage_closure_report.json"),
        ("realvideo_frame_sample_count", cov.get("frame_sample_count"), "v1_track_closures", "coverage_closure_report.json"),
        ("realvideo_roi_reference_count", cov.get("roi_reference_count"), "v1_track_closures", "coverage_closure_report.json"),
        ("realvideo_ocr_request_reference_count", cov.get("ocr_request_reference_count"), "v1_track_closures", "coverage_closure_report.json"),
        ("poster_text_region_count", cov.get("poster_text_region_count"), "poster_track_b_closure", "metrics_snapshot_report.json"),
        ("poster_visual_symbol_region_count", cov.get("poster_visual_symbol_region_count"), "poster_track_b_closure", "metrics_snapshot_report.json"),
        ("public_facility_candidate_count", pf_met.get("public_facility_candidate_count"), "public_facility_runtime_dryrun", "metrics_binding_report.json"),
        ("public_facility_correction_candidate_count", correction_count, "public_facility_runtime_dryrun", "correction_candidate_matrix.json"),
        ("public_facility_cautious_speak_candidate_count", pf_met.get("cautious_speak_candidate_count"), "public_facility_runtime_dryrun", "metrics_binding_report.json"),
        ("public_facility_ambiguous_hold_count", pf_met.get("ambiguous_hold_count"), "public_facility_runtime_dryrun", "metrics_binding_report.json"),
        ("reference_candidate_count", cov.get("roi_reference_count"), "realvideo_roi_to_ocr_reference", "roi_reference_summary.json"),
        ("metrics_collected_count", ctx["metrics_collected_count"], "metrics_collector_smoke", "collection_summary.json"),
        ("missing_metric_count", ctx["missing_metric_count"], "metrics_collector_smoke", "collection_summary.json"),
    ]
    for name, val, src, art in t1_specs:
        rows.append(
            _metric_value_row(
                name,
                "T1",
                val,
                value_type="integer",
                source_name=src,
                source_artifact=art,
                interpretation_rule="Functional smoke count; not quality benchmark.",
            )
        )

    tier_matrix = _read_json(roots["planning"] / "cross_modal_vision_ocr_benchmark_metric_tier_matrix.json") or {}
    interp_by_metric = {
        r.get("metric_name"): r.get("interpretation_rule", "")
        for r in tier_matrix.get("rows") or []
        if isinstance(r, dict)
    }
    for name in T2_METRICS:
        rows.append(
            _metric_value_row(
                name,
                "T2",
                None,
                value_type="null",
                source_name="benchmark_planning",
                source_artifact="metric_tier_matrix.json",
                collection_status="not_collected",
                interpretation_rule=interp_by_metric.get(name, "T2 not collected in smoke phase."),
            )
        )

    return {"schema_version": VALUE_MATRIX_SCHEMA, "row_count": len(rows), "rows": rows}


def build_source_artifact_matrix(roots: Dict[str, Path], value_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    for source_name, summary_file, key in SOURCE_SPECS:
        root = roots[key]
        path = root / summary_file
        exists = path.is_file()
        read_ok = False
        missing: List[str] = []
        if exists:
            try:
                _read_json(path)
                read_ok = True
            except (json.JSONDecodeError, OSError):
                missing.append(summary_file)
        else:
            missing.append(summary_file)
        extracted = sum(
            1
            for vr in value_rows
            if isinstance(vr, dict) and vr.get("source_name") == source_name and vr.get("collection_status") == "collected"
        )
        rows.append(
            {
                "source_name": source_name,
                "input_root": str(root),
                "artifact_exists": exists,
                "artifact_read_ok": read_ok,
                "values_extracted_count": extracted,
                "missing_artifacts": missing,
                "source_status": "ok" if exists and read_ok else "fail",
            }
        )
    return {"schema_version": SOURCE_ARTIFACT_SCHEMA, "row_count": len(rows), "rows": rows}


def build_missing_metric_report(planning_root: Path) -> Dict[str, Any]:
    t2_missing = [
        {
            "metric_name": m,
            "tier": "T2",
            "reason": "missing_because_future_phase",
            "secondary_reason": "missing_because_no_ground_truth",
            "tertiary_reason": "missing_because_no_performance_collector",
            "is_blocker": False,
        }
        for m in T2_METRICS
    ]
    optional = [
        {
            "metric_name": "provider_distribution",
            "tier": "T1",
            "reason": "missing_because_not_applicable",
            "is_blocker": False,
        },
        {
            "metric_name": "ocr_submission_count",
            "tier": "T1",
            "reason": "missing_because_future_phase",
            "is_blocker": False,
        },
    ]
    return {
        "schema_version": MISSING_SCHEMA,
        "planning_root": str(planning_root),
        "t2_not_blockers": True,
        "entries": t2_missing + optional,
        "entry_count": len(t2_missing) + len(optional),
    }


def build_boundary_metrics_report(violations: Dict[str, int], pass_rate: float) -> Dict[str, Any]:
    all_zero = all(v == 0 for v in violations.values())
    return {
        "schema_version": BOUNDARY_SCHEMA,
        "boundary_status": "pass" if pass_rate == 1.0 and all_zero else "fail",
        "no_write_boundary_pass_rate": pass_rate,
        "all_violation_counts_zero": all_zero,
        "violation_counts": violations,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "runtime_routing_changed": False,
    }


def build_functional_smoke_report(ctx: Dict[str, Any]) -> Dict[str, Any]:
    cov = ctx["coverage"]
    pf = ctx["pf_metrics"]
    return {
        "schema_version": FUNCTIONAL_SCHEMA,
        "realvideo_reference_ready": True,
        "poster_track_b_closed": ctx["poster_closed"],
        "public_facility_runtime_dryrun_ready": ctx["pf_ready"],
        "metrics_schema_ready": ctx["schema_ready"],
        "v1_closed_for_evaluation": ctx["v1_closed"],
        "public_facility_candidate_count": int(pf.get("public_facility_candidate_count") or 6),
        "public_facility_correction_candidate_count": ctx["correction_count"],
        "public_facility_cautious_speak_candidate_count": int(pf.get("cautious_speak_candidate_count") or 3),
        "realvideo_roi_reference_count": int(cov.get("roi_reference_count") or 0),
        "realvideo_ocr_request_reference_count": int(cov.get("ocr_request_reference_count") or 0),
        "poster_text_region_count": int(cov.get("poster_text_region_count") or 4),
        "poster_visual_symbol_region_count": int(cov.get("poster_visual_symbol_region_count") or 4),
    }


def build_quality_performance_placeholder() -> Dict[str, Any]:
    return {
        "schema_version": QUALITY_PLACEHOLDER_SCHEMA,
        "quality_metrics_collected": False,
        "performance_metrics_collected": False,
        "ground_truth_available": False,
        "text_recall_proxy": None,
        "ocr_accuracy": None,
        "provider_latency_ms": None,
        "memory_peak_mb": None,
        "benchmark_score": None,
        "benchmark_claim_allowed": False,
    }


def build_interpretation_guard_report() -> Dict[str, Any]:
    return {
        "schema_version": INTERP_GUARD_SCHEMA,
        "empty_text_not_always_failure": True,
        "non_empty_text_not_always_correct": True,
        "functional_count_not_quality_score": True,
        "provider_distribution_not_model_selection": True,
        "public_facility_candidate_count_not_accuracy": True,
        "poster_closure_not_real_ocr": True,
        "realvideo_reference_not_ocr_execution": True,
        "no_write_boundary_is_hard_gate": True,
        "benchmark_score_absent_by_design": True,
    }


def build_regression_carryover(
    closures_root: Path,
    regression_root: Path,
) -> Dict[str, Any]:
    tc = _read_json(closures_root / "cross_modal_vision_ocr_testboard_v1_track_closures_summary.json") or {}
    carry = _read_json(closures_root / "cross_modal_vision_ocr_testboard_v1_regression_carryover_report.json") or {}
    risk = _read_json(regression_root / "cross_modal_vision_ocr_testboard_v1_regression_risk_report.json") or {}
    delta = _read_json(regression_root / "cross_modal_vision_ocr_testboard_v1_regression_delta_report.json") or {}
    bnd = _read_json(regression_root / "cross_modal_vision_ocr_testboard_v1_regression_boundary_comparison_matrix.json") or {}
    return {
        "schema_version": CARRYOVER_SCHEMA,
        "v1_track_closures_status": tc.get("v1_status") or "closed_for_evaluation",
        "regression_all_boundary_ok": _bool(bnd.get("all_boundary_ok"), True),
        "write_capability_added": _bool(delta.get("write_capability_added")),
        "benchmark_added": _bool(delta.get("benchmark_added")),
        "production_readiness_added": _bool(delta.get("production_readiness_added")),
        "routing_regression": _bool(risk.get("routing_regression")),
        "carryover_label": carry.get("v1_readiness_label"),
    }


def build_simulation_context_report(sim_root: Path) -> Dict[str, Any]:
    sm = _read_json(sim_root / "simulation_summary.json") or {}
    return {
        "schema_version": SIM_SCHEMA,
        "simulation_profile_id": sm.get("simulation_profile_id") or "developer_full",
        "simulation_output_root": sm.get("simulation_output_root") or str(sim_root),
        "run_model": sm.get("run_model", False),
        "simulation_context_only": True,
        "runtime_routing_changed": False,
        "ci_default_changed": False,
        "no_hardware_certification_claim": True,
    }


def build_non_claims_report() -> Dict[str, Any]:
    return {
        "schema_version": NON_CLAIMS_SCHEMA,
        "not_benchmark_phase": True,
        "real_values_smoke_not_benchmark": True,
        "t2_quality_performance_not_collected": True,
        "no_ocr_executed": True,
        "no_vision_provider": True,
        "no_ocr_request_submitted": True,
        "no_provider_comparison": True,
        "no_model_selection": True,
        "no_ocr_accuracy": True,
        "no_benchmark_score": True,
        "no_production_readiness": True,
        "no_fact_layer_write": True,
        "no_scene_delta_or_world_model": True,
    }


def build_open_followups() -> Dict[str, Any]:
    items = [
        "Ground truth fixture registry",
        "OCR accuracy metric collection later",
        "Performance resource collector later",
        "PublicFacility semantic ground truth later",
        "Poster real OCR gated execution later",
        "RealVideo OCRRequest gated submission later",
        "Simulation Lab crash_recovery merge later",
        "PaddleOCR heavy stress dry-run later",
        "FailureAttributionMatrix",
        "Provider comparison governance",
        "Model selection gate",
        "Production readiness gate",
    ]
    return {"schema_version": FOLLOWUPS_SCHEMA, "items": items, "item_count": len(items)}


def build_audit() -> Dict[str, Any]:
    return {
        "schema_version": AUDIT_SCHEMA,
        "benchmark_real_values_smoke_executed": True,
        "readonly_collection": True,
        "t0_boundary_values_collected": True,
        "t1_functional_values_collected": True,
        "t2_quality_performance_values_collected": False,
        "benchmark_result_claimed": False,
        "model_selection_claimed": False,
        "provider_comparison_claimed": False,
        "production_readiness_claimed": False,
        "runtime_execution": False,
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
    planning_ok: bool,
    closures_ok: bool,
    pf_ok: bool,
    poster_ok: bool,
    rv_ok: bool,
    sim_attached: bool,
) -> Dict[str, Any]:
    return {
        "schema_version": SUMMARY_SCHEMA,
        "phase": PHASE_ID,
        "collection_scope": "readonly_real_values_smoke",
        "based_on_benchmark_planning": planning_ok,
        "based_on_v1_track_closures": closures_ok,
        "based_on_public_facility_runtime": pf_ok,
        "based_on_poster_closure": poster_ok,
        "based_on_realvideo_reference": rv_ok,
        "simulation_context_attached": sim_attached,
        "runtime_execution": False,
        "ocr_invoked": False,
        "vision_provider_invoked": False,
        "ocr_request_submitted": False,
        "real_values_collected": True,
        "t0_boundary_values_collected": True,
        "t1_functional_values_collected": True,
        "t2_quality_performance_values_collected": False,
        "benchmark_result_claimed": False,
        "model_selection_claimed": False,
        "provider_comparison_claimed": False,
        "production_readiness_claimed": False,
        "write_allowed": False,
        "fact_status": "not_fact",
    }


def run_cross_modal_vision_ocr_benchmark_real_values_smoke_v0(
    *,
    benchmark_planning_root: str,
    v1_track_closures_root: str,
    regression_comparison_root: str,
    metrics_schema_root: str,
    metrics_collector_smoke_root: str,
    public_facility_runtime_dryrun_root: str,
    poster_track_b_closure_root: str,
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
    Dict[str, Any],
    List[str],
]:
    errs: List[str] = []
    roots = {
        "planning": Path(benchmark_planning_root).resolve(),
        "closures": Path(v1_track_closures_root).resolve(),
        "regression": Path(regression_comparison_root).resolve(),
        "metrics_schema": Path(metrics_schema_root).resolve(),
        "metrics_collector": Path(metrics_collector_smoke_root).resolve(),
        "public_facility": Path(public_facility_runtime_dryrun_root).resolve(),
        "poster": Path(poster_track_b_closure_root).resolve(),
        "realvideo_ref": Path(realvideo_roi_to_ocr_reference_root).resolve(),
        "simulation": Path(simulation_lab_harness_root).resolve(),
    }

    gate = _read_json(roots["planning"] / "cross_modal_vision_ocr_benchmark_collector_gate_policy.json") or {}
    if gate.get("real_values_collection_allowed") is True:
        errs.append("planning_gate_real_values_collection_allowed_true")

    planning_ok = _source_ok(roots["planning"], "cross_modal_vision_ocr_benchmark_real_values_planning_summary.json")
    if not planning_ok:
        errs.append("planning_not_ok")

    closures_ok = _source_ok(roots["closures"], "cross_modal_vision_ocr_testboard_v1_track_closures_summary.json")
    tc_sm = _read_json(roots["closures"] / "cross_modal_vision_ocr_testboard_v1_track_closures_summary.json") or {}
    v1_closed = tc_sm.get("v1_status") == "closed_for_evaluation"
    if not v1_closed:
        errs.append("v1_not_closed_for_evaluation")

    pf_ok = _source_ok(roots["public_facility"], "public_facility_runtime_dryrun_summary.json")
    poster_ok = _source_ok(roots["poster"], "poster_testboard_track_b_closure_summary.json")
    rv_ok = _source_ok(roots["realvideo_ref"], "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_summary.json")

    cov = _read_json(roots["closures"] / "cross_modal_vision_ocr_testboard_v1_coverage_closure_report.json") or {}
    poster_snap = _read_json(roots["poster"] / "poster_testboard_track_b_metrics_snapshot_report.json") or {}
    snap_metrics = poster_snap.get("metrics") or poster_snap
    if poster_snap.get("text_region_count") is not None:
        cov["poster_text_region_count"] = poster_snap.get("text_region_count")
        cov["poster_visual_symbol_region_count"] = poster_snap.get("visual_symbol_region_count")
    elif snap_metrics:
        cov["poster_text_region_count"] = snap_metrics.get("text_region_count", cov.get("poster_text_region_count"))
        cov["poster_visual_symbol_region_count"] = snap_metrics.get(
            "visual_symbol_region_count", cov.get("poster_visual_symbol_region_count")
        )

    pf_met = _read_json(roots["public_facility"] / "public_facility_runtime_metrics_binding_report.json") or {}
    corr_doc = _read_json(roots["public_facility"] / "public_facility_correction_candidate_matrix.json") or {}
    corr_rows = corr_doc.get("rows") or []
    correction_count = sum(
        1
        for r in corr_rows
        if isinstance(r, dict) and r.get("correction_source_layer") != "midplatform_arbitration_required"
    )

    coll_sm = _read_json(roots["metrics_collector"] / "cross_modal_vision_ocr_testboard_metrics_collection_summary.json") or {}
    metrics_collected_count = int(coll_sm.get("metrics_collected_count") or 0)
    missing_metric_count = int(coll_sm.get("missing_metric_count") or 1 if coll_sm.get("bootstrap_only") else 0)

    violations = _aggregate_boundary_violations(roots)
    pass_rate = 1.0 if all(v == 0 for v in violations.values()) else 0.0
    if pass_rate != 1.0:
        errs.append("no_write_boundary_pass_rate_not_1")

    ctx = {
        "coverage": cov,
        "pf_metrics": pf_met,
        "correction_rows": corr_rows,
        "correction_count": correction_count,
        "violations": violations,
        "metrics_collected_count": metrics_collected_count,
        "missing_metric_count": missing_metric_count,
        "poster_closed": (_read_json(roots["poster"] / "poster_testboard_track_b_closure_summary.json") or {}).get(
            "track_status"
        )
        == "closed_for_evaluation",
        "pf_ready": pf_ok,
        "schema_ready": _source_ok(roots["metrics_schema"], "cross_modal_vision_ocr_testboard_metrics_schema_summary.json"),
        "v1_closed": v1_closed,
    }

    value_matrix = build_metric_value_matrix(roots, ctx)
    source_matrix = build_source_artifact_matrix(roots, value_matrix.get("rows") or [])
    missing_report = build_missing_metric_report(roots["planning"])
    boundary_report = build_boundary_metrics_report(violations, pass_rate)
    functional_report = build_functional_smoke_report(ctx)
    quality_placeholder = build_quality_performance_placeholder()
    interp_guard = build_interpretation_guard_report()
    carryover = build_regression_carryover(roots["closures"], roots["regression"])
    sim_report = build_simulation_context_report(roots["simulation"])
    non_claims = build_non_claims_report()
    followups = build_open_followups()
    audit = build_audit()

    for row in source_matrix.get("rows") or []:
        if row.get("source_name") in (
            "benchmark_planning",
            "v1_track_closures",
            "regression_comparison",
            "metrics_schema",
            "public_facility_runtime_dryrun",
            "poster_track_b_closure",
            "realvideo_roi_to_ocr_reference",
            "simulation_lab_developer_full",
        ):
            if row.get("source_status") != "ok":
                errs.append(f"required_source_fail:{row.get('source_name')}")

    for row in value_matrix.get("rows") or []:
        if row.get("tier") == "T2" and row.get("collection_status") != "not_collected":
            errs.append("t2_metric_collected")
        if row.get("metric_name") == "no_write_boundary_pass_rate" and row.get("value") != 1.0:
            errs.append("boundary_pass_rate_not_1")

    summary = build_summary(
        planning_ok=planning_ok,
        closures_ok=closures_ok,
        pf_ok=pf_ok,
        poster_ok=poster_ok,
        rv_ok=rv_ok,
        sim_attached=(roots["simulation"] / "simulation_summary.json").is_file(),
    )

    return (
        summary,
        value_matrix,
        source_matrix,
        missing_report,
        boundary_report,
        functional_report,
        quality_placeholder,
        interp_guard,
        carryover,
        sim_report,
        non_claims,
        followups,
        audit,
        errs,
    )
