#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Selective Tracking Adapter Policy v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


DEFAULT_WORKSPACE_ROOT = Path("/Users/luanlei/Desktop/Luna-Workspace-Min")
DEFAULT_OUTPUT_ROOT = DEFAULT_WORKSPACE_ROOT / "_eval_out" / "selective_tracking_adapter_policy_v1_smoke_v0"
PHASE_ID = "Phase-Selective-Tracking-Adapter-Policy-v1-001"
FINAL_DECISION = "SELECTIVE_TRACKING_ADAPTER_POLICY_READY_FOR_VISUAL_OCR_MAP_TASK_FEEDBACK_DRYRUN"
NEXT_PHASE = "Phase-Visual-OCR-Map-Task-Feedback-DryRun-v1-001"
MIN_CHECKS = 180
BASELINE_REQUIREMENT = 140


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify Selective Tracking Adapter Policy v1")
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
    selective_tracking_adapter_policy = _load_json(output_root / "selective_tracking_adapter_policy.json")
    tracking_request_candidate_schema = _load_json(output_root / "tracking_request_candidate_schema.json")
    tracklet_candidate_schema = _load_json(output_root / "tracklet_candidate_schema.json")
    tracking_budget_policy = _load_json(output_root / "tracking_budget_policy.json")
    tracking_target_admission_policy = _load_json(output_root / "tracking_target_admission_policy.json")
    road_surface_tracking_policy = _load_json(output_root / "road_surface_tracking_policy.json")
    pedestrian_vehicle_tracking_policy = _load_json(output_root / "pedestrian_vehicle_tracking_policy.json")
    crowd_flow_tracking_policy = _load_json(output_root / "crowd_flow_tracking_policy.json")
    traffic_light_crossing_tracking_policy = _load_json(output_root / "traffic_light_crossing_tracking_policy.json")
    tracking_adapter_candidate_registry = _load_json(output_root / "tracking_adapter_candidate_registry.json")
    tracking_lifecycle_policy = _load_json(output_root / "tracking_lifecycle_policy.json")
    tracking_feedback_policy = _load_json(output_root / "tracking_feedback_policy.json")
    selective_tracking_scenario_matrix = _load_json(output_root / "selective_tracking_scenario_matrix.json")
    selective_tracking_boundary_matrix = _load_json(output_root / "selective_tracking_boundary_matrix.json")
    governance_debt_register = _load_json(output_root / "governance_debt_register.json")
    next_phase_recommendation = _load_json(output_root / "next_phase_recommendation.json")
    no_runtime_boundary_report = _load_json(output_root / "no_runtime_boundary_report.json")
    no_write_boundary_report = _load_json(output_root / "no_write_boundary_report.json")

    input_rows = input_root_matrix.get("rows", [])
    input_intake_ids = {row.get("intake_id"): row for row in input_rows}

    required_inputs = [
        "world_observation_entity_feature",
        "task_aware_visual_focus",
        "midplatform_perception_orchestration",
        "return_to_vision_planning",
        "preplan_input",
        "ocr_final_closure",
        "minimal_runtime_integration_closure",
        "world_observation_entity_feature_doc",
        "task_aware_visual_focus_doc",
        "midplatform_perception_orchestration_doc",
        "vision_planning_doc",
        "vision_preplan_doc",
        "ocr_final_closure_doc",
        "minimal_runtime_integration_closure_doc",
        "ocr_phase_verdict_table",
    ]
    for intake_id in required_inputs:
        expect(f"input.required.{intake_id}", intake_id in input_intake_ids and input_intake_ids[intake_id].get("loaded") is True)

    expect("input.root_matrix_rows_present", isinstance(input_rows, list))
    expect("input.root_matrix_row_count_match", input_root_matrix.get("row_count") == len(input_rows))
    expect("input.world_observation_entity_feature_input_loaded", summary.get("world_observation_entity_feature_input_loaded") is True)
    expect("input.task_aware_visual_focus_input_loaded", summary.get("task_aware_visual_focus_input_loaded") is True)
    expect("input.midplatform_perception_orchestration_input_loaded", summary.get("midplatform_perception_orchestration_input_loaded") is True)
    expect("input.return_to_vision_planning_input_loaded", summary.get("return_to_vision_planning_input_loaded") is True)
    expect("input.preplan_input_loaded", summary.get("preplan_input_loaded") is True)
    expect("input.ocr_final_closure_loaded", summary.get("ocr_final_closure_loaded") is True)
    expect("input.minimal_runtime_integration_closure_loaded", summary.get("minimal_runtime_integration_closure_loaded") is True)

    expect("summary.policy_scope", summary.get("policy_scope") == "selective_tracking_adapter_policy_only")
    expect("summary.selective_tracking_adapter_policy_defined", summary.get("selective_tracking_adapter_policy_defined") is True)
    expect("summary.tracking_request_candidate_schema_defined", summary.get("tracking_request_candidate_schema_defined") is True)
    expect("summary.tracklet_candidate_schema_defined", summary.get("tracklet_candidate_schema_defined") is True)
    expect("summary.tracking_budget_policy_defined", summary.get("tracking_budget_policy_defined") is True)
    expect("summary.tracking_target_admission_policy_defined", summary.get("tracking_target_admission_policy_defined") is True)
    expect("summary.road_surface_tracking_policy_defined", summary.get("road_surface_tracking_policy_defined") is True)
    expect("summary.pedestrian_vehicle_tracking_policy_defined", summary.get("pedestrian_vehicle_tracking_policy_defined") is True)
    expect("summary.crowd_flow_tracking_policy_defined", summary.get("crowd_flow_tracking_policy_defined") is True)
    expect("summary.traffic_light_crossing_tracking_policy_defined", summary.get("traffic_light_crossing_tracking_policy_defined") is True)
    expect("summary.tracking_adapter_candidate_registry_defined", summary.get("tracking_adapter_candidate_registry_defined") is True)
    expect("summary.tracking_lifecycle_policy_defined", summary.get("tracking_lifecycle_policy_defined") is True)
    expect("summary.tracking_feedback_policy_defined", summary.get("tracking_feedback_policy_defined") is True)
    expect("summary.scenario_matrix_generated", summary.get("scenario_matrix_generated") is True)
    expect("summary.scenario_count", summary.get("scenario_count", 0) >= 10, summary.get("scenario_count"))
    expect("summary.tracking_authority_owner", summary.get("tracking_authority_owner") == "MidPlatform")
    expect("summary.full_scene_tracking_allowed", summary.get("full_scene_tracking_allowed") is False)
    expect("summary.all_moving_objects_tracking_allowed", summary.get("all_moving_objects_tracking_allowed") is False)
    expect("summary.all_person_tracking_allowed", summary.get("all_person_tracking_allowed") is False)
    expect("summary.all_vehicle_tracking_allowed", summary.get("all_vehicle_tracking_allowed") is False)
    expect("summary.crowd_flow_follow_action_allowed", summary.get("crowd_flow_follow_action_allowed") is False)
    expect("summary.traffic_light_crossing_action_allowed", summary.get("traffic_light_crossing_action_allowed") is False)
    expect("summary.tracking_request_candidate_only", summary.get("tracking_request_candidate_only") is True)
    expect("summary.tracklet_candidate_not_fact", summary.get("tracklet_candidate_not_fact") is True)
    expect("summary.external_tracking_adapters_future_candidate_only", summary.get("external_tracking_adapters_future_candidate_only") is True)
    expect("summary.worldmodel_handoff_candidate_allowed", summary.get("worldmodel_handoff_candidate_allowed") is True)
    expect("summary.memory_handoff_candidate_allowed", summary.get("memory_handoff_candidate_allowed") is True)
    expect("summary.library_handoff_placeholder_allowed", summary.get("library_handoff_placeholder_allowed") is True)
    expect("summary.entity_resolution_deferred", summary.get("entity_resolution_deferred") is True)
    expect("summary.fact_admission_deferred", summary.get("fact_admission_deferred") is True)
    expect("summary.memory_consolidation_deferred", summary.get("memory_consolidation_deferred") is True)
    expect("summary.library_experience_governance_deferred", summary.get("library_experience_governance_deferred") is True)
    expect("summary.worldmodel_write_allowed", summary.get("worldmodel_write_allowed") is False)
    expect("summary.memory_write_allowed", summary.get("memory_write_allowed") is False)
    expect("summary.library_write_allowed", summary.get("library_write_allowed") is False)
    expect("summary.handoff_candidate_not_fact", summary.get("handoff_candidate_not_fact") is True)
    expect("summary.placeholder_not_runtime", summary.get("placeholder_not_runtime") is True)
    expect("summary.governance_debt_register_generated", summary.get("governance_debt_register_generated") is True)

    expect("policy.tracking_authority_owner", selective_tracking_adapter_policy.get("tracking_authority_owner") == "MidPlatform")
    expect("policy.scope", selective_tracking_adapter_policy.get("scope") == "approved_focus_slot_tracking_candidate_layer")
    expect("policy.tracking_authority_belongs_to_midplatform", selective_tracking_adapter_policy.get("tracking_authority_belongs_to_midplatform") is True)
    expect("policy.vision_module_cannot_start_tracking_by_itself", selective_tracking_adapter_policy.get("vision_module_cannot_start_tracking_by_itself") is True)
    expect("policy.detector_cannot_start_tracking_by_itself", selective_tracking_adapter_policy.get("detector_cannot_start_tracking_by_itself") is True)
    expect("policy.adapter_cannot_start_tracking_by_itself", selective_tracking_adapter_policy.get("adapter_cannot_start_tracking_by_itself") is True)
    expect("policy.tracking_requires_approved_visual_focus_slot", selective_tracking_adapter_policy.get("tracking_requires_approved_visual_focus_slot") is True)
    expect("policy.tracking_requires_midplatform_resource_budget", selective_tracking_adapter_policy.get("tracking_requires_midplatform_resource_budget") is True)
    expect("policy.tracking_requires_safety_or_task_relevance", selective_tracking_adapter_policy.get("tracking_requires_safety_or_task_relevance") is True)
    expect("policy.tracking_result_candidate_only", selective_tracking_adapter_policy.get("tracking_result_candidate_only") is True)
    expect("policy.tracking_result_cannot_directly_trigger_navigation_action", selective_tracking_adapter_policy.get("tracking_result_cannot_directly_trigger_navigation_action") is True)
    for focus_slot_type in (
        "safety_focus",
        "route_path_focus",
        "walkable_surface_focus",
        "route_alignment_focus",
        "crossing_focus",
        "traffic_light_focus",
        "dynamic_obstacle_focus",
        "pedestrian_flow_focus",
        "vehicle_flow_focus",
        "destination_landmark_focus",
        "shopfront_focus",
        "doorway_or_entrance_focus",
        "temporary_facility_focus",
        "user_feedback_focus",
    ):
        expect(f"policy.allowed_focus_slot_type.{focus_slot_type}", focus_slot_type in selective_tracking_adapter_policy.get("allowed_focus_slot_types", []))
    for forbidden_mode in (
        "full_scene_tracking",
        "all_moving_objects_tracking",
        "all_person_tracking",
        "all_vehicle_tracking",
        "all_background_motion_tracking",
        "curiosity_only_tracking",
        "emotional_interest_only_tracking",
    ):
        expect(f"policy.forbidden_tracking_mode.{forbidden_mode}", forbidden_mode in selective_tracking_adapter_policy.get("forbidden_tracking_modes", []))

    request_fields = [field.get("name") for field in tracking_request_candidate_schema.get("fields", [])]
    expect("request.object_name", tracking_request_candidate_schema.get("object_name") == "TrackingRequestCandidate")
    expect("request.field_count_match", tracking_request_candidate_schema.get("field_count") == len(tracking_request_candidate_schema.get("fields", [])))
    for field_name in (
        "tracking_request_candidate_id",
        "source_work_order_id",
        "source_visual_focus_plan_id",
        "source_focus_slot_id",
        "requested_target_type",
        "requested_tracking_reason",
        "priority",
        "task_relevance",
        "safety_relevance",
        "route_relevance",
        "map_memory_relevance",
        "allowed_adapter_candidates",
        "max_duration",
        "max_tracklets",
        "freshness_requirement",
        "ttl_policy_ref",
        "privacy_filter_required",
        "budget_ref",
        "approval_status",
        "runtime_invocation_allowed",
        "fact_status",
        "source_chain",
    ):
        expect(f"request.field.{field_name}", field_name in request_fields)
    for target_type in (
        "walkable_path",
        "road_surface",
        "route_alignment",
        "near_field_obstacle",
        "dynamic_obstacle",
        "pedestrian",
        "vehicle",
        "bike_or_e_scooter",
        "traffic_light",
        "crosswalk",
        "pedestrian_flow",
        "vehicle_flow",
        "crowd_flow",
        "destination_landmark",
        "shopfront",
        "doorway_or_entrance",
        "temporary_facility",
        "user_feedback_target",
    ):
        expect(f"request.target_type.{target_type}", target_type in tracking_request_candidate_schema.get("requested_target_types", []))
    expect("request.tracking_request_candidate_only", tracking_request_candidate_schema.get("tracking_request_candidate_only") is True)
    expect("request.runtime_invocation_allowed", tracking_request_candidate_schema.get("runtime_invocation_allowed") is False)
    expect("request.non_claims_count", len(tracking_request_candidate_schema.get("non_claims", [])) >= 4)

    tracklet_fields = [field.get("name") for field in tracklet_candidate_schema.get("fields", [])]
    expect("tracklet.object_name", tracklet_candidate_schema.get("object_name") == "TrackletCandidate")
    expect("tracklet.field_count_match", tracklet_candidate_schema.get("field_count") == len(tracklet_candidate_schema.get("fields", [])))
    for field_name in (
        "tracklet_candidate_id",
        "source_tracking_request_candidate_id",
        "target_type",
        "target_candidate_ref",
        "track_state",
        "temporal_span_candidate",
        "spatial_path_candidate",
        "motion_state_candidate",
        "relative_position_candidate",
        "approach_or_departure_candidate",
        "occlusion_status_candidate",
        "stability_score_candidate",
        "confidence",
        "freshness_status",
        "ttl_policy_ref",
        "privacy_tags",
        "current_action_allowed",
        "feedback_allowed_candidate",
        "archive_allowed_candidate",
        "worldmodel_handoff_allowed_candidate",
        "fact_status",
        "source_chain",
    ):
        expect(f"tracklet.field.{field_name}", field_name in tracklet_fields)
    for track_state in (
        "active_candidate",
        "tentative_candidate",
        "lost_candidate",
        "stale_candidate",
        "expired_candidate",
        "archived_candidate",
        "rejected_candidate",
    ):
        expect(f"tracklet.state.{track_state}", track_state in tracklet_candidate_schema.get("track_states", []))
    expect("tracklet.tracklet_candidate_not_fact", tracklet_candidate_schema.get("tracklet_candidate_not_fact") is True)
    expect("tracklet.current_action_allowed", tracklet_candidate_schema.get("current_action_allowed") is False)
    expect("tracklet.worldmodel_handoff_allowed_candidate_default", tracklet_candidate_schema.get("worldmodel_handoff_allowed_candidate_default") is False)
    expect("tracklet.non_claims_count", len(tracklet_candidate_schema.get("non_claims", [])) >= 4)

    expect("budget.source_resource_budget_ref", tracking_budget_policy.get("source_resource_budget_ref") == "MidPlatformResourceBudgetPolicy")
    expect("budget.safety_reserved_tracklets", tracking_budget_policy.get("safety_reserved_tracklets") >= 1)
    expect("budget.primary_task_tracklets", tracking_budget_policy.get("primary_task_tracklets") >= 1)
    expect("budget.secondary_task_tracklets", tracking_budget_policy.get("secondary_task_tracklets") >= 0)
    expect("budget.background_observation_tracklets", tracking_budget_policy.get("background_observation_tracklets") == 0)
    expect("budget.max_active_tracklets_total", tracking_budget_policy.get("max_active_tracklets_total") >= tracking_budget_policy.get("safety_reserved_tracklets", 0))
    expect("budget.max_tracklets_per_focus_slot", tracking_budget_policy.get("max_tracklets_per_focus_slot") >= 1)
    expect("budget.drop_low_value_tracklets", tracking_budget_policy.get("drop_low_value_tracklets") is True)
    expect("budget.preempt_by_safety", tracking_budget_policy.get("preempt_by_safety") is True)
    expect("budget.degrade_on_low_hardware_health", tracking_budget_policy.get("degrade_on_low_hardware_health") is True)
    expect("budget.principles_count", len(tracking_budget_policy.get("principles", [])) >= 7)

    expect("admission.requires_source_chain", tracking_target_admission_policy.get("requires_source_chain") is True)
    expect("admission.requires_privacy_filtering", tracking_target_admission_policy.get("requires_privacy_filtering") is True)
    expect("admission.requires_midplatform_approval", tracking_target_admission_policy.get("requires_midplatform_approval") is True)
    expect("admission.requires_budget", tracking_target_admission_policy.get("requires_budget") is True)
    expect("admission.full_scene_tracking_allowed", tracking_target_admission_policy.get("full_scene_tracking_allowed") is False)
    expect("admission.all_moving_objects_tracking_allowed", tracking_target_admission_policy.get("all_moving_objects_tracking_allowed") is False)
    expect("admission.all_person_tracking_allowed", tracking_target_admission_policy.get("all_person_tracking_allowed") is False)
    expect("admission.all_vehicle_tracking_allowed", tracking_target_admission_policy.get("all_vehicle_tracking_allowed") is False)
    for allowed in (
        "P0 safety target",
        "task-relevant target",
        "route-relevant target",
        "user-feedback target",
        "crossing / traffic safety target",
        "destination confirmation target",
        "temporary facility only if task/safety relevant",
        "world observation target only under low-frequency budget",
    ):
        expect(f"admission.allowed.{allowed}", allowed in tracking_target_admission_policy.get("allowed_tracking_targets", []))
    for forbidden in (
        "full scene",
        "all moving objects",
        "all persons",
        "all vehicles",
        "unrelated background pedestrians",
        "distant unrelated vehicles",
        "privacy-sensitive targets without filtering",
        "low-confidence one-frame noise",
        "curiosity-only targets",
        "emotional-interest-only targets",
        "no source_chain targets",
    ):
        expect(f"admission.forbidden.{forbidden}", forbidden in tracking_target_admission_policy.get("forbidden_tracking_targets", []))

    for covered in (
        "walkable_surface tracking candidate",
        "road_surface candidate",
        "route_direction candidate",
        "sidewalk_boundary candidate",
        "curb / step candidate",
        "crossing surface candidate",
        "path_continuity candidate",
    ):
        expect(f"road_surface.covered.{covered}", covered in road_surface_tracking_policy.get("covered_candidates", []))
    expect("road_surface.route_surface_direct_navigation_allowed", road_surface_tracking_policy.get("route_surface_direct_navigation_allowed") is False)
    expect("road_surface.crowd_flow_fallback_allowed", road_surface_tracking_policy.get("crowd_flow_fallback_allowed") is True)
    expect("road_surface.arbitration_required", road_surface_tracking_policy.get("arbitration_required") is True)
    expect("road_surface.principles_count", len(road_surface_tracking_policy.get("principles", [])) >= 5)

    for covered in (
        "pedestrian_approach_candidate",
        "vehicle_approach_candidate",
        "bike_or_e_scooter_candidate",
        "crossing_conflict_candidate",
        "near_field_dynamic_obstacle_candidate",
    ):
        expect(f"pedestrian_vehicle.covered.{covered}", covered in pedestrian_vehicle_tracking_policy.get("covered_candidates", []))
    expect("pedestrian_vehicle.all_person_tracking_allowed", pedestrian_vehicle_tracking_policy.get("all_person_tracking_allowed") is False)
    expect("pedestrian_vehicle.all_vehicle_tracking_allowed", pedestrian_vehicle_tracking_policy.get("all_vehicle_tracking_allowed") is False)
    expect("pedestrian_vehicle.identity_recognition_allowed", pedestrian_vehicle_tracking_policy.get("identity_recognition_allowed") is False)
    expect("pedestrian_vehicle.license_plate_recognition_allowed", pedestrian_vehicle_tracking_policy.get("license_plate_recognition_allowed") is False)
    expect("pedestrian_vehicle.principles_count", len(pedestrian_vehicle_tracking_policy.get("principles", [])) >= 7)

    for covered in (
        "crowd_flow_candidate",
        "pedestrian_flow_direction_candidate",
        "crowd_density_candidate",
        "queue_flow_candidate",
        "occluded_path_fallback_candidate",
    ):
        expect(f"crowd_flow.covered.{covered}", covered in crowd_flow_tracking_policy.get("covered_candidates", []))
    expect("crowd_flow.crowd_flow_follow_action_allowed", crowd_flow_tracking_policy.get("crowd_flow_follow_action_allowed") is False)
    expect("crowd_flow.crowd_flow_overrides_map_or_task_or_safety", crowd_flow_tracking_policy.get("crowd_flow_overrides_map_or_task_or_safety") is False)
    expect("crowd_flow.arbitration_required", crowd_flow_tracking_policy.get("arbitration_required") is True)
    expect("crowd_flow.principles_count", len(crowd_flow_tracking_policy.get("principles", [])) >= 6)

    for covered in (
        "traffic_light_candidate",
        "traffic_light_state_change_candidate",
        "countdown_text_tracking_candidate placeholder",
        "crosswalk_candidate",
        "vehicle_flow_near_crossing",
        "pedestrian_flow_near_crossing",
    ):
        expect(f"traffic_light.covered.{covered}", covered in traffic_light_crossing_tracking_policy.get("covered_candidates", []))
    expect("traffic_light.traffic_light_crossing_action_allowed", traffic_light_crossing_tracking_policy.get("traffic_light_crossing_action_allowed") is False)
    expect("traffic_light.current_action_instruction_allowed", traffic_light_crossing_tracking_policy.get("current_action_instruction_allowed") is False)
    expect("traffic_light.crossing_decision_governance_required", traffic_light_crossing_tracking_policy.get("crossing_decision_governance_required") is True)
    expect("traffic_light.principles_count", len(traffic_light_crossing_tracking_policy.get("principles", [])) >= 6)

    adapters = tracking_adapter_candidate_registry.get("adapters", [])
    adapter_names = [adapter.get("adapter_name") for adapter in adapters]
    expect("adapter_registry.external_tracking_adapters_future_candidate_only", tracking_adapter_candidate_registry.get("external_tracking_adapters_future_candidate_only") is True)
    expect("adapter_registry.must_not_install_or_import_or_execute_now", tracking_adapter_candidate_registry.get("must_not_install_or_import_or_execute_now") is True)
    for adapter_name in (
        "Supervision candidate",
        "ByteTrack candidate",
        "OC-SORT candidate",
        "SORT candidate",
        "BoT-SORT candidate",
        "Optical Flow candidate",
        "Frame-diff / motion-score candidate",
        "Tracklet stability evaluator candidate",
    ):
        expect(f"adapter_registry.name.{adapter_name}", adapter_name in adapter_names)
    for idx, adapter in enumerate(adapters):
        expect(f"adapter_registry.integration_status_{idx}", adapter.get("integration_status") == "future_candidate")
        expect(f"adapter_registry.runtime_invoked_{idx}", adapter.get("runtime_invoked") is False)
        expect(f"adapter_registry.allowed_now_{idx}", adapter.get("allowed_now") is False)
        expect(f"adapter_registry.experiment_branch_required_{idx}", adapter.get("experiment_branch_required") is True)
        expect(f"adapter_registry.privacy_review_required_{idx}", "privacy_review_required" in adapter)
        expect(f"adapter_registry.performance_budget_required_{idx}", "performance_budget_required" in adapter)
    expect("adapter_registry.supervision_not_imported", summary.get("supervision_imported") is False)
    expect("adapter_registry.bytetrack_not_imported", summary.get("bytetrack_imported") is False)
    expect("adapter_registry.ocsort_not_imported", summary.get("ocsort_imported") is False)

    lifecycle_states = tracking_lifecycle_policy.get("states", [])
    lifecycle_state_names = [state.get("state") for state in lifecycle_states]
    expect("lifecycle.state_count_match", tracking_lifecycle_policy.get("state_count") == len(lifecycle_states))
    expect("lifecycle.source_visual_lifecycle_loaded", tracking_lifecycle_policy.get("source_visual_lifecycle_loaded") is True)
    for state_name in (
        "requested",
        "admitted_candidate",
        "active_candidate",
        "tentative_candidate",
        "lost_candidate",
        "stale_candidate",
        "expired_candidate",
        "archived_candidate",
        "rejected_candidate",
    ):
        expect(f"lifecycle.state.{state_name}", state_name in lifecycle_state_names)
    for idx, state in enumerate(lifecycle_states):
        expect(f"lifecycle.current_action_allowed_{idx}", state.get("current_action_allowed") is False)
        expect(f"lifecycle.ttl_required_{idx}", state.get("ttl_required") is True)
        expect(f"lifecycle.privacy_filter_required_{idx}", state.get("privacy_filter_required") is True)
        expect(f"lifecycle.source_chain_required_{idx}", state.get("source_chain_required") is True)

    expect("feedback.speech_allowed_false_until_gate", tracking_feedback_policy.get("speech_allowed_false_until_gate") is True)
    expect("feedback.action_allowed_false", tracking_feedback_policy.get("action_allowed_false") is True)
    expect("feedback.fact_status_not_fact", tracking_feedback_policy.get("fact_status_not_fact") is True)
    expect("feedback.requires_arbitration", tracking_feedback_policy.get("requires_arbitration") is True)
    for output_name in (
        "TrackingFeedbackCandidate",
        "SafetyTrackingFeedbackCandidate",
        "TaskTrackingFeedbackCandidate",
        "RouteTrackingFeedbackCandidate",
        "CrowdFlowFeedbackCandidate",
        "CrossingTrackingFeedbackCandidate",
        "TrackingDegradationFeedbackCandidate",
    ):
        expect(f"feedback.output.{output_name}", output_name in tracking_feedback_policy.get("output_candidates", []))

    scenarios = selective_tracking_scenario_matrix.get("scenarios", [])
    scenario_ids = [row.get("scenario_id") for row in scenarios]
    expect("scenario_matrix.count_match", selective_tracking_scenario_matrix.get("scenario_count") == len(scenarios))
    expect("scenario_matrix.count_ge_10", len(scenarios) >= 10, len(scenarios))
    for scenario_id in (
        "route_surface_tracking_candidate",
        "near_field_obstacle_tracking_candidate",
        "pedestrian_approach_safety_candidate",
        "vehicle_approach_safety_candidate",
        "crowded_path_occluded_surface",
        "traffic_light_state_tracking_candidate",
        "shopfront_tracking_for_target_confirmation",
        "temporary_facility_tracking_candidate",
        "user_feedback_target_tracking_candidate",
        "low_value_background_tracking_rejected",
    ):
        expect(f"scenario_matrix.id.{scenario_id}", scenario_id in scenario_ids)

    scenario_lookup = {row.get("scenario_id"): row for row in scenarios}
    expect("scenario.route_surface_direct_navigation_allowed", scenario_lookup.get("route_surface_tracking_candidate", {}).get("direct_navigation_allowed") is False)
    expect("scenario.near_field_safety_arbitration_required", scenario_lookup.get("near_field_obstacle_tracking_candidate", {}).get("safety_arbitration_required") is True)
    expect("scenario.pedestrian_identity_recognition_allowed", scenario_lookup.get("pedestrian_approach_safety_candidate", {}).get("identity_recognition_allowed") is False)
    expect("scenario.vehicle_license_plate_recognition_allowed", scenario_lookup.get("vehicle_approach_safety_candidate", {}).get("license_plate_recognition_allowed") is False)
    expect("scenario.crowded_path_fallback", scenario_lookup.get("crowded_path_occluded_surface", {}).get("crowd_flow_fallback_candidate") is True)
    expect("scenario.crowded_path_follow_action_allowed", scenario_lookup.get("crowded_path_occluded_surface", {}).get("follow_crowd_action_allowed") is False)
    expect("scenario.traffic_light_crossing_action_allowed", scenario_lookup.get("traffic_light_state_tracking_candidate", {}).get("crossing_action_allowed") is False)
    expect("scenario.shopfront_ocr_followup_placeholder_allowed", scenario_lookup.get("shopfront_tracking_for_target_confirmation", {}).get("ocr_followup_placeholder_allowed") is True)
    expect("scenario.temporary_ttl_required", scenario_lookup.get("temporary_facility_tracking_candidate", {}).get("ttl_required") is True)
    expect("scenario.temporary_fixed_poi_write_allowed", scenario_lookup.get("temporary_facility_tracking_candidate", {}).get("fixed_poi_write_allowed") is False)
    expect("scenario.user_feedback_focus_slot_adjustment_required", scenario_lookup.get("user_feedback_target_tracking_candidate", {}).get("focus_slot_adjustment_required") is True)
    expect("scenario.low_value_rejected", scenario_lookup.get("low_value_background_tracking_rejected", {}).get("rejected") is True)
    expect("scenario.low_value_admission_allowed", scenario_lookup.get("low_value_background_tracking_rejected", {}).get("admission_allowed") is False)
    for idx, row in enumerate(scenarios):
        expect(f"scenario.requires_runtime_now_{idx}", row.get("requires_runtime_now") is False)
        expect(f"scenario.fact_write_allowed_{idx}", row.get("fact_write_allowed") is False)

    expect("boundary.tracking_authority_owner", selective_tracking_boundary_matrix.get("tracking_authority_owner") == "MidPlatform")
    expect("boundary.full_scene_tracking_allowed", selective_tracking_boundary_matrix.get("full_scene_tracking_allowed") is False)
    expect("boundary.all_moving_objects_tracking_allowed", selective_tracking_boundary_matrix.get("all_moving_objects_tracking_allowed") is False)
    expect("boundary.all_person_tracking_allowed", selective_tracking_boundary_matrix.get("all_person_tracking_allowed") is False)
    expect("boundary.all_vehicle_tracking_allowed", selective_tracking_boundary_matrix.get("all_vehicle_tracking_allowed") is False)
    expect("boundary.crowd_flow_follow_action_allowed", selective_tracking_boundary_matrix.get("crowd_flow_follow_action_allowed") is False)
    expect("boundary.traffic_light_crossing_action_allowed", selective_tracking_boundary_matrix.get("traffic_light_crossing_action_allowed") is False)
    expect("boundary.external_tracking_adapters_future_candidate_only", selective_tracking_boundary_matrix.get("external_tracking_adapters_future_candidate_only") is True)
    expect("boundary.tracking_runtime_enabled", selective_tracking_boundary_matrix.get("tracking_runtime_enabled") is False)
    expect("boundary.camera_runtime_allowed", selective_tracking_boundary_matrix.get("camera_runtime_allowed") is False)
    expect("boundary.map_api_allowed", selective_tracking_boundary_matrix.get("map_api_allowed") is False)
    expect("boundary.ocr_provider_runtime_allowed", selective_tracking_boundary_matrix.get("ocr_provider_runtime_allowed") is False)
    expect("boundary.ocrrequest_submitted", selective_tracking_boundary_matrix.get("ocrrequest_submitted") is False)
    expect("boundary.tracking_runtime_allowed", selective_tracking_boundary_matrix.get("tracking_runtime_allowed") is False)
    expect("boundary.optical_flow_runtime_allowed", selective_tracking_boundary_matrix.get("optical_flow_runtime_allowed") is False)
    expect("boundary.supervision_allowed_now", selective_tracking_boundary_matrix.get("supervision_allowed_now") is False)
    expect("boundary.bytetrack_allowed_now", selective_tracking_boundary_matrix.get("bytetrack_allowed_now") is False)
    expect("boundary.ocsort_allowed_now", selective_tracking_boundary_matrix.get("ocsort_allowed_now") is False)
    expect("boundary.sort_allowed_now", selective_tracking_boundary_matrix.get("sort_allowed_now") is False)
    expect("boundary.botsort_allowed_now", selective_tracking_boundary_matrix.get("botsort_allowed_now") is False)
    expect("boundary.entity_resolution_runtime_allowed", selective_tracking_boundary_matrix.get("entity_resolution_runtime_allowed") is False)
    expect("boundary.fact_admission_runtime_allowed", selective_tracking_boundary_matrix.get("fact_admission_runtime_allowed") is False)
    expect("boundary.memory_consolidation_allowed", selective_tracking_boundary_matrix.get("memory_consolidation_allowed") is False)
    expect("boundary.library_experience_commit_allowed", selective_tracking_boundary_matrix.get("library_experience_commit_allowed") is False)
    expect("boundary.worldmodel_write_allowed", selective_tracking_boundary_matrix.get("worldmodel_write_allowed") is False)
    expect("boundary.memory_write_allowed", selective_tracking_boundary_matrix.get("memory_write_allowed") is False)
    expect("boundary.library_write_allowed", selective_tracking_boundary_matrix.get("library_write_allowed") is False)
    expect("boundary.fact_write_allowed", selective_tracking_boundary_matrix.get("fact_write_allowed") is False)
    expect("boundary.scene_delta_allowed", selective_tracking_boundary_matrix.get("scene_delta_allowed") is False)
    expect("boundary.task_state_commit_allowed", selective_tracking_boundary_matrix.get("task_state_commit_allowed") is False)
    expect("boundary.navigation_action_allowed", selective_tracking_boundary_matrix.get("navigation_action_allowed") is False)
    expect("boundary.speech_gate_allowed", selective_tracking_boundary_matrix.get("speech_gate_allowed") is False)
    expect("boundary.vop_allowed", selective_tracking_boundary_matrix.get("vop_allowed") is False)

    debt_rows = governance_debt_register.get("debts", [])
    expect("governance_debt.count_ge_9", len(debt_rows) >= 9, len(debt_rows))
    expect("governance_debt.future_midplatform_function_governance_required", governance_debt_register.get("future_midplatform_function_governance_required") is True)
    expect("governance_debt.no_duplicate_governance_module_allowed", governance_debt_register.get("no_duplicate_governance_module_allowed") is True)
    for topic in (
        "tracking admission arbitration complexity",
        "tracking budget preemption governance complexity",
        "road surface fallback governance complexity",
        "crowd flow conservative output governance complexity",
        "crossing tracking escalation governance complexity",
        "external tracking adapter review governance complexity",
        "tracking lifecycle archival governance complexity",
        "duplicated schema risk",
        "future midplatform function governance required",
    ):
        expect(f"governance_debt.topic.{topic}", any(row.get("topic") == topic for row in debt_rows))
    for idx, row in enumerate(debt_rows):
        expect(f"governance_debt.reuse_or_consolidation_required_{idx}", row.get("reuse_or_consolidation_required") is True)
        expect(f"governance_debt.duplicate_governance_module_allowed_{idx}", row.get("duplicate_governance_module_allowed") is False)
        expect(f"governance_debt.future_owner_phase_{idx}", row.get("future_owner_phase") == "MidPlatform Function Governance / Consolidation")

    runtime_flags = (
        ("no_runtime_executed", True),
        ("no_new_runtime_enabled", True),
        ("tracking_runtime_enabled", False),
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
        ("sort_invoked", False),
        ("botsort_invoked", False),
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
    )
    for flag_name, expected in runtime_flags:
        expect(f"runtime.summary.{flag_name}", summary.get(flag_name) is expected)
    expect("runtime.summary.boundary_ok", summary.get("boundary_ok") is True)
    expect("runtime.summary.violations_empty", summary.get("violations") == [])

    for payload_name, payload in (("no_runtime", no_runtime_boundary_report), ("no_write", no_write_boundary_report)):
        expect(f"{payload_name}.tracking_authority_owner", payload.get("tracking_authority_owner") == "MidPlatform")
        expect(f"{payload_name}.full_scene_tracking_allowed", payload.get("full_scene_tracking_allowed") is False)
        expect(f"{payload_name}.all_moving_objects_tracking_allowed", payload.get("all_moving_objects_tracking_allowed") is False)
        expect(f"{payload_name}.all_person_tracking_allowed", payload.get("all_person_tracking_allowed") is False)
        expect(f"{payload_name}.all_vehicle_tracking_allowed", payload.get("all_vehicle_tracking_allowed") is False)
        expect(f"{payload_name}.crowd_flow_follow_action_allowed", payload.get("crowd_flow_follow_action_allowed") is False)
        expect(f"{payload_name}.traffic_light_crossing_action_allowed", payload.get("traffic_light_crossing_action_allowed") is False)
        expect(f"{payload_name}.worldmodel_write_allowed", payload.get("worldmodel_write_allowed") is False)
        expect(f"{payload_name}.memory_write_allowed", payload.get("memory_write_allowed") is False)
        expect(f"{payload_name}.library_write_allowed", payload.get("library_write_allowed") is False)
        expect(f"{payload_name}.handoff_candidate_not_fact", payload.get("handoff_candidate_not_fact") is True)
        expect(f"{payload_name}.placeholder_not_runtime", payload.get("placeholder_not_runtime") is True)
        expect(f"{payload_name}.boundary_ok", payload.get("boundary_ok") is True)
        expect(f"{payload_name}.violations_empty", payload.get("violations") == [])
        for flag_name, expected in runtime_flags:
            expect(f"{payload_name}.{flag_name}", payload.get(flag_name) is expected)

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
        "final_decision": FINAL_DECISION if verdict == "GO" else "SELECTIVE_TRACKING_ADAPTER_POLICY_REVIEW_REQUIRED",
        "recommended_next_phase": NEXT_PHASE if verdict == "GO" else PHASE_ID,
        "failed_checks": [item for item in checks if not item["passed"]],
        "checks": checks,
    }
    (output_root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verdict": verdict, "checks_passed": passed_count, "checks_total": len(checks)}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
