# -*- coding: utf-8 -*-
"""CrossModal Vision-OCR TestBoard metrics collector (readonly aggregation only).

Phase-CrossModal-Vision-OCR-TestBoard-Metrics-Collector-Smoke-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "CrossModal-Vision-OCR-TestBoard-Metrics-Collector-Smoke-001"

SUMMARY_SCHEMA = "cross_modal_vision_ocr_testboard_metrics_collection_summary_v0"
VALUE_MATRIX_SCHEMA = "cross_modal_vision_ocr_testboard_metrics_value_matrix_v0"
MISSING_SCHEMA = "cross_modal_vision_ocr_testboard_metrics_missing_artifact_report_v0"
BOUNDARY_REPORT_SCHEMA = "cross_modal_vision_ocr_testboard_boundary_metrics_report_v0"
POSTER_REPORT_SCHEMA = "cross_modal_vision_ocr_testboard_poster_metrics_report_v0"
GUARD_SCHEMA = "cross_modal_vision_ocr_testboard_metrics_interpretation_guard_report_v0"
AUDIT_SCHEMA = "cross_modal_vision_ocr_testboard_metrics_collector_audit_v0"


def _read_json(p: Path) -> Any:
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _row(
    metric_name: str,
    metric_group: str,
    value: Any,
    value_type: str,
    source_artifact: str,
    source_status: str,
    interpretation_note: str,
) -> Dict[str, Any]:
    return {
        "metric_name": metric_name,
        "metric_group": metric_group,
        "value": value,
        "value_type": value_type,
        "source_artifact": source_artifact,
        "source_status": source_status,
        "interpretation_note": interpretation_note,
        "benchmark_claim": False,
    }


def _source_entry(
    source_name: str,
    expected_path: Path,
    missing_behavior: str,
    affected_metrics: List[str],
) -> Dict[str, Any]:
    exists = expected_path.is_file()
    return {
        "source_name": source_name,
        "expected_path": str(expected_path),
        "exists": exists,
        "missing_behavior": missing_behavior,
        "affected_metrics": affected_metrics,
    }


def _count_rapidocr_matrix(matrix_doc: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    rows = matrix_doc.get("rows") if isinstance(matrix_doc, dict) else []
    if not isinstance(rows, list):
        rows = []
    empty = sum(1 for r in rows if isinstance(r, dict) and r.get("empty_text") is True)
    non_empty = sum(1 for r in rows if isinstance(r, dict) and r.get("empty_text") is False)
    rapidocr = sum(1 for r in rows if isinstance(r, dict) and r.get("rapidocr_invoked") is True)
    paddle = sum(1 for r in rows if isinstance(r, dict) and r.get("paddleocr_invoked") is True)
    stub_fb = sum(1 for r in rows if isinstance(r, dict) and r.get("fallback_to_stub") is True)
    failed = sum(
        1
        for r in rows
        if isinstance(r, dict) and str(r.get("ocr_bridge_status") or "") not in ("success", "submitted", "")
    )
    success = len(rows) - failed
    text_total = sum(int(r.get("text_item_count") or 0) for r in rows if isinstance(r, dict))
    return {
        "submission_count": len(rows),
        "success_count": success,
        "failed_count": failed,
        "empty_count": empty,
        "non_empty_count": non_empty,
        "rapidocr_count": rapidocr,
        "paddle_count": paddle,
        "stub_fallback_count": stub_fb,
        "text_item_count_total": text_total,
    }


def _boundary_violations(boundary_doc: Optional[Dict[str, Any]]) -> Dict[str, int]:
    rows = boundary_doc.get("rows") if isinstance(boundary_doc, dict) else []
    if not isinstance(rows, list):
        return {
            "midplatform_fact_write_violation_count": 0,
            "scene_delta_write_violation_count": 0,
            "world_model_write_violation_count": 0,
            "navigation_decision_violation_count": 0,
            "auto_approval_violation_count": 0,
            "executor_invocation_violation_count": 0,
        }
    viol = {
        "midplatform_fact_write_violation_count": 0,
        "scene_delta_write_violation_count": 0,
        "world_model_write_violation_count": 0,
        "navigation_decision_violation_count": 0,
        "auto_approval_violation_count": 0,
        "executor_invocation_violation_count": 0,
    }
    for r in rows:
        if not isinstance(r, dict):
            continue
        if r.get("midplatform_fact_written") is True:
            viol["midplatform_fact_write_violation_count"] += 1
        if r.get("scene_delta_written") is True:
            viol["scene_delta_write_violation_count"] += 1
        if r.get("world_model_written") is True:
            viol["world_model_write_violation_count"] += 1
        if r.get("navigation_decision_invoked") is True:
            viol["navigation_decision_violation_count"] += 1
        if r.get("auto_approve_invoked") is True or r.get("approval_granted") is True:
            viol["auto_approval_violation_count"] += 1
        if r.get("scene_delta_executor_invoked") is True:
            viol["executor_invocation_violation_count"] += 1
    return viol


def run_cross_modal_vision_ocr_testboard_metrics_collector_v0(
    *,
    schema_root: str,
    v0_closure_root: str,
    poster_governance_root: str,
    rapidocr_submission_root: str,
    rapidocr_readonly_consumer_root: str,
    reference_only_rapidocr_root: str,
    fusion_dryrun_root: str,
    gate_evaluator_root: str,
    executor_trace_stub_root: str,
) -> Tuple[
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
    schema_p = Path(schema_root).resolve()
    v0 = Path(v0_closure_root).resolve()
    poster = Path(poster_governance_root).resolve()
    rapid = Path(rapidocr_submission_root).resolve()
    ro_con = Path(rapidocr_readonly_consumer_root).resolve()
    ref = Path(reference_only_rapidocr_root).resolve()
    fusion = Path(fusion_dryrun_root).resolve()
    gate = Path(gate_evaluator_root).resolve()
    exec_stub = Path(executor_trace_stub_root).resolve()

    schema_summary = _read_json(schema_p / "cross_modal_vision_ocr_testboard_metrics_schema_summary.json")
    if not schema_summary:
        errs.append("missing_metrics_schema_summary")

    v0_summary = _read_json(v0 / "cross_modal_vision_ocr_testboard_v0_closure_summary.json")
    if not v0_summary:
        errs.append("missing_v0_closure_summary")

    poster_summary = _read_json(poster / "poster_layout_governance_summary.json")
    if not poster_summary:
        errs.append("missing_poster_governance_summary")

    missing_sources: List[Dict[str, Any]] = []
    critical_missing_names = {"metrics_schema", "v0_closure", "poster_governance"}

    for name, path, metrics in (
        (
            "metrics_schema",
            schema_p / "cross_modal_vision_ocr_testboard_metrics_schema_summary.json",
            ["schema_version"],
        ),
        (
            "v0_closure",
            v0 / "cross_modal_vision_ocr_testboard_v0_closure_summary.json",
            ["case_count", "executed_case_count"],
        ),
        (
            "poster_governance",
            poster / "poster_layout_governance_summary.json",
            ["poster_image_count"],
        ),
    ):
        missing_sources.append(_source_entry(name, path, "mark_metric_unavailable", metrics))

    def _track(name: str, path: Path, behavior: str, metrics: List[str], critical: bool = False) -> Optional[Any]:
        entry = _source_entry(name, path, behavior, metrics)
        missing_sources.append(entry)
        if not entry["exists"]:
            if critical:
                errs.append(f"missing_critical:{name}")
            return None
        return _read_json(path)

    rapid_summary = _track(
        "rapidocr_submission",
        rapid / "rapidocr_submission_from_vision_roi_summary.json",
        "mark_metric_unavailable",
        ["ocr_submission_count", "ocr_empty_text_count"],
    )
    rapid_provider = _track(
        "rapidocr_provider_summary",
        rapid / "rapidocr_submission_provider_summary.json",
        "mark_metric_unavailable",
        ["provider_distribution", "ocr_empty_text_count"],
    )
    rapid_matrix_doc = _track(
        "rapidocr_result_matrix",
        rapid / "rapidocr_submission_result_matrix.json",
        "mark_metric_unavailable",
        ["rapidocr_invoked_count", "paddleocr_invoked_count"],
    )
    _track(
        "rapidocr_readonly_consumer",
        ro_con / "vision_triggered_rapidocr_evidence_readonly_consumer_summary.json",
        "mark_metric_unavailable",
        ["text_item_count_total"],
    )
    ref_summary = _track(
        "reference_only_rapidocr",
        ref / "cross_modal_vision_ocr_reference_only_rapidocr_summary.json",
        "mark_metric_unavailable",
        ["reference_candidate_count"],
    )
    ref_cands = _track(
        "reference_candidates_rapidocr",
        ref / "cross_modal_vision_ocr_reference_candidates_rapidocr.json",
        "mark_metric_unavailable",
        ["reference_candidate_count"],
    )
    fusion_summary = _track(
        "fusion_dryrun",
        fusion / "cross_modal_vision_ocr_fusion_candidate_dryrun_summary.json",
        "mark_metric_unavailable",
        ["fusion_candidate_count"],
    )
    gate_result = _track(
        "gate_evaluator",
        gate / "cross_modal_scene_delta_gate_evaluation_result.json",
        "mark_metric_unavailable",
        ["gate_hold_for_review_count"],
    )
    exec_blocked = _track(
        "executor_trace_stub",
        exec_stub / "cross_modal_scene_delta_executor_blocked_reason_report.json",
        "mark_metric_unavailable",
        ["executor_blocked_by_gate_count"],
    )

    v0_risk = _read_json(v0 / "cross_modal_vision_ocr_testboard_v0_risk_coverage_report.json")
    v0_boundary = _read_json(v0 / "cross_modal_vision_ocr_testboard_v0_no_write_boundary_matrix.json")

    ws_root = schema_p.parent.parent
    gate_summary_doc = _read_json(gate / "cross_modal_scene_delta_gate_evaluation_summary.json")
    sd_root = (gate_summary_doc or {}).get("scene_delta_candidate_dryrun_root")
    sd_summary = (
        _read_json(Path(str(sd_root)) / "cross_modal_scene_delta_candidate_dryrun_summary.json")
        if sd_root
        else None
    )
    review_summary = _read_json(
        ws_root / "_eval_out/cross_modal_fusion_review_queue_smoke_v0/cross_modal_fusion_review_queue_summary.json"
    )
    ai_summary = _read_json(
        ws_root / "_eval_out/cross_modal_ai_interpretation_dryrun_smoke_v0/cross_modal_ai_interpretation_dryrun_summary.json"
    )

    matrix_rows: List[Dict[str, Any]] = []
    ocr_stats = _count_rapidocr_matrix(rapid_matrix_doc if isinstance(rapid_matrix_doc, dict) else None)
    provider_dist = (
        (rapid_provider or {}).get("selected_provider_distribution")
        if isinstance(rapid_provider, dict)
        else {}
    )
    if rapid_summary and not provider_dist:
        provider_dist = {"rapidocr_candidate": rapid_summary.get("submission_count", 0)}

    def _add_ocr(name: str, val: Any, vtype: str, artifact: str, status: str, note: str) -> None:
        matrix_rows.append(_row(name, "OCR Output Metrics", val, vtype, artifact, status, note))

    ocr_status = "collected" if rapid_summary else "unavailable"
    _add_ocr("ocr_submission_count", ocr_stats["submission_count"], "integer", "rapidocr_submission", ocr_status, "readonly_count")
    _add_ocr("ocr_success_count", ocr_stats["success_count"], "integer", "rapidocr_submission", ocr_status, "bridge_success_rows")
    _add_ocr("ocr_failed_count", ocr_stats["failed_count"], "integer", "rapidocr_submission", ocr_status, "non_success_rows")
    _add_ocr(
        "ocr_empty_text_count",
        (rapid_provider or {}).get("empty_text_count", ocr_stats["empty_count"]),
        "integer",
        "rapidocr_provider_summary",
        ocr_status,
        "case_type_dependent_empty_text_not_always_failure",
    )
    _add_ocr("ocr_non_empty_text_count", ocr_stats["non_empty_count"], "integer", "rapidocr_result_matrix", ocr_status, "non_empty_rows")
    _add_ocr("provider_distribution", provider_dist or {}, "object", "rapidocr_provider_summary", ocr_status, "distribution_only_not_benchmark")
    _add_ocr("rapidocr_invoked_count", ocr_stats["rapidocr_count"], "integer", "rapidocr_result_matrix", ocr_status, "invocation_count")
    _add_ocr("paddleocr_invoked_count", ocr_stats["paddle_count"], "integer", "rapidocr_result_matrix", ocr_status, "invocation_count")
    _add_ocr(
        "fallback_to_stub_count",
        (rapid_provider or {}).get("stub_fallback_count", ocr_stats["stub_fallback_count"]),
        "integer",
        "rapidocr_provider_summary",
        ocr_status,
        "stub_fallback_rows",
    )

    case_status = "collected" if v0_summary else "unavailable"
    cg = "Case Outcome Metrics"
    matrix_rows.append(_row("case_count", cg, (v0_summary or {}).get("case_count"), "integer", "v0_closure", case_status, "testboard_v0"))
    matrix_rows.append(
        _row("executed_case_count", cg, (v0_summary or {}).get("executed_case_count"), "integer", "v0_closure", case_status, "testboard_v0")
    )
    matrix_rows.append(
        _row("planned_only_case_count", cg, (v0_summary or {}).get("planned_only_case_count"), "integer", "v0_closure", case_status, "testboard_v0")
    )
    matrix_rows.append(
        _row(
            "not_fact_case_count",
            cg,
            (v0_summary or {}).get("case_count") if (v0_summary or {}).get("final_fact_status") == "not_fact" else 0,
            "integer",
            "v0_closure",
            case_status,
            "all_cases_not_fact",
        )
    )
    matrix_rows.append(
        _row(
            "no_write_case_count",
            cg,
            (v0_summary or {}).get("case_count") if (v0_summary or {}).get("final_write_status") == "no_write" else 0,
            "integer",
            "v0_closure",
            case_status,
            "all_cases_no_write",
        )
    )
    blocked_gate = 0
    if isinstance(gate_result, dict):
        results = gate_result.get("results") if isinstance(gate_result.get("results"), list) else []
        blocked_gate = sum(1 for r in results if isinstance(r, dict) and r.get("decision") == "hold_for_review")
    matrix_rows.append(
        _row(
            "blocked_by_gate_count",
            cg,
            blocked_gate,
            "integer",
            "gate_evaluator",
            "collected" if gate_result else "unavailable",
            "hold_for_review_decisions",
        )
    )

    risk_map = {
        "positive_text_case_covered": "positive_text_case_covered",
        "empty_text_case_covered": "empty_text_case_covered",
        "non_text_rejection_case_covered": "non_text_rejection_case_covered",
        "low_quality_text_case_covered": "low_quality_text_case_covered",
        "partial_text_case_covered": "partial_text_case_covered",
        "multi_line_text_case_covered": "multi_line_text_case_covered",
        "mixed_language_case_covered": "mixed_language_text_case_covered",
        "false_positive_visual_roi_case_covered": "false_positive_visual_roi_case_covered",
        "duplicate_text_case_covered": "duplicate_text_case_covered",
        "conflicting_text_case_covered": "conflicting_text_case_covered",
    }
    for metric, key in risk_map.items():
        val = (v0_risk or {}).get(key) if v0_risk else None
        matrix_rows.append(
            _row(metric, "Risk Coverage Metrics", val, "boolean", "v0_risk_coverage", "collected" if v0_risk else "unavailable", "coverage_flag_only")
        )

    viol = _boundary_violations(v0_boundary if isinstance(v0_boundary, dict) else None)
    total_cases = int((v0_summary or {}).get("case_count") or 0)
    boundary_ok = (v0_boundary or {}).get("boundary_all_ok") is True and sum(viol.values()) == 0
    pass_rate = 1.0 if boundary_ok and total_cases > 0 else (1.0 if boundary_ok else None)
    for vk, vv in viol.items():
        matrix_rows.append(_row(vk, "Boundary Metrics", vv, "integer", "v0_boundary_matrix", "collected", "must_be_zero"))
    matrix_rows.append(
        _row(
            "no_write_boundary_pass_rate",
            "Boundary Metrics",
            pass_rate,
            "float",
            "v0_boundary_matrix",
            "collected",
            "must_equal_1_for_go",
        )
    )

    poster_text = _read_json(poster / "poster_text_region_candidates.json")
    poster_non = _read_json(poster / "poster_non_text_region_candidates.json")
    poster_vis = _read_json(poster / "poster_visual_symbol_candidates.json")
    poster_plan = _read_json(poster / "poster_ocr_region_plan.json")
    poster_read = _read_json(poster / "poster_reading_order_candidate.json")
    text_n = int((poster_text or {}).get("candidate_count") or 0)
    non_n = int((poster_non or {}).get("candidate_count") or 0)
    vis_n = int((poster_vis or {}).get("candidate_count") or 0)
    plan_n = len((poster_plan or {}).get("planned_regions") or [])
    read_low = 1 if (poster_read or {}).get("reading_order_confidence") == "low" else 0
    pstatus = "collected" if poster_summary else "unavailable"
    pg = "Poster Layout Metrics"
    matrix_rows.append(_row("poster_image_count", pg, 1 if poster_summary else 0, "integer", "poster_governance", pstatus, "synthetic_fixture"))
    matrix_rows.append(_row("poster_like_detected_count", pg, 1 if (poster_summary or {}).get("image_type") == "poster_like" else 0, "integer", "poster_governance", pstatus, "poster_like"))
    matrix_rows.append(_row("full_image_ocr_forbidden_count", pg, 1 if (poster_summary or {}).get("full_image_ocr_allowed") is False else 0, "integer", "poster_governance", pstatus, "compliance"))
    matrix_rows.append(_row("segment_first_required_count", pg, 1 if (poster_summary or {}).get("ocr_strategy") == "segment_first" else 0, "integer", "poster_governance", pstatus, "compliance"))
    matrix_rows.append(_row("text_region_count", pg, text_n, "integer", "poster_text_regions", pstatus, "layout_governance"))
    matrix_rows.append(_row("non_text_region_count", pg, non_n, "integer", "poster_non_text_regions", pstatus, "layout_governance"))
    matrix_rows.append(_row("visual_symbol_region_count", pg, vis_n, "integer", "poster_visual_symbols", pstatus, "layout_governance"))
    matrix_rows.append(_row("ocr_region_plan_count", pg, plan_n, "integer", "poster_ocr_region_plan", pstatus, "text_regions_only"))
    matrix_rows.append(_row("reading_order_low_confidence_count", pg, read_low, "integer", "poster_reading_order", pstatus, "low_confidence_stub"))
    matrix_rows.append(_row("visual_symbol_split_count", pg, vis_n, "integer", "poster_visual_symbols", pstatus, "split_from_ocr_text_chain"))

    ref_count = int((ref_cands or {}).get("reference_count") or (ref_summary or {}).get("matched_reference_count") or 0)
    fg = "Reference / Fusion Metrics"
    matrix_rows.append(
        _row(
            "reference_candidate_count",
            fg,
            ref_count,
            "integer",
            "reference_only_rapidocr",
            "collected" if ref_count else "unavailable",
            "not_fact_candidates",
        )
    )
    matrix_rows.append(
        _row(
            "fusion_candidate_count",
            fg,
            int((fusion_summary or {}).get("fusion_candidate_count") or 0),
            "integer",
            "fusion_dryrun",
            "collected" if fusion_summary else "unavailable",
            "dryrun_only",
        )
    )
    matrix_rows.append(
        _row(
            "review_queue_count",
            fg,
            int(
                (review_summary or {}).get("queue_item_count")
                or (review_summary or {}).get("pending_review_count")
                or 0
            ),
            "integer",
            "fusion_review_queue",
            "collected" if review_summary else "unavailable",
            "optional_lineage",
        )
    )
    matrix_rows.append(
        _row(
            "ai_interpretation_dryrun_count",
            fg,
            int((ai_summary or {}).get("interpretation_count") or (ai_summary or {}).get("candidate_count") or 0),
            "integer",
            "ai_interpretation_dryrun",
            "collected" if ai_summary else "unavailable",
            "optional_lineage",
        )
    )
    matrix_rows.append(
        _row(
            "scene_delta_candidate_dryrun_count",
            fg,
            int((sd_summary or {}).get("candidate_count") or 0),
            "integer",
            "scene_delta_candidate_dryrun",
            "collected" if sd_summary else "unavailable",
            "dryrun_only",
        )
    )
    matrix_rows.append(
        _row(
            "gate_hold_for_review_count",
            fg,
            blocked_gate,
            "integer",
            "gate_evaluator",
            "collected" if gate_result else "unavailable",
            "hold_for_review",
        )
    )
    exec_blocked_n = 1 if isinstance(exec_blocked, dict) and exec_blocked.get("execution_status") == "blocked_by_gate" else 0
    matrix_rows.append(
        _row(
            "executor_blocked_by_gate_count",
            fg,
            exec_blocked_n,
            "integer",
            "executor_trace_stub",
            "collected" if exec_blocked else "unavailable",
            "blocked_by_gate",
        )
    )

    perf = "Performance Placeholder Metrics"
    matrix_rows.append(_row("performance_metrics_available", perf, False, "boolean", "schema_default", "collected", "placeholder_not_measured"))
    matrix_rows.append(_row("per_case_latency_ms", perf, None, "object", "future_collector", "unavailable", "not_collected_in_smoke"))
    matrix_rows.append(_row("per_provider_latency_ms", perf, None, "object", "future_collector", "unavailable", "not_collected_in_smoke"))
    matrix_rows.append(_row("total_pipeline_latency_ms", perf, None, "float", "future_collector", "unavailable", "not_collected_in_smoke"))

    collected = sum(1 for r in matrix_rows if r.get("source_status") == "collected")
    missing_metric = sum(1 for r in matrix_rows if r.get("source_status") == "unavailable" and r.get("value") is None)

    value_matrix = {
        "schema_version": VALUE_MATRIX_SCHEMA,
        "row_count": len(matrix_rows),
        "rows": matrix_rows,
    }

    missing_report = {
        "schema_version": MISSING_SCHEMA,
        "source_count": len(missing_sources),
        "sources": missing_sources,
        "critical_missing": [
            s["source_name"] for s in missing_sources if not s["exists"] and s["source_name"] in critical_missing_names
        ],
    }

    boundary_report = {
        "schema_version": BOUNDARY_REPORT_SCHEMA,
        "no_write_boundary_pass_rate": pass_rate,
        "violation_counts": viol,
        "violation_sources": ["testboard_v0_no_write_boundary_matrix"],
        "boundary_status": "pass" if pass_rate == 1.0 else "fail",
        "boundary_all_ok": (v0_boundary or {}).get("boundary_all_ok"),
    }

    poster_report = {
        "schema_version": POSTER_REPORT_SCHEMA,
        "full_image_ocr_allowed": (poster_summary or {}).get("full_image_ocr_allowed"),
        "ocr_strategy": (poster_summary or {}).get("ocr_strategy"),
        "text_region_count": text_n,
        "non_text_region_count": non_n,
        "visual_symbol_region_count": vis_n,
        "ocr_region_plan_count": plan_n,
        "reading_order_confidence": (poster_read or {}).get("reading_order_confidence"),
        "force_semantic_join_allowed": (poster_read or {}).get("force_semantic_join_allowed"),
        "poster_governance_root": str(poster),
    }

    guard = {
        "schema_version": GUARD_SCHEMA,
        "metrics_are_not_benchmark": True,
        "metrics_do_not_approve_candidate": True,
        "metrics_do_not_select_provider": True,
        "metrics_do_not_drive_navigation": True,
        "empty_text_case_type_dependent": True,
        "no_write_boundary_required_for_go": True,
    }

    audit = {
        "schema_version": AUDIT_SCHEMA,
        "cross_modal_testboard_metrics_collector_executed": True,
        "readonly_collection": True,
        "runtime_execution": False,
        "ocr_invoked": False,
        "vision_provider_invoked": False,
        "rapidocr_invoked": False,
        "paddleocr_invoked": False,
        "yolo_invoked": False,
        "vlm_invoked": False,
        "ai_interpretation_invoked": False,
        "benchmark_result_claimed": False,
        "model_selection_claimed": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
    }

    phase_verdict = "GO"
    if errs:
        phase_verdict = "NO_GO"
    elif any(not s["exists"] for s in missing_sources if s["source_name"] in ("rapidocr_submission", "fusion_dryrun")):
        phase_verdict = "CONDITIONAL_GO"
    if pass_rate != 1.0:
        phase_verdict = "NO_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": PHASE_ID,
        "collection_scope": "readonly_smoke",
        "schema_root": str(schema_p),
        "source_root_count": 8,
        "metrics_collected_count": collected,
        "missing_metric_count": missing_metric,
        "runtime_execution": False,
        "ocr_invoked": False,
        "vision_provider_invoked": False,
        "benchmark_result_claimed": False,
        "model_selection_claimed": False,
        "phase_verdict_hint": phase_verdict,
        "errors": list(errs),
    }

    return summary, value_matrix, missing_report, boundary_report, poster_report, guard, audit, errs
