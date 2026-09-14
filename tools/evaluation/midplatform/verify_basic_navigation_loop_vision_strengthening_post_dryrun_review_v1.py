#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Basic Navigation Loop Vision Strengthening Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


DEFAULT_WORKSPACE_ROOT = Path("/Users/luanlei/Desktop/Luna-Workspace-Min")
DEFAULT_OUTPUT_ROOT = DEFAULT_WORKSPACE_ROOT / "_eval_out" / "basic_navigation_loop_vision_strengthening_post_dryrun_review_v1_smoke_v0"
PHASE_ID = "Phase-Basic-Navigation-Loop-Vision-Strengthening-Post-DryRun-Review-v1-001"
FINAL_DECISION = "BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
NEXT_PHASE = "Phase-Basic-Navigation-Loop-Vision-Strengthening-Closure-v1-001"
MIN_CHECKS = 180
BASELINE_REQUIREMENT = 140
REQUIRED_SCENARIOS = [
    "route_walking_clear_path_guidance",
    "route_walking_near_field_obstacle",
    "approaching_destination_signage_candidate",
    "shop_search_right_side_view_adjustment",
    "object_search_home_privacy_sensitive",
    "crowded_path_crowd_flow_caution",
    "crossing_uncertain_red_green_light",
    "visual_map_memory_conflict_navigation",
    "low_quality_view_hold_still",
    "temporary_facility_route_impact",
    "tracking_later_needed_dynamic_obstacle",
    "ocr_later_needed_readable_sign",
]


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify Basic Navigation Loop Vision Strengthening Post-DryRun Review v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def expect(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(output_root / "summary.json")
    input_root_matrix = _load_json(output_root / "input_root_matrix.json")
    dryrun_input_root_review = _load_json(output_root / "dryrun_input_root_review.json")
    scenario_coverage_review = _load_json(output_root / "scenario_coverage_review.json")
    guidance_candidate_review = _load_json(output_root / "guidance_candidate_review.json")
    safety_arbitration_bridge_review = _load_json(output_root / "safety_arbitration_bridge_review.json")
    text_only_dry_output_review = _load_json(output_root / "text_only_dry_output_review.json")
    high_risk_scenario_review = _load_json(output_root / "high_risk_scenario_review.json")
    worldmodel_memory_library_boundary_review = _load_json(output_root / "worldmodel_memory_library_boundary_review.json")
    runtime_write_action_speech_boundary_review = _load_json(output_root / "runtime_write_action_speech_boundary_review.json")
    governance_debt_review = _load_json(output_root / "governance_debt_review.json")
    closure_readiness_decision = _load_json(output_root / "closure_readiness_decision.json")
    next_phase_recommendation = _load_json(output_root / "next_phase_recommendation.json")
    no_runtime_boundary_report = _load_json(output_root / "no_runtime_boundary_report.json")
    no_write_boundary_report = _load_json(output_root / "no_write_boundary_report.json")

    root_rows = input_root_matrix.get("rows", [])
    root_index = {row.get("intake_id"): row for row in root_rows}
    required_roots = [
        "navigation_vision_strengthening_dryrun",
        "visual_ocr_map_task_feedback",
        "selective_tracking",
        "world_observation_entity_feature",
        "task_aware_visual_focus",
        "midplatform_perception_orchestration",
        "basic_navigation_loop_stabilization",
        "safety_task_arbitration_policy",
        "minimal_runtime_integration_closure",
        "ocr_final_closure",
    ]
    for intake_id in required_roots:
        expect(f"input.required.{intake_id}", intake_id in root_index and root_index[intake_id].get("loaded") is True)
    expect("input.row_count_match", input_root_matrix.get("row_count") == len(root_rows))
    for summary_flag in (
        "dryrun_input_loaded",
        "visual_ocr_map_task_feedback_input_loaded",
        "selective_tracking_input_loaded",
        "world_observation_entity_feature_input_loaded",
        "task_aware_visual_focus_input_loaded",
        "midplatform_perception_orchestration_input_loaded",
        "basic_navigation_loop_stabilization_input_loaded",
        "safety_task_arbitration_policy_input_loaded",
        "minimal_runtime_integration_closure_loaded",
        "ocr_final_closure_loaded",
    ):
        expect(f"summary.{summary_flag}", summary.get(summary_flag) is True)

    expect("summary.review_scope", summary.get("review_scope") == "basic_navigation_loop_vision_strengthening_post_dryrun_review_only")
    for summary_flag in (
        "dryrun_input_root_review_generated",
        "scenario_coverage_review_generated",
        "guidance_candidate_review_generated",
        "safety_arbitration_bridge_review_generated",
        "text_only_dry_output_review_generated",
        "high_risk_scenario_review_generated",
        "worldmodel_memory_library_boundary_review_generated",
        "runtime_write_action_speech_boundary_review_generated",
        "governance_debt_review_generated",
        "closure_readiness_decision_generated",
        "candidate_only_boundary_pass",
        "safety_priority_review_pass",
        "high_risk_conservative_handling_pass",
        "text_only_dry_output_boundary_pass",
        "worldmodel_memory_library_boundary_pass",
        "no_runtime_boundary_pass",
        "no_write_boundary_pass",
        "no_action_boundary_pass",
        "no_speech_boundary_pass",
        "governance_debt_recorded",
        "future_midplatform_function_governance_required",
        "no_duplicate_governance_module_allowed",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "boundary_ok",
    ):
        expect(f"summary.{summary_flag}", summary.get(summary_flag) is True)
    expect("summary.reviewed_scenario_count_ge_12", summary.get("reviewed_scenario_count", 0) >= 12, summary.get("reviewed_scenario_count"))
    expect("summary.reviewed_guidance_candidate_count_ge_12", summary.get("reviewed_guidance_candidate_count", 0) >= 12, summary.get("reviewed_guidance_candidate_count"))
    expect("summary.reviewed_output_candidate_count_ge_12", summary.get("reviewed_output_candidate_count", 0) >= 12, summary.get("reviewed_output_candidate_count"))
    for summary_flag in (
        "camera_invoked",
        "map_api_invoked",
        "ocr_provider_invoked",
        "ocrrequest_submitted",
        "tracking_runtime_invoked",
        "optical_flow_runtime_invoked",
        "supervision_imported",
        "supervision_invoked",
        "bytetrack_imported",
        "bytetrack_invoked",
        "ocsort_imported",
        "ocsort_invoked",
        "safety_task_arbitration_runtime_invoked",
        "speech_gate_invoked",
        "vop_invoked",
        "tts_invoked",
        "user_heard_assumed",
        "task_state_committed_now",
        "navigation_action_triggered",
        "route_modified",
        "scene_delta_generated",
        "world_model_written",
        "memory_written",
        "library_written",
        "fact_written",
        "entity_resolution_runtime_invoked",
        "fact_admission_runtime_invoked",
        "memory_consolidation_invoked",
        "library_experience_commit_invoked",
    ):
        expect(f"summary.{summary_flag}", summary.get(summary_flag) is False)
    expect("summary.violations_empty", summary.get("violations") == [])

    expect("review.input.review_id", dryrun_input_root_review.get("review_id") == "bnlvspr_v1_001")
    expect("review.input.required_roots_count", len(dryrun_input_root_review.get("required_roots", [])) == 10)
    expect("review.input.missing_required_empty", dryrun_input_root_review.get("missing_required_roots") == [])
    expect("review.input.status_ok", dryrun_input_root_review.get("input_root_status") == "all_required_loaded")

    expect("review.scenario.count_ge_12", scenario_coverage_review.get("reviewed_scenario_count", 0) >= 12)
    expect("review.scenario.expected_count", scenario_coverage_review.get("expected_scenario_count") == 12)
    expect("review.scenario.verdict", scenario_coverage_review.get("verdict") == "PASS")
    expect("review.scenario.missing_empty", scenario_coverage_review.get("missing_scenarios") == [])
    for scenario_id in REQUIRED_SCENARIOS:
        expect(f"review.scenario.covered.{scenario_id}", scenario_id in scenario_coverage_review.get("covered_scenarios", []))
    for summary_flag in (
        "safety_priority_cases_present",
        "task_guidance_cases_present",
        "active_view_adjustment_cases_present",
        "ocr_later_needed_cases_present",
        "tracking_later_needed_cases_present",
        "map_visual_conflict_cases_present",
        "crossing_uncertain_cases_present",
    ):
        expect(f"review.scenario.{summary_flag}", scenario_coverage_review.get(summary_flag) is True)

    expect("review.guidance.count_ge_12", guidance_candidate_review.get("guidance_candidate_count", 0) >= 12)
    for flag_name in (
        "candidate_only_verified",
        "action_instruction_allowed_false",
        "navigation_action_allowed_false",
        "fact_status_not_fact",
        "source_chain_complete",
        "high_risk_guidance_conservative",
    ):
        expect(f"review.guidance.{flag_name}", guidance_candidate_review.get(flag_name) is True)
    expect("review.guidance.verdict", guidance_candidate_review.get("verdict") == "PASS")

    expect("review.bridge.count_ge_12", safety_arbitration_bridge_review.get("bridge_candidate_count", 0) >= 12)
    for flag_name in (
        "bridge_only_verified",
        "safety_priority_preserved",
        "task_guidance_suppression_or_delay_verified",
        "crossing_and_crowd_flow_guardrails_verified",
    ):
        expect(f"review.bridge.{flag_name}", safety_arbitration_bridge_review.get(flag_name) is True)
    expect("review.bridge.runtime_arbitration_invoked_false", safety_arbitration_bridge_review.get("runtime_arbitration_invoked") is False)
    expect("review.bridge.verdict", safety_arbitration_bridge_review.get("verdict") == "PASS")

    expect("review.output.count_ge_12", text_only_dry_output_review.get("output_candidate_count", 0) >= 12)
    expect("review.output.text_only_or_dry_preview_verified", text_only_dry_output_review.get("text_only_or_dry_preview_verified") is True)
    for flag_name in ("speech_gate_invoked", "vop_invoked", "tts_invoked", "user_heard_assumed", "real_output_generated"):
        expect(f"review.output.{flag_name}", text_only_dry_output_review.get(flag_name) is False)
    expect("review.output.verdict", text_only_dry_output_review.get("verdict") == "PASS")

    reviewed_high_risk = high_risk_scenario_review.get("reviewed_scenarios", [])
    high_risk_index = {row.get("scenario_id"): row for row in reviewed_high_risk}
    expect("review.high_risk.count", high_risk_scenario_review.get("reviewed_high_risk_scenario_count") == 7)
    expect("review.high_risk.all_conservative", high_risk_scenario_review.get("all_high_risk_conservative") is True)
    expect("review.high_risk.verdict", high_risk_scenario_review.get("verdict") == "PASS")
    for scenario_id in (
        "crossing_uncertain_red_green_light",
        "crowded_path_crowd_flow_caution",
        "visual_map_memory_conflict_navigation",
        "low_quality_view_hold_still",
        "temporary_facility_route_impact",
        "ocr_later_needed_readable_sign",
        "tracking_later_needed_dynamic_obstacle",
    ):
        row = high_risk_index.get(scenario_id, {})
        expect(f"review.high_risk.present.{scenario_id}", bool(row))
        expect(f"review.high_risk.conservative.{scenario_id}", row.get("conservative_handling_verified") is True)
        expect(f"review.high_risk.action_false.{scenario_id}", row.get("action_instruction_allowed") is False)
        expect(f"review.high_risk.fact_write_false.{scenario_id}", row.get("fact_write_allowed") is False)
        expect(f"review.high_risk.future_governance.{scenario_id}", row.get("requires_future_governance") is True)
        expect(f"review.high_risk.verdict.{scenario_id}", row.get("verdict") == "PASS")

    for flag_name in (
        "handoff_candidate_allowed",
        "placeholder_allowed",
        "entity_resolution_deferred",
        "fact_admission_deferred",
        "memory_consolidation_deferred",
        "library_experience_governance_deferred",
    ):
        expect(f"review.wml.{flag_name}", worldmodel_memory_library_boundary_review.get(flag_name) is True)
    for flag_name in ("worldmodel_write_allowed", "memory_write_allowed", "library_write_allowed", "fact_write_allowed"):
        expect(f"review.wml.{flag_name}", worldmodel_memory_library_boundary_review.get(flag_name) is False)
    expect("review.wml.verdict", worldmodel_memory_library_boundary_review.get("verdict") == "PASS")

    for flag_name in (
        "camera_invoked",
        "map_api_invoked",
        "ocr_provider_invoked",
        "ocrrequest_submitted",
        "tracking_runtime_invoked",
        "optical_flow_runtime_invoked",
        "supervision_invoked",
        "bytetrack_invoked",
        "ocsort_invoked",
        "speech_gate_invoked",
        "vop_invoked",
        "tts_invoked",
        "task_state_committed_now",
        "navigation_action_triggered",
        "route_modified",
        "scene_delta_generated",
        "world_model_written",
        "memory_written",
        "library_written",
        "fact_written",
    ):
        expect(f"review.boundary.{flag_name}", runtime_write_action_speech_boundary_review.get(flag_name) is False)
    expect("review.boundary.verdict", runtime_write_action_speech_boundary_review.get("verdict") == "PASS")
    expect("review.boundary.violations_empty", runtime_write_action_speech_boundary_review.get("violations") == [])

    for flag_name in (
        "governance_debt_register_loaded",
        "future_midplatform_function_governance_required",
        "no_duplicate_governance_module_allowed",
        "duplicate_module_risk_recorded",
        "perception_orchestration_complexity_recorded",
        "visual_focus_complexity_recorded",
        "tracking_policy_complexity_recorded",
        "world_observation_handoff_complexity_recorded",
    ):
        expect(f"review.debt.{flag_name}", governance_debt_review.get(flag_name) is True)
    expect("review.debt.verdict", governance_debt_review.get("verdict") == "PASS")
    expect("review.debt.recommendation_present", bool(governance_debt_review.get("recommendation")))

    expect("closure.verdict", closure_readiness_decision.get("post_dryrun_review_verdict") == "GO")
    expect("closure.blockers_empty", closure_readiness_decision.get("blockers") == [])
    expect("closure.ready_for_closure", closure_readiness_decision.get("ready_for_closure") is True)
    expect("closure.next_phase", closure_readiness_decision.get("next_phase_recommendation") == NEXT_PHASE)
    expect("closure.final_decision", closure_readiness_decision.get("final_decision") == FINAL_DECISION)
    expect("closure.conditional_notes_present", len(closure_readiness_decision.get("conditional_notes", [])) >= 3)

    expect("next_phase.final_decision", next_phase_recommendation.get("final_decision") == FINAL_DECISION)
    expect("next_phase.recommended_next_phase", next_phase_recommendation.get("recommended_next_phase") == NEXT_PHASE)

    for payload_name, payload in (("no_runtime", no_runtime_boundary_report), ("no_write", no_write_boundary_report)):
        for flag_name in (
            "review_only",
            "no_runtime_boundary_pass",
            "no_write_boundary_pass",
            "no_action_boundary_pass",
            "no_speech_boundary_pass",
            "no_runtime_executed",
            "no_new_runtime_enabled",
            "boundary_ok",
        ):
            expect(f"{payload_name}.{flag_name}", payload.get(flag_name) is True)
        for flag_name in (
            "camera_invoked",
            "map_api_invoked",
            "ocr_provider_invoked",
            "ocrrequest_submitted",
            "tracking_runtime_invoked",
            "optical_flow_runtime_invoked",
            "supervision_imported",
            "supervision_invoked",
            "bytetrack_imported",
            "bytetrack_invoked",
            "ocsort_imported",
            "ocsort_invoked",
            "safety_task_arbitration_runtime_invoked",
            "speech_gate_invoked",
            "vop_invoked",
            "tts_invoked",
            "user_heard_assumed",
            "task_state_committed_now",
            "navigation_action_triggered",
            "route_modified",
            "scene_delta_generated",
            "world_model_written",
            "memory_written",
            "library_written",
            "fact_written",
            "entity_resolution_runtime_invoked",
            "fact_admission_runtime_invoked",
            "memory_consolidation_invoked",
            "library_experience_commit_invoked",
        ):
            expect(f"{payload_name}.{flag_name}", payload.get(flag_name) is False)
        expect(f"{payload_name}.violations_empty", payload.get("violations") == [])

    passed_count = sum(1 for item in checks if item["passed"])
    verdict = "GO" if passed_count >= MIN_CHECKS and not any(not item["passed"] for item in checks) else "NO_GO"
    report = {
        "phase": PHASE_ID,
        "verdict": verdict,
        "checks_passed": passed_count,
        "checks_total": len(checks),
        "min_checks_required": MIN_CHECKS,
        "baseline_requirement": BASELINE_REQUIREMENT,
        "final_decision": FINAL_DECISION if verdict == "GO" else "BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if verdict == "GO" else PHASE_ID,
        "failed_checks": [item for item in checks if not item["passed"]],
        "checks": checks,
    }
    (output_root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verdict": verdict, "checks_passed": passed_count, "checks_total": len(checks)}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
