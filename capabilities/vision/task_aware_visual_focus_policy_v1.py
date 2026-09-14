# -*- coding: utf-8 -*-
"""Task-Aware Visual Focus Policy v1.

Phase-Task-Aware-Visual-Focus-Policy-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Task-Aware-Visual-Focus-Policy-v1-001"
POLICY_ID = "tavfp_v1_001"
POLICY_SCOPE = "task_aware_visual_focus_policy_only"
SOURCE_CHAIN = "task_aware_visual_focus_policy_v1"
FINAL_DECISION = "TASK_AWARE_VISUAL_FOCUS_POLICY_READY_FOR_WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY"
NEXT_PHASE = "Phase-World-Observation-and-Entity-Feature-Policy-v1-001"
MIDPLATFORM_FINAL_DECISION = "MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY_READY_FOR_TASK_AWARE_VISUAL_FOCUS_POLICY"
PLANNING_FINAL_DECISION = "RETURN_TO_VISION_MAINLINE_PLANNING_READY_FOR_MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY"
PREPLAN_READY_FLAG = "preplan_ready_for_formal_phase_decision"
OCR_FINAL_DECISION = "OCR_MAINLINE_FINAL_CLOSURE_RETURN_TO_VISION_MAINLINE"
MRI_FINAL_DECISION = "MINIMAL_RUNTIME_INTEGRATION_CLOSED_RETURN_TO_VISION_MAINLINE"

ROOT_INPUT_SPECS = [
    {
        "intake_id": "midplatform_perception_orchestration",
        "path_arg": "midplatform_perception_orchestration_root",
        "label": "MidPlatform Perception Orchestration Policy v1",
        "required": True,
        "summary_file": "summary.json",
        "extra_artifacts": [
            "perception_work_order_schema.json",
            "worldmodel_memory_library_handoff_boundary.json",
            "perception_feedback_candidate_policy.json",
        ],
    },
    {
        "intake_id": "return_to_vision_planning",
        "path_arg": "return_to_vision_planning_root",
        "label": "Return-To-Vision Mainline Planning v1",
        "required": True,
        "summary_file": "summary.json",
        "extra_artifacts": [
            "vision_mainline_roadmap.json",
            "deferred_worldmodel_memory_library_boundary.json",
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
            "deferred_worldmodel_memory_library_boundary.json",
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
    "midplatform_perception_orchestration_doc": "docs/architecture/midplatform/LUNA_MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY_V1.md",
    "vision_planning_doc": "docs/architecture/vision/LUNA_RETURN_TO_VISION_MAINLINE_PLANNING_V1.md",
    "vision_preplan_doc": "docs/architecture/vision/LUNA_RETURN_TO_VISION_MAINLINE_PREPLAN_V1.md",
    "ocr_final_closure_doc": "docs/architecture/ocr/LUNA_OCR_MAINLINE_FINAL_CLOSURE_V1.md",
    "minimal_runtime_integration_closure_doc": "docs/architecture/midplatform/LUNA_MINIMAL_RUNTIME_INTEGRATION_CLOSURE_V1.md",
    "ocr_phase_verdict_table": "docs/architecture/evaluation/LUNA_EVALUATION_OCR_PHASE_VERDICT_STATUS_TABLE_V0.md",
}

OPTIONAL_DOCS = {
    "task_observation_request_contract": "docs/architecture/evaluation/LUNA_EVALUATION_TASK_OBSERVATION_REQUEST_CONTRACT_V1.md",
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
}

BOUNDARY_FALSE_FLAGS = {
    "no_runtime_executed": True,
    "no_new_runtime_enabled": True,
    "camera_invoked": False,
    "map_api_invoked": False,
    "ocr_provider_invoked": False,
    "ocrrequest_submitted": False,
    "tracking_runtime_invoked": False,
    "optical_flow_runtime_invoked": False,
    "supervision_invoked": False,
    "bytetrack_invoked": False,
    "ocsort_invoked": False,
    "world_model_written": False,
    "memory_written": False,
    "library_written": False,
    "fact_written": False,
    "scene_delta_generated": False,
    "task_state_committed_now": False,
    "navigation_action_triggered": False,
    "speech_gate_invoked": False,
    "vop_invoked": False,
}

SCENE_SKETCH_FIELD_SPECS = [
    {"name": "scene_sketch_id", "type": "string", "required": True},
    {"name": "source_work_order_id", "type": "string", "required": True},
    {"name": "source_frame_ref_placeholder", "type": "string", "required": False},
    {"name": "task_context_ref", "type": "string", "required": True},
    {"name": "location_context_ref", "type": "string", "required": False},
    {"name": "pose_or_view_context_ref", "type": "string", "required": False},
    {"name": "scene_type_candidate", "type": "string", "required": True},
    {"name": "self_position_hint", "type": "string", "required": False},
    {"name": "left_context", "type": "list", "required": True},
    {"name": "right_context", "type": "list", "required": True},
    {"name": "front_context", "type": "list", "required": True},
    {"name": "far_context", "type": "list", "required": True},
    {"name": "near_ground_context", "type": "list", "required": True},
    {"name": "walkable_area_hint", "type": "string", "required": False},
    {"name": "human_density_candidate", "type": "string", "required": False},
    {"name": "vehicle_presence_candidate", "type": "string", "required": False},
    {"name": "signage_or_text_hint", "type": "list", "required": True},
    {"name": "obstacle_hint", "type": "list", "required": True},
    {"name": "traffic_light_or_crossing_hint", "type": "list", "required": True},
    {"name": "temporary_facility_hint", "type": "list", "required": True},
    {"name": "visibility_quality_ref", "type": "string", "required": True},
    {"name": "uncertainty", "type": "number", "required": True},
    {"name": "freshness_status", "type": "string", "required": True},
    {"name": "ttl_policy_ref", "type": "string", "required": True},
    {"name": "privacy_tags", "type": "list", "required": True},
    {"name": "fact_status", "type": "string", "required": True, "default": "not_fact"},
    {"name": "write_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

VISUAL_FOCUS_PLAN_FIELD_SPECS = [
    {"name": "visual_focus_plan_id", "type": "string", "required": True},
    {"name": "source_work_order_id", "type": "string", "required": True},
    {"name": "source_scene_sketch_id", "type": "string", "required": True},
    {"name": "task_id", "type": "string", "required": True},
    {"name": "task_type", "type": "enum", "required": True},
    {"name": "task_phase", "type": "enum", "required": True},
    {"name": "focus_slots", "type": "list", "required": True},
    {"name": "ignored_by_default", "type": "boolean", "required": True},
    {"name": "ocr_activation_slots", "type": "list", "required": True},
    {"name": "tracking_request_slots", "type": "list", "required": True},
    {"name": "map_memory_binding_slots", "type": "list", "required": True},
    {"name": "safety_focus_slots", "type": "list", "required": True},
    {"name": "active_view_adjustment_slots", "type": "list", "required": True},
    {"name": "budget_policy_ref", "type": "string", "required": True},
    {"name": "privacy_policy_ref", "type": "string", "required": True},
    {"name": "freshness_policy_ref", "type": "string", "required": True},
    {"name": "conflict_policy_ref", "type": "string", "required": True},
    {"name": "output_handoff_policy_ref", "type": "string", "required": True},
    {"name": "fact_status", "type": "string", "required": True, "default": "not_fact"},
    {"name": "runtime_action_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

VISUAL_FOCUS_SLOT_FIELD_SPECS = [
    {"name": "slot_id", "type": "string", "required": True},
    {"name": "source_visual_focus_plan_id", "type": "string", "required": True},
    {"name": "slot_type", "type": "enum", "required": True},
    {"name": "target", "type": "string", "required": True},
    {"name": "priority", "type": "enum", "required": True},
    {"name": "task_relevance", "type": "number", "required": True},
    {"name": "safety_relevance", "type": "number", "required": True},
    {"name": "route_relevance", "type": "number", "required": True},
    {"name": "map_memory_relevance", "type": "number", "required": True},
    {"name": "expected_evidence_type", "type": "string", "required": True},
    {"name": "tracking_required", "type": "boolean", "required": True},
    {"name": "ocr_required", "type": "boolean", "required": True},
    {"name": "map_binding_required", "type": "boolean", "required": True},
    {"name": "active_view_adjustment_allowed", "type": "boolean", "required": True},
    {"name": "activation_condition", "type": "string", "required": True},
    {"name": "expiration_condition", "type": "string", "required": True},
    {"name": "max_budget", "type": "string", "required": True},
    {"name": "stc_policy_ref", "type": "string", "required": True},
    {"name": "ttl_policy_ref", "type": "string", "required": True},
    {"name": "freshness_requirement", "type": "string", "required": True},
    {"name": "privacy_filter_required", "type": "boolean", "required": True},
    {"name": "output_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "action_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "fact_status", "type": "string", "required": True, "default": "not_fact"},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

VISUAL_FOCUS_SLOT_TYPES = [
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
]

VIEW_QUALITY_FIELD_SPECS = [
    {"name": "view_quality_id", "type": "string", "required": True},
    {"name": "source_work_order_id", "type": "string", "required": True},
    {"name": "source_frame_ref_placeholder", "type": "string", "required": False},
    {"name": "blur_level_candidate", "type": "string", "required": True},
    {"name": "brightness_quality_candidate", "type": "string", "required": True},
    {"name": "exposure_quality_candidate", "type": "string", "required": True},
    {"name": "occlusion_level_candidate", "type": "string", "required": True},
    {"name": "camera_shake_candidate", "type": "string", "required": True},
    {"name": "target_distance_quality_candidate", "type": "string", "required": True},
    {"name": "dynamic_motion_quality_candidate", "type": "string", "required": True},
    {"name": "crowd_occlusion_candidate", "type": "string", "required": True},
    {"name": "reflection_or_weather_candidate", "type": "string", "required": True},
    {"name": "frame_stability_candidate", "type": "string", "required": True},
    {"name": "readable_region_quality_hint", "type": "string", "required": False},
    {"name": "safe_for_scene_sketch", "type": "boolean", "required": True},
    {"name": "safe_for_ocr_activation", "type": "boolean", "required": True},
    {"name": "safe_for_tracking_request", "type": "boolean", "required": True},
    {"name": "requires_active_view_adjustment", "type": "boolean", "required": True},
    {"name": "recommended_degradation", "type": "string", "required": True},
    {"name": "fact_status", "type": "string", "required": True, "default": "not_fact"},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

VIEW_QUALITY_DEGRADATION_POLICY = {
    "GOOD": {
        "scene_sketch_allowed": True,
        "visual_focus_plan_allowed": True,
        "ocr_activation_allowed": True,
        "tracking_request_allowed": True,
        "active_view_adjustment_required": False,
    },
    "DEGRADED": {
        "scene_sketch_allowed": True,
        "visual_focus_plan_allowed": True,
        "ocr_activation_allowed": "limited",
        "tracking_request_allowed": "limited",
        "active_view_adjustment_required": False,
        "degradation_rule": "只允许 safety + primary task focus",
    },
    "POOR": {
        "scene_sketch_allowed": "partial",
        "visual_focus_plan_allowed": "safety_first_only",
        "ocr_activation_allowed": False,
        "tracking_request_allowed": False,
        "active_view_adjustment_required": True,
        "degradation_rule": "只允许 safety focus / active view adjustment candidate",
    },
    "BLOCKED": {
        "scene_sketch_allowed": False,
        "visual_focus_plan_allowed": False,
        "ocr_activation_allowed": False,
        "tracking_request_allowed": False,
        "active_view_adjustment_required": True,
        "degradation_rule": "暂停任务视觉，只保留 safety candidate",
    },
}

ACTIVE_VIEW_ADJUSTMENT_FIELD_SPECS = [
    {"name": "active_view_adjustment_id", "type": "string", "required": True},
    {"name": "source_focus_slot_id", "type": "string", "required": True},
    {"name": "missing_visual_evidence", "type": "string", "required": True},
    {"name": "suggested_view_adjustment", "type": "string", "required": True},
    {"name": "adjustment_type", "type": "enum", "required": True},
    {"name": "urgency", "type": "enum", "required": True},
    {"name": "safety_constraint", "type": "string", "required": True},
    {"name": "user_message_candidate", "type": "string", "required": False},
    {"name": "speech_gate_required", "type": "boolean", "required": True, "default": True},
    {"name": "output_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "action_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "fact_status", "type": "string", "required": True, "default": "not_fact"},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

ACTIVE_VIEW_ADJUSTMENT_TYPES = [
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
]

VISUAL_OBSERVATION_LIFECYCLE_STATES = [
    {
        "state": "active",
        "current_action_allowed": True,
        "task_feedback_allowed": True,
        "archive_allowed": True,
        "worldmodel_handoff_allowed_candidate": False,
        "memory_handoff_allowed_candidate": False,
        "library_handoff_placeholder_allowed": False,
        "ttl_required": True,
        "source_chain_required": True,
        "privacy_filter_required": True,
    },
    {
        "state": "stale",
        "current_action_allowed": "limited",
        "task_feedback_allowed": True,
        "archive_allowed": True,
        "worldmodel_handoff_allowed_candidate": False,
        "memory_handoff_allowed_candidate": False,
        "library_handoff_placeholder_allowed": False,
        "ttl_required": True,
        "source_chain_required": True,
        "privacy_filter_required": True,
    },
    {
        "state": "expired",
        "current_action_allowed": False,
        "task_feedback_allowed": False,
        "archive_allowed": True,
        "worldmodel_handoff_allowed_candidate": False,
        "memory_handoff_allowed_candidate": False,
        "library_handoff_placeholder_allowed": False,
        "ttl_required": True,
        "source_chain_required": True,
        "privacy_filter_required": True,
    },
    {
        "state": "archived_candidate",
        "current_action_allowed": False,
        "task_feedback_allowed": False,
        "archive_allowed": True,
        "worldmodel_handoff_allowed_candidate": True,
        "memory_handoff_allowed_candidate": True,
        "library_handoff_placeholder_allowed": True,
        "ttl_required": True,
        "source_chain_required": True,
        "privacy_filter_required": True,
    },
    {
        "state": "worldmodel_handoff_candidate",
        "current_action_allowed": False,
        "task_feedback_allowed": False,
        "archive_allowed": True,
        "worldmodel_handoff_allowed_candidate": True,
        "memory_handoff_allowed_candidate": True,
        "library_handoff_placeholder_allowed": True,
        "ttl_required": True,
        "source_chain_required": True,
        "privacy_filter_required": True,
    },
    {
        "state": "rejected",
        "current_action_allowed": False,
        "task_feedback_allowed": False,
        "archive_allowed": True,
        "worldmodel_handoff_allowed_candidate": False,
        "memory_handoff_allowed_candidate": False,
        "library_handoff_placeholder_allowed": False,
        "ttl_required": True,
        "source_chain_required": True,
        "privacy_filter_required": True,
    },
    {
        "state": "promoted_later_placeholder",
        "current_action_allowed": False,
        "task_feedback_allowed": False,
        "archive_allowed": True,
        "worldmodel_handoff_allowed_candidate": True,
        "memory_handoff_allowed_candidate": True,
        "library_handoff_placeholder_allowed": True,
        "ttl_required": True,
        "source_chain_required": True,
        "privacy_filter_required": True,
    },
]

OCR_ALLOWED_FOCUS_TYPES = [
    "readable_region_focus",
    "signage_focus",
    "shopfront_focus",
    "doorway_or_entrance_focus",
    "destination_landmark_focus",
    "traffic_light_focus",
    "temporary_facility_focus",
]

OCR_FORBIDDEN_CASES = [
    "full_frame_ocr",
    "low_quality_view_ocr",
    "non_task_relevant_background_text",
    "privacy_sensitive_text_without_filtering",
    "ocr_provider_runtime_invocation_in_this_phase",
]

TRACKING_ALLOWED_FOCUS_TYPES = [
    "safety_focus",
    "route_path_focus",
    "walkable_surface_focus",
    "dynamic_obstacle_focus",
    "traffic_light_focus",
    "pedestrian_flow_focus",
    "vehicle_flow_focus",
    "destination_landmark_focus",
    "user_feedback_focus",
]

TRACKING_FORBIDDEN_CASES = [
    "full_scene_tracking",
    "all_moving_objects_tracking",
    "all_person_tracking",
    "all_vehicle_tracking",
    "background_tracking_without_task_or_safety_relevance",
    "tracking_runtime_invocation_in_this_phase",
]

VISUAL_FOCUS_FEEDBACK_OUTPUTS = [
    "VisualFocusFeedbackCandidate",
    "SceneSketchFeedbackCandidate",
    "ViewQualityFeedbackCandidate",
    "ActiveViewAdjustmentFeedbackCandidate",
    "OCRActivationRequestCandidate",
    "TrackingRequestCandidate",
    "SafetyFocusFeedbackCandidate",
    "TaskFocusFeedbackCandidate",
]

SCENARIO_ROWS = [
    {
        "scenario_id": "navigation_route_walking",
        "focus_slots": [
            "route_path_focus",
            "walkable_surface_focus",
            "safety_focus",
            "dynamic_obstacle_focus",
        ],
        "view_quality_expectation": "GOOD_or_DEGRADED",
        "ocr_activation_candidate": False,
        "tracking_request_candidate": True,
        "safety_arbitration_required": True,
    },
    {
        "scenario_id": "navigation_approaching_crossing",
        "focus_slots": [
            "crossing_focus",
            "traffic_light_focus",
            "vehicle_flow_focus",
            "pedestrian_flow_focus",
        ],
        "view_quality_expectation": "GOOD_or_DEGRADED",
        "ocr_activation_candidate": False,
        "tracking_request_candidate": True,
        "active_view_adjustment_if_low_confidence": True,
        "safety_arbitration_required": True,
    },
    {
        "scenario_id": "navigation_approaching_destination",
        "focus_slots": [
            "destination_landmark_focus",
            "signage_focus",
            "doorway_or_entrance_focus",
        ],
        "view_quality_expectation": "GOOD",
        "ocr_activation_candidate": True,
        "tracking_request_candidate": False,
        "safety_arbitration_required": True,
    },
    {
        "scenario_id": "shop_search_right_side_storefront",
        "focus_slots": [
            "shopfront_focus",
            "signage_focus",
            "doorway_or_entrance_focus",
        ],
        "map_memory_binding_slot": True,
        "ocr_activation_candidate": True,
        "tracking_request_candidate": False,
        "safety_arbitration_required": True,
    },
    {
        "scenario_id": "object_search_home_keys",
        "focus_slots": [
            "support_surface_focus",
            "tabletop_focus",
            "shelf_or_counter_focus",
            "floor_near_user_focus",
            "user_feedback_focus",
        ],
        "ocr_activation_candidate": False,
        "tracking_request_candidate": False,
        "privacy_filter_required": True,
    },
    {
        "scenario_id": "home_familiar_object_interaction",
        "focus_slots": [
            "user_feedback_focus",
            "world_observation_focus",
        ],
        "object_identity_candidate_placeholder": True,
        "memory_handoff_candidate_placeholder": True,
        "privacy_filter_required": True,
    },
    {
        "scenario_id": "low_quality_view_hold_still",
        "focus_slots": [
            "safety_focus",
        ],
        "view_quality_candidate": "POOR",
        "active_view_adjustment": "hold_still",
        "task_visual_focus_suppressed": True,
        "safety_focus_retained": True,
    },
    {
        "scenario_id": "crowded_path_occluded_surface",
        "focus_slots": [
            "walkable_surface_focus",
            "pedestrian_flow_focus",
        ],
        "walkable_surface_focus_mode": "degraded",
        "pedestrian_flow_focus_enabled": True,
        "crowd_flow_follow_candidate_not_action": True,
        "safety_arbitration_required": True,
    },
]

GOVERNANCE_DEBT_TOPICS = [
    "visual focus slot schema complexity",
    "view quality degradation complexity",
    "active view adjustment boundary complexity",
    "visual observation lifecycle complexity",
    "ocr activation request gating complexity",
    "tracking request gating complexity",
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
        "full_frame_ocr_allowed": False,
        "full_scene_tracking_allowed": False,
        "ocr_activation_request_candidate_only": True,
        "tracking_request_candidate_only": True,
        "worldmodel_write_allowed": False,
        "memory_write_allowed": False,
        "library_write_allowed": False,
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


def run_task_aware_visual_focus_policy_v1(
    *,
    midplatform_perception_orchestration_root: str,
    return_to_vision_planning_root: str,
    preplan_input_root: str,
    ocr_final_closure_root: str,
    minimal_runtime_integration_closure_root: str,
    workspace_root: str,
) -> Dict[str, Any]:
    repo_root = Path(__file__).resolve().parents[2]
    workspace = Path(workspace_root).expanduser().resolve()

    root_arg_values = {
        "midplatform_perception_orchestration_root": midplatform_perception_orchestration_root,
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

    midplatform_summary = _read_json(root_meta["midplatform_perception_orchestration"]["summary_path"]) if root_meta["midplatform_perception_orchestration"]["summary_path"] else {}
    planning_summary = _read_json(root_meta["return_to_vision_planning"]["summary_path"]) if root_meta["return_to_vision_planning"]["summary_path"] else {}
    preplan_summary = _read_json(root_meta["preplan_input"]["summary_path"]) if root_meta["preplan_input"]["summary_path"] else {}
    ocr_summary = _read_json(root_meta["ocr_final_closure"]["summary_path"]) if root_meta["ocr_final_closure"]["summary_path"] else {}
    mri_summary = _read_json(root_meta["minimal_runtime_integration_closure"]["summary_path"]) if root_meta["minimal_runtime_integration_closure"]["summary_path"] else {}

    midplatform_boundary = _load_optional_json(root_meta["midplatform_perception_orchestration"], "worldmodel_memory_library_handoff_boundary.json")
    planning_boundary = _load_optional_json(root_meta["return_to_vision_planning"], "deferred_worldmodel_memory_library_boundary.json")
    preplan_boundary = _load_optional_json(root_meta["preplan_input"], "deferred_worldmodel_memory_library_boundary.json")

    midplatform_perception_orchestration_input_loaded = (
        root_meta["midplatform_perception_orchestration"]["loaded"]
        and midplatform_summary.get("final_decision") == MIDPLATFORM_FINAL_DECISION
        and midplatform_summary.get("worldmodel_handoff_candidate_allowed") is True
    )
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
    ocr_final_closure_loaded = root_meta["ocr_final_closure"]["loaded"] and ocr_summary.get("final_decision") == OCR_FINAL_DECISION
    minimal_runtime_integration_closure_loaded = (
        root_meta["minimal_runtime_integration_closure"]["loaded"]
        and mri_summary.get("final_decision") == MRI_FINAL_DECISION
    )

    scene_sketch_candidate_schema = {
        "schema_id": f"{POLICY_ID}_scene_sketch",
        "object_name": "SceneSketchCandidate",
        "policy_scope": POLICY_SCOPE,
        "fields": SCENE_SKETCH_FIELD_SPECS,
        "field_count": len(SCENE_SKETCH_FIELD_SPECS),
        "input_contract": ["MidPlatformPerceptionWorkOrder", "ViewQualityCandidate", "Map/Memory context hints"],
        "output_role": "VisualFocusPlan input candidate",
        "non_claims": [
            "SceneSketchCandidate 不是环境事实。",
            "SceneSketchCandidate 不直接播报。",
            "SceneSketchCandidate 不直接写 WorldModel。",
            "SceneSketchCandidate 不直接触发导航动作。",
        ],
        "fact_status": "not_fact",
        "write_allowed": False,
        "source_chain": SOURCE_CHAIN,
    }

    visual_focus_plan_schema = {
        "schema_id": f"{POLICY_ID}_visual_focus_plan",
        "object_name": "VisualFocusPlan",
        "policy_scope": POLICY_SCOPE,
        "fields": VISUAL_FOCUS_PLAN_FIELD_SPECS,
        "field_count": len(VISUAL_FOCUS_PLAN_FIELD_SPECS),
        "non_claims": [
            "VisualFocusPlan 不等于真实画面切割。",
            "VisualFocusPlan 不等于模型已执行。",
            "VisualFocusPlan 不等于 tracking 已执行。",
            "VisualFocusPlan 只是后续 visual candidate / OCR activation / tracking candidate 的规划合同。",
        ],
        "runtime_action_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    visual_focus_slot_schema = {
        "schema_id": f"{POLICY_ID}_visual_focus_slot",
        "object_name": "VisualFocusSlot",
        "policy_scope": POLICY_SCOPE,
        "fields": VISUAL_FOCUS_SLOT_FIELD_SPECS,
        "field_count": len(VISUAL_FOCUS_SLOT_FIELD_SPECS),
        "slot_types": VISUAL_FOCUS_SLOT_TYPES,
        "safety_focus_slots_defined": True,
        "task_focus_slots_defined": True,
        "non_claims": [
            "VisualFocusSlot 不等于真实视觉执行。",
            "VisualFocusSlot 不等于直接用户指令。",
            "VisualFocusSlot 不得直接输出 action。",
        ],
        "action_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    view_quality_candidate_schema = {
        "schema_id": f"{POLICY_ID}_view_quality",
        "object_name": "ViewQualityCandidate",
        "policy_scope": POLICY_SCOPE,
        "fields": VIEW_QUALITY_FIELD_SPECS,
        "field_count": len(VIEW_QUALITY_FIELD_SPECS),
        "degradation_policy": VIEW_QUALITY_DEGRADATION_POLICY,
        "view_quality_degradation_policy_defined": True,
        "non_claims": [
            "ViewQualityCandidate 不是环境事实。",
            "ViewQualityCandidate 只是视角质量候选。",
            "ViewQualityCandidate 只能驱动焦点降级与主动视角调整候选。",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    active_view_adjustment_candidate_schema = {
        "schema_id": f"{POLICY_ID}_active_view_adjustment",
        "object_name": "ActiveViewAdjustmentCandidate",
        "policy_scope": POLICY_SCOPE,
        "fields": ACTIVE_VIEW_ADJUSTMENT_FIELD_SPECS,
        "field_count": len(ACTIVE_VIEW_ADJUSTMENT_FIELD_SPECS),
        "adjustment_types": ACTIVE_VIEW_ADJUSTMENT_TYPES,
        "active_view_adjustment_policy_defined": True,
        "non_claims": [
            "ActiveViewAdjustmentCandidate 只是用户引导候选。",
            "ActiveViewAdjustmentCandidate 不直接控制用户行动。",
            "ActiveViewAdjustmentCandidate 不直接播报，必须经过 Speech Gate / Output boundary。",
        ],
        "speech_gate_required": True,
        "action_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    visual_observation_lifecycle_policy = {
        "policy_id": f"{POLICY_ID}_observation_lifecycle",
        "states": VISUAL_OBSERVATION_LIFECYCLE_STATES,
        "state_count": len(VISUAL_OBSERVATION_LIFECYCLE_STATES),
        "principles": [
            "过期视觉信息可归档为历史候选，但不得作为当前行动依据。",
            "WorldModel / Memory / Library 只允许 handoff candidate / placeholder，不写入。",
            "source_chain、TTL、privacy filter 在所有状态都必须保留。",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    focus_to_ocr_activation_policy = {
        "policy_id": f"{POLICY_ID}_focus_to_ocr",
        "allowed_focus_slot_types": OCR_ALLOWED_FOCUS_TYPES,
        "forbidden_cases": OCR_FORBIDDEN_CASES,
        "ocr_activation_request_candidate_only": True,
        "ocrrequest_submitted": False,
        "ocr_provider_runtime_invocation_allowed": False,
        "note": "本阶段只定义 OCR activation request candidate，不提交 OCRRequest，不调用 provider。",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    focus_to_tracking_request_policy = {
        "policy_id": f"{POLICY_ID}_focus_to_tracking",
        "allowed_focus_slot_types": TRACKING_ALLOWED_FOCUS_TYPES,
        "forbidden_cases": TRACKING_FORBIDDEN_CASES,
        "tracking_request_candidate_only": True,
        "tracking_runtime_invocation_allowed": False,
        "note": "本阶段只定义 tracking request candidate，不调用 tracking runtime。",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    visual_focus_feedback_policy = {
        "policy_id": f"{POLICY_ID}_feedback",
        "output_candidates": VISUAL_FOCUS_FEEDBACK_OUTPUTS,
        "feedback_common_fields": [
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
        ],
        "feedback_candidate_not_spoken": True,
        "speech_allowed_false_until_gate": True,
        "action_allowed_false": True,
        "fact_status_not_fact": True,
        "requires_arbitration": True,
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

    deferred_worldmodel_memory_library_boundary = {
        "boundary_id": f"{POLICY_ID}_deferred_wml",
        "entity_resolution_deferred": True,
        "fact_admission_deferred": True,
        "memory_consolidation_deferred": True,
        "library_experience_governance_deferred": True,
        "worldmodel_write_allowed": False,
        "memory_write_allowed": False,
        "library_write_allowed": False,
        "handoff_candidate_not_fact": True,
        "placeholder_not_runtime": True,
        "worldmodel_handoff_candidate_allowed": True,
        "memory_handoff_candidate_allowed": True,
        "library_handoff_placeholder_allowed": True,
        "midplatform_boundary_loaded": bool(midplatform_boundary.get("boundary_id")),
        "planning_boundary_loaded": bool(planning_boundary.get("boundary_scope")),
        "preplan_boundary_loaded": bool(preplan_boundary.get("boundary_scope")),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    task_aware_visual_focus_scenario_matrix = {
        "matrix_id": f"{POLICY_ID}_scenario_matrix",
        "scenarios": [
            {
                **row,
                "requires_runtime_now": False,
                "fact_write_allowed": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for row in SCENARIO_ROWS
        ],
        "scenario_count": len(SCENARIO_ROWS),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    visual_focus_boundary_matrix = {
        "matrix_id": f"{POLICY_ID}_boundary_matrix",
        "camera_runtime_allowed": False,
        "ocr_provider_runtime_allowed": False,
        "ocrrequest_submitted": False,
        "tracking_runtime_allowed": False,
        "optical_flow_runtime_allowed": False,
        "supervision_runtime_allowed": False,
        "bytetrack_runtime_allowed": False,
        "ocsort_runtime_allowed": False,
        "map_api_allowed": False,
        "speech_gate_allowed": False,
        "vop_allowed": False,
        "full_frame_ocr_allowed": False,
        "full_scene_tracking_allowed": False,
        "worldmodel_write_allowed": False,
        "memory_write_allowed": False,
        "library_write_allowed": False,
        "fact_write_allowed": False,
        "scene_delta_allowed": False,
        "task_state_commit_allowed": False,
        "navigation_action_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_register = {
        "register_id": f"{POLICY_ID}_governance_debt",
        "debts": [
            {
                "debt_id": f"debt_{idx:02d}",
                "topic": topic,
                "deferred_reason": "先完成视觉焦点主链，再统一做 MidPlatform Function Governance / Consolidation。",
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
        "reason": "视觉焦点 policy 已定义完成，下一阶段应进入 World Observation / Entity Feature policy 以定义 handoff layer。",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    boundary = _boundary_payload()
    summary = {
        "phase": PHASE_ID,
        "policy_scope": POLICY_SCOPE,
        "midplatform_perception_orchestration_input_loaded": midplatform_perception_orchestration_input_loaded,
        "return_to_vision_planning_input_loaded": return_to_vision_planning_input_loaded,
        "preplan_input_loaded": preplan_input_loaded,
        "ocr_final_closure_loaded": ocr_final_closure_loaded,
        "minimal_runtime_integration_closure_loaded": minimal_runtime_integration_closure_loaded,
        "scene_sketch_candidate_schema_defined": True,
        "visual_focus_plan_schema_defined": True,
        "visual_focus_slot_schema_defined": True,
        "view_quality_candidate_schema_defined": True,
        "active_view_adjustment_candidate_schema_defined": True,
        "visual_observation_lifecycle_policy_defined": True,
        "focus_to_ocr_activation_policy_defined": True,
        "focus_to_tracking_request_policy_defined": True,
        "visual_focus_feedback_policy_defined": True,
        "scenario_matrix_generated": True,
        "scenario_count": len(SCENARIO_ROWS),
        "safety_focus_slots_defined": True,
        "task_focus_slots_defined": True,
        "view_quality_degradation_policy_defined": True,
        "active_view_adjustment_policy_defined": True,
        "ocr_activation_request_candidate_only": True,
        "tracking_request_candidate_only": True,
        "full_frame_ocr_allowed": False,
        "full_scene_tracking_allowed": False,
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
        "governance_debt_register_generated": True,
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
        "scene_sketch_candidate_schema": scene_sketch_candidate_schema,
        "visual_focus_plan_schema": visual_focus_plan_schema,
        "visual_focus_slot_schema": visual_focus_slot_schema,
        "view_quality_candidate_schema": view_quality_candidate_schema,
        "active_view_adjustment_candidate_schema": active_view_adjustment_candidate_schema,
        "visual_observation_lifecycle_policy": visual_observation_lifecycle_policy,
        "focus_to_ocr_activation_policy": focus_to_ocr_activation_policy,
        "focus_to_tracking_request_policy": focus_to_tracking_request_policy,
        "visual_focus_feedback_policy": visual_focus_feedback_policy,
        "deferred_worldmodel_memory_library_boundary": deferred_worldmodel_memory_library_boundary,
        "task_aware_visual_focus_scenario_matrix": task_aware_visual_focus_scenario_matrix,
        "visual_focus_boundary_matrix": visual_focus_boundary_matrix,
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_runtime_boundary_report": boundary,
        "no_write_boundary_report": boundary,
        "debug_refs": {
            "workspace_root": str(workspace),
            "midplatform_final_decision": midplatform_summary.get("final_decision"),
            "planning_final_decision": planning_summary.get("final_decision"),
            "preplan_ready_flag": preplan_summary.get(PREPLAN_READY_FLAG),
            "ocr_final_decision": ocr_summary.get("final_decision"),
            "minimal_runtime_final_decision": mri_summary.get("final_decision"),
            "scenario_count": len(SCENARIO_ROWS),
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
