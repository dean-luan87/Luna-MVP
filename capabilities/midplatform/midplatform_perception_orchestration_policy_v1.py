# -*- coding: utf-8 -*-
"""MidPlatform Perception Orchestration Policy v1.

Phase-MidPlatform-Perception-Orchestration-Policy-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-MidPlatform-Perception-Orchestration-Policy-v1-001"
POLICY_ID = "mp_pop_v1_001"
POLICY_SCOPE = "midplatform_perception_orchestration_policy_only"
SOURCE_CHAIN = "midplatform_perception_orchestration_policy_v1"
FINAL_DECISION = "MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY_READY_FOR_TASK_AWARE_VISUAL_FOCUS_POLICY"
NEXT_PHASE = "Phase-Task-Aware-Visual-Focus-Policy-v1-001"
PLANNING_FINAL_DECISION = "RETURN_TO_VISION_MAINLINE_PLANNING_READY_FOR_MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY"
PREPLAN_READY_FLAG = "preplan_ready_for_formal_phase_decision"
OCR_FINAL_DECISION = "OCR_MAINLINE_FINAL_CLOSURE_RETURN_TO_VISION_MAINLINE"
MRI_FINAL_DECISION = "MINIMAL_RUNTIME_INTEGRATION_CLOSED_RETURN_TO_VISION_MAINLINE"

ROOT_INPUT_SPECS = [
    {
        "intake_id": "return_to_vision_planning",
        "path_arg": "return_to_vision_planning_root",
        "label": "Return-To-Vision Mainline Planning v1",
        "required": True,
        "summary_file": "summary.json",
        "extra_artifacts": [
            "vision_mainline_planning_report.json",
            "governance_boundary_matrix.json",
            "deferred_worldmodel_memory_library_boundary.json",
            "worldmodel_memory_library_placeholder_plan.json",
        ],
    },
    {
        "intake_id": "preplan_input",
        "path_arg": "preplan_input_root",
        "label": "Return-To-Vision Mainline Preplan v1",
        "required": True,
        "summary_file": "summary.json",
        "extra_artifacts": [
            "proposed_vision_mainline_architecture.json",
            "preplan_readiness_gate.json",
            "deferred_worldmodel_memory_library_boundary.json",
            "worldmodel_memory_library_placeholder_plan.json",
        ],
    },
    {
        "intake_id": "ocr_final_closure",
        "path_arg": "ocr_final_closure_root",
        "label": "OCR Mainline Final Closure v1",
        "required": True,
        "summary_file": "summary.json",
        "extra_artifacts": [
            "ocr_mainline_final_closure_report.json",
            "ocr_to_vision_handoff_plan.json",
        ],
    },
    {
        "intake_id": "minimal_runtime_integration_closure",
        "path_arg": "minimal_runtime_integration_closure_root",
        "label": "Minimal Runtime Integration Closure v1",
        "required": True,
        "summary_file": "summary.json",
        "extra_artifacts": [
            "minimal_runtime_integration_closure_report.json",
            "vision_mainline_handoff_plan.json",
        ],
    },
]

REQUIRED_DOCS = {
    "vision_planning_doc": "docs/architecture/vision/LUNA_RETURN_TO_VISION_MAINLINE_PLANNING_V1.md",
    "vision_preplan_doc": "docs/architecture/vision/LUNA_RETURN_TO_VISION_MAINLINE_PREPLAN_V1.md",
    "ocr_final_closure_doc": "docs/architecture/ocr/LUNA_OCR_MAINLINE_FINAL_CLOSURE_V1.md",
    "minimal_runtime_integration_closure_doc": "docs/architecture/midplatform/LUNA_MINIMAL_RUNTIME_INTEGRATION_CLOSURE_V1.md",
    "ocr_phase_verdict_table": "docs/architecture/evaluation/LUNA_EVALUATION_OCR_PHASE_VERDICT_STATUS_TABLE_V0.md",
}

OPTIONAL_DOCS = {
    "task_observation_request_contract": "docs/architecture/evaluation/LUNA_EVALUATION_TASK_OBSERVATION_REQUEST_CONTRACT_V1.md",
    "task_manager_contract": "docs/architecture/evaluation/LUNA_EVALUATION_TASK_MANAGER_CONTRACT_V1.md",
    "midplatform_task_state_runtime_dryrun": "docs/architecture/evaluation/LUNA_EVALUATION_MIDPLATFORM_TASK_STATE_RUNTIME_DRYRUN_V1.md",
    "safety_task_arbitration_policy": "docs/architecture/midplatform/LUNA_SAFETY_TASK_ARBITRATION_POLICY_V1.md",
    "stc_sampling_guidance_policy": "docs/architecture/midplatform/LUNA_STC_SAMPLING_GUIDANCE_POLICY_V1.md",
    "ocr_activation_governance_policy": "docs/architecture/midplatform/LUNA_OCR_ACTIVATION_GOVERNANCE_POLICY_V1.md",
    "static_readable_region_discovery": "docs/architecture/midplatform/LUNA_STATIC_READABLE_REGION_DISCOVERY_GUIDANCE_POLICY_V1.md",
    "vision_frame_trace_stream_registry": "docs/architecture/vision/LUNA_VISION_FRAME_TRACE_STREAM_REGISTRY_V0.md",
    "vision_frame_input_governance": "docs/architecture/vision/LUNA_VISION_FRAME_INPUT_GOVERNANCE_V0.md",
    "vision_roi_proposal_stub": "docs/architecture/vision/LUNA_VISION_FRAME_ROI_PROPOSAL_AND_SEGMENTATION_STUB_V0.md",
    "vision_recognition_evidence_pack": "docs/architecture/vision/LUNA_VISION_RECOGNITION_EVIDENCE_PACK_V0.md",
    "worldmodel_unresolved_observation_slot_contract": "docs/architecture/evaluation/LUNA_EVALUATION_WORLDMODEL_UNRESOLVED_OBSERVATION_SLOT_CONTRACT_V0.md",
    "worldmodel_lookup_for_reading_framework": "docs/architecture/midplatform/LUNA_WORLDMODEL_LOOKUP_FOR_READING_FRAMEWORK_V1.md",
    "confirmed_text_evidence_memory_governance_contract": "docs/architecture/midplatform/LUNA_CONFIRMED_TEXT_EVIDENCE_MEMORY_GOVERNANCE_CONTRACT_V1.md",
    "map_anchor": "docs/architecture/LUNA_MAP_ANCHOR_EVIDENCE_SCHEMA_V0.md",
    "system_health_center_governance": "docs/architecture/system_health/LUNA_SYSTEM_HEALTH_CENTER_GOVERNANCE_V0.md",
    "hardware_profile_capability_registry": "docs/architecture/midplatform/LUNA_HARDWARE_PROFILE_CAPABILITY_REGISTRY_V1.md",
    "speech_gate_or_vop_reference": "docs/architecture/midplatform/LUNA_MINIMAL_RUNTIME_INTEGRATION_CONTROLLED_OUTPUT_DEFINITION_V1.md",
}

BOUNDARY_FALSE_FLAGS = {
    "no_runtime_executed": True,
    "no_new_runtime_enabled": True,
    "camera_invoked": False,
    "map_api_invoked": False,
    "ocr_provider_invoked": False,
    "tracking_runtime_invoked": False,
    "optical_flow_runtime_invoked": False,
    "world_model_written": False,
    "memory_written": False,
    "library_written": False,
    "fact_written": False,
    "scene_delta_generated": False,
    "task_state_committed_now": False,
    "navigation_action_triggered": False,
}

COMMON_FORBIDDEN_RUNTIME_ACTIONS = [
    "camera_runtime",
    "ocr_provider_runtime",
    "full_frame_ocr",
    "full_scene_tracking",
    "tracking_runtime",
    "optical_flow_runtime",
    "map_api_runtime",
    "worldmodel_write",
    "memory_write",
    "library_write",
    "fact_write",
    "task_state_commit",
    "scene_delta_generation",
    "navigation_action",
]

WORK_ORDER_FIELD_SPECS = [
    {"name": "work_order_id", "type": "string", "required": True},
    {"name": "related_task_id", "type": "string", "required": True},
    {"name": "task_type", "type": "enum", "required": True},
    {"name": "task_phase", "type": "enum", "required": True},
    {"name": "priority", "type": "enum", "required": True},
    {"name": "perception_time_window", "type": "object", "required": True},
    {"name": "safety_lane_required", "type": "boolean", "required": True},
    {"name": "task_lane_required", "type": "boolean", "required": True},
    {"name": "scene_context_ref", "type": "string", "required": False},
    {"name": "map_context_ref", "type": "string", "required": False},
    {"name": "route_context_ref", "type": "string", "required": False},
    {"name": "location_context_ref", "type": "string", "required": False},
    {"name": "memory_context_ref", "type": "string", "required": False},
    {"name": "system_health_ref", "type": "string", "required": False},
    {"name": "hardware_state_ref", "type": "string", "required": False},
    {"name": "focus_request_targets", "type": "list", "required": True},
    {"name": "ocr_activation_request", "type": "object", "required": True},
    {"name": "tracking_request", "type": "object", "required": True},
    {"name": "map_memory_hint_request", "type": "object", "required": True},
    {"name": "world_observation_handoff_allowed", "type": "boolean", "required": True},
    {"name": "privacy_filtering_required", "type": "boolean", "required": True},
    {"name": "resource_budget_ref", "type": "string", "required": True},
    {"name": "freshness_policy_ref", "type": "string", "required": True},
    {"name": "stc_policy_ref", "type": "string", "required": True},
    {"name": "conflict_policy_ref", "type": "string", "required": True},
    {"name": "output_handoff_policy_ref", "type": "string", "required": True},
    {"name": "runtime_action_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "task_commit_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "fact_write_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "worldmodel_write_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "memory_write_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "library_write_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

SAFETY_TARGETS = [
    "near_field_obstacle",
    "moving_vehicle",
    "pedestrian_approach",
    "bike_or_e_scooter",
    "traffic_light",
    "crosswalk",
    "curb_or_step",
    "pothole_or_ground_risk",
    "walkable_path_interruption",
    "sudden_dynamic_risk",
]

TASK_LANE_CATEGORIES = [
    "navigation",
    "shop_search",
    "object_search",
    "reading_task",
    "queue_or_crowd_observation",
    "target_confirmation",
    "user_visual_feedback_response",
]

PRIVACY_TAGS = [
    "human_identity_sensitive",
    "face_visible",
    "license_plate_visible",
    "private_space_candidate",
    "medical_context_candidate",
    "school_or_child_context_candidate",
    "home_context_candidate",
    "workplace_context_candidate",
    "commercial_sensitive_candidate",
    "personal_item_candidate",
    "bystander_presence_candidate",
]

CONFLICT_SOURCES = [
    "visual_vs_ocr",
    "visual_vs_map",
    "visual_vs_memory",
    "visual_vs_user_feedback",
    "ocr_vs_actual_function",
    "signboard_vs_business_function",
    "map_poi_vs_current_scene",
    "historical_observation_vs_current_observation",
    "temporary_facility_vs_static_poi",
    "fresh_vs_stale_conflict",
]

FEEDBACK_OUTPUTS = [
    "SafetyFeedbackCandidate",
    "TaskFeedbackCandidate",
    "ViewAdjustmentFeedbackCandidate",
    "OCRActivationFeedbackCandidate",
    "MapMemoryConflictFeedbackCandidate",
    "UserVisualFeedbackCandidate",
]

GOVERNANCE_DEBT_TOPICS = [
    "resource budget complexity",
    "privacy filtering complexity",
    "conflict correction complexity",
    "temporary facility governance complexity",
    "world observation handoff complexity",
    "duplicated schema risk",
    "future midplatform function governance required",
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_root(path_str: Optional[str], summary_file: str) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    loaded = bool(root and root.is_dir())
    summary_path = root / summary_file if loaded else None
    summary_loaded = bool(summary_path and summary_path.is_file())
    return {
        "root": root,
        "loaded": loaded and summary_loaded,
        "summary_path": summary_path if summary_loaded else None,
    }


def _doc_row(repo_root: Path, intake_id: str, rel_path: str, required: bool) -> Dict[str, Any]:
    abs_path = repo_root / rel_path
    loaded = abs_path.is_file()
    return {
        "intake_id": intake_id,
        "label": intake_id,
        "path": rel_path,
        "loaded": loaded,
        "required": required,
        "status": "loaded" if loaded else ("missing_required" if required else "optional_missing"),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _boundary_payload() -> Dict[str, Any]:
    return {
        "phase": PHASE_ID,
        "policy_scope": POLICY_SCOPE,
        **BOUNDARY_FALSE_FLAGS,
        "full_scene_tracking_allowed": False,
        "full_frame_ocr_allowed": False,
        "map_memory_context_hint_only": True,
        "worldmodel_write_allowed": False,
        "memory_write_allowed": False,
        "library_write_allowed": False,
        "fact_write_allowed": False,
        "entity_resolution_deferred": True,
        "fact_admission_deferred": True,
        "memory_consolidation_deferred": True,
        "library_experience_governance_deferred": True,
        "handoff_candidate_not_fact": True,
        "placeholder_not_runtime": True,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _load_optional_json(root_meta: Dict[str, Any], filename: str) -> Dict[str, Any]:
    root = root_meta.get("root")
    path = root / filename if root else None
    if path and path.is_file():
        return _read_json(path)
    return {}


def _phase_row(
    task_type: str,
    task_phase: str,
    required_focus_targets: List[str],
    optional_focus_targets: List[str],
    safety_lane_policy: str,
    task_lane_policy: str,
    ocr_activation_policy: str,
    tracking_policy: str,
    map_memory_hint_policy: str,
    output_policy: str,
) -> Dict[str, Any]:
    return {
        "task_type": task_type,
        "task_phase": task_phase,
        "required_focus_targets": required_focus_targets,
        "optional_focus_targets": optional_focus_targets,
        "safety_lane_policy": safety_lane_policy,
        "task_lane_policy": task_lane_policy,
        "ocr_activation_policy": ocr_activation_policy,
        "tracking_policy": tracking_policy,
        "map_memory_hint_policy": map_memory_hint_policy,
        "output_policy": output_policy,
        "handoff_boundary": "handoff_only_no_fact_write_no_runtime",
        "forbidden_runtime_actions": COMMON_FORBIDDEN_RUNTIME_ACTIONS,
        "runtime_action_allowed": False,
        "task_commit_allowed": False,
        "fact_write_allowed": False,
        "worldmodel_write_allowed": False,
        "memory_write_allowed": False,
        "library_write_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


TASK_PHASE_POLICY_ROWS = [
    _phase_row(
        "navigation",
        "ROUTE_START",
        ["route_direction_hint", "initial_walkable_path", "first_landmark_candidate"],
        ["signage_or_text_hint", "entry_side_hint"],
        "always_on_near_field_safety_scan",
        "route_start_context_bootstrap",
        "disabled_unless_text_target_explicit",
        "disabled_unless_dynamic_target_relevant",
        "route_stage_and_landmark_hint_only",
        "candidate_only_feedback",
    ),
    _phase_row(
        "navigation",
        "ROUTE_WALKING",
        ["forward_walkable_path", "near_field_obstacle", "landmark_progress_candidate"],
        ["storefront_or_intersection_hint", "crosswalk_pre_signal_hint"],
        "always_on_dynamic_path_safety",
        "route_progress_visual_followup",
        "focus_triggered_landmark_or_sign_only",
        "selective_for_moving_hazard_or_user_target",
        "route_progress_hint_only",
        "candidate_only_feedback",
    ),
    _phase_row(
        "navigation",
        "APPROACHING_CROSSING",
        ["crosswalk_candidate", "traffic_light_candidate", "vehicle_flow_candidate"],
        ["pedestrian_density_candidate", "curb_alignment_hint"],
        "crossing_precheck_safety_priority",
        "crossing_context_support_only",
        "disabled_by_default",
        "selective_for_crossing_relevant_motion",
        "crossing_location_hint_only",
        "safety_first_candidate_feedback",
    ),
    _phase_row(
        "navigation",
        "CROSSING_DECISION",
        ["traffic_light_candidate", "moving_vehicle", "pedestrian_approach"],
        ["crosswalk_state_hint", "freshness_conflict_candidate"],
        "crossing_safety_override",
        "task_lane_degraded_support_only",
        "disabled",
        "selective_for_vehicle_and_flow_only",
        "crossing_history_hint_only",
        "safety_first_candidate_feedback",
    ),
    _phase_row(
        "navigation",
        "APPROACHING_TARGET",
        ["target_landmark_candidate", "entrance_side_candidate", "poi_alignment_candidate"],
        ["signage_or_text_hint", "shopfront_layout_hint"],
        "approach_safety_scan",
        "target_approach_disambiguation",
        "focus_triggered_target_signage_only",
        "disabled_unless_relevant_dynamic_target",
        "target_proximity_hint_only",
        "candidate_only_feedback",
    ),
    _phase_row(
        "navigation",
        "TARGET_SEARCH",
        ["shopfront_candidate", "signage_candidate", "entrance_candidate"],
        ["queue_or_crowd_hint", "delivery_window_hint"],
        "target_search_safety_scan",
        "task_search_focus_policy",
        "focus_triggered_text_region_only",
        "disabled_by_default",
        "poi_search_hint_only",
        "candidate_only_feedback",
    ),
    _phase_row(
        "navigation",
        "TARGET_CONFIRMATION",
        ["target_signage_candidate", "entrance_candidate", "business_function_candidate"],
        ["map_poi_conflict_candidate", "user_feedback_correction_hint"],
        "target_confirmation_safety_scan",
        "high_confidence_confirmation_focus",
        "allowed_for_explicit_confirmation_slot",
        "disabled_by_default",
        "confirmation_hint_only",
        "candidate_only_feedback",
    ),
    _phase_row(
        "navigation",
        "ARRIVED_CANDIDATE",
        ["arrival_visual_evidence", "entrance_confirmation_candidate"],
        ["map_alignment_hint", "user_confirmation_hint"],
        "arrival_safety_hold_scan",
        "arrival_candidate_confirmation_only",
        "allowed_for_single_confirmation_slot",
        "disabled",
        "arrival_hint_only",
        "candidate_only_feedback",
    ),
    _phase_row(
        "navigation",
        "SAFETY_HOLD",
        ["near_field_obstacle", "moving_vehicle", "walkable_path_interruption"],
        ["user_refocus_request", "route_recovery_hint"],
        "hard_safety_priority",
        "task_lane_minimal_or_paused",
        "disabled",
        "selective_for_dynamic_risk_only",
        "recovery_hint_only",
        "safety_first_candidate_feedback",
    ),
    _phase_row(
        "shop_search",
        "SEARCH_AREA_APPROACHING",
        ["shop_cluster_candidate", "street_side_candidate", "landmark_alignment_candidate"],
        ["cross_street_hint", "route_progress_hint"],
        "always_on_near_field_safety_scan",
        "shop_search_bootstrap",
        "disabled_by_default",
        "disabled_by_default",
        "area_hint_only",
        "candidate_only_feedback",
    ),
    _phase_row(
        "shop_search",
        "SHOPFRONT_SCAN",
        ["shopfront_candidate", "signage_region_candidate", "entrance_candidate"],
        ["window_display_candidate", "queue_candidate"],
        "shopfront_scan_safety_scan",
        "shopfront_focus_scan",
        "focus_triggered_signage_only",
        "disabled_by_default",
        "shopfront_history_hint_only",
        "candidate_only_feedback",
    ),
    _phase_row(
        "shop_search",
        "SIGNAGE_CONFIRMATION",
        ["signage_candidate", "business_name_candidate"],
        ["text_layout_hint", "brand_color_hint"],
        "signage_confirmation_safety_scan",
        "signage_confirmation_focus",
        "allowed_for_text_confirmation_slot",
        "disabled",
        "shop_name_hint_only",
        "candidate_only_feedback",
    ),
    _phase_row(
        "shop_search",
        "ENTRANCE_CONFIRMATION",
        ["entrance_candidate", "doorway_candidate", "queue_entry_candidate"],
        ["open_or_closed_candidate", "stair_or_ramp_candidate"],
        "entrance_confirmation_safety_scan",
        "entrance_confirmation_focus",
        "disabled_unless_text_target_present",
        "disabled_by_default",
        "entrance_side_hint_only",
        "candidate_only_feedback",
    ),
    _phase_row(
        "shop_search",
        "TARGET_FOUND_CANDIDATE",
        ["shop_match_candidate", "business_function_candidate"],
        ["map_poi_conflict_candidate", "user_feedback_candidate"],
        "target_found_safety_scan",
        "target_found_confirmation_only",
        "allowed_if_text_confirmation_needed",
        "disabled",
        "target_found_hint_only",
        "candidate_only_feedback",
    ),
    _phase_row(
        "object_search",
        "SEARCH_CONTEXT_IDENTIFICATION",
        ["likely_room_or_zone_candidate", "surface_family_candidate"],
        ["historical_search_hint", "private_space_candidate"],
        "context_identification_safety_scan",
        "search_context_bootstrap",
        "disabled_by_default",
        "disabled_by_default",
        "historical_search_hint_only",
        "candidate_only_feedback",
    ),
    _phase_row(
        "object_search",
        "LIKELY_SURFACE_SCAN",
        ["surface_candidate", "container_candidate", "object_cluster_candidate"],
        ["occlusion_candidate", "visibility_quality_candidate"],
        "surface_scan_safety_scan",
        "surface_scan_focus",
        "disabled_unless_text_label_target",
        "disabled_by_default",
        "surface_memory_hint_only",
        "candidate_only_feedback",
    ),
    _phase_row(
        "object_search",
        "OBJECT_CANDIDATE_CONFIRMATION",
        ["object_candidate", "identity_hint_candidate", "supporting_context_candidate"],
        ["ocr_label_hint", "user_correction_hint"],
        "object_confirmation_safety_scan",
        "object_confirmation_focus",
        "focus_triggered_label_confirmation_only",
        "disabled_by_default",
        "object_history_hint_only",
        "candidate_only_feedback",
    ),
    _phase_row(
        "object_search",
        "OBJECT_LOCATION_GUIDANCE",
        ["object_relative_location_candidate", "surface_alignment_candidate"],
        ["user_feedback_adjustment_hint", "approach_safety_hint"],
        "location_guidance_safety_scan",
        "location_guidance_focus",
        "disabled_by_default",
        "disabled",
        "location_hint_only",
        "candidate_only_feedback",
    ),
    _phase_row(
        "reading_task",
        "READING_TARGET_IDENTIFICATION",
        ["readable_region_candidate", "text_surface_candidate"],
        ["lighting_or_glare_candidate", "view_adjustment_hint"],
        "reading_task_safety_scan",
        "reading_target_bootstrap",
        "allowed_for_explicit_text_target",
        "disabled",
        "reading_context_hint_only",
        "candidate_only_feedback",
    ),
    _phase_row(
        "reading_task",
        "READING_SEGMENT_CONFIRMATION",
        ["ocr_focus_slot", "text_region_alignment_candidate"],
        ["multiframe_stability_hint", "user_feedback_hint"],
        "reading_confirmation_safety_scan",
        "reading_segment_confirmation",
        "allowed_for_confirmed_focus_slot_only",
        "disabled",
        "reading_history_hint_only",
        "candidate_only_feedback",
    ),
    _phase_row(
        "queue_or_crowd_observation",
        "QUEUE_ENTRY_CANDIDATE",
        ["queue_shape_candidate", "entry_side_candidate"],
        ["crowd_density_candidate", "temporary_facility_candidate"],
        "queue_observation_safety_scan",
        "queue_entry_estimation",
        "disabled_by_default",
        "selective_for_crowd_flow_only",
        "queue_history_hint_only",
        "candidate_only_feedback",
    ),
    _phase_row(
        "queue_or_crowd_observation",
        "QUEUE_FLOW_MONITORING",
        ["queue_progress_candidate", "crowd_flow_candidate"],
        ["detour_space_candidate", "temporary_barrier_candidate"],
        "crowd_flow_safety_scan",
        "queue_flow_monitoring",
        "disabled",
        "selective_for_crowd_flow_only",
        "crowd_history_hint_only",
        "candidate_only_feedback",
    ),
    _phase_row(
        "target_confirmation",
        "VISUAL_TARGET_CONFIRMATION",
        ["target_visual_match_candidate", "supporting_signage_candidate"],
        ["map_poi_conflict_candidate", "memory_conflict_candidate"],
        "target_confirmation_safety_scan",
        "visual_target_confirmation",
        "allowed_if_text_needed",
        "disabled",
        "target_confirmation_hint_only",
        "candidate_only_feedback",
    ),
    _phase_row(
        "target_confirmation",
        "VISUAL_DISAMBIGUATION",
        ["candidate_a_vs_b_disambiguation", "supporting_context_candidate"],
        ["user_feedback_correction_hint", "business_function_conflict_candidate"],
        "visual_disambiguation_safety_scan",
        "candidate_disambiguation_focus",
        "allowed_if_text_disambiguation_needed",
        "disabled",
        "disambiguation_hint_only",
        "candidate_only_feedback",
    ),
    _phase_row(
        "user_visual_feedback_response",
        "USER_REQUEST_REFOCUS",
        ["user_requested_focus_target", "view_adjustment_candidate"],
        ["ocr_reactivation_candidate", "memory_conflict_candidate"],
        "user_refocus_safety_scan",
        "user_refocus_response",
        "allowed_if_user_request_includes_text_need",
        "disabled_by_default",
        "user_request_hint_only",
        "candidate_only_feedback",
    ),
    _phase_row(
        "user_visual_feedback_response",
        "USER_CORRECTION_RESPONSE",
        ["user_correction_target", "perception_conflict_candidate"],
        ["route_or_location_conflict_hint", "historical_observation_candidate"],
        "user_correction_safety_scan",
        "user_correction_response",
        "allowed_if_text_correction_relevant",
        "disabled_by_default",
        "user_correction_hint_only",
        "candidate_only_feedback",
    ),
]


def run_midplatform_perception_orchestration_policy_v1(
    *,
    return_to_vision_planning_root: str,
    preplan_input_root: str,
    ocr_final_closure_root: str,
    minimal_runtime_integration_closure_root: str,
    workspace_root: str,
) -> Dict[str, Any]:
    repo_root = Path(__file__).resolve().parents[2]
    workspace = Path(workspace_root).expanduser().resolve()

    root_arg_values = {
        "return_to_vision_planning_root": return_to_vision_planning_root,
        "preplan_input_root": preplan_input_root,
        "ocr_final_closure_root": ocr_final_closure_root,
        "minimal_runtime_integration_closure_root": minimal_runtime_integration_closure_root,
    }
    root_meta = {
        spec["intake_id"]: _load_root(root_arg_values[spec["path_arg"]], spec["summary_file"])
        for spec in ROOT_INPUT_SPECS
    }

    input_root_rows: List[Dict[str, Any]] = []
    for spec in ROOT_INPUT_SPECS:
        meta = root_meta[spec["intake_id"]]
        input_root_rows.append(
            {
                "intake_id": spec["intake_id"],
                "label": spec["label"],
                "path": str(meta["root"]) if meta["root"] else "(not_provided)",
                "loaded": meta["loaded"],
                "required": spec["required"],
                "status": "loaded" if meta["loaded"] else ("missing_required" if spec["required"] else "optional_missing"),
                "summary_file": spec["summary_file"],
                "extra_artifacts": spec["extra_artifacts"],
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    for intake_id, rel_path in REQUIRED_DOCS.items():
        input_root_rows.append(_doc_row(repo_root, intake_id, rel_path, True))
    for intake_id, rel_path in OPTIONAL_DOCS.items():
        input_root_rows.append(_doc_row(repo_root, intake_id, rel_path, False))

    planning_summary = _read_json(root_meta["return_to_vision_planning"]["summary_path"]) if root_meta["return_to_vision_planning"]["summary_path"] else {}
    preplan_summary = _read_json(root_meta["preplan_input"]["summary_path"]) if root_meta["preplan_input"]["summary_path"] else {}
    ocr_summary = _read_json(root_meta["ocr_final_closure"]["summary_path"]) if root_meta["ocr_final_closure"]["summary_path"] else {}
    mri_summary = _read_json(root_meta["minimal_runtime_integration_closure"]["summary_path"]) if root_meta["minimal_runtime_integration_closure"]["summary_path"] else {}

    planning_wml_boundary = _load_optional_json(root_meta["return_to_vision_planning"], "deferred_worldmodel_memory_library_boundary.json")
    planning_wml_placeholder = _load_optional_json(root_meta["return_to_vision_planning"], "worldmodel_memory_library_placeholder_plan.json")
    preplan_wml_boundary = _load_optional_json(root_meta["preplan_input"], "deferred_worldmodel_memory_library_boundary.json")
    preplan_wml_placeholder = _load_optional_json(root_meta["preplan_input"], "worldmodel_memory_library_placeholder_plan.json")

    return_to_vision_planning_input_loaded = (
        root_meta["return_to_vision_planning"]["loaded"]
        and planning_summary.get("final_decision") == PLANNING_FINAL_DECISION
        and planning_summary.get("worldmodel_memory_library_boundary_deferred") is True
    )
    preplan_input_loaded = (
        root_meta["preplan_input"]["loaded"]
        and preplan_summary.get(PREPLAN_READY_FLAG) is True
        and preplan_summary.get("worldmodel_memory_library_boundary_deferred") is True
    )
    ocr_final_closure_loaded = (
        root_meta["ocr_final_closure"]["loaded"]
        and ocr_summary.get("final_decision") == OCR_FINAL_DECISION
    )
    minimal_runtime_integration_closure_loaded = (
        root_meta["minimal_runtime_integration_closure"]["loaded"]
        and mri_summary.get("final_decision") == MRI_FINAL_DECISION
    )

    perception_work_order_schema = {
        "schema_id": f"{POLICY_ID}_work_order_schema",
        "object_name": "MidPlatformPerceptionWorkOrder",
        "policy_scope": POLICY_SCOPE,
        "fields": WORK_ORDER_FIELD_SPECS,
        "field_count": len(WORK_ORDER_FIELD_SPECS),
        "non_claims": [
            "PerceptionWorkOrder 是调度候选，不是 runtime 执行。",
            "PerceptionWorkOrder 不能直接触发 camera / OCR / tracking / map API。",
            "PerceptionWorkOrder 只作为后续 visual focus / OCR / tracking / feedback dry-run 的输入合同。",
        ],
        "allowed_downstream_consumers": [
            "Task-Aware Visual Focus Policy",
            "OCR activation policy evaluation",
            "Selective tracking policy evaluation",
            "Map-memory hint evaluation",
            "Perception feedback dry-run planning",
        ],
        "forbidden_direct_triggers": [
            "camera_runtime",
            "ocr_provider_runtime",
            "tracking_runtime",
            "map_api_runtime",
            "navigation_action",
            "task_state_commit",
        ],
        "runtime_action_allowed": False,
        "task_commit_allowed": False,
        "fact_write_allowed": False,
        "worldmodel_write_allowed": False,
        "memory_write_allowed": False,
        "library_write_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    task_phase_perception_policy_matrix = {
        "matrix_id": f"{POLICY_ID}_task_phase_matrix",
        "policy_name": "TaskPhasePerceptionPolicy",
        "rows": TASK_PHASE_POLICY_ROWS,
        "task_types": sorted({row["task_type"] for row in TASK_PHASE_POLICY_ROWS}),
        "phase_count": len(TASK_PHASE_POLICY_ROWS),
        "required_field_contract": [
            "required_focus_targets",
            "optional_focus_targets",
            "safety_lane_policy",
            "task_lane_policy",
            "ocr_activation_policy",
            "tracking_policy",
            "map_memory_hint_policy",
            "output_policy",
            "handoff_boundary",
            "forbidden_runtime_actions",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    safety_lane_orchestration_policy = {
        "policy_id": f"{POLICY_ID}_safety_lane",
        "always_on": True,
        "task_disable_allowed": False,
        "output_candidates": ["SafetyObservationCandidate"],
        "must_enter_safety_task_arbitration": True,
        "can_preempt_task_lane_budget": True,
        "priority_bands": ["P0", "P1"],
        "can_request_view_quality_candidate": True,
        "can_request_active_adjustment_candidate": True,
        "fact_write_allowed": False,
        "runtime_action_allowed": False,
        "coverage_targets": SAFETY_TARGETS,
        "principles": [
            "Safety Lane always-on。",
            "Safety Lane 不受普通 task 禁用。",
            "Safety Lane 只生成 SafetyObservationCandidate。",
            "Safety Lane 不直接行动。",
            "Safety Lane 必须进入 Safety-Task Arbitration。",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    task_lane_orchestration_policy = {
        "policy_id": f"{POLICY_ID}_task_lane",
        "task_dependent": True,
        "approved_focus_targets_only": True,
        "resource_budget_controlled": True,
        "full_scene_tracking_allowed": False,
        "full_frame_ocr_allowed": False,
        "safety_lane_bypass_allowed": False,
        "output_candidates": ["TaskObservationCandidate", "TaskFeedbackCandidate"],
        "must_enter_arbitration_or_speech_prechain": True,
        "runtime_action_allowed": False,
        "fact_write_allowed": False,
        "supported_task_categories": TASK_LANE_CATEGORIES,
        "principles": [
            "Task Lane task-dependent。",
            "Task Lane 只处理中台批准的 focus targets。",
            "Task Lane 受资源预算控制。",
            "Task Lane 不允许绕过 Safety Lane。",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    midplatform_resource_budget_policy = {
        "budget_policy_id": f"{POLICY_ID}_resource_budget",
        "hardware_state_ref_required": True,
        "system_health_ref_required": True,
        "task_priority_ref_required": True,
        "safety_reserved_budget": "always_reserved",
        "primary_task_budget": "task_priority_weighted",
        "secondary_task_budget": "degradable",
        "background_world_observation_budget": "low_frequency_only",
        "ocr_budget": "focus_triggered_only",
        "tracking_budget": "selective_tracking_only",
        "map_memory_query_budget": "hint_query_only",
        "max_active_focus_slots": 4,
        "max_active_tracklets": 3,
        "max_ocr_requests_per_window": 2,
        "max_background_observation_items": 2,
        "degradation_policy": "safety_first_then_primary_task_only",
        "preemption_policy": "safety_lane_may_preempt_task_lane",
        "principles": [
            "P0 Safety budget 永远保留。",
            "主任务优先于附加任务。",
            "附加任务不得挤占安全链。",
            "后台 World Observation 只能低频运行。",
            "OCR / tracking / map query 均需受中台预算控制。",
            "资源不足时降级为 safety-first + primary-task-only。",
        ],
        "resource_budget_owned_by_midplatform": True,
        "vision_module_may_expand_budget": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    midplatform_privacy_filtering_policy = {
        "policy_id": f"{POLICY_ID}_privacy_filtering",
        "privacy_filtering_owned_by_midplatform": True,
        "candidate_stages": [
            "Raw Observation Candidate",
            "Privacy-Filtered Candidate",
            "Restricted Use Candidate",
            "Long-Term Eligible Candidate",
        ],
        "privacy_tags": PRIVACY_TAGS,
        "principles": [
            "采集阶段不直接等于可用。",
            "可用不等于可存。",
            "可存不等于可写 WorldModel。",
            "可写候选不等于事实。",
            "陌生人 / 车牌 / 私人空间默认限制使用。",
            "隐私过滤应由中台统一执行，不由视觉模块自行判断。",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    perception_conflict_correction_policy = {
        "policy_id": f"{POLICY_ID}_conflict_correction",
        "conflict_sources": CONFLICT_SOURCES,
        "output_candidates": [
            "PerceptionConflictCandidate",
            "PerceptionCorrectionCandidate",
            "RealityMismatchCandidate",
            "WorldModelCorrectionHandoffCandidate",
        ],
        "principles": [
            "冲突不等于自动修正。",
            "用户反馈也先是 correction candidate。",
            "多次观察一致后才可进入 WorldModel correction handoff。",
            "对当前导航安全有影响时，可生成 safety/task feedback candidate。",
            "对长期信息有价值时，进入 review / memory / worldmodel governance。",
            "当前阶段不写事实。",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    map_memory_context_hint_policy = {
        "policy_id": f"{POLICY_ID}_map_memory_hint",
        "allowed_uses": [
            "目标接近 hint",
            "路线阶段 hint",
            "方向 / 左右侧 / 入口 / 路口 / POI hint",
            "历史混淆点",
            "过去观察候选",
            "下次观察优先级",
        ],
        "forbidden_uses": [
            "直接触发行动",
            "直接播报为事实",
            "覆盖实时安全视觉",
            "直接写 WorldModel / Memory / Fact",
            "直接触发 OCR / tracking runtime",
            "直接判定到达",
        ],
        "map_memory_context_hint_only": True,
        "realtime_safety_visual_priority": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    worldmodel_memory_library_handoff_boundary = {
        "boundary_id": f"{POLICY_ID}_wml_boundary",
        "allowed_now": [
            "WorldModelHandoffCandidate",
            "MemoryHandoffCandidate",
            "LibraryHandoffPlaceholder",
            "ExperienceCandidatePlaceholder",
        ],
        "forbidden_now": [
            "entity_resolution_runtime",
            "fact_admission",
            "worldmodel_write",
            "memory_write",
            "library_experience_commit",
            "memory_consolidation",
            "object_identity_fact_commit",
            "emotional_attachment_fact_commit",
            "temporary_facility_long_term_promotion",
            "route_experience_commit",
        ],
        "entity_resolution_deferred": True,
        "fact_admission_deferred": True,
        "memory_consolidation_deferred": True,
        "library_experience_governance_deferred": True,
        "worldmodel_write_allowed": False,
        "memory_write_allowed": False,
        "library_write_allowed": False,
        "handoff_candidate_not_fact": True,
        "placeholder_not_runtime": True,
        "planning_boundary_loaded": bool(planning_wml_boundary.get("boundary_scope")),
        "planning_placeholder_loaded": bool(planning_wml_placeholder.get("placeholder_scope")),
        "preplan_boundary_loaded": bool(preplan_wml_boundary.get("boundary_scope")),
        "preplan_placeholder_loaded": bool(preplan_wml_placeholder.get("placeholder_scope")),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    perception_feedback_candidate_policy = {
        "policy_id": f"{POLICY_ID}_feedback_candidates",
        "output_candidates": FEEDBACK_OUTPUTS,
        "feedback_common_fields": [
            "feedback_id",
            "feedback_type",
            "related_task_id",
            "evidence_refs",
            "source_chain",
            "requires_arbitration",
            "speech_allowed",
            "action_allowed",
            "fact_status",
        ],
        "feedback_candidate_requires_arbitration": True,
        "speech_allowed_false_until_gate": True,
        "action_allowed_false": True,
        "fact_status_not_fact": True,
        "principles": [
            "feedback candidate 不直接播报。",
            "speech_allowed=false until Speech Gate。",
            "action_allowed=false。",
            "fact_status=not_fact。",
            "requires_arbitration=true。",
            "source_chain required。",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    orchestration_boundary_matrix = {
        "matrix_id": f"{POLICY_ID}_boundary_matrix",
        "camera_runtime_allowed": False,
        "ocr_provider_runtime_allowed": False,
        "tracking_runtime_allowed": False,
        "optical_flow_runtime_allowed": False,
        "map_api_allowed": False,
        "full_scene_tracking_allowed": False,
        "full_frame_ocr_allowed": False,
        "worldmodel_write_allowed": False,
        "memory_write_allowed": False,
        "library_write_allowed": False,
        "fact_write_allowed": False,
        "entity_resolution_runtime_allowed": False,
        "fact_admission_allowed": False,
        "memory_consolidation_allowed": False,
        "library_experience_commit_allowed": False,
        "scene_delta_allowed": False,
        "task_commit_allowed": False,
        "navigation_action_allowed": False,
        "map_memory_context_hint_only": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_register = {
        "register_id": f"{POLICY_ID}_governance_debt",
        "debts": [
            {
                "debt_id": f"debt_{idx:02d}",
                "topic": topic,
                "deferred_reason": "先完成中台感知编排主链，再统一做 MidPlatform Function Governance / Consolidation。",
                "future_owner_phase": "MidPlatform Function Governance / Consolidation",
                "reuse_or_consolidation_required": True,
                "duplicate_governance_module_allowed": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for idx, topic in enumerate(GOVERNANCE_DEBT_TOPICS, start=1)
        ],
        "future_midplatform_function_governance_required": True,
        "no_duplicate_governance_module_allowed": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommendation_id": f"{POLICY_ID}_next_phase",
        "recommended_next_phase": NEXT_PHASE,
        "final_decision": FINAL_DECISION,
        "reason": "中台感知编排 policy 已定义完成，下一阶段应进入 Task-Aware Visual Focus Policy 以承接 work order 输入合同。",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    boundary = _boundary_payload()
    summary = {
        "phase": PHASE_ID,
        "policy_scope": POLICY_SCOPE,
        "return_to_vision_planning_input_loaded": return_to_vision_planning_input_loaded,
        "preplan_input_loaded": preplan_input_loaded,
        "ocr_final_closure_loaded": ocr_final_closure_loaded,
        "minimal_runtime_integration_closure_loaded": minimal_runtime_integration_closure_loaded,
        "perception_work_order_schema_defined": True,
        "task_phase_perception_policy_defined": True,
        "safety_lane_orchestration_defined": True,
        "task_lane_orchestration_defined": True,
        "midplatform_resource_budget_policy_defined": True,
        "midplatform_privacy_filtering_policy_defined": True,
        "perception_conflict_correction_policy_defined": True,
        "map_memory_context_hint_policy_defined": True,
        "worldmodel_memory_library_handoff_boundary_defined": True,
        "perception_feedback_candidate_policy_defined": True,
        "governance_debt_register_generated": True,
        "resource_budget_owned_by_midplatform": True,
        "privacy_filtering_owned_by_midplatform": True,
        "safety_lane_always_on": True,
        "task_lane_task_dependent": True,
        "full_scene_tracking_allowed": False,
        "full_frame_ocr_allowed": False,
        "map_memory_context_hint_only": True,
        "worldmodel_handoff_candidate_allowed": True,
        "memory_handoff_candidate_allowed": True,
        "library_handoff_placeholder_allowed": True,
        "entity_resolution_deferred": True,
        "fact_admission_deferred": True,
        "memory_consolidation_deferred": True,
        "library_experience_governance_deferred": True,
        "worldmodel_write_allowed": False,
        "memory_write_allowed": False,
        "library_write_allowed": False,
        "handoff_candidate_not_fact": True,
        "placeholder_not_runtime": True,
        **BOUNDARY_FALSE_FLAGS,
        "boundary_ok": True,
        "violations": [],
        "final_decision": FINAL_DECISION,
        "recommended_next_phase": NEXT_PHASE,
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    return {
        "summary": summary,
        "input_root_matrix": {
            "row_count": len(input_root_rows),
            "rows": input_root_rows,
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        "perception_work_order_schema": perception_work_order_schema,
        "task_phase_perception_policy_matrix": task_phase_perception_policy_matrix,
        "safety_lane_orchestration_policy": safety_lane_orchestration_policy,
        "task_lane_orchestration_policy": task_lane_orchestration_policy,
        "midplatform_resource_budget_policy": midplatform_resource_budget_policy,
        "midplatform_privacy_filtering_policy": midplatform_privacy_filtering_policy,
        "perception_conflict_correction_policy": perception_conflict_correction_policy,
        "map_memory_context_hint_policy": map_memory_context_hint_policy,
        "worldmodel_memory_library_handoff_boundary": worldmodel_memory_library_handoff_boundary,
        "perception_feedback_candidate_policy": perception_feedback_candidate_policy,
        "orchestration_boundary_matrix": orchestration_boundary_matrix,
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_runtime_boundary_report": boundary,
        "no_write_boundary_report": boundary,
        "debug_refs": {
            "workspace_root": str(workspace),
            "planning_final_decision": planning_summary.get("final_decision"),
            "preplan_ready_flag": preplan_summary.get(PREPLAN_READY_FLAG),
            "ocr_final_decision": ocr_summary.get("final_decision"),
            "minimal_runtime_final_decision": mri_summary.get("final_decision"),
            "task_phase_count": len(TASK_PHASE_POLICY_ROWS),
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        "final": {
            "final_decision": FINAL_DECISION,
            "phase_verdict": "GO_CANDIDATE_PENDING_VERIFIER",
            "recommended_next_phase": NEXT_PHASE,
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
    }
