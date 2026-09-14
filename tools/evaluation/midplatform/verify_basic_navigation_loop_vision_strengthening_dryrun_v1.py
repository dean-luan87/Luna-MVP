#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Basic Navigation Loop Vision Strengthening DryRun v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


DEFAULT_WORKSPACE_ROOT = Path("/Users/luanlei/Desktop/Luna-Workspace-Min")
DEFAULT_OUTPUT_ROOT = DEFAULT_WORKSPACE_ROOT / "_eval_out" / "basic_navigation_loop_vision_strengthening_dryrun_v1_smoke_v0"
PHASE_ID = "Phase-Basic-Navigation-Loop-Vision-Strengthening-DryRun-v1-001"
FINAL_DECISION = "BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Basic-Navigation-Loop-Vision-Strengthening-Post-DryRun-Review-v1-001"
MIN_CHECKS = 220
BASELINE_REQUIREMENT = 180


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify Basic Navigation Loop Vision Strengthening DryRun v1")
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
    case_schema = _load_json(output_root / "navigation_vision_strengthening_dryrun_case_schema.json")
    intake_schema = _load_json(output_root / "navigation_feedback_intake_candidate_schema.json")
    guidance_schema = _load_json(output_root / "vision_aware_navigation_guidance_candidate_schema.json")
    bridge_schema = _load_json(output_root / "navigation_safety_arbitration_bridge_candidate_schema.json")
    output_schema = _load_json(output_root / "navigation_output_candidate_dryrun_schema.json")
    boundary_schema = _load_json(output_root / "navigation_vision_strengthening_boundary_decision_schema.json")
    scenario_matrix = _load_json(output_root / "navigation_loop_vision_strengthening_scenario_matrix.json")
    dryrun_results = _load_json(output_root / "navigation_loop_vision_strengthening_dryrun_results.json")
    boundary_matrix = _load_json(output_root / "navigation_loop_vision_strengthening_boundary_matrix.json")
    governance_debt_register = _load_json(output_root / "governance_debt_register.json")
    next_phase_recommendation = _load_json(output_root / "next_phase_recommendation.json")
    no_runtime_boundary_report = _load_json(output_root / "no_runtime_boundary_report.json")
    no_write_boundary_report = _load_json(output_root / "no_write_boundary_report.json")

    input_rows = input_root_matrix.get("rows", [])
    input_index = {row.get("intake_id"): row for row in input_rows}
    required_intakes = [
        "visual_ocr_map_task_feedback",
        "selective_tracking",
        "world_observation_entity_feature",
        "task_aware_visual_focus",
        "midplatform_perception_orchestration",
        "basic_navigation_loop_stabilization",
        "safety_task_arbitration_policy",
        "minimal_runtime_integration_closure",
        "ocr_final_closure",
        "visual_ocr_map_task_feedback_doc",
        "selective_tracking_doc",
        "world_observation_entity_feature_doc",
        "task_aware_visual_focus_doc",
        "midplatform_perception_orchestration_doc",
        "basic_navigation_loop_stabilization_doc",
        "safety_task_arbitration_doc",
        "minimal_runtime_integration_closure_doc",
        "ocr_final_closure_doc",
        "ocr_phase_verdict_table",
    ]
    for intake_id in required_intakes:
        expect(f"input.required.{intake_id}", intake_id in input_index and input_index[intake_id].get("loaded") is True)
    expect("input.root_rows_present", isinstance(input_rows, list))
    expect("input.root_count_match", input_root_matrix.get("row_count") == len(input_rows))
    for summary_flag in (
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

    expect("summary.dryrun_scope", summary.get("dryrun_scope") == "basic_navigation_loop_vision_strengthening_dryrun_only")
    for summary_flag in (
        "navigation_vision_strengthening_dryrun_case_schema_defined",
        "navigation_feedback_intake_candidate_schema_defined",
        "vision_aware_navigation_guidance_candidate_schema_defined",
        "navigation_safety_arbitration_bridge_candidate_schema_defined",
        "navigation_output_candidate_dryrun_schema_defined",
        "boundary_decision_schema_defined",
        "scenario_matrix_generated",
        "dryrun_results_generated",
        "safety_priority_cases_generated",
        "task_guidance_cases_generated",
        "active_view_adjustment_cases_generated",
        "ocr_later_needed_cases_generated",
        "tracking_later_needed_cases_generated",
        "map_visual_conflict_cases_generated",
        "crossing_uncertain_cases_generated",
        "feedback_candidates_require_arbitration",
        "speech_allowed_false_until_gate",
        "action_allowed_false",
        "fact_status_not_fact",
        "worldmodel_handoff_candidate_allowed",
        "memory_handoff_candidate_allowed",
        "library_handoff_placeholder_allowed",
        "entity_resolution_deferred",
        "fact_admission_deferred",
        "memory_consolidation_deferred",
        "library_experience_governance_deferred",
        "handoff_candidate_not_fact",
        "placeholder_not_runtime",
        "dryrun_only",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "boundary_ok",
        "governance_debt_register_generated",
    ):
        expect(f"summary.{summary_flag}", summary.get(summary_flag) is True)
    expect("summary.scenario_count_ge_12", summary.get("scenario_count", 0) >= 12, summary.get("scenario_count"))
    expect("summary.guidance_candidate_count_ge_12", summary.get("guidance_candidate_count", 0) >= 12, summary.get("guidance_candidate_count"))
    expect("summary.output_candidate_count_ge_12", summary.get("output_candidate_count", 0) >= 12, summary.get("output_candidate_count"))
    for summary_flag in (
        "navigation_action_allowed",
        "ocrrequest_submission_allowed",
        "ocr_provider_allowed",
        "tracking_runtime_allowed",
        "crossing_action_instruction_allowed",
        "crowd_flow_follow_action_allowed",
        "fixed_poi_commit_allowed",
        "identity_fact_allowed",
        "worldmodel_write_allowed",
        "memory_write_allowed",
        "library_write_allowed",
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

    def field_names(schema: Dict[str, Any]) -> List[str]:
        return [field.get("name") for field in schema.get("fields", [])]

    case_fields = field_names(case_schema)
    expect("schema.case.object_name", case_schema.get("object_name") == "NavigationVisionStrengtheningDryRunCase")
    expect("schema.case.field_count_match", case_schema.get("field_count") == len(case_schema.get("fields", [])))
    for name in (
        "dryrun_case_id",
        "case_type",
        "source_feedback_case_ref",
        "related_task_id",
        "task_phase",
        "incoming_feedback_candidates",
        "safety_feedback_refs",
        "task_feedback_refs",
        "ocr_activation_feedback_refs",
        "tracking_feedback_refs",
        "map_memory_context_feedback_refs",
        "conflict_correction_feedback_refs",
        "active_view_adjustment_feedback_refs",
        "expected_arbitration_path",
        "expected_guidance_candidate",
        "expected_output_candidate",
        "expected_boundary_flags",
        "source_chain",
    ):
        expect(f"schema.case.field.{name}", name in case_fields)

    intake_fields = field_names(intake_schema)
    expect("schema.intake.object_name", intake_schema.get("object_name") == "NavigationFeedbackIntakeCandidate")
    for name in (
        "intake_candidate_id",
        "source_dryrun_case_id",
        "feedback_refs",
        "intake_status",
        "accepted_feedback_types",
        "delayed_feedback_types",
        "suppressed_feedback_types",
        "requires_safety_task_arbitration",
        "requires_user_confirmation",
        "requires_view_adjustment",
        "requires_ocr_later",
        "requires_tracking_later",
        "fact_status",
        "action_allowed",
        "source_chain",
    ):
        expect(f"schema.intake.field.{name}", name in intake_fields)
    expect("schema.intake.action_allowed_false", intake_schema.get("action_allowed_false") is True)

    guidance_fields = field_names(guidance_schema)
    expect("schema.guidance.object_name", guidance_schema.get("object_name") == "VisionAwareNavigationGuidanceCandidate")
    for name in (
        "guidance_candidate_id",
        "source_intake_candidate_id",
        "guidance_type",
        "related_task_id",
        "task_phase",
        "safety_priority",
        "evidence_refs",
        "map_memory_hint_refs",
        "visual_feedback_refs",
        "ocr_feedback_refs",
        "tracking_feedback_refs",
        "confidence",
        "uncertainty",
        "allowed_output_mode",
        "requires_safety_task_arbitration",
        "requires_speech_gate",
        "action_instruction_allowed",
        "navigation_action_allowed",
        "fact_status",
        "source_chain",
    ):
        expect(f"schema.guidance.field.{name}", name in guidance_fields)
    for guidance_type in (
        "route_alignment_hint",
        "continue_walking_candidate",
        "slow_down_candidate",
        "hold_still_candidate",
        "look_left_right_candidate",
        "active_view_adjustment_hint",
        "destination_approach_hint",
        "target_search_hint",
        "crossing_uncertain_hint",
        "crowd_flow_caution_hint",
        "obstacle_caution_hint",
        "map_visual_conflict_hint",
        "ocr_later_needed_hint",
        "tracking_later_needed_hint",
    ):
        expect(f"schema.guidance.type.{guidance_type}", guidance_type in guidance_schema.get("guidance_types", []))
    expect("schema.guidance.speech_allowed_false_until_gate", guidance_schema.get("speech_allowed_false_until_gate") is True)
    expect("schema.guidance.navigation_action_allowed", guidance_schema.get("navigation_action_allowed") is False)

    bridge_fields = field_names(bridge_schema)
    expect("schema.bridge.object_name", bridge_schema.get("object_name") == "NavigationSafetyArbitrationBridgeCandidate")
    for name in (
        "bridge_candidate_id",
        "source_guidance_candidate_id",
        "safety_feedback_refs",
        "task_feedback_refs",
        "arbitration_priority",
        "suppress_task_guidance",
        "delay_task_guidance",
        "allow_safety_guidance_candidate",
        "requires_confirmation",
        "requires_reobserve",
        "fact_status",
        "action_allowed",
        "source_chain",
    ):
        expect(f"schema.bridge.field.{name}", name in bridge_fields)
    expect("schema.bridge.action_allowed_false", bridge_schema.get("action_allowed_false") is True)

    output_fields = field_names(output_schema)
    expect("schema.output.object_name", output_schema.get("object_name") == "NavigationOutputCandidateDryRun")
    for name in (
        "output_candidate_id",
        "source_guidance_candidate_id",
        "output_mode",
        "user_visible_text_candidate",
        "speech_gate_required",
        "speech_allowed",
        "tts_allowed",
        "vop_allowed",
        "user_heard_assumed",
        "action_instruction_allowed",
        "fact_status",
        "source_chain",
    ):
        expect(f"schema.output.field.{name}", name in output_fields)
    for output_mode in (
        "TEXT_ONLY_DRY_PREVIEW",
        "STRUCTURED_LOG_ONLY",
        "DRY_SPEECH_PREVIEW",
        "NO_OUTPUT_SUPPRESSED",
        "SAFETY_HOLD_PROMPT_CANDIDATE",
        "ACTIVE_VIEW_ADJUSTMENT_PROMPT_CANDIDATE",
    ):
        expect(f"schema.output.mode.{output_mode}", output_mode in output_schema.get("output_modes", []))
    for flag_name, expected in (
        ("speech_allowed_false_until_gate", True),
        ("tts_allowed", False),
        ("vop_allowed", False),
        ("user_heard_assumed", False),
        ("action_instruction_allowed", False),
    ):
        if expected is True:
            expect(f"schema.output.{flag_name}", output_schema.get(flag_name) is True)
        else:
            expect(f"schema.output.{flag_name}", output_schema.get(flag_name) is False)

    boundary_fields = field_names(boundary_schema)
    expect("schema.boundary.object_name", boundary_schema.get("object_name") == "NavigationVisionStrengtheningBoundaryDecision")
    for name in (
        "case_id",
        "intake_boundary_ok",
        "arbitration_boundary_ok",
        "guidance_boundary_ok",
        "output_boundary_ok",
        "runtime_boundary_ok",
        "write_boundary_ok",
        "speech_boundary_ok",
        "action_boundary_ok",
        "violations",
        "source_chain",
    ):
        expect(f"schema.boundary.field.{name}", name in boundary_fields)
    expect("schema.boundary.all_boundary_dimensions_defined", boundary_schema.get("all_boundary_dimensions_defined") is True)

    scenarios = scenario_matrix.get("scenarios", [])
    scenario_ids = [item.get("scenario_id") for item in scenarios]
    expect("scenario.count_match", scenario_matrix.get("scenario_count") == len(scenarios))
    expect("scenario.count_ge_12", len(scenarios) >= 12, len(scenarios))
    for scenario_id in (
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
    ):
        expect(f"scenario.id.{scenario_id}", scenario_id in scenario_ids)

    case_results = dryrun_results.get("case_results", [])
    expect("results.case_count_match", dryrun_results.get("case_count") == len(case_results))
    expect("results.generated", dryrun_results.get("dryrun_results_generated") is True)
    expect("results.guidance_count_ge_12", dryrun_results.get("guidance_candidate_count", 0) >= 12, dryrun_results.get("guidance_candidate_count"))
    expect("results.output_count_ge_12", dryrun_results.get("output_candidate_count", 0) >= 12, dryrun_results.get("output_candidate_count"))
    for flag_name in (
        "safety_priority_cases_generated",
        "task_guidance_cases_generated",
        "active_view_adjustment_cases_generated",
        "ocr_later_needed_cases_generated",
        "tracking_later_needed_cases_generated",
        "map_visual_conflict_cases_generated",
        "crossing_uncertain_cases_generated",
        "boundary_ok",
    ):
        expect(f"results.{flag_name}", dryrun_results.get(flag_name) is True)
    expect("results.violations_empty", dryrun_results.get("violations") == [])

    result_index = {
        item.get("navigation_vision_strengthening_dryrun_case", {}).get("dryrun_case_id"): item
        for item in case_results
    }
    route_case = result_index["route_walking_clear_path_guidance"]
    obstacle_case = result_index["route_walking_near_field_obstacle"]
    destination_case = result_index["approaching_destination_signage_candidate"]
    shop_case = result_index["shop_search_right_side_view_adjustment"]
    object_case = result_index["object_search_home_privacy_sensitive"]
    crowd_case = result_index["crowded_path_crowd_flow_caution"]
    crossing_case = result_index["crossing_uncertain_red_green_light"]
    conflict_case = result_index["visual_map_memory_conflict_navigation"]
    poor_case = result_index["low_quality_view_hold_still"]
    temp_case = result_index["temporary_facility_route_impact"]
    tracking_case = result_index["tracking_later_needed_dynamic_obstacle"]
    ocr_case = result_index["ocr_later_needed_readable_sign"]

    def guidance_of(case: Dict[str, Any]) -> Dict[str, Any]:
        return case.get("vision_aware_navigation_guidance_candidate", {})

    def intake_of(case: Dict[str, Any]) -> Dict[str, Any]:
        return case.get("navigation_feedback_intake_candidate", {})

    def bridge_of(case: Dict[str, Any]) -> Dict[str, Any]:
        return case.get("navigation_safety_arbitration_bridge_candidate", {})

    def output_of(case: Dict[str, Any]) -> Dict[str, Any]:
        return case.get("navigation_output_candidate_dryrun", {})

    expect("results.route.guidance_type", guidance_of(route_case).get("guidance_type") == "continue_walking_candidate")
    expect("results.route.output_mode", output_of(route_case).get("output_mode") == "TEXT_ONLY_DRY_PREVIEW")
    expect("results.route.no_safety", intake_of(route_case).get("requires_safety_task_arbitration") is False)

    expect("results.obstacle.guidance_type", guidance_of(obstacle_case).get("guidance_type") == "slow_down_candidate")
    expect("results.obstacle.delay_task_guidance", bridge_of(obstacle_case).get("delay_task_guidance") is True)
    expect("results.obstacle.allow_safety_guidance", bridge_of(obstacle_case).get("allow_safety_guidance_candidate") is True)
    expect("results.obstacle.output_mode", output_of(obstacle_case).get("output_mode") == "SAFETY_HOLD_PROMPT_CANDIDATE")

    expect("results.destination.guidance_type", guidance_of(destination_case).get("guidance_type") == "destination_approach_hint")
    expect("results.destination.requires_ocr_later", intake_of(destination_case).get("requires_ocr_later") is True)
    expect("results.destination.no_arrival_claim", "不判定已到达" in (output_of(destination_case).get("user_visible_text_candidate") or ""))

    expect("results.shop.guidance_type", guidance_of(shop_case).get("guidance_type") == "active_view_adjustment_hint")
    expect("results.shop.requires_view_adjustment", intake_of(shop_case).get("requires_view_adjustment") is True)
    expect("results.shop.output_mode", output_of(shop_case).get("output_mode") == "ACTIVE_VIEW_ADJUSTMENT_PROMPT_CANDIDATE")

    expect("results.object.guidance_type", guidance_of(object_case).get("guidance_type") == "target_search_hint")
    expect("results.object.identity_fact_not_allowed", summary.get("identity_fact_allowed") is False)
    expect("results.object.long_term_write_blocked", summary.get("worldmodel_write_allowed") is False)

    expect("results.crowd.guidance_type", guidance_of(crowd_case).get("guidance_type") == "crowd_flow_caution_hint")
    expect("results.crowd.requires_tracking_later", intake_of(crowd_case).get("requires_tracking_later") is True)
    expect("results.crowd.follow_action_blocked", summary.get("crowd_flow_follow_action_allowed") is False)

    expect("results.crossing.guidance_type", guidance_of(crossing_case).get("guidance_type") == "crossing_uncertain_hint")
    expect("results.crossing.requires_confirmation", bridge_of(crossing_case).get("requires_confirmation") is True)
    expect("results.crossing.action_instruction_blocked", summary.get("crossing_action_instruction_allowed") is False)

    expect("results.conflict.guidance_type", guidance_of(conflict_case).get("guidance_type") == "map_visual_conflict_hint")
    expect("results.conflict.requires_reobserve", bridge_of(conflict_case).get("requires_reobserve") is True)
    expect("results.conflict.output_mode", output_of(conflict_case).get("output_mode") == "STRUCTURED_LOG_ONLY")

    expect("results.poor.guidance_type", guidance_of(poor_case).get("guidance_type") == "hold_still_candidate")
    expect("results.poor.suppress_task_guidance", bridge_of(poor_case).get("suppress_task_guidance") is True)
    expect("results.poor.output_mode", output_of(poor_case).get("output_mode") == "ACTIVE_VIEW_ADJUSTMENT_PROMPT_CANDIDATE")

    expect("results.temp.guidance_type", guidance_of(temp_case).get("guidance_type") == "temporary_route_caution_candidate")
    expect("results.temp.fixed_poi_commit_blocked", summary.get("fixed_poi_commit_allowed") is False)

    expect("results.tracking.guidance_type", guidance_of(tracking_case).get("guidance_type") == "tracking_later_needed_hint")
    expect("results.tracking.requires_tracking_later", intake_of(tracking_case).get("requires_tracking_later") is True)
    expect("results.tracking.runtime_blocked", summary.get("tracking_runtime_allowed") is False)

    expect("results.ocr.guidance_type", guidance_of(ocr_case).get("guidance_type") == "ocr_later_needed_hint")
    expect("results.ocr.requires_ocr_later", intake_of(ocr_case).get("requires_ocr_later") is True)
    expect("results.ocr.request_submission_blocked", summary.get("ocrrequest_submission_allowed") is False)

    for case_id, case in result_index.items():
        expect(f"results.case.{case_id}.source_chain.case", case.get("navigation_vision_strengthening_dryrun_case", {}).get("source_chain") == "basic_navigation_loop_vision_strengthening_dryrun_v1")
        expect(f"results.case.{case_id}.intake.not_fact", intake_of(case).get("fact_status") == "not_fact")
        expect(f"results.case.{case_id}.intake.action_allowed", intake_of(case).get("action_allowed") is False)
        expect(f"results.case.{case_id}.guidance.not_fact", guidance_of(case).get("fact_status") == "not_fact")
        expect(f"results.case.{case_id}.guidance.navigation_action_allowed", guidance_of(case).get("navigation_action_allowed") is False)
        expect(f"results.case.{case_id}.guidance.action_instruction_allowed", guidance_of(case).get("action_instruction_allowed") is False)
        expect(f"results.case.{case_id}.bridge.not_fact", bridge_of(case).get("fact_status") == "not_fact")
        expect(f"results.case.{case_id}.bridge.action_allowed", bridge_of(case).get("action_allowed") is False)
        expect(f"results.case.{case_id}.output.not_fact", output_of(case).get("fact_status") == "not_fact")
        expect(f"results.case.{case_id}.output.speech_allowed", output_of(case).get("speech_allowed") is False)
        expect(f"results.case.{case_id}.output.tts_allowed", output_of(case).get("tts_allowed") is False)
        expect(f"results.case.{case_id}.output.vop_allowed", output_of(case).get("vop_allowed") is False)
        expect(f"results.case.{case_id}.output.user_heard_assumed", output_of(case).get("user_heard_assumed") is False)
        expect(f"results.case.{case_id}.output.action_instruction_allowed", output_of(case).get("action_instruction_allowed") is False)
        boundary_decision = case.get("navigation_vision_strengthening_boundary_decision", {})
        expect(f"results.case.{case_id}.boundary.intake_ok", boundary_decision.get("intake_boundary_ok") is True)
        expect(f"results.case.{case_id}.boundary.arbitration_ok", boundary_decision.get("arbitration_boundary_ok") is True)
        expect(f"results.case.{case_id}.boundary.guidance_ok", boundary_decision.get("guidance_boundary_ok") is True)
        expect(f"results.case.{case_id}.boundary.output_ok", boundary_decision.get("output_boundary_ok") is True)
        expect(f"results.case.{case_id}.boundary.runtime_ok", boundary_decision.get("runtime_boundary_ok") is True)
        expect(f"results.case.{case_id}.boundary.write_ok", boundary_decision.get("write_boundary_ok") is True)
        expect(f"results.case.{case_id}.boundary.speech_ok", boundary_decision.get("speech_boundary_ok") is True)
        expect(f"results.case.{case_id}.boundary.action_ok", boundary_decision.get("action_boundary_ok") is True)
        expect(f"results.case.{case_id}.boundary.violations_empty", boundary_decision.get("violations") == [])

    for flag_name, expected in (
        ("feedback_candidates_require_arbitration", True),
        ("speech_allowed_false_until_gate", True),
        ("action_allowed_false", True),
        ("navigation_action_allowed", False),
        ("fact_status_not_fact", True),
        ("ocrrequest_submission_allowed", False),
        ("ocr_provider_allowed", False),
        ("tracking_runtime_allowed", False),
        ("crossing_action_instruction_allowed", False),
        ("crowd_flow_follow_action_allowed", False),
        ("fixed_poi_commit_allowed", False),
        ("identity_fact_allowed", False),
        ("worldmodel_handoff_candidate_allowed", True),
        ("memory_handoff_candidate_allowed", True),
        ("library_handoff_placeholder_allowed", True),
        ("worldmodel_write_allowed", False),
        ("memory_write_allowed", False),
        ("library_write_allowed", False),
    ):
        if expected is True:
            expect(f"boundary_matrix.{flag_name}", boundary_matrix.get(flag_name) is True)
        else:
            expect(f"boundary_matrix.{flag_name}", boundary_matrix.get(flag_name) is False)

    debt_rows = governance_debt_register.get("debts", [])
    expect("governance_debt.generated", summary.get("governance_debt_register_generated") is True)
    expect("governance_debt.future_midplatform_function_governance_required", governance_debt_register.get("future_midplatform_function_governance_required") is True)
    expect("governance_debt.no_duplicate_governance_module_allowed", governance_debt_register.get("no_duplicate_governance_module_allowed") is True)
    expect("governance_debt.count_ge_11", len(debt_rows) >= 11, len(debt_rows))
    for topic in (
        "navigation feedback intake weighting complexity",
        "safety-first suppression governance complexity",
        "view-adjustment prompt gating complexity",
        "ocr-later guidance prioritization complexity",
        "tracking-later guidance prioritization complexity",
        "crossing uncertainty conservative output governance complexity",
        "map-visual conflict reobserve governance complexity",
        "temporary facility route impact governance complexity",
        "text-only dry output mode consolidation complexity",
        "duplicated schema risk",
        "future midplatform function governance required",
    ):
        expect(f"governance_debt.topic.{topic}", any(row.get("topic") == topic for row in debt_rows))

    runtime_flags = (
        ("dryrun_only", True),
        ("no_runtime_executed", True),
        ("no_new_runtime_enabled", True),
        ("camera_invoked", False),
        ("map_api_invoked", False),
        ("ocr_provider_invoked", False),
        ("ocrrequest_submitted", False),
        ("tracking_runtime_invoked", False),
        ("optical_flow_runtime_invoked", False),
        ("supervision_imported", False),
        ("supervision_invoked", False),
        ("bytetrack_imported", False),
        ("bytetrack_invoked", False),
        ("ocsort_imported", False),
        ("ocsort_invoked", False),
        ("safety_task_arbitration_runtime_invoked", False),
        ("speech_gate_invoked", False),
        ("vop_invoked", False),
        ("tts_invoked", False),
        ("user_heard_assumed", False),
        ("task_state_committed_now", False),
        ("navigation_action_triggered", False),
        ("route_modified", False),
        ("scene_delta_generated", False),
        ("world_model_written", False),
        ("memory_written", False),
        ("library_written", False),
        ("fact_written", False),
        ("entity_resolution_runtime_invoked", False),
        ("fact_admission_runtime_invoked", False),
        ("memory_consolidation_invoked", False),
        ("library_experience_commit_invoked", False),
    )
    for flag_name, expected in runtime_flags:
        expect(f"runtime.summary.{flag_name}", summary.get(flag_name) is expected)
    expect("runtime.summary.boundary_ok", summary.get("boundary_ok") is True)
    expect("runtime.summary.violations_empty", summary.get("violations") == [])

    for payload_name, payload in (("no_runtime", no_runtime_boundary_report), ("no_write", no_write_boundary_report)):
        for flag_name, expected in runtime_flags:
            expect(f"{payload_name}.{flag_name}", payload.get(flag_name) is expected)
        for flag_name, expected in (
            ("feedback_candidates_require_arbitration", True),
            ("speech_allowed_false_until_gate", True),
            ("action_allowed_false", True),
            ("navigation_action_allowed", False),
            ("fact_status_not_fact", True),
            ("ocrrequest_submission_allowed", False),
            ("ocr_provider_allowed", False),
            ("tracking_runtime_allowed", False),
            ("crossing_action_instruction_allowed", False),
            ("crowd_flow_follow_action_allowed", False),
            ("fixed_poi_commit_allowed", False),
            ("identity_fact_allowed", False),
            ("worldmodel_write_allowed", False),
            ("memory_write_allowed", False),
            ("library_write_allowed", False),
            ("handoff_candidate_not_fact", True),
            ("placeholder_not_runtime", True),
            ("boundary_ok", True),
        ):
            if expected is True:
                expect(f"{payload_name}.{flag_name}", payload.get(flag_name) is True)
            else:
                expect(f"{payload_name}.{flag_name}", payload.get(flag_name) is False)
        expect(f"{payload_name}.violations_empty", payload.get("violations") == [])

    expect("final.summary_final_decision", summary.get("final_decision") == FINAL_DECISION)
    expect("final.summary_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    expect("final.next_phase_final_decision", next_phase_recommendation.get("final_decision") == FINAL_DECISION)
    expect("final.next_phase_recommended_next_phase", next_phase_recommendation.get("recommended_next_phase") == NEXT_PHASE)

    passed_count = sum(1 for item in checks if item["passed"])
    verdict = "GO" if passed_count >= MIN_CHECKS and not any(not item["passed"] for item in checks) else "NO_GO"
    report = {
        "phase": PHASE_ID,
        "verdict": verdict,
        "checks_passed": passed_count,
        "checks_total": len(checks),
        "min_checks_required": MIN_CHECKS,
        "baseline_requirement": BASELINE_REQUIREMENT,
        "final_decision": FINAL_DECISION if verdict == "GO" else "BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_DRYRUN_REVIEW_REQUIRED",
        "recommended_next_phase": NEXT_PHASE if verdict == "GO" else PHASE_ID,
        "failed_checks": [item for item in checks if not item["passed"]],
        "checks": checks,
    }
    (output_root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verdict": verdict, "checks_passed": passed_count, "checks_total": len(checks)}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
