#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Visual OCR Map Task Feedback DryRun v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


DEFAULT_WORKSPACE_ROOT = Path("/Users/luanlei/Desktop/Luna-Workspace-Min")
DEFAULT_OUTPUT_ROOT = DEFAULT_WORKSPACE_ROOT / "_eval_out" / "visual_ocr_map_task_feedback_dryrun_v1_smoke_v0"
PHASE_ID = "Phase-Visual-OCR-Map-Task-Feedback-DryRun-v1-001"
FINAL_DECISION = "VISUAL_OCR_MAP_TASK_FEEDBACK_DRYRUN_READY_FOR_BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING"
NEXT_PHASE = "Phase-Basic-Navigation-Loop-Vision-Strengthening-DryRun-v1-001"
MIN_CHECKS = 200
BASELINE_REQUIREMENT = 160


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify Visual OCR Map Task Feedback DryRun v1")
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
    dryrun_case_schema = _load_json(output_root / "dryrun_case_schema.json")
    feedback_fusion_candidate_schema = _load_json(output_root / "feedback_fusion_candidate_schema.json")
    task_feedback_candidate_schema = _load_json(output_root / "task_feedback_candidate_schema.json")
    safety_feedback_candidate_schema = _load_json(output_root / "safety_feedback_candidate_schema.json")
    ocr_activation_feedback_candidate_schema = _load_json(output_root / "ocr_activation_feedback_candidate_schema.json")
    tracking_feedback_candidate_schema = _load_json(output_root / "tracking_feedback_candidate_schema.json")
    map_memory_context_feedback_candidate_schema = _load_json(output_root / "map_memory_context_feedback_candidate_schema.json")
    conflict_correction_feedback_candidate_schema = _load_json(output_root / "conflict_correction_feedback_candidate_schema.json")
    active_view_adjustment_feedback_candidate_schema = _load_json(output_root / "active_view_adjustment_feedback_candidate_schema.json")
    dryrun_boundary_decision_schema = _load_json(output_root / "dryrun_boundary_decision_schema.json")
    scenario_matrix = _load_json(output_root / "visual_ocr_map_task_feedback_scenario_matrix.json")
    dryrun_results = _load_json(output_root / "visual_ocr_map_task_feedback_dryrun_results.json")
    feedback_boundary_matrix = _load_json(output_root / "feedback_boundary_matrix.json")
    governance_debt_register = _load_json(output_root / "governance_debt_register.json")
    next_phase_recommendation = _load_json(output_root / "next_phase_recommendation.json")
    no_runtime_boundary_report = _load_json(output_root / "no_runtime_boundary_report.json")
    no_write_boundary_report = _load_json(output_root / "no_write_boundary_report.json")

    input_rows = input_root_matrix.get("rows", [])
    input_index = {row.get("intake_id"): row for row in input_rows}
    required_intakes = [
        "selective_tracking",
        "world_observation_entity_feature",
        "task_aware_visual_focus",
        "midplatform_perception_orchestration",
        "return_to_vision_planning",
        "preplan_input",
        "ocr_final_closure",
        "minimal_runtime_integration_closure",
        "selective_tracking_doc",
        "world_observation_entity_feature_doc",
        "task_aware_visual_focus_doc",
        "midplatform_perception_orchestration_doc",
        "vision_planning_doc",
        "vision_preplan_doc",
        "ocr_final_closure_doc",
        "minimal_runtime_integration_closure_doc",
        "ocr_phase_verdict_table",
    ]
    for intake_id in required_intakes:
        expect(f"input.required.{intake_id}", intake_id in input_index and input_index[intake_id].get("loaded") is True)
    expect("input.root_rows_present", isinstance(input_rows, list))
    expect("input.root_row_count_match", input_root_matrix.get("row_count") == len(input_rows))
    expect("input.selective_tracking_input_loaded", summary.get("selective_tracking_input_loaded") is True)
    expect("input.world_observation_entity_feature_input_loaded", summary.get("world_observation_entity_feature_input_loaded") is True)
    expect("input.task_aware_visual_focus_input_loaded", summary.get("task_aware_visual_focus_input_loaded") is True)
    expect("input.midplatform_perception_orchestration_input_loaded", summary.get("midplatform_perception_orchestration_input_loaded") is True)
    expect("input.return_to_vision_planning_input_loaded", summary.get("return_to_vision_planning_input_loaded") is True)
    expect("input.preplan_input_loaded", summary.get("preplan_input_loaded") is True)
    expect("input.ocr_final_closure_loaded", summary.get("ocr_final_closure_loaded") is True)
    expect("input.minimal_runtime_integration_closure_loaded", summary.get("minimal_runtime_integration_closure_loaded") is True)

    expect("summary.dryrun_scope", summary.get("dryrun_scope") == "visual_ocr_map_task_feedback_dryrun_only")
    for field_name in (
        "dryrun_case_schema_defined",
        "feedback_fusion_candidate_schema_defined",
        "task_feedback_candidate_schema_defined",
        "safety_feedback_candidate_schema_defined",
        "ocr_activation_feedback_candidate_schema_defined",
        "tracking_feedback_candidate_schema_defined",
        "map_memory_context_feedback_candidate_schema_defined",
        "conflict_correction_feedback_candidate_schema_defined",
        "active_view_adjustment_feedback_candidate_schema_defined",
        "dryrun_boundary_decision_schema_defined",
        "scenario_matrix_generated",
        "dryrun_results_generated",
        "task_feedback_candidate_generated",
        "safety_feedback_candidate_generated",
        "ocr_activation_feedback_candidate_generated",
        "tracking_feedback_candidate_generated",
        "map_memory_context_feedback_candidate_generated",
        "conflict_correction_feedback_candidate_generated",
        "active_view_adjustment_feedback_candidate_generated",
        "feedback_candidates_require_arbitration",
        "speech_allowed_false_until_gate",
        "action_allowed_false",
        "fact_status_not_fact",
        "governance_debt_register_generated",
    ):
        expect(f"summary.{field_name}", summary.get(field_name) is True)
    expect("summary.scenario_count", summary.get("scenario_count", 0) >= 10, summary.get("scenario_count"))
    expect("summary.feedback_candidate_count", summary.get("feedback_candidate_count", 0) >= 10, summary.get("feedback_candidate_count"))
    for field_name in (
        "ocrrequest_submission_allowed",
        "ocr_provider_allowed",
        "tracking_runtime_allowed",
        "crossing_action_instruction_allowed",
        "crowd_flow_follow_action_allowed",
        "fixed_poi_commit_allowed",
        "identity_fact_allowed",
    ):
        expect(f"summary.{field_name}", summary.get(field_name) is False)
    for field_name in (
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
    ):
        expect(f"summary.{field_name}", summary.get(field_name) is True)
    for field_name in (
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
        "entity_resolution_runtime_invoked",
        "fact_admission_runtime_invoked",
        "memory_consolidation_invoked",
        "library_experience_commit_invoked",
        "world_model_written",
        "memory_written",
        "library_written",
        "fact_written",
        "scene_delta_generated",
        "task_state_committed_now",
        "navigation_action_triggered",
        "speech_gate_invoked",
        "vop_invoked",
        "tts_invoked",
    ):
        expect(f"summary.{field_name}", summary.get(field_name) is False)

    def field_names(schema: Dict[str, Any]) -> List[str]:
        return [field.get("name") for field in schema.get("fields", [])]

    case_fields = field_names(dryrun_case_schema)
    expect("schema.case.object_name", dryrun_case_schema.get("object_name") == "VisualOcrMapTaskFeedbackDryRunCase")
    expect("schema.case.field_count_match", dryrun_case_schema.get("field_count") == len(dryrun_case_schema.get("fields", [])))
    for name in (
        "dryrun_case_id",
        "case_type",
        "simulated_task_context",
        "simulated_task_phase",
        "simulated_scene_sketch_ref",
        "simulated_visual_focus_plan_ref",
        "simulated_visual_focus_slots",
        "simulated_view_quality_ref",
        "simulated_map_context_hint",
        "simulated_memory_context_hint",
        "simulated_ocr_activation_candidate",
        "simulated_tracking_request_candidate",
        "simulated_world_observation_candidate",
        "expected_feedback_candidates",
        "expected_boundary_flags",
        "source_chain",
    ):
        expect(f"schema.case.field.{name}", name in case_fields)

    fusion_fields = field_names(feedback_fusion_candidate_schema)
    expect("schema.fusion.object_name", feedback_fusion_candidate_schema.get("object_name") == "FeedbackFusionCandidate")
    expect("schema.fusion.field_count_match", feedback_fusion_candidate_schema.get("field_count") == len(feedback_fusion_candidate_schema.get("fields", [])))
    for name in (
        "feedback_fusion_candidate_id",
        "source_case_id",
        "related_task_id",
        "task_phase",
        "visual_refs",
        "ocr_activation_refs",
        "tracking_refs",
        "map_hint_refs",
        "memory_hint_refs",
        "world_observation_refs",
        "conflict_refs",
        "correction_refs",
        "confidence",
        "freshness_status",
        "uncertainty",
        "requires_arbitration",
        "speech_allowed",
        "action_allowed",
        "fact_status",
        "source_chain",
    ):
        expect(f"schema.fusion.field.{name}", name in fusion_fields)
    expect("schema.fusion.requires_arbitration", feedback_fusion_candidate_schema.get("feedback_candidates_require_arbitration") is True)
    expect("schema.fusion.speech_allowed_false_until_gate", feedback_fusion_candidate_schema.get("speech_allowed_false_until_gate") is True)
    expect("schema.fusion.action_allowed_false", feedback_fusion_candidate_schema.get("action_allowed_false") is True)
    expect("schema.fusion.fact_status_not_fact", feedback_fusion_candidate_schema.get("fact_status_not_fact") is True)

    task_fields = field_names(task_feedback_candidate_schema)
    expect("schema.task.object_name", task_feedback_candidate_schema.get("object_name") == "TaskFeedbackCandidate")
    expect("schema.task.field_count_match", task_feedback_candidate_schema.get("field_count") == len(task_feedback_candidate_schema.get("fields", [])))
    for name in (
        "task_feedback_candidate_id",
        "source_fusion_candidate_id",
        "feedback_type",
        "related_task_id",
        "task_phase",
        "evidence_refs",
        "recommended_next_focus",
        "recommended_user_prompt_candidate",
        "requires_safety_arbitration",
        "requires_speech_gate",
        "confidence",
        "fact_status",
        "action_allowed",
        "source_chain",
    ):
        expect(f"schema.task.field.{name}", name in task_fields)
    for feedback_type in (
        "route_alignment_feedback",
        "destination_approach_feedback",
        "target_search_feedback",
        "target_confirmation_feedback",
        "object_search_feedback",
        "shopfront_search_feedback",
        "view_adjustment_needed",
        "map_memory_conflict_feedback",
        "ocr_activation_needed",
        "tracking_needed",
        "world_observation_handoff_feedback",
    ):
        expect(f"schema.task.feedback_type.{feedback_type}", feedback_type in task_feedback_candidate_schema.get("feedback_types", []))

    safety_fields = field_names(safety_feedback_candidate_schema)
    expect("schema.safety.object_name", safety_feedback_candidate_schema.get("object_name") == "SafetyFeedbackCandidate")
    for name in (
        "safety_feedback_candidate_id",
        "source_fusion_candidate_id",
        "safety_type",
        "evidence_refs",
        "priority",
        "requires_safety_task_arbitration",
        "speech_allowed",
        "action_allowed",
        "fact_status",
        "source_chain",
    ):
        expect(f"schema.safety.field.{name}", name in safety_fields)
    for safety_type in (
        "near_field_obstacle",
        "vehicle_approach",
        "pedestrian_approach",
        "crossing_uncertain",
        "traffic_light_uncertain",
        "route_surface_occluded",
        "crowd_flow_risk",
        "view_quality_poor",
    ):
        expect(f"schema.safety.type.{safety_type}", safety_type in safety_feedback_candidate_schema.get("safety_types", []))
    expect("schema.safety.speech_allowed_false_until_gate", safety_feedback_candidate_schema.get("speech_allowed_false_until_gate") is True)
    expect("schema.safety.action_allowed_false", safety_feedback_candidate_schema.get("action_allowed_false") is True)

    ocr_fields = field_names(ocr_activation_feedback_candidate_schema)
    expect("schema.ocr.object_name", ocr_activation_feedback_candidate_schema.get("object_name") == "OCRActivationFeedbackCandidate")
    for name in (
        "ocr_activation_feedback_id",
        "source_focus_slot_id",
        "ocr_target_type",
        "ocr_activation_reason",
        "readable_region_required",
        "ocrrequest_submission_allowed",
        "ocr_provider_allowed",
        "fact_status",
        "source_chain",
    ):
        expect(f"schema.ocr.field.{name}", name in ocr_fields)
    expect("schema.ocr.ocrrequest_submission_allowed", ocr_activation_feedback_candidate_schema.get("ocrrequest_submission_allowed") is False)
    expect("schema.ocr.ocr_provider_allowed", ocr_activation_feedback_candidate_schema.get("ocr_provider_allowed") is False)

    tracking_fields = field_names(tracking_feedback_candidate_schema)
    expect("schema.tracking.object_name", tracking_feedback_candidate_schema.get("object_name") == "TrackingFeedbackCandidate")
    for name in (
        "tracking_feedback_id",
        "source_tracking_request_candidate_id",
        "tracking_target_type",
        "tracking_reason",
        "candidate_only",
        "tracking_runtime_allowed",
        "full_scene_tracking_allowed",
        "action_allowed",
        "fact_status",
        "source_chain",
    ):
        expect(f"schema.tracking.field.{name}", name in tracking_fields)
    expect("schema.tracking.tracking_runtime_allowed", tracking_feedback_candidate_schema.get("tracking_runtime_allowed") is False)
    expect("schema.tracking.full_scene_tracking_allowed", tracking_feedback_candidate_schema.get("full_scene_tracking_allowed") is False)
    expect("schema.tracking.candidate_only", tracking_feedback_candidate_schema.get("candidate_only") is True)

    map_memory_fields = field_names(map_memory_context_feedback_candidate_schema)
    expect("schema.map_memory.object_name", map_memory_context_feedback_candidate_schema.get("object_name") == "MapMemoryContextFeedbackCandidate")
    for name in (
        "map_memory_feedback_id",
        "map_context_hint_ref",
        "memory_context_hint_ref",
        "hint_type",
        "hint_supports_task_phase",
        "hint_conflicts_with_visual",
        "hint_conflicts_with_ocr",
        "hint_conflicts_with_user_feedback",
        "current_fact_allowed",
        "action_allowed",
        "fact_status",
        "source_chain",
    ):
        expect(f"schema.map_memory.field.{name}", name in map_memory_fields)
    expect("schema.map_memory.current_fact_allowed", map_memory_context_feedback_candidate_schema.get("current_fact_allowed") is False)
    expect("schema.map_memory.action_allowed_false", map_memory_context_feedback_candidate_schema.get("action_allowed_false") is True)

    conflict_fields = field_names(conflict_correction_feedback_candidate_schema)
    expect("schema.conflict.object_name", conflict_correction_feedback_candidate_schema.get("object_name") == "ConflictCorrectionFeedbackCandidate")
    for name in (
        "conflict_correction_feedback_id",
        "conflict_type",
        "conflicting_refs",
        "correction_candidate_ref",
        "requires_review",
        "current_action_allowed",
        "fact_status",
        "source_chain",
    ):
        expect(f"schema.conflict.field.{name}", name in conflict_fields)
    expect("schema.conflict.current_action_allowed_default", conflict_correction_feedback_candidate_schema.get("current_action_allowed_default") is False)

    adjustment_fields = field_names(active_view_adjustment_feedback_candidate_schema)
    expect("schema.adjustment.object_name", active_view_adjustment_feedback_candidate_schema.get("object_name") == "ActiveViewAdjustmentFeedbackCandidate")
    for name in (
        "active_view_adjustment_feedback_id",
        "source_view_quality_ref",
        "source_focus_slot_ref",
        "adjustment_type",
        "user_prompt_candidate",
        "speech_gate_required",
        "action_allowed",
        "fact_status",
        "source_chain",
    ):
        expect(f"schema.adjustment.field.{name}", name in adjustment_fields)
    expect("schema.adjustment.speech_gate_required_default", active_view_adjustment_feedback_candidate_schema.get("speech_gate_required_default") is True)
    expect("schema.adjustment.action_allowed_false", active_view_adjustment_feedback_candidate_schema.get("action_allowed_false") is True)

    boundary_decision_fields = field_names(dryrun_boundary_decision_schema)
    expect("schema.boundary_decision.object_name", dryrun_boundary_decision_schema.get("object_name") == "DryRunBoundaryDecision")
    for name in (
        "case_id",
        "runtime_boundary_ok",
        "write_boundary_ok",
        "action_boundary_ok",
        "speech_boundary_ok",
        "worldmodel_boundary_ok",
        "memory_boundary_ok",
        "library_boundary_ok",
        "violations",
        "source_chain",
    ):
        expect(f"schema.boundary_decision.field.{name}", name in boundary_decision_fields)
    expect("schema.boundary_decision.all_boundaries_default_true", dryrun_boundary_decision_schema.get("all_boundaries_default_true") is True)

    scenarios = scenario_matrix.get("scenarios", [])
    scenario_ids = [item.get("scenario_id") for item in scenarios]
    expect("scenario_matrix.count_match", scenario_matrix.get("scenario_count") == len(scenarios))
    expect("scenario_matrix.count_ge_10", len(scenarios) >= 10, len(scenarios))
    for scenario_id in (
        "navigation_route_walking_clear_path",
        "navigation_approaching_destination_with_signage",
        "shop_search_right_side_storefront",
        "object_search_home_keys",
        "home_familiar_object_interaction",
        "crowded_path_occluded_surface",
        "crossing_uncertain_traffic_light",
        "temporary_mobile_vendor_near_route",
        "visual_map_memory_conflict",
        "low_quality_view_requires_hold_still",
    ):
        expect(f"scenario_matrix.id.{scenario_id}", scenario_id in scenario_ids)
    scenario_lookup = {item.get("scenario_id"): item for item in scenarios}
    expect("scenario.navigation_route.task_phase", scenario_lookup["navigation_route_walking_clear_path"].get("task_phase") == "ROUTE_WALKING")
    expect("scenario.navigation_destination.task_phase", scenario_lookup["navigation_approaching_destination_with_signage"].get("task_phase") == "APPROACHING_TARGET")
    expect("scenario.shop_search.has_signage_focus", "signage_focus" in scenario_lookup["shop_search_right_side_storefront"].get("focus_slots", []))
    expect("scenario.object_search.home_memory", scenario_lookup["object_search_home_keys"].get("memory_hint") == "tabletop_bag_area_hint")
    expect("scenario.home_familiar.expected_worldobs", "world_observation_handoff_feedback" in scenario_lookup["home_familiar_object_interaction"].get("expected_feedback", []))
    expect("scenario.crowded_path.expected_tracking_needed", "tracking_needed" in scenario_lookup["crowded_path_occluded_surface"].get("expected_feedback", []))
    expect("scenario.crossing.expected_tracking_needed", "tracking_needed" in scenario_lookup["crossing_uncertain_traffic_light"].get("expected_feedback", []))
    expect("scenario.temporary_facility.expected_temp_feedback", "temporary_facility_task_feedback" in scenario_lookup["temporary_mobile_vendor_near_route"].get("expected_feedback", []))
    expect("scenario.conflict.expected_map_memory_conflict", "map_memory_conflict_feedback" in scenario_lookup["visual_map_memory_conflict"].get("expected_feedback", []))
    expect("scenario.low_quality.expected_view_adjustment", "view_adjustment_needed" in scenario_lookup["low_quality_view_requires_hold_still"].get("expected_feedback", []))

    case_results = dryrun_results.get("case_results", [])
    expect("results.case_count_match", dryrun_results.get("case_count") == len(case_results))
    expect("results.generated", dryrun_results.get("dryrun_results_generated") is True)
    expect("results.feedback_candidate_count_ge_10", dryrun_results.get("feedback_candidate_count", 0) >= 10, dryrun_results.get("feedback_candidate_count"))
    expect("results.boundary_ok", dryrun_results.get("boundary_ok") is True)
    expect("results.violations_empty", dryrun_results.get("violations") == [])
    for count_field in (
        "task_feedback_candidate_count",
        "safety_feedback_candidate_count",
        "ocr_activation_feedback_candidate_count",
        "tracking_feedback_candidate_count",
        "map_memory_context_feedback_candidate_count",
        "conflict_correction_feedback_candidate_count",
        "active_view_adjustment_feedback_candidate_count",
    ):
        expect(f"results.count.{count_field}", dryrun_results.get(count_field, 0) > 0, dryrun_results.get(count_field))

    case_lookup = {entry.get("dryrun_case", {}).get("dryrun_case_id"): entry for entry in case_results}
    for case_id in (
        "navigation_route_walking_clear_path",
        "navigation_approaching_destination_with_signage",
        "shop_search_right_side_storefront",
        "object_search_home_keys",
        "home_familiar_object_interaction",
        "crowded_path_occluded_surface",
        "crossing_uncertain_traffic_light",
        "temporary_mobile_vendor_near_route",
        "visual_map_memory_conflict",
        "low_quality_view_requires_hold_still",
    ):
        expect(f"results.case_present.{case_id}", case_id in case_lookup)

    route_case = case_lookup["navigation_route_walking_clear_path"]
    dest_case = case_lookup["navigation_approaching_destination_with_signage"]
    shop_case = case_lookup["shop_search_right_side_storefront"]
    object_case = case_lookup["object_search_home_keys"]
    familiar_case = case_lookup["home_familiar_object_interaction"]
    crowded_case = case_lookup["crowded_path_occluded_surface"]
    crossing_case = case_lookup["crossing_uncertain_traffic_light"]
    temp_case = case_lookup["temporary_mobile_vendor_near_route"]
    conflict_case = case_lookup["visual_map_memory_conflict"]
    poor_case = case_lookup["low_quality_view_requires_hold_still"]

    expect("results.route_case.task_feedback_exists", len(route_case.get("task_feedback_candidates", [])) >= 1)
    expect("results.route_case.no_ocr_feedback", len(route_case.get("ocr_activation_feedback_candidates", [])) == 0)
    expect("results.route_case.no_tracking_feedback", len(route_case.get("tracking_feedback_candidates", [])) == 0)

    expect("results.dest_case.ocr_feedback_exists", len(dest_case.get("ocr_activation_feedback_candidates", [])) >= 1)
    expect("results.dest_case.destination_feedback", any(item.get("feedback_type") == "destination_approach_feedback" for item in dest_case.get("task_feedback_candidates", [])))

    expect("results.shop_case.shopfront_feedback", any(item.get("feedback_type") == "shopfront_search_feedback" for item in shop_case.get("task_feedback_candidates", [])))
    expect("results.shop_case.ocr_feedback_exists", len(shop_case.get("ocr_activation_feedback_candidates", [])) >= 1)
    expect("results.shop_case.view_adjustment_exists", len(shop_case.get("active_view_adjustment_feedback_candidates", [])) >= 1)

    expect("results.object_case.object_search_feedback", any(item.get("feedback_type") == "object_search_feedback" for item in object_case.get("task_feedback_candidates", [])))
    expect("results.object_case.memory_hint_present", object_case.get("dryrun_case", {}).get("simulated_memory_context_hint") == "tabletop_bag_area_hint")

    expect("results.familiar_case.worldobs_feedback_exists", len(familiar_case.get("world_observation_feedback_candidates", [])) >= 1)
    expect("results.familiar_case.task_feedback_worldobs_handoff", any(item.get("feedback_type") == "world_observation_handoff_feedback" for item in familiar_case.get("task_feedback_candidates", [])))

    crowded_safety_types = [item.get("safety_type") for item in crowded_case.get("safety_feedback_candidates", [])]
    expect("results.crowded_case.route_surface_occluded", "route_surface_occluded" in crowded_safety_types)
    expect("results.crowded_case.crowd_flow_risk", "crowd_flow_risk" in crowded_safety_types)
    expect("results.crowded_case.tracking_feedback_exists", len(crowded_case.get("tracking_feedback_candidates", [])) >= 1)

    crossing_safety_types = [item.get("safety_type") for item in crossing_case.get("safety_feedback_candidates", [])]
    expect("results.crossing_case.crossing_uncertain", "crossing_uncertain" in crossing_safety_types)
    expect("results.crossing_case.traffic_light_uncertain", "traffic_light_uncertain" in crossing_safety_types)
    expect("results.crossing_case.tracking_feedback_exists", len(crossing_case.get("tracking_feedback_candidates", [])) >= 1)
    expect("results.crossing_case.action_not_allowed", all(item.get("action_allowed") is False for item in crossing_case.get("tracking_feedback_candidates", [])))

    expect("results.temp_case.temp_task_feedback", any(item.get("feedback_type") == "temporary_facility_task_feedback" for item in temp_case.get("task_feedback_candidates", [])))
    expect("results.temp_case.tracking_feedback_exists", len(temp_case.get("tracking_feedback_candidates", [])) >= 1)
    expect("results.temp_case.worldobs_feedback_exists", len(temp_case.get("world_observation_feedback_candidates", [])) >= 1)

    expect("results.conflict_case.map_memory_feedback_exists", len(conflict_case.get("map_memory_context_feedback_candidates", [])) >= 1)
    expect("results.conflict_case.conflict_feedback_exists", len(conflict_case.get("conflict_correction_feedback_candidates", [])) >= 1)
    expect("results.conflict_case.task_feedback_map_memory_conflict", any(item.get("feedback_type") == "map_memory_conflict_feedback" for item in conflict_case.get("task_feedback_candidates", [])))

    expect("results.poor_case.task_feedback_suppressed", poor_case.get("task_feedback_suppressed") is True)
    expect("results.poor_case.no_task_feedback", len(poor_case.get("task_feedback_candidates", [])) == 0)
    expect("results.poor_case.safety_feedback_exists", len(poor_case.get("safety_feedback_candidates", [])) >= 1)
    expect("results.poor_case.view_adjustment_exists", len(poor_case.get("active_view_adjustment_feedback_candidates", [])) >= 1)
    expect("results.poor_case.adjustment_hold_still", any(item.get("adjustment_type") == "hold_still" for item in poor_case.get("active_view_adjustment_feedback_candidates", [])))

    for case_id, case_entry in case_lookup.items():
        dryrun_case = case_entry.get("dryrun_case", {})
        fusion = case_entry.get("feedback_fusion_candidate", {})
        boundary = case_entry.get("dryrun_boundary_decision", {})
        expect(f"results.case.{case_id}.source_chain", dryrun_case.get("source_chain") == "visual_ocr_map_task_feedback_dryrun_v1")
        expect(f"results.case.{case_id}.fusion_requires_arbitration", fusion.get("requires_arbitration") is True)
        expect(f"results.case.{case_id}.fusion_speech_allowed", fusion.get("speech_allowed") is False)
        expect(f"results.case.{case_id}.fusion_action_allowed", fusion.get("action_allowed") is False)
        expect(f"results.case.{case_id}.fusion_not_fact", fusion.get("fact_status") == "not_fact")
        expect(f"results.case.{case_id}.boundary.runtime_ok", boundary.get("runtime_boundary_ok") is True)
        expect(f"results.case.{case_id}.boundary.write_ok", boundary.get("write_boundary_ok") is True)
        expect(f"results.case.{case_id}.boundary.action_ok", boundary.get("action_boundary_ok") is True)
        expect(f"results.case.{case_id}.boundary.speech_ok", boundary.get("speech_boundary_ok") is True)
        expect(f"results.case.{case_id}.boundary.worldmodel_ok", boundary.get("worldmodel_boundary_ok") is True)
        expect(f"results.case.{case_id}.boundary.memory_ok", boundary.get("memory_boundary_ok") is True)
        expect(f"results.case.{case_id}.boundary.library_ok", boundary.get("library_boundary_ok") is True)
        expect(f"results.case.{case_id}.boundary.violations_empty", boundary.get("violations") == [])
        for candidate_list_name in (
            "task_feedback_candidates",
            "safety_feedback_candidates",
            "ocr_activation_feedback_candidates",
            "tracking_feedback_candidates",
            "map_memory_context_feedback_candidates",
            "conflict_correction_feedback_candidates",
            "active_view_adjustment_feedback_candidates",
            "world_observation_feedback_candidates",
        ):
            for idx, candidate in enumerate(case_entry.get(candidate_list_name, [])):
                expect(f"results.case.{case_id}.{candidate_list_name}.{idx}.not_fact", candidate.get("fact_status") == "not_fact")
                if "action_allowed" in candidate:
                    expect(f"results.case.{case_id}.{candidate_list_name}.{idx}.action_allowed", candidate.get("action_allowed") is False)

    expect("feedback_boundary.feedback_candidates_require_arbitration", feedback_boundary_matrix.get("feedback_candidates_require_arbitration") is True)
    expect("feedback_boundary.speech_allowed_false_until_gate", feedback_boundary_matrix.get("speech_allowed_false_until_gate") is True)
    expect("feedback_boundary.action_allowed_false", feedback_boundary_matrix.get("action_allowed_false") is True)
    expect("feedback_boundary.fact_status_not_fact", feedback_boundary_matrix.get("fact_status_not_fact") is True)
    expect("feedback_boundary.ocrrequest_submission_allowed", feedback_boundary_matrix.get("ocrrequest_submission_allowed") is False)
    expect("feedback_boundary.ocr_provider_allowed", feedback_boundary_matrix.get("ocr_provider_allowed") is False)
    expect("feedback_boundary.tracking_runtime_allowed", feedback_boundary_matrix.get("tracking_runtime_allowed") is False)
    expect("feedback_boundary.crossing_action_instruction_allowed", feedback_boundary_matrix.get("crossing_action_instruction_allowed") is False)
    expect("feedback_boundary.crowd_flow_follow_action_allowed", feedback_boundary_matrix.get("crowd_flow_follow_action_allowed") is False)
    expect("feedback_boundary.fixed_poi_commit_allowed", feedback_boundary_matrix.get("fixed_poi_commit_allowed") is False)
    expect("feedback_boundary.identity_fact_allowed", feedback_boundary_matrix.get("identity_fact_allowed") is False)
    expect("feedback_boundary.worldmodel_handoff_candidate_allowed", feedback_boundary_matrix.get("worldmodel_handoff_candidate_allowed") is True)
    expect("feedback_boundary.memory_handoff_candidate_allowed", feedback_boundary_matrix.get("memory_handoff_candidate_allowed") is True)
    expect("feedback_boundary.library_handoff_placeholder_allowed", feedback_boundary_matrix.get("library_handoff_placeholder_allowed") is True)
    expect("feedback_boundary.worldmodel_write_allowed", feedback_boundary_matrix.get("worldmodel_write_allowed") is False)
    expect("feedback_boundary.memory_write_allowed", feedback_boundary_matrix.get("memory_write_allowed") is False)
    expect("feedback_boundary.library_write_allowed", feedback_boundary_matrix.get("library_write_allowed") is False)

    expect("governance_debt.generated", summary.get("governance_debt_register_generated") is True)
    expect("governance_debt.future_midplatform_function_governance_required", governance_debt_register.get("future_midplatform_function_governance_required") is True)
    expect("governance_debt.no_duplicate_governance_module_allowed", governance_debt_register.get("no_duplicate_governance_module_allowed") is True)
    debt_rows = governance_debt_register.get("debts", [])
    expect("governance_debt.count_ge_10", len(debt_rows) >= 10, len(debt_rows))
    for topic in (
        "feedback fusion weighting complexity",
        "ocr activation candidate prioritization complexity",
        "tracking feedback arbitration complexity",
        "map memory conflict correction governance complexity",
        "active view adjustment suppression governance complexity",
        "crossing uncertainty escalation governance complexity",
        "temporary facility TTL feedback governance complexity",
        "world observation handoff feedback governance complexity",
        "duplicated schema risk",
        "future midplatform function governance required",
    ):
        expect(f"governance_debt.topic.{topic}", any(row.get("topic") == topic for row in debt_rows))
    for idx, row in enumerate(debt_rows):
        expect(f"governance_debt.reuse_or_consolidation_required_{idx}", row.get("reuse_or_consolidation_required") is True)
        expect(f"governance_debt.duplicate_governance_module_allowed_{idx}", row.get("duplicate_governance_module_allowed") is False)

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
        ("entity_resolution_runtime_invoked", False),
        ("fact_admission_runtime_invoked", False),
        ("memory_consolidation_invoked", False),
        ("library_experience_commit_invoked", False),
        ("world_model_written", False),
        ("memory_written", False),
        ("library_written", False),
        ("fact_written", False),
        ("scene_delta_generated", False),
        ("task_state_committed_now", False),
        ("navigation_action_triggered", False),
        ("speech_gate_invoked", False),
        ("vop_invoked", False),
        ("tts_invoked", False),
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
        "final_decision": FINAL_DECISION if verdict == "GO" else "VISUAL_OCR_MAP_TASK_FEEDBACK_DRYRUN_REVIEW_REQUIRED",
        "recommended_next_phase": NEXT_PHASE if verdict == "GO" else PHASE_ID,
        "failed_checks": [item for item in checks if not item["passed"]],
        "checks": checks,
    }
    (output_root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verdict": verdict, "checks_passed": passed_count, "checks_total": len(checks)}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
