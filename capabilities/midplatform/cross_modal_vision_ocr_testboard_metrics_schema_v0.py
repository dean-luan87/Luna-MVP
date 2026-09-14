# -*- coding: utf-8 -*-
"""CrossModal Vision-OCR TestBoard metrics schema (definition only, no collection).

Phase-CrossModal-Vision-OCR-TestBoard-Metrics-Schema-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "CrossModal-Vision-OCR-TestBoard-Metrics-Schema-001"

SUMMARY_SCHEMA = "cross_modal_vision_ocr_testboard_metrics_schema_summary_v0"
METRICS_SCHEMA = "cross_modal_vision_ocr_testboard_metrics_schema_v0"
DEFINITION_MATRIX_SCHEMA = "cross_modal_vision_ocr_testboard_metrics_definition_matrix_v0"
SOURCE_MAP_SCHEMA = "cross_modal_vision_ocr_testboard_metrics_source_map_v0"
GATE_POLICY_SCHEMA = "cross_modal_vision_ocr_testboard_metrics_gate_policy_v0"
NON_CLAIMS_SCHEMA = "cross_modal_vision_ocr_testboard_metrics_non_claims_report_v0"
COLLECTOR_CONTRACT_SCHEMA = "cross_modal_vision_ocr_testboard_metrics_collector_contract_stub_v0"
AUDIT_SCHEMA = "cross_modal_vision_ocr_testboard_metrics_schema_audit_v0"


def _read_json(p: Path) -> Any:
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _metric_def(
    metric_name: str,
    metric_group: str,
    value_type: str,
    aggregation_method: str,
    source_artifact: str,
    required: bool,
    interpretation_rule: str,
    non_claims: str,
) -> Dict[str, Any]:
    return {
        "metric_name": metric_name,
        "metric_group": metric_group,
        "value_type": value_type,
        "aggregation_method": aggregation_method,
        "source_artifact": source_artifact,
        "required": required,
        "interpretation_rule": interpretation_rule,
        "non_claims": non_claims,
    }


def build_metrics_schema() -> Dict[str, Any]:
    return {
        "schema_version": METRICS_SCHEMA,
        "phase": PHASE_ID,
        "metric_groups": {
            "A_OCR_Output_Metrics": {
                "ocr_submission_count": {"value_type": "integer", "default": None},
                "ocr_success_count": {"value_type": "integer", "default": None},
                "ocr_failed_count": {"value_type": "integer", "default": None},
                "ocr_empty_text_count": {"value_type": "integer", "default": None},
                "ocr_non_empty_text_count": {"value_type": "integer", "default": None},
                "text_item_count_total": {"value_type": "integer", "default": None},
                "text_item_count_avg": {"value_type": "float", "default": None},
                "provider_distribution": {"value_type": "object", "default": {}},
                "fallback_to_stub_count": {"value_type": "integer", "default": None},
                "rapidocr_invoked_count": {"value_type": "integer", "default": None},
                "paddleocr_invoked_count": {"value_type": "integer", "default": None},
            },
            "B_Case_Outcome_Metrics": {
                "case_count": {"value_type": "integer", "default": None},
                "executed_case_count": {"value_type": "integer", "default": None},
                "planned_only_case_count": {"value_type": "integer", "default": None},
                "passed_case_count": {"value_type": "integer", "default": None},
                "conditional_case_count": {"value_type": "integer", "default": None},
                "failed_case_count": {"value_type": "integer", "default": None},
                "not_fact_case_count": {"value_type": "integer", "default": None},
                "no_write_case_count": {"value_type": "integer", "default": None},
                "blocked_by_gate_count": {"value_type": "integer", "default": None},
            },
            "C_Risk_Coverage_Metrics": {
                "positive_text_case_covered": {"value_type": "boolean", "default": None},
                "empty_text_case_covered": {"value_type": "boolean", "default": None},
                "non_text_rejection_case_covered": {"value_type": "boolean", "default": None},
                "low_quality_text_case_covered": {"value_type": "boolean", "default": None},
                "partial_text_case_covered": {"value_type": "boolean", "default": None},
                "multi_line_text_case_covered": {"value_type": "boolean", "default": None},
                "mixed_language_case_covered": {"value_type": "boolean", "default": None},
                "false_positive_visual_roi_case_covered": {"value_type": "boolean", "default": None},
                "duplicate_text_case_covered": {"value_type": "boolean", "default": None},
                "conflicting_text_case_covered": {"value_type": "boolean", "default": None},
            },
            "D_Boundary_Metrics": {
                "midplatform_fact_write_violation_count": {"value_type": "integer", "default": 0},
                "scene_delta_write_violation_count": {"value_type": "integer", "default": 0},
                "world_model_write_violation_count": {"value_type": "integer", "default": 0},
                "navigation_decision_violation_count": {"value_type": "integer", "default": 0},
                "auto_approval_violation_count": {"value_type": "integer", "default": 0},
                "executor_invocation_violation_count": {"value_type": "integer", "default": 0},
                "no_write_boundary_pass_rate": {"value_type": "float", "default": None},
            },
            "E_Poster_Layout_Metrics": {
                "poster_image_count": {"value_type": "integer", "default": None},
                "poster_like_detected_count": {"value_type": "integer", "default": None},
                "full_image_ocr_forbidden_count": {"value_type": "integer", "default": None},
                "segment_first_required_count": {"value_type": "integer", "default": None},
                "text_region_count": {"value_type": "integer", "default": None},
                "non_text_region_count": {"value_type": "integer", "default": None},
                "visual_symbol_region_count": {"value_type": "integer", "default": None},
                "ocr_region_plan_count": {"value_type": "integer", "default": None},
                "reading_order_low_confidence_count": {"value_type": "integer", "default": None},
                "visual_symbol_split_count": {"value_type": "integer", "default": None},
            },
            "F_Reference_Fusion_Metrics": {
                "reference_candidate_count": {"value_type": "integer", "default": None},
                "fusion_candidate_count": {"value_type": "integer", "default": None},
                "review_queue_count": {"value_type": "integer", "default": None},
                "ai_interpretation_dryrun_count": {"value_type": "integer", "default": None},
                "scene_delta_candidate_dryrun_count": {"value_type": "integer", "default": None},
                "gate_hold_for_review_count": {"value_type": "integer", "default": None},
                "executor_blocked_by_gate_count": {"value_type": "integer", "default": None},
            },
            "G_Performance_Placeholder_Metrics": {
                "per_case_latency_ms": {"value_type": "object", "default": {}},
                "per_provider_latency_ms": {"value_type": "object", "default": {}},
                "ocr_region_latency_ms": {"value_type": "object", "default": {}},
                "total_pipeline_latency_ms": {"value_type": "float", "default": None},
                "memory_usage_mb": {"value_type": "float", "default": None},
                "cpu_usage_percent": {"value_type": "float", "default": None},
                "gpu_usage_percent": {"value_type": "float", "default": None},
                "performance_metrics_available": {"value_type": "boolean", "default": False},
            },
        },
    }


def build_definition_matrix() -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []

    ocr_metrics = [
        ("ocr_submission_count", "count", "rapidocr_submission"),
        ("ocr_success_count", "count", "rapidocr_submission"),
        ("ocr_failed_count", "count", "rapidocr_submission"),
        ("ocr_empty_text_count", "count", "testboard_execution"),
        ("ocr_non_empty_text_count", "count", "testboard_execution"),
        ("text_item_count_total", "sum", "rapidocr_submission"),
        ("text_item_count_avg", "mean", "rapidocr_submission"),
        ("provider_distribution", "histogram", "rapidocr_submission"),
        ("fallback_to_stub_count", "count", "ocr_provider_selection"),
        ("rapidocr_invoked_count", "count", "rapidocr_submission"),
        ("paddleocr_invoked_count", "count", "rapidocr_submission"),
    ]
    for name, agg, src in ocr_metrics:
        interp = "evaluation_only_submission_count"
        if name == "ocr_empty_text_count":
            interp = "case_type_dependent_empty_text_not_always_failure"
        rows.append(
            _metric_def(
                name,
                "OCR Output Metrics",
                "integer" if agg != "histogram" and agg != "mean" else ("object" if agg == "histogram" else "float"),
                agg,
                src,
                True,
                interp,
                "Not a model quality benchmark score.",
            )
        )

    case_metrics = [
        ("case_count", "count", "testboard_v0_closure"),
        ("executed_case_count", "count", "testboard_v0_closure"),
        ("planned_only_case_count", "count", "testboard_v0_closure"),
        ("passed_case_count", "count", "testboard_execution"),
        ("conditional_case_count", "count", "testboard_execution"),
        ("failed_case_count", "count", "testboard_execution"),
        ("not_fact_case_count", "count", "testboard_v0_closure"),
        ("no_write_case_count", "count", "testboard_v0_closure"),
        ("blocked_by_gate_count", "count", "gate_evaluator"),
    ]
    for name, agg, src in case_metrics:
        rows.append(
            _metric_def(
                name,
                "Case Outcome Metrics",
                "integer",
                agg,
                src,
                True,
                "testboard_case_outcome_not_production_verdict",
                "Does not authorize navigation or auto-approve.",
            )
        )

    risk_metrics = [
        ("positive_text_case_covered", "POSITIVE_TEXT_CLEAR"),
        ("empty_text_case_covered", "EMPTY_TEXT_ROI"),
        ("non_text_rejection_case_covered", "NON_TEXT_ROI_REJECTED"),
        ("low_quality_text_case_covered", "LOW_QUALITY_TEXT"),
        ("partial_text_case_covered", "PARTIAL_TEXT"),
        ("multi_line_text_case_covered", "MULTI_TEXT_LINES"),
        ("mixed_language_case_covered", "MIXED_CN_EN"),
        ("false_positive_visual_roi_case_covered", "FALSE_POSITIVE_VISUAL_ROI"),
        ("duplicate_text_case_covered", "DUPLICATE_TEXT_ROI"),
        ("conflicting_text_case_covered", "CONFLICTING_TEXT_ROI"),
    ]
    for name, case_type in risk_metrics:
        rows.append(
            _metric_def(
                name,
                "Risk Coverage Metrics",
                "boolean",
                "presence",
                "testboard_v0_closure",
                True,
                f"coverage_for_case_type_{case_type}",
                "Coverage flag only; not risk elimination proof.",
            )
        )

    boundary_metrics = [
        ("midplatform_fact_write_violation_count", "count", "must_be_zero"),
        ("scene_delta_write_violation_count", "count", "must_be_zero"),
        ("world_model_write_violation_count", "count", "must_be_zero"),
        ("navigation_decision_violation_count", "count", "must_be_zero"),
        ("auto_approval_violation_count", "count", "must_be_zero"),
        ("executor_invocation_violation_count", "count", "must_be_zero"),
        ("no_write_boundary_pass_rate", "ratio", "must_equal_1_for_go"),
    ]
    for name, agg, interp in boundary_metrics:
        rows.append(
            _metric_def(
                name,
                "Boundary Metrics",
                "integer" if "rate" not in name else "float",
                agg,
                "testboard_audit",
                True,
                interp,
                "Boundary audit only; not production compliance certification.",
            )
        )

    poster_metrics = [
        ("poster_image_count", "count", "poster_governance"),
        ("poster_like_detected_count", "count", "poster_governance"),
        ("full_image_ocr_forbidden_count", "count", "poster_governance_compliance_signal"),
        ("segment_first_required_count", "count", "poster_governance"),
        ("text_region_count", "count", "poster_governance"),
        ("non_text_region_count", "count", "poster_governance"),
        ("visual_symbol_region_count", "count", "poster_governance"),
        ("ocr_region_plan_count", "count", "poster_governance"),
        ("reading_order_low_confidence_count", "count", "poster_governance"),
        ("visual_symbol_split_count", "count", "poster_governance"),
    ]
    for name, agg, interp in poster_metrics:
        rows.append(
            _metric_def(
                name,
                "Poster Layout Metrics",
                "integer",
                agg,
                "poster_layout_governance",
                True,
                interp,
                "Separates layout governance from OCR execution metrics.",
            )
        )

    fusion_metrics = [
        ("reference_candidate_count", "cross_modal_reference_only"),
        ("fusion_candidate_count", "fusion_dryrun"),
        ("review_queue_count", "fusion_review_queue"),
        ("ai_interpretation_dryrun_count", "ai_interpretation_dryrun"),
        ("scene_delta_candidate_dryrun_count", "scene_delta_candidate_dryrun"),
        ("gate_hold_for_review_count", "gate_evaluator"),
        ("executor_blocked_by_gate_count", "executor_trace_stub"),
    ]
    for name, src in fusion_metrics:
        rows.append(
            _metric_def(
                name,
                "Reference / Fusion Metrics",
                "integer",
                "count",
                src,
                False,
                "dryrun_candidate_count_not_fact",
                "Candidates are not facts; metrics do not approve writes.",
            )
        )

    perf_metrics = [
        "per_case_latency_ms",
        "per_provider_latency_ms",
        "ocr_region_latency_ms",
        "total_pipeline_latency_ms",
        "memory_usage_mb",
        "cpu_usage_percent",
        "gpu_usage_percent",
        "performance_metrics_available",
    ]
    for name in perf_metrics:
        rows.append(
            _metric_def(
                name,
                "Performance Placeholder Metrics",
                "boolean" if name == "performance_metrics_available" else ("object" if "latency" in name else "float"),
                "placeholder",
                "future_collector",
                False,
                "performance_metrics_available_defaults_false_until_collector",
                "No production performance promise.",
            )
        )

    return {"schema_version": DEFINITION_MATRIX_SCHEMA, "row_count": len(rows), "rows": rows}


def build_source_map(
    *,
    v0_closure_root: Path,
    v1_planning_root: Path,
    poster_governance_root: Path,
) -> Dict[str, Any]:
    ws = v0_closure_root.parent.parent if v0_closure_root.name.startswith("_eval") else v0_closure_root.parent
    sources = [
        {
            "source_id": "testboard_v0_closure",
            "artifact_name": "TestBoard v0 closure",
            "expected_path": str(v0_closure_root / "cross_modal_vision_ocr_testboard_v0_closure_summary.json"),
            "metrics_extracted": [
                "case_count",
                "executed_case_count",
                "planned_only_case_count",
                "not_fact_case_count",
                "no_write_case_count",
            ]
            + [f"{c}_case_covered" for c in (
                "positive_text",
                "empty_text",
                "non_text_rejection",
                "low_quality_text",
                "partial_text",
                "multi_line_text",
                "mixed_language",
                "false_positive_visual_roi",
                "duplicate_text",
                "conflicting_text",
            )],
            "missing_behavior": "mark_metric_unavailable",
        },
        {
            "source_id": "testboard_v1_planning",
            "artifact_name": "TestBoard v1 planning",
            "expected_path": str(v1_planning_root / "cross_modal_vision_ocr_testboard_v1_planning_summary.json"),
            "metrics_extracted": ["v1_scope_locked", "track_count"],
            "missing_behavior": "mark_metric_unavailable",
        },
        {
            "source_id": "poster_layout_governance",
            "artifact_name": "Poster layout governance",
            "expected_path": str(poster_governance_root / "poster_layout_governance_summary.json"),
            "metrics_extracted": [
                "poster_image_count",
                "poster_like_detected_count",
                "full_image_ocr_forbidden_count",
                "segment_first_required_count",
                "text_region_count",
                "non_text_region_count",
                "visual_symbol_region_count",
                "ocr_region_plan_count",
                "reading_order_low_confidence_count",
                "visual_symbol_split_count",
            ],
            "missing_behavior": "mark_poster_metrics_unavailable",
        },
        {
            "source_id": "rapidocr_submission",
            "artifact_name": "RapidOCR submission from Vision ROI",
            "expected_path": str(ws / "_eval_out/rapidocr_submission_from_vision_roi_smoke_v0/rapidocr_submission_from_vision_roi_summary.json"),
            "metrics_extracted": [
                "ocr_submission_count",
                "ocr_success_count",
                "ocr_failed_count",
                "ocr_empty_text_count",
                "ocr_non_empty_text_count",
                "rapidocr_invoked_count",
                "provider_distribution",
            ],
            "missing_behavior": "mark_metric_unavailable",
        },
        {
            "source_id": "ocr_readonly_consumer",
            "artifact_name": "OCR evidence readonly consumer",
            "expected_path": str(ws / "_eval_out/ocr_evidence_readonly_consumer_smoke_v0/ocr_evidence_readonly_consumer_summary.json"),
            "metrics_extracted": ["text_item_count_total"],
            "missing_behavior": "mark_metric_unavailable",
        },
        {
            "source_id": "cross_modal_reference_only",
            "artifact_name": "CrossModal reference-only",
            "expected_path": str(ws / "_eval_out/cross_modal_vision_ocr_reference_only_smoke_v0/cross_modal_vision_ocr_reference_only_summary.json"),
            "metrics_extracted": ["reference_candidate_count"],
            "missing_behavior": "mark_metric_unavailable",
        },
        {
            "source_id": "fusion_dryrun",
            "artifact_name": "Fusion candidate dry-run",
            "expected_path": str(ws / "_eval_out/cross_modal_vision_ocr_fusion_candidate_dryrun_smoke_v0/cross_modal_vision_ocr_fusion_candidate_dryrun_summary.json"),
            "metrics_extracted": ["fusion_candidate_count"],
            "missing_behavior": "mark_metric_unavailable",
        },
        {
            "source_id": "gate_evaluator",
            "artifact_name": "Scene Delta gate evaluator dry-run",
            "expected_path": str(ws / "_eval_out/cross_modal_scene_delta_gate_evaluator_dryrun_smoke_v0/cross_modal_scene_delta_gate_evaluator_dryrun_summary.json"),
            "metrics_extracted": ["gate_hold_for_review_count", "blocked_by_gate_count"],
            "missing_behavior": "mark_metric_unavailable",
        },
        {
            "source_id": "executor_trace_stub",
            "artifact_name": "Scene Delta executor trace stub",
            "expected_path": str(ws / "_eval_out/cross_modal_scene_delta_executor_trace_stub_smoke_v0/cross_modal_scene_delta_executor_trace_stub_summary.json"),
            "metrics_extracted": ["executor_blocked_by_gate_count"],
            "missing_behavior": "mark_metric_unavailable",
        },
    ]
    return {"schema_version": SOURCE_MAP_SCHEMA, "source_count": len(sources), "sources": sources}


def build_gate_policy() -> Dict[str, Any]:
    return {
        "schema_version": GATE_POLICY_SCHEMA,
        "metrics_do_not_write_fact": True,
        "metrics_do_not_approve_candidate": True,
        "metrics_do_not_drive_navigation": True,
        "metrics_do_not_replace_policy_review": True,
        "benchmark_claim_allowed": False,
        "performance_claim_allowed": False,
        "model_selection_claim_allowed": False,
    }


def build_non_claims_report() -> Dict[str, Any]:
    return {
        "schema_version": NON_CLAIMS_SCHEMA,
        "explicit_non_claims": [
            "This phase does not produce actual benchmark numeric results.",
            "Does not compare provider superiority.",
            "Does not evaluate OCR accuracy.",
            "Does not evaluate real-video performance.",
            "Does not promise production performance.",
            "Does not serve as model admission gate.",
            "Does not change TestBoard v0/v1 chain behavior.",
        ],
    }


def build_collector_contract_stub() -> Dict[str, Any]:
    return {
        "schema_version": COLLECTOR_CONTRACT_SCHEMA,
        "phase_hint": "Phase-CrossModal-Vision-OCR-TestBoard-Metrics-Collector-Smoke-001",
        "implementation_status": "stub_only",
        "inputs": {
            "metrics_schema": "cross_modal_vision_ocr_testboard_metrics_schema.json",
            "source_roots": {
                "testboard_v0_closure_root": "absolute path",
                "testboard_v1_planning_root": "absolute path",
                "poster_governance_root": "absolute path",
                "optional_chain_smoke_roots": "map of source_id -> path",
            },
            "artifact_map": "cross_modal_vision_ocr_testboard_metrics_source_map.json",
        },
        "outputs": {
            "metrics_collection_summary": "cross_modal_vision_ocr_testboard_metrics_collection_summary.json",
            "metrics_value_matrix": "cross_modal_vision_ocr_testboard_metrics_value_matrix.json",
            "missing_artifact_report": "cross_modal_vision_ocr_testboard_metrics_missing_artifact_report.json",
            "boundary_metrics_report": "cross_modal_vision_ocr_testboard_boundary_metrics_report.json",
            "metrics_audit_report": "cross_modal_vision_ocr_testboard_metrics_audit_report.json",
        },
        "constraints": {
            "ocr_re_run_allowed": False,
            "fact_write_allowed": False,
            "benchmark_verdict_allowed": False,
        },
    }


def build_audit() -> Dict[str, Any]:
    return {
        "schema_version": AUDIT_SCHEMA,
        "cross_modal_testboard_metrics_schema_executed": True,
        "schema_only": True,
        "runtime_execution": False,
        "ocr_invoked": False,
        "vision_provider_invoked": False,
        "rapidocr_invoked": False,
        "paddleocr_invoked": False,
        "yolo_invoked": False,
        "vlm_invoked": False,
        "ai_interpretation_invoked": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
    }


def build_summary(
    *,
    v0_closure_root: Path,
    v1_planning_root: Path,
    poster_governance_root: Path,
) -> Dict[str, Any]:
    return {
        "schema_version": SUMMARY_SCHEMA,
        "phase": PHASE_ID,
        "metrics_scope": "schema_only",
        "based_on_v1_planning": v1_planning_root.is_dir(),
        "based_on_poster_governance": poster_governance_root.is_dir(),
        "based_on_v0_closure": v0_closure_root.is_dir(),
        "v0_closure_root": str(v0_closure_root),
        "v1_planning_root": str(v1_planning_root),
        "poster_governance_root": str(poster_governance_root),
        "runtime_execution": False,
        "ocr_invoked": False,
        "vision_provider_invoked": False,
        "benchmark_result_claimed": False,
    }


def run_cross_modal_vision_ocr_testboard_metrics_schema_v0(
    *,
    v0_closure_root: str,
    v1_planning_root: str,
    poster_governance_root: str,
) -> Tuple[
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
    v1 = Path(v1_planning_root).resolve()
    poster = Path(poster_governance_root).resolve()

    if not _read_json(v0 / "cross_modal_vision_ocr_testboard_v0_closure_summary.json"):
        errs.append("missing_v0_closure_summary")
    if not _read_json(v1 / "cross_modal_vision_ocr_testboard_v1_planning_summary.json"):
        errs.append("missing_v1_planning_summary")
    if not _read_json(poster / "poster_layout_governance_summary.json"):
        errs.append("missing_poster_governance_summary")

    summary = build_summary(v0_closure_root=v0, v1_planning_root=v1, poster_governance_root=poster)
    schema = build_metrics_schema()
    matrix = build_definition_matrix()
    source_map = build_source_map(
        v0_closure_root=v0,
        v1_planning_root=v1,
        poster_governance_root=poster,
    )
    gate = build_gate_policy()
    non_claims = build_non_claims_report()
    collector = build_collector_contract_stub()
    audit = build_audit()

    phase_verdict = "GO" if not errs else "CONDITIONAL_GO"
    summary["phase_verdict_hint"] = phase_verdict
    summary["errors"] = list(errs)

    return summary, schema, matrix, source_map, gate, non_claims, collector, audit, errs
