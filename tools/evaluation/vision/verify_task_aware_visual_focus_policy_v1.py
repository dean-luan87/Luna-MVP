#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Task-Aware Visual Focus Policy v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


DEFAULT_WORKSPACE_ROOT = Path("/Users/luanlei/Desktop/Luna-Workspace-Min")
DEFAULT_OUTPUT_ROOT = DEFAULT_WORKSPACE_ROOT / "_eval_out" / "task_aware_visual_focus_policy_v1_smoke_v0"
PHASE_ID = "Phase-Task-Aware-Visual-Focus-Policy-v1-001"
FINAL_DECISION = "TASK_AWARE_VISUAL_FOCUS_POLICY_READY_FOR_WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY"
NEXT_PHASE = "Phase-World-Observation-and-Entity-Feature-Policy-v1-001"
MIN_CHECKS = 160
BASELINE_REQUIREMENT = 120


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify Task-Aware Visual Focus Policy v1")
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
    scene_sketch = _load_json(output_root / "scene_sketch_candidate_schema.json")
    focus_plan = _load_json(output_root / "visual_focus_plan_schema.json")
    focus_slot = _load_json(output_root / "visual_focus_slot_schema.json")
    view_quality = _load_json(output_root / "view_quality_candidate_schema.json")
    active_adjustment = _load_json(output_root / "active_view_adjustment_candidate_schema.json")
    lifecycle = _load_json(output_root / "visual_observation_lifecycle_policy.json")
    focus_to_ocr = _load_json(output_root / "focus_to_ocr_activation_policy.json")
    focus_to_tracking = _load_json(output_root / "focus_to_tracking_request_policy.json")
    feedback = _load_json(output_root / "visual_focus_feedback_policy.json")
    wml_boundary = _load_json(output_root / "deferred_worldmodel_memory_library_boundary.json")
    scenario_matrix = _load_json(output_root / "task_aware_visual_focus_scenario_matrix.json")
    boundary_matrix = _load_json(output_root / "visual_focus_boundary_matrix.json")
    governance_debt = _load_json(output_root / "governance_debt_register.json")
    next_phase = _load_json(output_root / "next_phase_recommendation.json")
    no_runtime = _load_json(output_root / "no_runtime_boundary_report.json")
    no_write = _load_json(output_root / "no_write_boundary_report.json")

    # Input checks
    expect("input.midplatform_perception_orchestration_input_loaded", summary.get("midplatform_perception_orchestration_input_loaded") is True)
    expect("input.return_to_vision_planning_input_loaded", summary.get("return_to_vision_planning_input_loaded") is True)
    expect("input.preplan_input_loaded", summary.get("preplan_input_loaded") is True)
    expect("input.ocr_final_closure_loaded", summary.get("ocr_final_closure_loaded") is True)
    expect("input.minimal_runtime_integration_closure_loaded", summary.get("minimal_runtime_integration_closure_loaded") is True)
    expect("input.root_matrix_rows_present", isinstance(input_root_matrix.get("rows"), list))
    expect("input.root_matrix_row_count_match", input_root_matrix.get("row_count") == len(input_root_matrix.get("rows", [])))
    for intake_id in (
        "midplatform_perception_orchestration",
        "return_to_vision_planning",
        "preplan_input",
        "ocr_final_closure",
        "minimal_runtime_integration_closure",
        "midplatform_perception_orchestration_doc",
        "vision_planning_doc",
        "vision_preplan_doc",
        "ocr_final_closure_doc",
        "minimal_runtime_integration_closure_doc",
        "ocr_phase_verdict_table",
    ):
        expect(
            f"input.required.{intake_id}",
            any(row.get("intake_id") == intake_id and row.get("loaded") is True for row in input_root_matrix.get("rows", [])),
        )

    # Summary checks
    expect("summary.policy_scope", summary.get("policy_scope") == "task_aware_visual_focus_policy_only")
    expect("summary.scene_sketch_candidate_schema_defined", summary.get("scene_sketch_candidate_schema_defined") is True)
    expect("summary.visual_focus_plan_schema_defined", summary.get("visual_focus_plan_schema_defined") is True)
    expect("summary.visual_focus_slot_schema_defined", summary.get("visual_focus_slot_schema_defined") is True)
    expect("summary.view_quality_candidate_schema_defined", summary.get("view_quality_candidate_schema_defined") is True)
    expect("summary.active_view_adjustment_candidate_schema_defined", summary.get("active_view_adjustment_candidate_schema_defined") is True)
    expect("summary.visual_observation_lifecycle_policy_defined", summary.get("visual_observation_lifecycle_policy_defined") is True)
    expect("summary.focus_to_ocr_activation_policy_defined", summary.get("focus_to_ocr_activation_policy_defined") is True)
    expect("summary.focus_to_tracking_request_policy_defined", summary.get("focus_to_tracking_request_policy_defined") is True)
    expect("summary.visual_focus_feedback_policy_defined", summary.get("visual_focus_feedback_policy_defined") is True)
    expect("summary.scenario_matrix_generated", summary.get("scenario_matrix_generated") is True)
    expect("summary.scenario_count", summary.get("scenario_count", 0) >= 8, summary.get("scenario_count"))
    expect("summary.safety_focus_slots_defined", summary.get("safety_focus_slots_defined") is True)
    expect("summary.task_focus_slots_defined", summary.get("task_focus_slots_defined") is True)
    expect("summary.view_quality_degradation_policy_defined", summary.get("view_quality_degradation_policy_defined") is True)
    expect("summary.active_view_adjustment_policy_defined", summary.get("active_view_adjustment_policy_defined") is True)
    expect("summary.ocr_activation_request_candidate_only", summary.get("ocr_activation_request_candidate_only") is True)
    expect("summary.tracking_request_candidate_only", summary.get("tracking_request_candidate_only") is True)
    expect("summary.full_frame_ocr_allowed", summary.get("full_frame_ocr_allowed") is False)
    expect("summary.full_scene_tracking_allowed", summary.get("full_scene_tracking_allowed") is False)

    # Scene sketch checks
    scene_fields = [item.get("name") for item in scene_sketch.get("fields", [])]
    expect("scene_sketch.object_name", scene_sketch.get("object_name") == "SceneSketchCandidate")
    expect("scene_sketch.field_count_match", scene_sketch.get("field_count") == len(scene_sketch.get("fields", [])))
    for field_name in (
        "scene_sketch_id",
        "source_work_order_id",
        "source_frame_ref_placeholder",
        "task_context_ref",
        "location_context_ref",
        "pose_or_view_context_ref",
        "scene_type_candidate",
        "self_position_hint",
        "left_context",
        "right_context",
        "front_context",
        "far_context",
        "near_ground_context",
        "walkable_area_hint",
        "human_density_candidate",
        "vehicle_presence_candidate",
        "signage_or_text_hint",
        "obstacle_hint",
        "traffic_light_or_crossing_hint",
        "temporary_facility_hint",
        "visibility_quality_ref",
        "uncertainty",
        "freshness_status",
        "ttl_policy_ref",
        "privacy_tags",
        "fact_status",
        "write_allowed",
        "source_chain",
    ):
        expect(f"scene_sketch.field.{field_name}", field_name in scene_fields)
    expect("scene_sketch.output_role", scene_sketch.get("output_role") == "VisualFocusPlan input candidate")
    expect("scene_sketch.input_contract_count", len(scene_sketch.get("input_contract", [])) >= 3)
    expect("scene_sketch.not_fact", scene_sketch.get("fact_status") == "not_fact")
    expect("scene_sketch.write_allowed", scene_sketch.get("write_allowed") is False)
    expect("scene_sketch.non_claims_count", len(scene_sketch.get("non_claims", [])) >= 4)

    # Visual focus plan checks
    focus_plan_fields = [item.get("name") for item in focus_plan.get("fields", [])]
    expect("focus_plan.object_name", focus_plan.get("object_name") == "VisualFocusPlan")
    expect("focus_plan.field_count_match", focus_plan.get("field_count") == len(focus_plan.get("fields", [])))
    for field_name in (
        "visual_focus_plan_id",
        "source_work_order_id",
        "source_scene_sketch_id",
        "task_id",
        "task_type",
        "task_phase",
        "focus_slots",
        "ignored_by_default",
        "ocr_activation_slots",
        "tracking_request_slots",
        "map_memory_binding_slots",
        "safety_focus_slots",
        "active_view_adjustment_slots",
        "budget_policy_ref",
        "privacy_policy_ref",
        "freshness_policy_ref",
        "conflict_policy_ref",
        "output_handoff_policy_ref",
        "fact_status",
        "runtime_action_allowed",
        "source_chain",
    ):
        expect(f"focus_plan.field.{field_name}", field_name in focus_plan_fields)
    expect("focus_plan.runtime_action_allowed", focus_plan.get("runtime_action_allowed") is False)
    expect("focus_plan.not_fact", focus_plan.get("fact_status") == "not_fact")
    expect("focus_plan.non_claims_count", len(focus_plan.get("non_claims", [])) >= 4)

    # Visual focus slot checks
    focus_slot_fields = [item.get("name") for item in focus_slot.get("fields", [])]
    slot_types = focus_slot.get("slot_types", [])
    expect("focus_slot.object_name", focus_slot.get("object_name") == "VisualFocusSlot")
    expect("focus_slot.field_count_match", focus_slot.get("field_count") == len(focus_slot.get("fields", [])))
    for field_name in (
        "slot_id",
        "source_visual_focus_plan_id",
        "slot_type",
        "target",
        "priority",
        "task_relevance",
        "safety_relevance",
        "route_relevance",
        "map_memory_relevance",
        "expected_evidence_type",
        "tracking_required",
        "ocr_required",
        "map_binding_required",
        "active_view_adjustment_allowed",
        "activation_condition",
        "expiration_condition",
        "max_budget",
        "stc_policy_ref",
        "ttl_policy_ref",
        "freshness_requirement",
        "privacy_filter_required",
        "output_allowed",
        "action_allowed",
        "fact_status",
        "source_chain",
    ):
        expect(f"focus_slot.field.{field_name}", field_name in focus_slot_fields)
    for slot_type in (
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
        "signage_focus",
        "doorway_or_entrance_focus",
        "support_surface_focus",
        "tabletop_focus",
        "shelf_or_counter_focus",
        "floor_near_user_focus",
        "readable_region_focus",
        "temporary_facility_focus",
        "user_feedback_focus",
        "world_observation_focus",
    ):
        expect(f"focus_slot.slot_type.{slot_type}", slot_type in slot_types)
    expect("focus_slot.output_allowed_default", all(item.get("default") is False for item in focus_slot.get("fields", []) if item.get("name") == "output_allowed"))
    expect("focus_slot.action_allowed_default", all(item.get("default") is False for item in focus_slot.get("fields", []) if item.get("name") == "action_allowed"))
    expect("focus_slot.non_claims_count", len(focus_slot.get("non_claims", [])) >= 3)

    # View quality checks
    view_quality_fields = [item.get("name") for item in view_quality.get("fields", [])]
    degradation = view_quality.get("degradation_policy", {})
    expect("view_quality.object_name", view_quality.get("object_name") == "ViewQualityCandidate")
    expect("view_quality.field_count_match", view_quality.get("field_count") == len(view_quality.get("fields", [])))
    for field_name in (
        "view_quality_id",
        "source_work_order_id",
        "source_frame_ref_placeholder",
        "blur_level_candidate",
        "brightness_quality_candidate",
        "exposure_quality_candidate",
        "occlusion_level_candidate",
        "camera_shake_candidate",
        "target_distance_quality_candidate",
        "dynamic_motion_quality_candidate",
        "crowd_occlusion_candidate",
        "reflection_or_weather_candidate",
        "frame_stability_candidate",
        "readable_region_quality_hint",
        "safe_for_scene_sketch",
        "safe_for_ocr_activation",
        "safe_for_tracking_request",
        "requires_active_view_adjustment",
        "recommended_degradation",
        "fact_status",
        "source_chain",
    ):
        expect(f"view_quality.field.{field_name}", field_name in view_quality_fields)
    for level in ("GOOD", "DEGRADED", "POOR", "BLOCKED"):
        expect(f"view_quality.level.{level}", level in degradation)
    expect("view_quality.good_scene_sketch_allowed", (degradation.get("GOOD") or {}).get("scene_sketch_allowed") is True)
    expect("view_quality.good_visual_focus_plan_allowed", (degradation.get("GOOD") or {}).get("visual_focus_plan_allowed") is True)
    expect("view_quality.degraded_rule", (degradation.get("DEGRADED") or {}).get("degradation_rule") == "只允许 safety + primary task focus")
    expect("view_quality.poor_rule", (degradation.get("POOR") or {}).get("degradation_rule") == "只允许 safety focus / active view adjustment candidate")
    expect("view_quality.blocked_rule", (degradation.get("BLOCKED") or {}).get("degradation_rule") == "暂停任务视觉，只保留 safety candidate")
    expect("view_quality.non_claims_count", len(view_quality.get("non_claims", [])) >= 3)

    # Active view adjustment checks
    adjustment_fields = [item.get("name") for item in active_adjustment.get("fields", [])]
    adjustment_types = active_adjustment.get("adjustment_types", [])
    expect("active_adjustment.object_name", active_adjustment.get("object_name") == "ActiveViewAdjustmentCandidate")
    expect("active_adjustment.field_count_match", active_adjustment.get("field_count") == len(active_adjustment.get("fields", [])))
    for field_name in (
        "active_view_adjustment_id",
        "source_focus_slot_id",
        "missing_visual_evidence",
        "suggested_view_adjustment",
        "adjustment_type",
        "urgency",
        "safety_constraint",
        "user_message_candidate",
        "speech_gate_required",
        "output_allowed",
        "action_allowed",
        "fact_status",
        "source_chain",
    ):
        expect(f"active_adjustment.field.{field_name}", field_name in adjustment_fields)
    for adjustment_type in (
        "turn_left_slightly",
        "turn_right_slightly",
        "look_up",
        "look_down",
        "move_closer",
        "step_back",
        "hold_still",
        "center_target",
        "scan_right_side",
        "scan_left_side",
        "focus_on_tabletop",
        "focus_on_doorplate",
        "focus_on_shopfront",
    ):
        expect(f"active_adjustment.type.{adjustment_type}", adjustment_type in adjustment_types)
    expect("active_adjustment.speech_gate_required", active_adjustment.get("speech_gate_required") is True)
    expect("active_adjustment.action_allowed", active_adjustment.get("action_allowed") is False)
    expect("active_adjustment.non_claims_count", len(active_adjustment.get("non_claims", [])) >= 3)

    # Lifecycle checks
    lifecycle_states = lifecycle.get("states", [])
    lifecycle_names = [row.get("state") for row in lifecycle_states]
    expect("lifecycle.state_count_match", lifecycle.get("state_count") == len(lifecycle_states))
    for state_name in (
        "active",
        "stale",
        "expired",
        "archived_candidate",
        "worldmodel_handoff_candidate",
        "rejected",
        "promoted_later_placeholder",
    ):
        expect(f"lifecycle.state.{state_name}", state_name in lifecycle_names)
    for idx, row in enumerate(lifecycle_states):
        expect(f"lifecycle.source_chain_required_{idx}", row.get("source_chain_required") is True)
        expect(f"lifecycle.privacy_filter_required_{idx}", row.get("privacy_filter_required") is True)
        expect(f"lifecycle.ttl_required_{idx}", row.get("ttl_required") is True)
    expired_row = next((row for row in lifecycle_states if row.get("state") == "expired"), {})
    archived_row = next((row for row in lifecycle_states if row.get("state") == "archived_candidate"), {})
    handoff_row = next((row for row in lifecycle_states if row.get("state") == "worldmodel_handoff_candidate"), {})
    expect("lifecycle.expired_current_action_allowed", expired_row.get("current_action_allowed") is False)
    expect("lifecycle.archived_worldmodel_handoff_allowed", archived_row.get("worldmodel_handoff_allowed_candidate") is True)
    expect("lifecycle.archived_memory_handoff_allowed", archived_row.get("memory_handoff_allowed_candidate") is True)
    expect("lifecycle.archived_library_handoff_allowed", archived_row.get("library_handoff_placeholder_allowed") is True)
    expect("lifecycle.handoff_worldmodel_handoff_allowed", handoff_row.get("worldmodel_handoff_allowed_candidate") is True)

    # OCR activation checks
    expect("focus_to_ocr.candidate_only", focus_to_ocr.get("ocr_activation_request_candidate_only") is True)
    expect("focus_to_ocr.ocrrequest_submitted", focus_to_ocr.get("ocrrequest_submitted") is False)
    expect("focus_to_ocr.provider_invocation_allowed", focus_to_ocr.get("ocr_provider_runtime_invocation_allowed") is False)
    for slot_type in (
        "readable_region_focus",
        "signage_focus",
        "shopfront_focus",
        "doorway_or_entrance_focus",
        "destination_landmark_focus",
        "traffic_light_focus",
        "temporary_facility_focus",
    ):
        expect(f"focus_to_ocr.allowed.{slot_type}", slot_type in focus_to_ocr.get("allowed_focus_slot_types", []))
    for forbidden in (
        "full_frame_ocr",
        "low_quality_view_ocr",
        "non_task_relevant_background_text",
        "privacy_sensitive_text_without_filtering",
        "ocr_provider_runtime_invocation_in_this_phase",
    ):
        expect(f"focus_to_ocr.forbidden.{forbidden}", forbidden in focus_to_ocr.get("forbidden_cases", []))

    # Tracking request checks
    expect("focus_to_tracking.candidate_only", focus_to_tracking.get("tracking_request_candidate_only") is True)
    expect("focus_to_tracking.runtime_invocation_allowed", focus_to_tracking.get("tracking_runtime_invocation_allowed") is False)
    for slot_type in (
        "safety_focus",
        "route_path_focus",
        "walkable_surface_focus",
        "dynamic_obstacle_focus",
        "traffic_light_focus",
        "pedestrian_flow_focus",
        "vehicle_flow_focus",
        "destination_landmark_focus",
        "user_feedback_focus",
    ):
        expect(f"focus_to_tracking.allowed.{slot_type}", slot_type in focus_to_tracking.get("allowed_focus_slot_types", []))
    for forbidden in (
        "full_scene_tracking",
        "all_moving_objects_tracking",
        "all_person_tracking",
        "all_vehicle_tracking",
        "background_tracking_without_task_or_safety_relevance",
        "tracking_runtime_invocation_in_this_phase",
    ):
        expect(f"focus_to_tracking.forbidden.{forbidden}", forbidden in focus_to_tracking.get("forbidden_cases", []))

    # Feedback checks
    expect("feedback.speech_allowed_false_until_gate", feedback.get("speech_allowed_false_until_gate") is True)
    expect("feedback.action_allowed_false", feedback.get("action_allowed_false") is True)
    expect("feedback.fact_status_not_fact", feedback.get("fact_status_not_fact") is True)
    expect("feedback.requires_arbitration", feedback.get("requires_arbitration") is True)
    for output_name in (
        "VisualFocusFeedbackCandidate",
        "SceneSketchFeedbackCandidate",
        "ViewQualityFeedbackCandidate",
        "ActiveViewAdjustmentFeedbackCandidate",
        "OCRActivationRequestCandidate",
        "TrackingRequestCandidate",
        "SafetyFocusFeedbackCandidate",
        "TaskFocusFeedbackCandidate",
    ):
        expect(f"feedback.output.{output_name}", output_name in feedback.get("output_candidates", []))
    for field_name in (
        "feedback_id",
        "feedback_type",
        "source_visual_focus_plan_id",
        "related_focus_slot_id",
        "evidence_refs",
        "requires_arbitration",
        "speech_allowed",
        "action_allowed",
        "fact_status",
        "source_chain",
    ):
        expect(f"feedback.field.{field_name}", field_name in feedback.get("feedback_common_fields", []))

    # Scenario checks
    scenarios = scenario_matrix.get("scenarios", [])
    scenario_ids = [row.get("scenario_id") for row in scenarios]
    expect("scenario_matrix.generated", summary.get("scenario_matrix_generated") is True)
    expect("scenario_matrix.count_match", scenario_matrix.get("scenario_count") == len(scenarios))
    expect("scenario_matrix.count_ge_8", len(scenarios) >= 8, len(scenarios))
    for scenario_id in (
        "navigation_route_walking",
        "navigation_approaching_crossing",
        "navigation_approaching_destination",
        "shop_search_right_side_storefront",
        "object_search_home_keys",
        "home_familiar_object_interaction",
        "low_quality_view_hold_still",
        "crowded_path_occluded_surface",
    ):
        expect(f"scenario_matrix.id.{scenario_id}", scenario_id in scenario_ids)
    low_quality_row = next((row for row in scenarios if row.get("scenario_id") == "low_quality_view_hold_still"), {})
    crowded_row = next((row for row in scenarios if row.get("scenario_id") == "crowded_path_occluded_surface"), {})
    crossing_row = next((row for row in scenarios if row.get("scenario_id") == "navigation_approaching_crossing"), {})
    destination_row = next((row for row in scenarios if row.get("scenario_id") == "navigation_approaching_destination"), {})
    home_row = next((row for row in scenarios if row.get("scenario_id") == "home_familiar_object_interaction"), {})
    expect("scenario.low_quality_view_quality", low_quality_row.get("view_quality_candidate") == "POOR")
    expect("scenario.low_quality_hold_still", low_quality_row.get("active_view_adjustment") == "hold_still")
    expect("scenario.low_quality_task_visual_focus_suppressed", low_quality_row.get("task_visual_focus_suppressed") is True)
    expect("scenario.low_quality_safety_focus_retained", low_quality_row.get("safety_focus_retained") is True)
    expect("scenario.crowded_walkable_surface_mode", crowded_row.get("walkable_surface_focus_mode") == "degraded")
    expect("scenario.crowded_pedestrian_flow_enabled", crowded_row.get("pedestrian_flow_focus_enabled") is True)
    expect("scenario.crowded_flow_not_action", crowded_row.get("crowd_flow_follow_candidate_not_action") is True)
    expect("scenario.crossing_active_view_adjustment_if_low_confidence", crossing_row.get("active_view_adjustment_if_low_confidence") is True)
    expect("scenario.destination_ocr_activation_candidate", destination_row.get("ocr_activation_candidate") is True)
    expect("scenario.home_memory_handoff_placeholder", home_row.get("memory_handoff_candidate_placeholder") is True)
    for idx, row in enumerate(scenarios):
        expect(f"scenario.requires_runtime_now_{idx}", row.get("requires_runtime_now") is False)
        expect(f"scenario.fact_write_allowed_{idx}", row.get("fact_write_allowed") is False)

    # WorldModel / Memory / Library checks
    expect("wml_boundary.entity_resolution_deferred", wml_boundary.get("entity_resolution_deferred") is True)
    expect("wml_boundary.fact_admission_deferred", wml_boundary.get("fact_admission_deferred") is True)
    expect("wml_boundary.memory_consolidation_deferred", wml_boundary.get("memory_consolidation_deferred") is True)
    expect("wml_boundary.library_experience_governance_deferred", wml_boundary.get("library_experience_governance_deferred") is True)
    expect("wml_boundary.worldmodel_write_allowed", wml_boundary.get("worldmodel_write_allowed") is False)
    expect("wml_boundary.memory_write_allowed", wml_boundary.get("memory_write_allowed") is False)
    expect("wml_boundary.library_write_allowed", wml_boundary.get("library_write_allowed") is False)
    expect("wml_boundary.handoff_candidate_not_fact", wml_boundary.get("handoff_candidate_not_fact") is True)
    expect("wml_boundary.placeholder_not_runtime", wml_boundary.get("placeholder_not_runtime") is True)
    expect("wml_boundary.worldmodel_handoff_candidate_allowed", wml_boundary.get("worldmodel_handoff_candidate_allowed") is True)
    expect("wml_boundary.memory_handoff_candidate_allowed", wml_boundary.get("memory_handoff_candidate_allowed") is True)
    expect("wml_boundary.library_handoff_placeholder_allowed", wml_boundary.get("library_handoff_placeholder_allowed") is True)
    expect("wml_boundary.midplatform_boundary_loaded", wml_boundary.get("midplatform_boundary_loaded") is True)
    expect("wml_boundary.planning_boundary_loaded", wml_boundary.get("planning_boundary_loaded") is True)
    expect("wml_boundary.preplan_boundary_loaded", wml_boundary.get("preplan_boundary_loaded") is True)

    # Boundary matrix checks
    expect("boundary.camera_runtime_allowed", boundary_matrix.get("camera_runtime_allowed") is False)
    expect("boundary.ocr_provider_runtime_allowed", boundary_matrix.get("ocr_provider_runtime_allowed") is False)
    expect("boundary.ocrrequest_submitted", boundary_matrix.get("ocrrequest_submitted") is False)
    expect("boundary.tracking_runtime_allowed", boundary_matrix.get("tracking_runtime_allowed") is False)
    expect("boundary.optical_flow_runtime_allowed", boundary_matrix.get("optical_flow_runtime_allowed") is False)
    expect("boundary.supervision_runtime_allowed", boundary_matrix.get("supervision_runtime_allowed") is False)
    expect("boundary.bytetrack_runtime_allowed", boundary_matrix.get("bytetrack_runtime_allowed") is False)
    expect("boundary.ocsort_runtime_allowed", boundary_matrix.get("ocsort_runtime_allowed") is False)
    expect("boundary.map_api_allowed", boundary_matrix.get("map_api_allowed") is False)
    expect("boundary.speech_gate_allowed", boundary_matrix.get("speech_gate_allowed") is False)
    expect("boundary.vop_allowed", boundary_matrix.get("vop_allowed") is False)
    expect("boundary.full_frame_ocr_allowed", boundary_matrix.get("full_frame_ocr_allowed") is False)
    expect("boundary.full_scene_tracking_allowed", boundary_matrix.get("full_scene_tracking_allowed") is False)
    expect("boundary.worldmodel_write_allowed", boundary_matrix.get("worldmodel_write_allowed") is False)
    expect("boundary.memory_write_allowed", boundary_matrix.get("memory_write_allowed") is False)
    expect("boundary.library_write_allowed", boundary_matrix.get("library_write_allowed") is False)
    expect("boundary.fact_write_allowed", boundary_matrix.get("fact_write_allowed") is False)
    expect("boundary.scene_delta_allowed", boundary_matrix.get("scene_delta_allowed") is False)
    expect("boundary.task_state_commit_allowed", boundary_matrix.get("task_state_commit_allowed") is False)
    expect("boundary.navigation_action_allowed", boundary_matrix.get("navigation_action_allowed") is False)

    # Governance debt checks
    debt_rows = governance_debt.get("debts", [])
    expect("governance_debt.generated", summary.get("governance_debt_register_generated") is True)
    expect("governance_debt.count_ge_8", len(debt_rows) >= 8, len(debt_rows))
    expect("governance_debt.future_midplatform_function_governance_required", governance_debt.get("future_midplatform_function_governance_required") is True)
    expect("governance_debt.no_duplicate_governance_module_allowed", governance_debt.get("no_duplicate_governance_module_allowed") is True)
    for topic in (
        "visual focus slot schema complexity",
        "view quality degradation complexity",
        "active view adjustment boundary complexity",
        "visual observation lifecycle complexity",
        "ocr activation request gating complexity",
        "tracking request gating complexity",
        "duplicated schema risk",
        "future midplatform function governance required",
    ):
        expect(f"governance_debt.topic.{topic}", any(row.get("topic") == topic for row in debt_rows))
    for idx, row in enumerate(debt_rows):
        expect(f"governance_debt.future_owner_phase_{idx}", row.get("future_owner_phase") == "MidPlatform Function Governance / Consolidation")
        expect(f"governance_debt.reuse_or_consolidation_required_{idx}", row.get("reuse_or_consolidation_required") is True)
        expect(f"governance_debt.duplicate_governance_module_allowed_{idx}", row.get("duplicate_governance_module_allowed") is False)

    # Runtime / write checks
    for check_name, expected in (
        ("no_runtime_executed", True),
        ("no_new_runtime_enabled", True),
        ("camera_invoked", False),
        ("map_api_invoked", False),
        ("ocr_provider_invoked", False),
        ("ocrrequest_submitted", False),
        ("tracking_runtime_invoked", False),
        ("optical_flow_runtime_invoked", False),
        ("supervision_invoked", False),
        ("bytetrack_invoked", False),
        ("ocsort_invoked", False),
        ("world_model_written", False),
        ("memory_written", False),
        ("library_written", False),
        ("fact_written", False),
        ("scene_delta_generated", False),
        ("task_state_committed_now", False),
        ("navigation_action_triggered", False),
        ("speech_gate_invoked", False),
        ("vop_invoked", False),
    ):
        expect(f"runtime.summary.{check_name}", summary.get(check_name) is expected)
    expect("runtime.summary.boundary_ok", summary.get("boundary_ok") is True)
    expect("runtime.summary.violations_empty", summary.get("violations") == [])
    for payload_name, payload in (("no_runtime", no_runtime), ("no_write", no_write)):
        for check_name, expected in (
            ("no_runtime_executed", True),
            ("no_new_runtime_enabled", True),
            ("camera_invoked", False),
            ("map_api_invoked", False),
            ("ocr_provider_invoked", False),
            ("ocrrequest_submitted", False),
            ("tracking_runtime_invoked", False),
            ("optical_flow_runtime_invoked", False),
            ("supervision_invoked", False),
            ("bytetrack_invoked", False),
            ("ocsort_invoked", False),
            ("world_model_written", False),
            ("memory_written", False),
            ("library_written", False),
            ("fact_written", False),
            ("scene_delta_generated", False),
            ("task_state_committed_now", False),
            ("navigation_action_triggered", False),
            ("speech_gate_invoked", False),
            ("vop_invoked", False),
        ):
            expect(f"{payload_name}.{check_name}", payload.get(check_name) is expected)
        expect(f"{payload_name}.full_frame_ocr_allowed", payload.get("full_frame_ocr_allowed") is False)
        expect(f"{payload_name}.full_scene_tracking_allowed", payload.get("full_scene_tracking_allowed") is False)
        expect(f"{payload_name}.ocr_activation_request_candidate_only", payload.get("ocr_activation_request_candidate_only") is True)
        expect(f"{payload_name}.tracking_request_candidate_only", payload.get("tracking_request_candidate_only") is True)
        expect(f"{payload_name}.worldmodel_write_allowed", payload.get("worldmodel_write_allowed") is False)
        expect(f"{payload_name}.memory_write_allowed", payload.get("memory_write_allowed") is False)
        expect(f"{payload_name}.library_write_allowed", payload.get("library_write_allowed") is False)
        expect(f"{payload_name}.handoff_candidate_not_fact", payload.get("handoff_candidate_not_fact") is True)
        expect(f"{payload_name}.placeholder_not_runtime", payload.get("placeholder_not_runtime") is True)
        expect(f"{payload_name}.boundary_ok", payload.get("boundary_ok") is True)
        expect(f"{payload_name}.violations_empty", payload.get("violations") == [])

    # Final decision checks
    expect("final.summary_final_decision", summary.get("final_decision") == FINAL_DECISION)
    expect("final.summary_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    expect("final.next_phase_final_decision", next_phase.get("final_decision") == FINAL_DECISION)
    expect("final.next_phase_recommended_next_phase", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    passed_count = sum(1 for item in checks if item["passed"])
    verdict = "GO" if passed_count >= MIN_CHECKS and not any(not item["passed"] for item in checks) else "NO_GO"
    report = {
        "phase": PHASE_ID,
        "verdict": verdict,
        "checks_passed": passed_count,
        "checks_total": len(checks),
        "min_checks_required": MIN_CHECKS,
        "baseline_requirement": BASELINE_REQUIREMENT,
        "final_decision": FINAL_DECISION if verdict == "GO" else "TASK_AWARE_VISUAL_FOCUS_POLICY_REVIEW_REQUIRED",
        "recommended_next_phase": NEXT_PHASE if verdict == "GO" else PHASE_ID,
        "failed_checks": [item for item in checks if not item["passed"]],
        "checks": checks,
    }
    (output_root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verdict": verdict, "checks_passed": passed_count, "checks_total": len(checks)}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
