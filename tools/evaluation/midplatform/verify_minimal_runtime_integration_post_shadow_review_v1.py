#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Minimal Runtime Integration Post Shadow Review v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

MIN_CHECKS = 80


def _require_abs(path_str: str, label: str) -> Path:
    p = Path(path_str).expanduser()
    if not p.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {path_str}")
    return p.resolve()


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    smoke_root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []
    checks_passed = 0

    def ok(cond: bool, name: str) -> None:
        nonlocal checks_passed
        if cond:
            checks_passed += 1
        else:
            blockers.append(name)

    files = {
        "summary": "summary.json",
        "input_root_matrix": "input_root_matrix.json",
        "post_shadow_review_report": "post_shadow_review_report.json",
        "shadow_trial_stability_review": "shadow_trial_stability_review.json",
        "boundary_weakness_review": "boundary_weakness_review.json",
        "source_chain_review": "source_chain_review.json",
        "abort_coverage_review": "abort_coverage_review.json",
        "handoff_readiness_review": "handoff_readiness_review.json",
        "controlled_output_readiness_decision": "controlled_output_readiness_decision.json",
        "risk_register": "risk_register.json",
        "next_phase_recommendation": "next_phase_recommendation.json",
        "no_runtime_boundary_report": "no_runtime_boundary_report.json",
        "no_write_boundary_report": "no_write_boundary_report.json",
    }

    data: Dict[str, Any] = {}
    for key, filename in files.items():
        path = smoke_root / filename
        if not path.is_file():
            blockers.append(f"missing:{key}")
        else:
            data[key] = json.loads(path.read_text(encoding="utf-8"))

    if blockers:
        report = {
            "verdict": "NO_GO",
            "checks_passed": 0,
            "checks_expected": MIN_CHECKS,
            "blockers": blockers,
            "phase": "Minimal-Runtime-Integration-Post-Shadow-Review-v1-001",
        }
        _write_json(smoke_root / "verifier_report.json", report)
        print(json.dumps(report, ensure_ascii=False))
        return 2

    summary = data["summary"]
    review_report = data["post_shadow_review_report"]
    stability = data["shadow_trial_stability_review"]
    boundary_review = data["boundary_weakness_review"]
    source_chain_review = data["source_chain_review"]
    abort_review = data["abort_coverage_review"]
    handoff_review = data["handoff_readiness_review"]
    readiness = data["controlled_output_readiness_decision"]
    risk_register = data["risk_register"]
    next_phase = data["next_phase_recommendation"]

    ok(summary.get("review_scope") == "minimal_runtime_integration_post_shadow_review_only", "review_scope")
    ok(summary.get("review_only") is True, "review_only")
    ok(summary.get("controlled_shadow_trial_input_loaded") is True, "controlled_shadow_trial_input_loaded")
    ok(summary.get("trial_definition_input_loaded") is True, "trial_definition_input_loaded")
    ok(summary.get("stabilization_input_loaded") is True, "stabilization_input_loaded")
    ok(summary.get("reviewed_input_case_count") == 8, "reviewed_input_case_count")
    ok(summary.get("reviewed_shadow_step_count") == 104, "reviewed_shadow_step_count")
    ok(summary.get("reviewed_candidate_trace_count") == 8, "reviewed_candidate_trace_count")
    ok(summary.get("reviewed_speech_gate_shadow_count") == 8, "reviewed_speech_gate_shadow_count")
    ok(summary.get("reviewed_vop_shadow_event_count") == 8, "reviewed_vop_shadow_event_count")
    ok(summary.get("reviewed_abort_check_count") == 8, "reviewed_abort_check_count")
    ok(summary.get("stability_review_completed") is True, "stability_review_completed")
    ok(summary.get("boundary_weakness_review_completed") is True, "boundary_weakness_review_completed")
    ok(summary.get("source_chain_review_completed") is True, "source_chain_review_completed")
    ok(summary.get("abort_coverage_review_completed") is True, "abort_coverage_review_completed")
    ok(summary.get("handoff_readiness_review_completed") is True, "handoff_readiness_review_completed")
    ok(
        summary.get("controlled_output_readiness_decision_generated") is True,
        "controlled_output_readiness_decision_generated",
    )
    ok(summary.get("boundary_weakness_found") is False, "boundary_weakness_found")
    ok(summary.get("source_chain_gap_found") is False, "source_chain_gap_found")
    ok(summary.get("abort_coverage_gap_found") is False, "abort_coverage_gap_found")
    ok(summary.get("handoff_gap_found") is False, "handoff_gap_found")

    for flag in [
        "runtime_trial_executed",
        "controlled_output_enabled",
        "runtime_camera_invoked",
        "runtime_microphone_invoked",
        "runtime_asr_invoked",
        "runtime_tts_invoked",
        "speech_gate_runtime_invoked",
        "vop_runtime_invoked",
        "map_api_invoked",
        "gps_runtime_invoked",
        "ocr_provider_invoked",
        "detector_invoked",
        "segmentation_invoked",
        "tracking_invoked",
        "task_state_committed_now",
        "navigation_action_triggered",
        "route_modified",
        "memory_written",
        "world_model_written",
        "scene_delta_generated",
        "fact_written",
        "benchmark_accuracy_updated",
        "runtime_routing_changed",
    ]:
        ok(summary.get(flag) is False, f"summary_{flag}")
    ok(summary.get("boundary_ok") is True, "summary_boundary_ok")
    ok(summary.get("fact_status") == "not_fact", "summary_fact_status")
    ok(summary.get("write_allowed") is False, "summary_write_allowed")
    ok(
        summary.get("final_decision") == "POST_SHADOW_REVIEW_READY_FOR_CONTROLLED_OUTPUT_DEFINITION",
        "summary_final_decision",
    )

    ok(review_report.get("review_id") == "psr_mrit_v1_001", "review_id")
    ok(review_report.get("source_shadow_trial_run_id") == "csrun_mrit_v1_001", "source_shadow_trial_run_id")
    ok(review_report.get("review_scope") == "minimal_runtime_integration_post_shadow_review", "review_scope_report")
    ok(review_report.get("reviewed_input_case_count") == 8, "report_input_count")
    ok(review_report.get("reviewed_shadow_step_count") == 104, "report_step_count")
    ok(review_report.get("reviewed_candidate_trace_count") == 8, "report_trace_count")
    ok(review_report.get("reviewed_speech_gate_shadow_count") == 8, "report_gate_count")
    ok(review_report.get("reviewed_vop_shadow_event_count") == 8, "report_vop_count")
    ok(review_report.get("reviewed_abort_check_count") == 8, "report_abort_count")
    ok(review_report.get("readiness_decision") == "READY_FOR_CONTROLLED_OUTPUT_DEFINITION", "report_readiness")
    ok(
        review_report.get("next_phase_recommendation")
        == "Phase-Minimal-Runtime-Integration-Controlled-Output-Definition-v1-001",
        "report_next_phase",
    )
    ok(review_report.get("source_chain") == "minimal_runtime_integration_post_shadow_review_v1", "report_source_chain")

    ok(stability.get("controlled_input_case_count_matches_definition") is True, "stability_case_count_match")
    ok(stability.get("shadow_execution_step_count_complete") is True, "stability_step_count_complete")
    ok(stability.get("candidate_trace_complete_for_every_case") is True, "stability_candidate_trace_complete")
    ok(stability.get("speech_gate_shadow_complete_for_every_case") is True, "stability_speech_gate_complete")
    ok(stability.get("vop_shadow_event_complete_for_every_case") is True, "stability_vop_complete")
    ok(stability.get("abort_check_complete_for_every_case") is True, "stability_abort_complete")
    ok(stability.get("unexpected_suppression_or_delay_found") is False, "stability_no_unexpected_delay")
    ok(stability.get("missing_final_case_status") == [], "stability_missing_final_case_status")
    ok(stability.get("inconsistent_final_decision_found") is False, "stability_no_inconsistent_decision")
    ok(stability.get("all_final_case_status_explainable") is True, "stability_status_explainable")
    ok(stability.get("missing_step_names") == [], "stability_missing_step_names")
    ok(stability.get("stability_gap_found") is False, "stability_gap_found")
    ok(stability.get("stability_review_result") == "STABLE_SHADOW_LOOP_REVIEW_PASS", "stability_result")
    ok(stability.get("source_chain") == "minimal_runtime_integration_post_shadow_review_v1", "stability_source_chain")
    ok(sorted(stability.get("explainable_delay_cases") or []) == ["shadow_case_04"], "stability_explainable_delay_cases")
    ok(
        sorted(stability.get("explainable_suppression_cases") or []) == ["shadow_case_06", "shadow_case_08"],
        "stability_explainable_suppression_cases",
    )
    step_counts = stability.get("step_name_counts") or {}
    for step_name in [
        "load_controlled_input",
        "generate_safety_candidate",
        "generate_task_navigation_candidate",
        "generate_ocr_guidance_candidate",
        "apply_ownership_gate_shadow",
        "apply_interruption_governance_shadow",
        "apply_safety_task_arbitration_shadow",
        "generate_speech_request_candidate",
        "apply_speech_gate_shadow",
        "generate_vop_shadow_event",
        "run_abort_checks",
        "generate_boundary_reports",
        "generate_final_shadow_decision",
    ]:
        ok(step_counts.get(step_name) == 8, f"step_count_{step_name}")

    boundary_checks = boundary_review.get("boundary_checks") or {}
    for name in [
        "no_real_camera",
        "no_real_microphone",
        "no_real_asr",
        "no_real_tts",
        "no_real_speech_gate_runtime",
        "no_real_vop_runtime",
        "no_map_api",
        "no_gps_runtime",
        "no_ocr_provider",
        "no_detector",
        "no_segmentation",
        "no_tracking",
        "no_task_commit",
        "no_navigation_action",
        "no_route_modification",
        "no_memory_write",
        "no_world_model_write",
        "no_scene_delta",
        "no_fact_write",
    ]:
        ok(boundary_checks.get(name) is True, f"boundary_check_{name}")
    ok(boundary_review.get("boundary_weakness_found") is False, "boundary_review_found_false")
    ok(boundary_review.get("weakness_items") == [], "boundary_review_weakness_items")
    ok(boundary_review.get("severity") == "NONE", "boundary_review_severity")
    ok(boundary_review.get("required_fix") == [], "boundary_review_required_fix")
    ok(boundary_review.get("source_chain") == "minimal_runtime_integration_post_shadow_review_v1", "boundary_review_source_chain")

    source_checks = source_chain_review.get("checks") or {}
    for name in [
        "every_candidate_has_source_chain",
        "every_shadow_decision_has_source_chain",
        "every_vop_shadow_event_has_source_chain",
        "every_abort_check_has_source_chain",
        "every_final_decision_has_source_chain",
        "every_observability_case_has_source_chain",
    ]:
        ok(source_checks.get(name) is True, f"source_chain_check_{name}")
    ok(source_chain_review.get("source_chain_gap_found") is False, "source_chain_gap_found_review")
    ok(source_chain_review.get("gap_items") == [], "source_chain_gap_items")
    ok(source_chain_review.get("source_chain_review_result") == "SOURCE_CHAIN_COMPLETE", "source_chain_result")
    ok(source_chain_review.get("source_chain") == "minimal_runtime_integration_post_shadow_review_v1", "source_chain_source_chain")

    coverage_rows = abort_review.get("coverage_rows") or []
    ok(len(coverage_rows) == 12, "abort_coverage_row_count")
    coverage_by_key = {row.get("review_key"): row for row in coverage_rows}
    for key in [
        "forbidden_runtime_invoked",
        "forbidden_write_occurred",
        "missing_source_chain",
        "stale_safety_speech_treated_as_current_fact",
        "non_owner_voice_triggers_task_control",
        "p0_safety_speech_cancelled_by_ordinary_stop",
        "task_state_committed_now_true",
        "navigation_action_triggered_true",
        "world_model_written_true",
        "memory_written_true",
        "map_api_invoked_true",
        "uncontrolled_tts_invoked_true",
    ]:
        row = coverage_by_key.get(key) or {}
        ok(row.get("covered_in_definition") is True, f"abort_definition_cover_{key}")
        ok(row.get("covered_in_shadow_abort_checks") is True, f"abort_shadow_cover_{key}")
    ok(abort_review.get("abort_coverage_gap_found") is False, "abort_coverage_gap_found")
    ok(abort_review.get("gap_items") == [], "abort_gap_items")
    ok(abort_review.get("abort_coverage_review_result") == "ABORT_COVERAGE_COMPLETE", "abort_result")
    ok(abort_review.get("source_chain") == "minimal_runtime_integration_post_shadow_review_v1", "abort_source_chain")

    handoff_checks = handoff_review.get("checks") or {}
    for name in [
        "speech_gate_shadow_handoff_complete",
        "vop_shadow_event_complete",
        "safety_task_arbitration_shadow_handoff_complete",
        "ownership_gate_handoff_complete_when_required",
        "interruption_governance_handoff_complete_when_required",
        "task_manager_handoff_candidate_only",
        "stc_ocr_navigation_freshness_handoff_future_check_only",
        "no_runtime_handoff_maintained",
    ]:
        ok(handoff_checks.get(name) is True, f"handoff_check_{name}")
    ok(handoff_review.get("handoff_gap_found") is False, "handoff_gap_found")
    ok(handoff_review.get("gap_items") == [], "handoff_gap_items")
    ok(handoff_review.get("handoff_review_result") == "HANDOFF_READY_FOR_DEFINITION", "handoff_result")
    ok(handoff_review.get("source_chain") == "minimal_runtime_integration_post_shadow_review_v1", "handoff_source_chain")

    ok(readiness.get("readiness_decision") == "READY_FOR_CONTROLLED_OUTPUT_DEFINITION", "readiness_decision")
    ok(
        readiness.get("next_phase_recommendation")
        == "Phase-Minimal-Runtime-Integration-Controlled-Output-Definition-v1-001",
        "readiness_next_phase",
    )
    ok(readiness.get("must_not_recommend_live_runtime") is True, "must_not_recommend_live_runtime")
    ok(readiness.get("must_not_recommend_camera_enablement") is True, "must_not_recommend_camera_enablement")
    ok(readiness.get("must_not_recommend_map_api_enablement") is True, "must_not_recommend_map_api_enablement")
    ok(
        readiness.get("must_not_recommend_memory_or_worldmodel_write") is True,
        "must_not_recommend_memory_or_worldmodel_write",
    )
    ok(
        readiness.get("allowed_next_scope") == "definition_only_for_minimal_controlled_output_path",
        "allowed_next_scope",
    )
    forbidden_scope = readiness.get("forbidden_next_scope") or []
    for name in [
        "live_runtime_enablement",
        "camera_enablement",
        "microphone_enablement",
        "map_api_enablement",
        "gps_enablement",
        "memory_write_enablement",
        "worldmodel_write_enablement",
        "task_commit_enablement",
        "navigation_action_enablement",
    ]:
        ok(name in forbidden_scope, f"forbidden_scope_{name}")
    ok(readiness.get("source_chain") == "minimal_runtime_integration_post_shadow_review_v1", "readiness_source_chain")

    risk_items = risk_register.get("items") or []
    ok(len(risk_items) == 4, "risk_item_count")
    for idx, risk in enumerate(risk_items, start=1):
        ok(bool(risk.get("risk_id")), f"risk_{idx}_id")
        ok(bool(risk.get("risk")), f"risk_{idx}_risk")
        ok(bool(risk.get("severity")), f"risk_{idx}_severity")
        ok(bool(risk.get("status")), f"risk_{idx}_status")
        ok(bool(risk.get("required_action")), f"risk_{idx}_required_action")
        ok(risk.get("fact_status") == "not_fact", f"risk_{idx}_fact_status")
        ok(risk.get("write_allowed") is False, f"risk_{idx}_write_allowed")
    ok(risk_register.get("source_chain") == "minimal_runtime_integration_post_shadow_review_v1", "risk_source_chain")

    ok(
        next_phase.get("next_phase_recommendation")
        == "Phase-Minimal-Runtime-Integration-Controlled-Output-Definition-v1-001",
        "next_phase_recommendation",
    )
    ok(
        next_phase.get("alternative_if_regression_found")
        == "Phase-Minimal-Runtime-Integration-Controlled-Shadow-Trial-v1-002",
        "next_phase_alternative",
    )
    ok(bool(next_phase.get("rationale")), "next_phase_rationale")
    ok(next_phase.get("source_chain") == "minimal_runtime_integration_post_shadow_review_v1", "next_phase_source_chain")

    for report_key in ["no_runtime_boundary_report", "no_write_boundary_report"]:
        report = data[report_key]
        ok(report.get("review_only") is True, f"{report_key}_review_only")
        ok(report.get("runtime_trial_executed") is False, f"{report_key}_runtime_trial_executed")
        ok(report.get("controlled_output_enabled") is False, f"{report_key}_controlled_output_enabled")
        ok(report.get("boundary_ok") is True, f"{report_key}_boundary_ok")
        ok(report.get("violations") == [], f"{report_key}_violations")
        ok(report.get("fact_status") == "not_fact", f"{report_key}_fact_status")
        ok(report.get("write_allowed") is False, f"{report_key}_write_allowed")
        for flag in [
            "runtime_camera_invoked",
            "runtime_microphone_invoked",
            "runtime_asr_invoked",
            "runtime_tts_invoked",
            "speech_gate_runtime_invoked",
            "vop_runtime_invoked",
            "map_api_invoked",
            "gps_runtime_invoked",
            "ocr_provider_invoked",
            "detector_invoked",
            "segmentation_invoked",
            "tracking_invoked",
            "task_state_committed_now",
            "navigation_action_triggered",
            "route_modified",
            "memory_written",
            "world_model_written",
            "scene_delta_generated",
            "fact_written",
            "benchmark_accuracy_updated",
            "runtime_routing_changed",
        ]:
            ok(report.get(flag) is False, f"{report_key}_{flag}")

    report = {
        "verdict": "GO" if not blockers else "NO_GO",
        "checks_passed": checks_passed,
        "checks_expected": MIN_CHECKS,
        "blockers": blockers,
        "final_decision": summary.get("final_decision"),
        "phase": "Minimal-Runtime-Integration-Post-Shadow-Review-v1-001",
    }
    _write_json(smoke_root / "verifier_report.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if not blockers else 2


if __name__ == "__main__":
    raise SystemExit(main())
