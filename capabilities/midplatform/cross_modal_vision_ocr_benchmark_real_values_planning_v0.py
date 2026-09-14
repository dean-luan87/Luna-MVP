# -*- coding: utf-8 -*-
"""Benchmark Collector real values planning (read-only, no collection).

Phase-CrossModal-Vision-OCR-TestBoard-Benchmark-Collector-Real-Values-Planning-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

PHASE_ID = "CrossModal-Vision-OCR-TestBoard-Benchmark-Collector-Real-Values-Planning-001"

SUMMARY_SCHEMA = "cross_modal_vision_ocr_benchmark_real_values_planning_summary_v0"
TIER_MATRIX_SCHEMA = "cross_modal_vision_ocr_benchmark_metric_tier_matrix_v0"
SOURCE_MAP_SCHEMA = "cross_modal_vision_ocr_benchmark_real_values_source_map_v0"
GATE_POLICY_SCHEMA = "cross_modal_vision_ocr_benchmark_collector_gate_policy_v0"
INTERP_POLICY_SCHEMA = "cross_modal_vision_ocr_benchmark_metric_interpretation_policy_v0"
GT_REPORT_SCHEMA = "cross_modal_vision_ocr_benchmark_ground_truth_requirement_report_v0"
SIM_BINDING_SCHEMA = "cross_modal_vision_ocr_benchmark_simulation_profile_binding_plan_v0"
OUTPUT_CONTRACT_SCHEMA = "cross_modal_vision_ocr_benchmark_real_values_collector_output_contract_v0"
REGRESSION_LINK_SCHEMA = "cross_modal_vision_ocr_benchmark_regression_link_report_v0"
NON_CLAIMS_SCHEMA = "cross_modal_vision_ocr_benchmark_non_claims_report_v0"
FOLLOWUPS_SCHEMA = "cross_modal_vision_ocr_benchmark_open_followups_v0"
AUDIT_SCHEMA = "cross_modal_vision_ocr_benchmark_real_values_planning_audit_v0"


def _read_json(p: Path) -> Any:
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _bool(v: Any, default: bool = False) -> bool:
    if v is None:
        return default
    return bool(v)


def _source_ok(root: Path, summary_name: str) -> Tuple[bool, str]:
    sm = _read_json(root / summary_name)
    if not sm:
        return False, "missing_summary"
    hint = str(sm.get("phase_verdict_hint") or sm.get("verdict") or "").upper()
    if sm.get("bootstrap_only"):
        return True, "bootstrap_ok"
    if hint in ("GO", "CONDITIONAL_GO") and not (sm.get("errors") or []):
        return True, hint
    if hint in ("GO", "CONDITIONAL_GO"):
        return True, hint
    return False, hint or "NO_GO"


def _metric_row(
    metric_name: str,
    tier: str,
    *,
    allowed_real: bool,
    allowed_smoke: bool,
    requires_gt: bool,
    requires_sim: bool,
    interpretation_rule: str,
    non_claims: str,
) -> Dict[str, Any]:
    return {
        "metric_name": metric_name,
        "tier": tier,
        "allowed_in_real_values_collector": allowed_real,
        "allowed_in_smoke_collector": allowed_smoke,
        "requires_ground_truth": requires_gt,
        "requires_simulation_profile": requires_sim,
        "interpretation_rule": interpretation_rule,
        "non_claims": non_claims,
    }


def build_metric_tier_matrix() -> Dict[str, Any]:
    t0 = [
        _metric_row(
            "no_write_boundary_pass_rate",
            "T0",
            allowed_real=True,
            allowed_smoke=True,
            requires_gt=False,
            requires_sim=False,
            interpretation_rule="Must remain 1.0; hard safety gate for any collector phase.",
            non_claims="Pass rate does not imply OCR quality or production readiness.",
        ),
        _metric_row(
            "fact_write_violation_count",
            "T0",
            allowed_real=True,
            allowed_smoke=True,
            requires_gt=False,
            requires_sim=False,
            interpretation_rule="Must be 0; any positive value is NO_GO.",
            non_claims="Count describes boundary audit only.",
        ),
        _metric_row(
            "scene_delta_write_violation_count",
            "T0",
            allowed_real=True,
            allowed_smoke=True,
            requires_gt=False,
            requires_sim=False,
            interpretation_rule="Must be 0.",
            non_claims="Not a Scene Delta readiness signal.",
        ),
        _metric_row(
            "world_model_write_violation_count",
            "T0",
            allowed_real=True,
            allowed_smoke=True,
            requires_gt=False,
            requires_sim=False,
            interpretation_rule="Must be 0.",
            non_claims="Not WorldModel write readiness.",
        ),
        _metric_row(
            "navigation_decision_violation_count",
            "T0",
            allowed_real=True,
            allowed_smoke=True,
            requires_gt=False,
            requires_sim=False,
            interpretation_rule="Must be 0.",
            non_claims="Not navigation capability proof.",
        ),
        _metric_row(
            "auto_approval_violation_count",
            "T0",
            allowed_real=True,
            allowed_smoke=True,
            requires_gt=False,
            requires_sim=False,
            interpretation_rule="Must be 0.",
            non_claims="Not approval policy certification.",
        ),
    ]
    t1 = [
        _metric_row("case_count", "T1", allowed_real=True, allowed_smoke=True, requires_gt=False, requires_sim=False,
                    interpretation_rule="Registry cardinality; not execution proof.",
                    non_claims="Registered cases are not executed cases."),
        _metric_row("executed_case_count", "T1", allowed_real=True, allowed_smoke=True, requires_gt=False, requires_sim=False,
                    interpretation_rule="Observed executor runs only when explicitly gated.",
                    non_claims="Execution count is not benchmark score."),
        _metric_row("planned_only_case_count", "T1", allowed_real=True, allowed_smoke=True, requires_gt=False, requires_sim=False,
                    interpretation_rule="Planned/reference-only cases; expected in v1 closure.",
                    non_claims="Planned-only is not failure by default."),
        _metric_row("ocr_submission_count", "T1", allowed_real=True, allowed_smoke=True, requires_gt=False, requires_sim=False,
                    interpretation_rule="Submission events when gated phase allows.",
                    non_claims="Submission is not OCR success."),
        _metric_row("ocr_success_count", "T1", allowed_real=True, allowed_smoke=True, requires_gt=False, requires_sim=False,
                    interpretation_rule="Transport/executor success; not text correctness.",
                    non_claims="Success is not accuracy."),
        _metric_row("ocr_empty_text_count", "T1", allowed_real=True, allowed_smoke=True, requires_gt=False, requires_sim=False,
                    interpretation_rule="Empty text allowed by case_type; interpret via policy.",
                    non_claims="Empty text is not always failure."),
        _metric_row("ocr_non_empty_text_count", "T1", allowed_real=True, allowed_smoke=True, requires_gt=False, requires_sim=False,
                    interpretation_rule="Non-empty output observed; not correctness proof.",
                    non_claims="Non-empty is not always correct."),
        _metric_row("reference_candidate_count", "T1", allowed_real=True, allowed_smoke=True, requires_gt=False, requires_sim=False,
                    interpretation_rule="Reference/ROI candidates from planning or bridge.",
                    non_claims="Candidates are not OCR evidence."),
        _metric_row("fusion_candidate_count", "T1", allowed_real=True, allowed_smoke=True, requires_gt=False, requires_sim=False,
                    interpretation_rule="Dry-run fusion candidates only when explicitly gated.",
                    non_claims="Fusion candidates are not Scene Delta facts."),
        _metric_row("gate_hold_count", "T1", allowed_real=True, allowed_smoke=True, requires_gt=False, requires_sim=False,
                    interpretation_rule="Gate holds are safety signals, not defects by default.",
                    non_claims="Hold count is not failure rate without context."),
    ]
    t2 = [
        _metric_row("text_recall_proxy", "T2", allowed_real=False, allowed_smoke=False, requires_gt=True, requires_sim=False,
                    interpretation_rule="Future benchmark only; requires labeled ground truth.",
                    non_claims="Proxy is not production OCR accuracy."),
        _metric_row("non_empty_text_rate_by_case_type", "T2", allowed_real=False, allowed_smoke=False, requires_gt=True, requires_sim=False,
                    interpretation_rule="Stratify by case_type; empty may be valid.",
                    non_claims="Rate is not quality score."),
        _metric_row("provider_latency_ms", "T2", allowed_real=False, allowed_smoke=False, requires_gt=False, requires_sim=True,
                    interpretation_rule="Provider path latency only; requires resource_report.",
                    non_claims="Provider latency is not end-to-end system latency."),
        _metric_row("per_case_latency_ms", "T2", allowed_real=False, allowed_smoke=False, requires_gt=False, requires_sim=True,
                    interpretation_rule="Per-case timing when executor runs under profile.",
                    non_claims="Not user-perceived latency."),
        _metric_row("memory_peak_mb", "T2", allowed_real=False, allowed_smoke=False, requires_gt=False, requires_sim=True,
                    interpretation_rule="From resource_report under simulation profile.",
                    non_claims="Not hardware certification."),
        _metric_row("cpu_peak_percent", "T2", allowed_real=False, allowed_smoke=False, requires_gt=False, requires_sim=True,
                    interpretation_rule="From resource_report; profile-bound.",
                    non_claims="Not fleet-wide capacity proof."),
        _metric_row("crash_count", "T2", allowed_real=False, allowed_smoke=False, requires_gt=False, requires_sim=True,
                    interpretation_rule="Crash recovery profile later; manual trigger.",
                    non_claims="Crash count is not provider ranking."),
        _metric_row("timeout_count", "T2", allowed_real=False, allowed_smoke=False, requires_gt=False, requires_sim=True,
                    interpretation_rule="Deadline/stress profiles later.",
                    non_claims="Timeouts are not automatic NO_GO without case context."),
        _metric_row("provider_error_count", "T2", allowed_real=False, allowed_smoke=False, requires_gt=False, requires_sim=True,
                    interpretation_rule="Provider path errors; distribution only.",
                    non_claims="Error count is not provider quality ranking."),
    ]
    rows = t0 + t1 + t2
    return {
        "schema_version": TIER_MATRIX_SCHEMA,
        "tier_definitions": {
            "T0": "Boundary Metrics — hard safety thresholds; GO depends on pass.",
            "T1": "Functional Smoke Metrics — chain observation; not quality benchmark.",
            "T2": "Quality/Performance Benchmark Metrics — future only; no values in this phase.",
        },
        "row_count": len(rows),
        "tiers_present": ["T0", "T1", "T2"],
        "rows": rows,
    }


def build_real_values_source_map() -> Dict[str, Any]:
    def src(
        source_name: str,
        expected_artifact: str,
        metrics_allowed: List[str],
        metrics_forbidden: List[str],
        required_before_collection: List[str],
        missing_behavior: str,
    ) -> Dict[str, Any]:
        return {
            "source_name": source_name,
            "expected_artifact": expected_artifact,
            "metrics_allowed": metrics_allowed,
            "metrics_forbidden": metrics_forbidden,
            "required_before_collection": required_before_collection,
            "missing_behavior": missing_behavior,
        }

    rows = [
        src("ocr_submission_collection", "ocr_submission_trace.json", ["ocr_submission_count", "gate_hold_count"],
            ["text_recall_proxy", "provider_latency_ms"], ["explicit_ocr_submission_phase"], "record_missing_metric"),
        src("ocr_readonly_consumer", "ocr_evidence_readonly_bundle.json", ["ocr_success_count", "ocr_empty_text_count", "ocr_non_empty_text_count"],
            ["benchmark_score"], ["ocr_submission_collection"], "skip_quality_metrics"),
        src("crossmodal_reference", "cross_modal_roi_reference_matrix.json", ["reference_candidate_count"],
            ["ocr_submission_count"], ["v1_track_closures_go"], "use_reference_only_counts"),
        src("fusion_dry_run", "fusion_dry_run_report.json", ["fusion_candidate_count"],
            ["scene_delta_write_violation_count"], ["fusion_dry_run_phase"], "zero_fusion_candidates"),
        src("gate_evaluator", "gate_evaluation_report.json", ["gate_hold_count", "no_write_boundary_pass_rate"],
            ["model_selection_claim"], ["collector_gate_policy"], "hold_all_t2"),
        src("executor_trace_stub", "executor_trace_stub.json", ["executed_case_count", "per_case_latency_ms"],
            ["text_recall_proxy"], ["executor_contract"], "planned_only_fallback"),
        src("simulation_lab_summary", "simulation_summary.json", ["simulation_profile_id"],
            ["production_readiness_claim"], ["simulation_profile_binding_plan"], "reject_collection"),
        src("resource_report", "resource_report.json", ["memory_peak_mb", "cpu_peak_percent", "provider_latency_ms"],
            ["no_write_boundary_pass_rate"], ["simulation_profile_required"], "performance_metrics_unavailable"),
        src("audit_report", "audit_report.json", ["fact_write_violation_count", "scene_delta_write_violation_count"],
            ["benchmark_result_claimed"], ["audit_required"], "boundary_unknown_no_go"),
        src("testboard_case_registry", "case_registry.json", ["case_count", "planned_only_case_count"],
            ["executed_case_count"], ["case_registry_go"], "case_count_zero"),
        src("poster_closure", "poster_testboard_track_b_closure_summary.json", ["reference_candidate_count"],
            ["real_poster_ocr_claim"], ["poster_track_b_closed"], "poster_metrics_deferred"),
        src("public_facility_runtime", "public_facility_runtime_report.json", [],
            ["facility_semantic_correctness"], ["public_facility_runtime_phase"], "source_not_available"),
    ]
    return {"schema_version": SOURCE_MAP_SCHEMA, "row_count": len(rows), "rows": rows}


def build_collector_gate_policy() -> Dict[str, Any]:
    return {
        "schema_version": GATE_POLICY_SCHEMA,
        "real_values_collection_allowed": False,
        "future_real_values_collection_requires_explicit_phase": True,
        "benchmark_claim_allowed": False,
        "provider_comparison_allowed": False,
        "model_selection_allowed": False,
        "production_readiness_claim_allowed": False,
        "no_write_boundary_pass_rate_required": 1.0,
        "simulation_profile_required": True,
        "ground_truth_required_for_quality_metrics": True,
        "performance_metrics_require_resource_report": True,
        "smoke_vs_benchmark_separation_required": True,
        "performance_placeholder_auto_upgrade_forbidden": True,
    }


def build_metric_interpretation_policy() -> Dict[str, Any]:
    return {
        "schema_version": INTERP_POLICY_SCHEMA,
        "rules": {
            "empty_text_not_always_failure": True,
            "non_empty_text_not_always_correct": True,
            "rapidocr_invoked_not_quality_pass": True,
            "provider_latency_not_system_latency": True,
            "case_pass_not_world_generalization": True,
            "no_write_boundary_is_hard_safety": True,
            "benchmark_metrics_without_values_not_for_decisions": True,
            "smoke_collector_not_provider_selection": True,
        },
        "policies": [
            "empty_text: interpret by case_type; absence of text may be expected.",
            "non_empty_text: does not imply semantic correctness or ground-truth match.",
            "RapidOCR invoked: describes call path only; not quality certification.",
            "provider_latency_ms: provider path only; not navigation or fusion latency.",
            "case pass: testboard pass is not real-world generalization.",
            "no_write_boundary_pass_rate: must remain 1.0; any regression is NO_GO.",
            "T2 metrics without collected values must not drive model or routing decisions.",
            "smoke collector outputs must not be used for provider selection.",
        ],
    }


def build_ground_truth_requirement_report() -> Dict[str, Any]:
    rows = [
        {"metric_name": "text_recall_proxy", "requires_ground_truth": True, "status": "required"},
        {"metric_name": "cer", "requires_ground_truth": True, "status": "required_future"},
        {"metric_name": "wer", "requires_ground_truth": True, "status": "required_future"},
        {"metric_name": "character_accuracy", "requires_ground_truth": True, "status": "required_future"},
        {"metric_name": "correct_text_region_count", "requires_ground_truth": True, "status": "required"},
        {"metric_name": "false_positive_text_region_count", "requires_ground_truth": True, "status": "required"},
        {"metric_name": "facility_semantic_correctness", "requires_ground_truth": True, "status": "required_future"},
        {"metric_name": "poster_reading_order_correctness", "requires_ground_truth": True, "status": "required_future"},
    ]
    return {
        "schema_version": GT_REPORT_SCHEMA,
        "current_v1_has_ground_truth": False,
        "ocr_accuracy_computed": False,
        "benchmark_score_computed": False,
        "row_count": len(rows),
        "rows": rows,
        "interpretation": {
            "v1_reference_only": True,
            "no_accuracy_claim_in_v1": True,
            "future_collector_must_check_gt_availability": True,
        },
    }


def build_simulation_profile_binding_plan() -> Dict[str, Any]:
    profiles = [
        ("developer_full", ["case_count", "no_write_boundary_pass_rate", "gate_hold_count"], "baseline smoke context"),
        ("crash_recovery", ["crash_count", "provider_error_count"], "PaddleOCR / provider crash later"),
        ("low_memory_4gb", ["memory_peak_mb"], "memory pressure later"),
        ("long_run_1h", ["timeout_count"], "stability later"),
        ("stcm_deadline_stress", ["timeout_count", "gate_hold_count"], "timeout / deadline later"),
        ("vision_frame_delay", ["per_case_latency_ms"], "frame pipeline latency later"),
    ]
    rows = [
        {
            "profile_id": pid,
            "intended_metrics": metrics,
            "purpose": purpose,
            "run_model_default": False,
            "manual_trigger_required": True,
            "production_certification_claim": False,
        }
        for pid, metrics, purpose in profiles
    ]
    return {"schema_version": SIM_BINDING_SCHEMA, "row_count": len(rows), "profiles": rows}


def build_output_contract() -> Dict[str, Any]:
    return {
        "schema_version": OUTPUT_CONTRACT_SCHEMA,
        "current_phase_generates_values": False,
        "future_phase_required": True,
        "future_collector_artifacts": [
            "collection_summary",
            "metric_value_matrix",
            "missing_metric_report",
            "boundary_metrics_report",
            "source_artifact_matrix",
            "simulation_profile_report",
            "ground_truth_availability_report",
            "performance_metrics_report",
            "benchmark_non_claims_report",
            "collector_audit_report",
        ],
        "value_generation_rules": {
            "t0_required_before_t1_publish": True,
            "t2_requires_ground_truth_and_explicit_phase": True,
            "performance_requires_resource_report": True,
        },
    }


def build_regression_link_report(
    track_closures_root: Path,
    regression_root: Path,
) -> Dict[str, Any]:
    tc = _read_json(track_closures_root / "cross_modal_vision_ocr_testboard_v1_track_closures_summary.json") or {}
    carry = _read_json(track_closures_root / "cross_modal_vision_ocr_testboard_v1_regression_carryover_report.json") or {}
    bnd = _read_json(regression_root / "cross_modal_vision_ocr_testboard_v1_regression_boundary_comparison_matrix.json") or {}
    delta = _read_json(regression_root / "cross_modal_vision_ocr_testboard_v1_regression_delta_report.json") or {}
    return {
        "schema_version": REGRESSION_LINK_SCHEMA,
        "v1_track_closures_status": tc.get("v1_status") or "closed_for_evaluation",
        "regression_all_boundary_ok": _bool(bnd.get("all_boundary_ok"), True),
        "write_capability_added": _bool(delta.get("write_capability_added")),
        "production_readiness_added": _bool(delta.get("production_readiness_added")),
        "benchmark_added": _bool(delta.get("benchmark_added")),
        "no_write_boundary_pass_rate_inherited": 1.0,
        "interpretation": {
            "real_values_collector_extends_only_on_boundary_ok": True,
            "metric_collection_must_not_lower_no_write_boundary": True,
            "carryover_write_capability_added": carry.get("write_capability_added"),
        },
    }


def build_non_claims_report() -> Dict[str, Any]:
    return {
        "schema_version": NON_CLAIMS_SCHEMA,
        "not_benchmark_phase": True,
        "no_real_metric_values_collected": True,
        "no_ocr_or_vision_execution": True,
        "no_provider_comparison": True,
        "no_ocr_accuracy_generated": True,
        "no_performance_conclusion": True,
        "no_model_admission_conclusion": True,
        "no_production_readiness": True,
        "v1_closed_for_evaluation_unchanged": True,
        "no_fact_layer_write": True,
        "no_scene_delta_or_world_model": True,
    }


def build_open_followups() -> Dict[str, Any]:
    items = [
        "Benchmark Collector Real Values Smoke later",
        "OCR ground truth fixture registry",
        "RealVideo labeled samples",
        "Poster region ground truth",
        "PublicFacility semantic ground truth",
        "Simulation Lab crash recovery merge",
        "PaddleOCR heavy stress profile",
        "Performance metrics collector",
        "FailureAttributionMatrix",
        "Provider comparison governance",
        "Model selection gate",
        "Production readiness gate",
    ]
    return {"schema_version": FOLLOWUPS_SCHEMA, "items": items, "item_count": len(items)}


def build_audit() -> Dict[str, Any]:
    return {
        "schema_version": AUDIT_SCHEMA,
        "benchmark_real_values_planning_executed": True,
        "planning_only": True,
        "runtime_execution": False,
        "benchmark_values_collected": False,
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
    track_closures_ok: bool,
    regression_ok: bool,
    metrics_schema_ok: bool,
    smoke_collector_ok: bool,
    simulation_attached: bool,
) -> Dict[str, Any]:
    return {
        "schema_version": SUMMARY_SCHEMA,
        "phase": PHASE_ID,
        "planning_scope": "benchmark_real_values_planning_only",
        "based_on_v1_track_closures": track_closures_ok,
        "based_on_regression_comparison": regression_ok,
        "based_on_metrics_schema": metrics_schema_ok,
        "based_on_smoke_collector": smoke_collector_ok,
        "simulation_context_attached": simulation_attached,
        "runtime_execution": False,
        "ocr_invoked": False,
        "vision_provider_invoked": False,
        "benchmark_values_collected": False,
        "benchmark_result_claimed": False,
        "model_selection_claimed": False,
        "production_readiness_claimed": False,
        "write_allowed": False,
        "fact_status": "not_fact",
    }


def run_cross_modal_vision_ocr_benchmark_real_values_planning_v0(
    *,
    v1_track_closures_root: str,
    regression_comparison_root: str,
    metrics_schema_root: str,
    metrics_collector_smoke_root: str,
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
    tc_root = Path(v1_track_closures_root).resolve()
    reg_root = Path(regression_comparison_root).resolve()
    schema_root = Path(metrics_schema_root).resolve()
    coll_root = Path(metrics_collector_smoke_root).resolve()
    sim_root = Path(simulation_lab_harness_root).resolve()

    tc_ok, tc_hint = _source_ok(tc_root, "cross_modal_vision_ocr_testboard_v1_track_closures_summary.json")
    if not tc_ok:
        errs.append(f"track_closures_not_ok:{tc_hint}")
    tc_sm = _read_json(tc_root / "cross_modal_vision_ocr_testboard_v1_track_closures_summary.json") or {}
    if tc_sm.get("v1_status") != "closed_for_evaluation":
        errs.append("v1_status_not_closed_for_evaluation")

    reg_ok, reg_hint = _source_ok(reg_root, "cross_modal_vision_ocr_testboard_v1_regression_comparison_summary.json")
    if not reg_ok:
        errs.append(f"regression_not_ok:{reg_hint}")

    schema_ok, _ = _source_ok(schema_root, "cross_modal_vision_ocr_testboard_metrics_schema_summary.json")
    if not schema_ok:
        errs.append("metrics_schema_not_ok")

    coll_ok, _ = _source_ok(coll_root, "cross_modal_vision_ocr_testboard_metrics_collection_summary.json")
    if not coll_ok:
        errs.append("metrics_collector_smoke_not_ok")

    sim_attached = (sim_root / "simulation_summary.json").is_file()
    if not sim_attached:
        errs.append("simulation_summary_missing")

    tier_matrix = build_metric_tier_matrix()
    tiers = {r["tier"] for r in tier_matrix.get("rows") or []}
    if not {"T0", "T1", "T2"}.issubset(tiers):
        errs.append("metric_tiers_incomplete")

    source_map = build_real_values_source_map()
    gate_policy = build_collector_gate_policy()
    interp_policy = build_metric_interpretation_policy()
    gt_report = build_ground_truth_requirement_report()
    sim_plan = build_simulation_profile_binding_plan()
    output_contract = build_output_contract()
    regression_link = build_regression_link_report(tc_root, reg_root)
    non_claims = build_non_claims_report()
    followups = build_open_followups()
    audit = build_audit()

    if gate_policy.get("real_values_collection_allowed"):
        errs.append("gate_real_values_collection_allowed_true")
    if regression_link.get("v1_track_closures_status") != "closed_for_evaluation":
        errs.append("regression_link_v1_status_wrong")
    if not regression_link.get("regression_all_boundary_ok"):
        errs.append("regression_all_boundary_ok_false")

    summary = build_summary(
        track_closures_ok=tc_ok,
        regression_ok=reg_ok,
        metrics_schema_ok=schema_ok,
        smoke_collector_ok=coll_ok,
        simulation_attached=sim_attached,
    )

    return (
        summary,
        tier_matrix,
        source_map,
        gate_policy,
        interp_policy,
        gt_report,
        sim_plan,
        output_contract,
        regression_link,
        non_claims,
        followups,
        audit,
        errs,
    )
