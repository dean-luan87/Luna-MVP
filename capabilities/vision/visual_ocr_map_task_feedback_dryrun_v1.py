# -*- coding: utf-8 -*-
"""Visual OCR Map Task Feedback DryRun v1.

Phase-Visual-OCR-Map-Task-Feedback-DryRun-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Visual-OCR-Map-Task-Feedback-DryRun-v1-001"
POLICY_ID = "vomtfd_v1_001"
DRYRUN_SCOPE = "visual_ocr_map_task_feedback_dryrun_only"
SOURCE_CHAIN = "visual_ocr_map_task_feedback_dryrun_v1"
FINAL_DECISION = "VISUAL_OCR_MAP_TASK_FEEDBACK_DRYRUN_READY_FOR_BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING"
NEXT_PHASE = "Phase-Basic-Navigation-Loop-Vision-Strengthening-DryRun-v1-001"
SELECTIVE_TRACKING_FINAL_DECISION = "SELECTIVE_TRACKING_ADAPTER_POLICY_READY_FOR_VISUAL_OCR_MAP_TASK_FEEDBACK_DRYRUN"
WORLDOBS_FINAL_DECISION = "WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY_READY_FOR_SELECTIVE_TRACKING_ADAPTER_POLICY"
VISUAL_FOCUS_FINAL_DECISION = "TASK_AWARE_VISUAL_FOCUS_POLICY_READY_FOR_WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY"
MIDPLATFORM_FINAL_DECISION = "MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY_READY_FOR_TASK_AWARE_VISUAL_FOCUS_POLICY"
PLANNING_FINAL_DECISION = "RETURN_TO_VISION_MAINLINE_PLANNING_READY_FOR_MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY"
PREPLAN_READY_FLAG = "preplan_ready_for_formal_phase_decision"
OCR_FINAL_DECISION = "OCR_MAINLINE_FINAL_CLOSURE_RETURN_TO_VISION_MAINLINE"
MRI_FINAL_DECISION = "MINIMAL_RUNTIME_INTEGRATION_CLOSED_RETURN_TO_VISION_MAINLINE"

ROOT_INPUT_SPECS = [
    {
        "intake_id": "selective_tracking",
        "path_arg": "selective_tracking_root",
        "label": "Selective Tracking Adapter Policy v1",
        "required": True,
        "summary_file": "summary.json",
        "extra_artifacts": [
            "tracking_feedback_policy.json",
            "tracking_request_candidate_schema.json",
            "selective_tracking_boundary_matrix.json",
        ],
    },
    {
        "intake_id": "world_observation_entity_feature",
        "path_arg": "world_observation_entity_feature_root",
        "label": "World Observation and Entity Feature Policy v1",
        "required": True,
        "summary_file": "summary.json",
        "extra_artifacts": [
            "world_observation_feedback_policy.json",
            "worldmodel_memory_library_placeholder_policy.json",
            "world_observation_entity_feature_scenario_matrix.json",
        ],
    },
    {
        "intake_id": "task_aware_visual_focus",
        "path_arg": "task_aware_visual_focus_root",
        "label": "Task-Aware Visual Focus Policy v1",
        "required": True,
        "summary_file": "summary.json",
        "extra_artifacts": [
            "focus_to_ocr_activation_policy.json",
            "focus_to_tracking_request_policy.json",
            "visual_observation_lifecycle_policy.json",
        ],
    },
    {
        "intake_id": "midplatform_perception_orchestration",
        "path_arg": "midplatform_perception_orchestration_root",
        "label": "MidPlatform Perception Orchestration Policy v1",
        "required": True,
        "summary_file": "summary.json",
        "extra_artifacts": [
            "perception_work_order_schema.json",
            "map_memory_context_hint_policy.json",
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
    "selective_tracking_doc": "docs/architecture/vision/LUNA_SELECTIVE_TRACKING_ADAPTER_POLICY_V1.md",
    "world_observation_entity_feature_doc": "docs/architecture/vision/LUNA_WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY_V1.md",
    "task_aware_visual_focus_doc": "docs/architecture/vision/LUNA_TASK_AWARE_VISUAL_FOCUS_POLICY_V1.md",
    "midplatform_perception_orchestration_doc": "docs/architecture/midplatform/LUNA_MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY_V1.md",
    "vision_planning_doc": "docs/architecture/vision/LUNA_RETURN_TO_VISION_MAINLINE_PLANNING_V1.md",
    "vision_preplan_doc": "docs/architecture/vision/LUNA_RETURN_TO_VISION_MAINLINE_PREPLAN_V1.md",
    "ocr_final_closure_doc": "docs/architecture/ocr/LUNA_OCR_MAINLINE_FINAL_CLOSURE_V1.md",
    "minimal_runtime_integration_closure_doc": "docs/architecture/midplatform/LUNA_MINIMAL_RUNTIME_INTEGRATION_CLOSURE_V1.md",
    "ocr_phase_verdict_table": "docs/architecture/evaluation/LUNA_EVALUATION_OCR_PHASE_VERDICT_STATUS_TABLE_V0.md",
}

OPTIONAL_DOCS = {
    "ocr_activation_governance_policy": "docs/architecture/midplatform/LUNA_OCR_ACTIVATION_GOVERNANCE_POLICY_V1.md",
    "ocrrequest_gate_doc": "docs/architecture/ocr/LUNA_OCRREQUEST_GATED_SUBMISSION_FROM_ROI_V2_BBOX_EXPANSION.md",
    "readable_region_guidance_doc": "docs/architecture/midplatform/LUNA_STATIC_READABLE_REGION_DISCOVERY_GUIDANCE_POLICY_V1.md",
    "vision_recognition_evidence_pack": "docs/architecture/vision/LUNA_VISION_RECOGNITION_EVIDENCE_PACK_V0.md",
    "map_anchor_evidence_schema": "docs/architecture/LUNA_MAP_ANCHOR_EVIDENCE_SCHEMA_V0.md",
    "map_gps_poi_binding_policy": "docs/architecture/LUNA_MAP_GPS_POI_OBSERVED_WHERE_BINDING_POLICY_V0.md",
    "world_model_map_anchor_integration": "docs/architecture/LUNA_WORLD_MODEL_MAP_ANCHOR_INTEGRATION_DEFINITION_V0.md",
    "worldmodel_unresolved_observation_slot_contract": "docs/architecture/midplatform/LUNA_WORLDMODEL_UNRESOLVED_OBSERVATION_SLOT_CONTRACT_V0.md",
    "worldmodel_lookup_for_reading_framework": "docs/architecture/evaluation/LUNA_EVALUATION_WORLDMODEL_LOOKUP_FOR_READING_FRAMEWORK_V1.md",
    "confirmed_text_evidence_memory_governance_contract": "docs/architecture/evaluation/LUNA_EVALUATION_CONFIRMED_TEXT_EVIDENCE_MEMORY_GOVERNANCE_CONTRACT_V1.md",
    "safety_task_arbitration_policy": "docs/architecture/evaluation/LUNA_EVALUATION_SAFETY_TASK_ARBITRATION_POLICY_V1.md",
    "speech_gate_boundary_doc": "docs/architecture/LUNA_VOICE_OUTPUT_SPEECH_GATE_MAINLINE_CONTRACT_V0.md",
    "vop_boundary_doc": "docs/architecture/voice/LUNA_VOICE_OUTPUT_PLANE_ADAPTER_FOR_GUIDANCE_V1.md",
    "system_health_center_governance": "docs/architecture/evaluation/LUNA_EVALUATION_SYSTEM_HEALTH_CENTER_GOVERNANCE_V0.md",
    "hardware_profile_capability_registry": "docs/architecture/evaluation/LUNA_EVALUATION_HARDWARE_PROFILE_CAPABILITY_REGISTRY_V1.md",
}

BOUNDARY_FALSE_FLAGS = {
    "dryrun_only": True,
    "no_runtime_executed": True,
    "no_new_runtime_enabled": True,
    "camera_invoked": False,
    "map_api_invoked": False,
    "ocr_provider_invoked": False,
    "ocrrequest_submitted": False,
    "tracking_runtime_invoked": False,
    "optical_flow_runtime_invoked": False,
    "supervision_imported": False,
    "supervision_invoked": False,
    "bytetrack_imported": False,
    "bytetrack_invoked": False,
    "ocsort_imported": False,
    "ocsort_invoked": False,
    "entity_resolution_runtime_invoked": False,
    "fact_admission_runtime_invoked": False,
    "memory_consolidation_invoked": False,
    "library_experience_commit_invoked": False,
    "world_model_written": False,
    "memory_written": False,
    "library_written": False,
    "fact_written": False,
    "scene_delta_generated": False,
    "task_state_committed_now": False,
    "navigation_action_triggered": False,
    "speech_gate_invoked": False,
    "vop_invoked": False,
    "tts_invoked": False,
}

CASE_FIELD_SPECS = [
    {"name": "dryrun_case_id", "type": "string", "required": True},
    {"name": "case_type", "type": "string", "required": True},
    {"name": "simulated_task_context", "type": "object", "required": True},
    {"name": "simulated_task_phase", "type": "string", "required": True},
    {"name": "simulated_scene_sketch_ref", "type": "string", "required": True},
    {"name": "simulated_visual_focus_plan_ref", "type": "string", "required": True},
    {"name": "simulated_visual_focus_slots", "type": "list", "required": True},
    {"name": "simulated_view_quality_ref", "type": "string", "required": True},
    {"name": "simulated_map_context_hint", "type": "string", "required": False},
    {"name": "simulated_memory_context_hint", "type": "string", "required": False},
    {"name": "simulated_ocr_activation_candidate", "type": "string", "required": False},
    {"name": "simulated_tracking_request_candidate", "type": "string", "required": False},
    {"name": "simulated_world_observation_candidate", "type": "string", "required": False},
    {"name": "expected_feedback_candidates", "type": "list", "required": True},
    {"name": "expected_boundary_flags", "type": "object", "required": True},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

FUSION_FIELD_SPECS = [
    {"name": "feedback_fusion_candidate_id", "type": "string", "required": True},
    {"name": "source_case_id", "type": "string", "required": True},
    {"name": "related_task_id", "type": "string", "required": True},
    {"name": "task_phase", "type": "string", "required": True},
    {"name": "visual_refs", "type": "list", "required": True},
    {"name": "ocr_activation_refs", "type": "list", "required": True},
    {"name": "tracking_refs", "type": "list", "required": True},
    {"name": "map_hint_refs", "type": "list", "required": True},
    {"name": "memory_hint_refs", "type": "list", "required": True},
    {"name": "world_observation_refs", "type": "list", "required": True},
    {"name": "conflict_refs", "type": "list", "required": True},
    {"name": "correction_refs", "type": "list", "required": True},
    {"name": "confidence", "type": "number", "required": True},
    {"name": "freshness_status", "type": "string", "required": True},
    {"name": "uncertainty", "type": "number", "required": True},
    {"name": "requires_arbitration", "type": "boolean", "required": True, "default": True},
    {"name": "speech_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "action_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "fact_status", "type": "string", "required": True, "default": "not_fact"},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

TASK_FEEDBACK_TYPES = [
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
    "temporary_facility_task_feedback",
]

TASK_FEEDBACK_FIELD_SPECS = [
    {"name": "task_feedback_candidate_id", "type": "string", "required": True},
    {"name": "source_fusion_candidate_id", "type": "string", "required": True},
    {"name": "feedback_type", "type": "enum", "required": True},
    {"name": "related_task_id", "type": "string", "required": True},
    {"name": "task_phase", "type": "string", "required": True},
    {"name": "evidence_refs", "type": "list", "required": True},
    {"name": "recommended_next_focus", "type": "string", "required": False},
    {"name": "recommended_user_prompt_candidate", "type": "string", "required": False},
    {"name": "requires_safety_arbitration", "type": "boolean", "required": True},
    {"name": "requires_speech_gate", "type": "boolean", "required": True},
    {"name": "confidence", "type": "number", "required": True},
    {"name": "fact_status", "type": "string", "required": True, "default": "not_fact"},
    {"name": "action_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

SAFETY_TYPES = [
    "near_field_obstacle",
    "vehicle_approach",
    "pedestrian_approach",
    "crossing_uncertain",
    "traffic_light_uncertain",
    "route_surface_occluded",
    "crowd_flow_risk",
    "view_quality_poor",
]

SAFETY_FEEDBACK_FIELD_SPECS = [
    {"name": "safety_feedback_candidate_id", "type": "string", "required": True},
    {"name": "source_fusion_candidate_id", "type": "string", "required": True},
    {"name": "safety_type", "type": "enum", "required": True},
    {"name": "evidence_refs", "type": "list", "required": True},
    {"name": "priority", "type": "string", "required": True},
    {"name": "requires_safety_task_arbitration", "type": "boolean", "required": True, "default": True},
    {"name": "speech_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "action_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "fact_status", "type": "string", "required": True, "default": "not_fact"},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

OCR_ACTIVATION_FIELD_SPECS = [
    {"name": "ocr_activation_feedback_id", "type": "string", "required": True},
    {"name": "source_focus_slot_id", "type": "string", "required": True},
    {"name": "ocr_target_type", "type": "string", "required": True},
    {"name": "ocr_activation_reason", "type": "string", "required": True},
    {"name": "readable_region_required", "type": "boolean", "required": True},
    {"name": "ocrrequest_submission_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "ocr_provider_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "fact_status", "type": "string", "required": True, "default": "not_fact"},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

TRACKING_FEEDBACK_FIELD_SPECS = [
    {"name": "tracking_feedback_id", "type": "string", "required": True},
    {"name": "source_tracking_request_candidate_id", "type": "string", "required": True},
    {"name": "tracking_target_type", "type": "string", "required": True},
    {"name": "tracking_reason", "type": "string", "required": True},
    {"name": "candidate_only", "type": "boolean", "required": True, "default": True},
    {"name": "tracking_runtime_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "full_scene_tracking_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "action_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "fact_status", "type": "string", "required": True, "default": "not_fact"},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

MAP_MEMORY_FEEDBACK_FIELD_SPECS = [
    {"name": "map_memory_feedback_id", "type": "string", "required": True},
    {"name": "map_context_hint_ref", "type": "string", "required": False},
    {"name": "memory_context_hint_ref", "type": "string", "required": False},
    {"name": "hint_type", "type": "string", "required": True},
    {"name": "hint_supports_task_phase", "type": "boolean", "required": True},
    {"name": "hint_conflicts_with_visual", "type": "boolean", "required": True},
    {"name": "hint_conflicts_with_ocr", "type": "boolean", "required": True},
    {"name": "hint_conflicts_with_user_feedback", "type": "boolean", "required": True},
    {"name": "current_fact_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "action_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "fact_status", "type": "string", "required": True, "default": "not_fact"},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

CONFLICT_CORRECTION_FIELD_SPECS = [
    {"name": "conflict_correction_feedback_id", "type": "string", "required": True},
    {"name": "conflict_type", "type": "string", "required": True},
    {"name": "conflicting_refs", "type": "list", "required": True},
    {"name": "correction_candidate_ref", "type": "string", "required": False},
    {"name": "requires_review", "type": "boolean", "required": True},
    {"name": "current_action_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "fact_status", "type": "string", "required": True, "default": "not_fact"},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

ACTIVE_VIEW_ADJUSTMENT_FIELD_SPECS = [
    {"name": "active_view_adjustment_feedback_id", "type": "string", "required": True},
    {"name": "source_view_quality_ref", "type": "string", "required": True},
    {"name": "source_focus_slot_ref", "type": "string", "required": True},
    {"name": "adjustment_type", "type": "string", "required": True},
    {"name": "user_prompt_candidate", "type": "string", "required": False},
    {"name": "speech_gate_required", "type": "boolean", "required": True, "default": True},
    {"name": "action_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "fact_status", "type": "string", "required": True, "default": "not_fact"},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

DRYRUN_BOUNDARY_DECISION_FIELD_SPECS = [
    {"name": "case_id", "type": "string", "required": True},
    {"name": "runtime_boundary_ok", "type": "boolean", "required": True},
    {"name": "write_boundary_ok", "type": "boolean", "required": True},
    {"name": "action_boundary_ok", "type": "boolean", "required": True},
    {"name": "speech_boundary_ok", "type": "boolean", "required": True},
    {"name": "worldmodel_boundary_ok", "type": "boolean", "required": True},
    {"name": "memory_boundary_ok", "type": "boolean", "required": True},
    {"name": "library_boundary_ok", "type": "boolean", "required": True},
    {"name": "violations", "type": "list", "required": True},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

SCENARIO_ROWS = [
    {
        "scenario_id": "navigation_route_walking_clear_path",
        "case_type": "navigation_route_walking_clear_path",
        "task_phase": "ROUTE_WALKING",
        "focus_slots": ["walkable_surface_focus", "safety_focus"],
        "view_quality": "GOOD",
        "map_hint": "route_segment_forward_hint",
        "memory_hint": "none",
        "ocr_target": None,
        "tracking_target": None,
        "world_observation": "walkable_path_candidate",
        "expected_feedback": ["route_alignment_feedback"],
    },
    {
        "scenario_id": "navigation_approaching_destination_with_signage",
        "case_type": "navigation_approaching_destination_with_signage",
        "task_phase": "APPROACHING_TARGET",
        "focus_slots": ["destination_landmark_focus", "signage_focus"],
        "view_quality": "GOOD",
        "map_hint": "destination_nearby_hint",
        "memory_hint": "previous_destination_sign_hint",
        "ocr_target": "shopfront_signage_text",
        "tracking_target": None,
        "world_observation": "destination_landmark_candidate",
        "expected_feedback": ["destination_approach_feedback", "ocr_activation_needed"],
    },
    {
        "scenario_id": "shop_search_right_side_storefront",
        "case_type": "shop_search_right_side_storefront",
        "task_phase": "SHOP_SEARCH",
        "focus_slots": ["shopfront_focus", "signage_focus"],
        "view_quality": "DEGRADED",
        "map_hint": "right_side_storefront_hint",
        "memory_hint": "historical_shop_side_hint",
        "ocr_target": "shopfront_nameplate_text",
        "tracking_target": None,
        "world_observation": "shopfront_or_signage_candidate",
        "expected_feedback": ["shopfront_search_feedback", "ocr_activation_needed", "view_adjustment_needed"],
    },
    {
        "scenario_id": "object_search_home_keys",
        "case_type": "object_search_home_keys",
        "task_phase": "OBJECT_SEARCH",
        "focus_slots": ["tabletop_focus", "user_feedback_focus"],
        "view_quality": "GOOD",
        "map_hint": "none",
        "memory_hint": "tabletop_bag_area_hint",
        "ocr_target": None,
        "tracking_target": None,
        "world_observation": "user_relevant_place_candidate",
        "expected_feedback": ["object_search_feedback"],
    },
    {
        "scenario_id": "home_familiar_object_interaction",
        "case_type": "home_familiar_object_interaction",
        "task_phase": "OBJECT_CONFIRMATION",
        "focus_slots": ["destination_landmark_focus", "user_feedback_focus"],
        "view_quality": "GOOD",
        "map_hint": "none",
        "memory_hint": "familiar_object_placeholder_hint",
        "ocr_target": None,
        "tracking_target": None,
        "world_observation": "recurring_observation_candidate",
        "expected_feedback": ["world_observation_handoff_feedback"],
    },
    {
        "scenario_id": "crowded_path_occluded_surface",
        "case_type": "crowded_path_occluded_surface",
        "task_phase": "ROUTE_WALKING",
        "focus_slots": ["walkable_surface_focus", "pedestrian_flow_focus"],
        "view_quality": "DEGRADED",
        "map_hint": "route_continue_forward_hint",
        "memory_hint": "crowded_corridor_history_hint",
        "ocr_target": None,
        "tracking_target": "crowd_flow",
        "world_observation": "scene_change_candidate",
        "expected_feedback": ["route_surface_occluded", "crowd_flow_risk", "tracking_needed"],
    },
    {
        "scenario_id": "crossing_uncertain_traffic_light",
        "case_type": "crossing_uncertain_traffic_light",
        "task_phase": "CROSSING_APPROACH",
        "focus_slots": ["crossing_focus", "traffic_light_focus"],
        "view_quality": "DEGRADED",
        "map_hint": "intersection_ahead_hint",
        "memory_hint": "crossing_confusion_history_hint",
        "ocr_target": "traffic_light_countdown_placeholder",
        "tracking_target": "traffic_light",
        "world_observation": "safety_risk_point_candidate",
        "expected_feedback": ["crossing_uncertain", "traffic_light_uncertain", "tracking_needed"],
    },
    {
        "scenario_id": "temporary_mobile_vendor_near_route",
        "case_type": "temporary_mobile_vendor_near_route",
        "task_phase": "ROUTE_WALKING",
        "focus_slots": ["temporary_facility_focus", "route_path_focus"],
        "view_quality": "GOOD",
        "map_hint": "route_side_activity_hint",
        "memory_hint": "none",
        "ocr_target": "temporary_notice_text",
        "tracking_target": "temporary_facility",
        "world_observation": "temporary_facility_candidate",
        "expected_feedback": ["temporary_facility_task_feedback", "tracking_needed", "world_observation_handoff_feedback"],
    },
    {
        "scenario_id": "visual_map_memory_conflict",
        "case_type": "visual_map_memory_conflict",
        "task_phase": "APPROACHING_TARGET",
        "focus_slots": ["shopfront_focus", "destination_landmark_focus"],
        "view_quality": "GOOD",
        "map_hint": "map_says_shop_right",
        "memory_hint": "memory_says_previous_left",
        "ocr_target": None,
        "tracking_target": None,
        "world_observation": "scene_change_candidate",
        "expected_feedback": ["map_memory_conflict_feedback"],
    },
    {
        "scenario_id": "low_quality_view_requires_hold_still",
        "case_type": "low_quality_view_requires_hold_still",
        "task_phase": "GENERAL_SCAN",
        "focus_slots": ["safety_focus", "destination_landmark_focus"],
        "view_quality": "POOR",
        "map_hint": "none",
        "memory_hint": "none",
        "ocr_target": None,
        "tracking_target": None,
        "world_observation": "none",
        "expected_feedback": ["view_quality_poor", "view_adjustment_needed"],
    },
]

GOVERNANCE_DEBT_TOPICS = [
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


def _schema_payload(schema_id: str, object_name: str, fields: List[Dict[str, Any]], **extra: Any) -> Dict[str, Any]:
    payload = {
        "schema_id": schema_id,
        "object_name": object_name,
        "fields": fields,
        "field_count": len(fields),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }
    payload.update(extra)
    return payload


def _load_optional_json(root_meta: Dict[str, Any], filename: str) -> Dict[str, Any]:
    root = root_meta.get("root")
    path = root / filename if root else None
    if path and path.is_file():
        return _read_json(path)
    return {}


def _boundary_payload() -> Dict[str, Any]:
    return {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        **BOUNDARY_FALSE_FLAGS,
        "feedback_candidates_require_arbitration": True,
        "speech_allowed_false_until_gate": True,
        "action_allowed_false": True,
        "fact_status_not_fact": True,
        "ocrrequest_submission_allowed": False,
        "ocr_provider_allowed": False,
        "tracking_runtime_allowed": False,
        "crossing_action_instruction_allowed": False,
        "crowd_flow_follow_action_allowed": False,
        "fixed_poi_commit_allowed": False,
        "identity_fact_allowed": False,
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


def _fusion_candidate(case: Dict[str, Any], idx: int) -> Dict[str, Any]:
    return {
        "feedback_fusion_candidate_id": f"fusion_{idx:02d}",
        "source_case_id": case["scenario_id"],
        "related_task_id": f"task_{idx:02d}",
        "task_phase": case["task_phase"],
        "visual_refs": [f"visual_focus_plan_{idx:02d}", *[f"{slot}_{idx:02d}" for slot in case["focus_slots"]]],
        "ocr_activation_refs": [f"ocr_activation_{idx:02d}"] if case["ocr_target"] else [],
        "tracking_refs": [f"tracking_request_{idx:02d}"] if case["tracking_target"] else [],
        "map_hint_refs": [case["map_hint"]] if case["map_hint"] != "none" else [],
        "memory_hint_refs": [case["memory_hint"]] if case["memory_hint"] != "none" else [],
        "world_observation_refs": [case["world_observation"]] if case["world_observation"] != "none" else [],
        "conflict_refs": [f"conflict_{idx:02d}"] if case["scenario_id"] == "visual_map_memory_conflict" else [],
        "correction_refs": [f"correction_{idx:02d}"] if case["scenario_id"] == "visual_map_memory_conflict" else [],
        "confidence": 0.74,
        "freshness_status": "fresh_candidate",
        "uncertainty": 0.19,
        "requires_arbitration": True,
        "speech_allowed": False,
        "action_allowed": False,
        "fact_status": "not_fact",
        "source_chain": SOURCE_CHAIN,
    }


def _task_feedback(case: Dict[str, Any], fusion_id: str, idx: int) -> List[Dict[str, Any]]:
    feedbacks: List[Dict[str, Any]] = []
    if case["scenario_id"] == "low_quality_view_requires_hold_still":
        return feedbacks

    mapping = {
        "navigation_route_walking_clear_path": ("route_alignment_feedback", "继续保持前方可行走路径焦点"),
        "navigation_approaching_destination_with_signage": ("destination_approach_feedback", "继续关注前方与右侧标识"),
        "shop_search_right_side_storefront": ("shopfront_search_feedback", "右侧门头与招牌继续确认"),
        "object_search_home_keys": ("object_search_feedback", "优先查看桌面与包附近区域"),
        "home_familiar_object_interaction": ("world_observation_handoff_feedback", "保留熟悉物体候选供未来 handoff"),
        "crowded_path_occluded_surface": ("tracking_needed", "优先保守观察遮挡路径与人流方向"),
        "crossing_uncertain_traffic_light": ("tracking_needed", "继续保持过街相关焦点，等待 arbitration"),
        "temporary_mobile_vendor_near_route": ("temporary_facility_task_feedback", "保留临时设施候选并检查路线相关性"),
        "visual_map_memory_conflict": ("map_memory_conflict_feedback", "冲突需要 review，不更新事实"),
    }
    feedback_type, next_focus = mapping[case["scenario_id"]]
    feedbacks.append(
        {
            "task_feedback_candidate_id": f"task_feedback_{idx:02d}_1",
            "source_fusion_candidate_id": fusion_id,
            "feedback_type": feedback_type,
            "related_task_id": f"task_{idx:02d}",
            "task_phase": case["task_phase"],
            "evidence_refs": [fusion_id],
            "recommended_next_focus": next_focus,
            "recommended_user_prompt_candidate": None if case["scenario_id"] != "shop_search_right_side_storefront" else "请稍微把视角对准右侧门头",
            "requires_safety_arbitration": case["scenario_id"] in {"crowded_path_occluded_surface", "crossing_uncertain_traffic_light"},
            "requires_speech_gate": True,
            "confidence": 0.71,
            "fact_status": "not_fact",
            "action_allowed": False,
            "source_chain": SOURCE_CHAIN,
        }
    )
    if case["scenario_id"] in {"navigation_approaching_destination_with_signage", "shop_search_right_side_storefront"}:
        feedbacks.append(
            {
                "task_feedback_candidate_id": f"task_feedback_{idx:02d}_2",
                "source_fusion_candidate_id": fusion_id,
                "feedback_type": "ocr_activation_needed",
                "related_task_id": f"task_{idx:02d}",
                "task_phase": case["task_phase"],
                "evidence_refs": [fusion_id, f"ocr_activation_{idx:02d}"],
                "recommended_next_focus": "readable_region_focus",
                "recommended_user_prompt_candidate": None,
                "requires_safety_arbitration": False,
                "requires_speech_gate": True,
                "confidence": 0.66,
                "fact_status": "not_fact",
                "action_allowed": False,
                "source_chain": SOURCE_CHAIN,
            }
        )
    return feedbacks


def _safety_feedback(case: Dict[str, Any], fusion_id: str, idx: int) -> List[Dict[str, Any]]:
    outputs: List[Dict[str, Any]] = []
    scenario_to_types = {
        "crowded_path_occluded_surface": ["route_surface_occluded", "crowd_flow_risk"],
        "crossing_uncertain_traffic_light": ["crossing_uncertain", "traffic_light_uncertain"],
        "low_quality_view_requires_hold_still": ["view_quality_poor"],
        "navigation_route_walking_clear_path": ["near_field_obstacle"],
    }
    for order, safety_type in enumerate(scenario_to_types.get(case["scenario_id"], []), start=1):
        outputs.append(
            {
                "safety_feedback_candidate_id": f"safety_feedback_{idx:02d}_{order}",
                "source_fusion_candidate_id": fusion_id,
                "safety_type": safety_type,
                "evidence_refs": [fusion_id],
                "priority": "P0" if safety_type in {"crossing_uncertain", "traffic_light_uncertain", "near_field_obstacle"} else "P1",
                "requires_safety_task_arbitration": True,
                "speech_allowed": False,
                "action_allowed": False,
                "fact_status": "not_fact",
                "source_chain": SOURCE_CHAIN,
            }
        )
    return outputs


def _ocr_feedback(case: Dict[str, Any], idx: int) -> List[Dict[str, Any]]:
    if not case["ocr_target"]:
        return []
    return [
        {
            "ocr_activation_feedback_id": f"ocr_activation_feedback_{idx:02d}",
            "source_focus_slot_id": f"{case['focus_slots'][-1]}_{idx:02d}",
            "ocr_target_type": case["ocr_target"],
            "ocr_activation_reason": "focus-triggered readable target candidate",
            "readable_region_required": True,
            "ocrrequest_submission_allowed": False,
            "ocr_provider_allowed": False,
            "fact_status": "not_fact",
            "source_chain": SOURCE_CHAIN,
        }
    ]


def _tracking_feedback(case: Dict[str, Any], idx: int) -> List[Dict[str, Any]]:
    if not case["tracking_target"]:
        return []
    return [
        {
            "tracking_feedback_id": f"tracking_feedback_{idx:02d}",
            "source_tracking_request_candidate_id": f"tracking_request_{idx:02d}",
            "tracking_target_type": case["tracking_target"],
            "tracking_reason": "focus-approved tracking candidate for task/safety feedback",
            "candidate_only": True,
            "tracking_runtime_allowed": False,
            "full_scene_tracking_allowed": False,
            "action_allowed": False,
            "fact_status": "not_fact",
            "source_chain": SOURCE_CHAIN,
        }
    ]


def _map_memory_feedback(case: Dict[str, Any], idx: int) -> List[Dict[str, Any]]:
    if case["map_hint"] == "none" and case["memory_hint"] == "none":
        return []
    is_conflict = case["scenario_id"] == "visual_map_memory_conflict"
    return [
        {
            "map_memory_feedback_id": f"map_memory_feedback_{idx:02d}",
            "map_context_hint_ref": None if case["map_hint"] == "none" else case["map_hint"],
            "memory_context_hint_ref": None if case["memory_hint"] == "none" else case["memory_hint"],
            "hint_type": "conflict_hint" if is_conflict else "supporting_hint",
            "hint_supports_task_phase": not is_conflict,
            "hint_conflicts_with_visual": is_conflict,
            "hint_conflicts_with_ocr": False,
            "hint_conflicts_with_user_feedback": is_conflict,
            "current_fact_allowed": False,
            "action_allowed": False,
            "fact_status": "not_fact",
            "source_chain": SOURCE_CHAIN,
        }
    ]


def _conflict_feedback(case: Dict[str, Any], idx: int) -> List[Dict[str, Any]]:
    if case["scenario_id"] != "visual_map_memory_conflict":
        return []
    return [
        {
            "conflict_correction_feedback_id": f"conflict_feedback_{idx:02d}",
            "conflict_type": "visual_vs_map_vs_memory",
            "conflicting_refs": ["visual_ref_current_scene", case["map_hint"], case["memory_hint"]],
            "correction_candidate_ref": f"correction_{idx:02d}",
            "requires_review": True,
            "current_action_allowed": False,
            "fact_status": "not_fact",
            "source_chain": SOURCE_CHAIN,
        }
    ]


def _active_view_adjustment_feedback(case: Dict[str, Any], idx: int) -> List[Dict[str, Any]]:
    if case["scenario_id"] not in {"shop_search_right_side_storefront", "low_quality_view_requires_hold_still"}:
        return []
    adjustment_type = "center_target" if case["scenario_id"] == "shop_search_right_side_storefront" else "hold_still"
    prompt = "请稍微把镜头对准右侧门头" if case["scenario_id"] == "shop_search_right_side_storefront" else "请先保持不动，让画面稳定一点"
    return [
        {
            "active_view_adjustment_feedback_id": f"view_adjustment_feedback_{idx:02d}",
            "source_view_quality_ref": f"view_quality_{idx:02d}_{case['view_quality']}",
            "source_focus_slot_ref": f"{case['focus_slots'][0]}_{idx:02d}",
            "adjustment_type": adjustment_type,
            "user_prompt_candidate": prompt,
            "speech_gate_required": True,
            "action_allowed": False,
            "fact_status": "not_fact",
            "source_chain": SOURCE_CHAIN,
        }
    ]


def _world_observation_feedback(case: Dict[str, Any], idx: int) -> List[Dict[str, Any]]:
    if case["world_observation"] == "none":
        return []
    return [
        {
            "world_observation_feedback_id": f"world_observation_feedback_{idx:02d}",
            "source_world_observation_candidate_id": case["world_observation"],
            "feedback_type": "world_observation_handoff_feedback",
            "worldmodel_handoff_candidate_allowed": True,
            "memory_handoff_candidate_allowed": True,
            "library_handoff_placeholder_allowed": True,
            "action_allowed": False,
            "fact_status": "not_fact",
            "source_chain": SOURCE_CHAIN,
        }
    ]


def _boundary_decision(case_id: str) -> Dict[str, Any]:
    return {
        "case_id": case_id,
        "runtime_boundary_ok": True,
        "write_boundary_ok": True,
        "action_boundary_ok": True,
        "speech_boundary_ok": True,
        "worldmodel_boundary_ok": True,
        "memory_boundary_ok": True,
        "library_boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _build_dryrun_results() -> Dict[str, Any]:
    case_results: List[Dict[str, Any]] = []
    task_feedback_total = 0
    safety_feedback_total = 0
    ocr_feedback_total = 0
    tracking_feedback_total = 0
    map_memory_feedback_total = 0
    conflict_feedback_total = 0
    view_adjustment_feedback_total = 0
    world_observation_feedback_total = 0

    for idx, case in enumerate(SCENARIO_ROWS, start=1):
        dryrun_case = {
            "dryrun_case_id": case["scenario_id"],
            "case_type": case["case_type"],
            "simulated_task_context": {
                "task_id": f"task_{idx:02d}",
                "task_name": case["case_type"],
            },
            "simulated_task_phase": case["task_phase"],
            "simulated_scene_sketch_ref": f"scene_sketch_{idx:02d}",
            "simulated_visual_focus_plan_ref": f"visual_focus_plan_{idx:02d}",
            "simulated_visual_focus_slots": case["focus_slots"],
            "simulated_view_quality_ref": f"view_quality_{idx:02d}_{case['view_quality']}",
            "simulated_map_context_hint": case["map_hint"],
            "simulated_memory_context_hint": case["memory_hint"],
            "simulated_ocr_activation_candidate": None if case["ocr_target"] is None else f"ocr_activation_{idx:02d}",
            "simulated_tracking_request_candidate": None if case["tracking_target"] is None else f"tracking_request_{idx:02d}",
            "simulated_world_observation_candidate": None if case["world_observation"] == "none" else case["world_observation"],
            "expected_feedback_candidates": case["expected_feedback"],
            "expected_boundary_flags": {
                "speech_allowed_false_until_gate": True,
                "action_allowed_false": True,
                "fact_status_not_fact": True,
                "runtime_not_allowed": True,
            },
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }

        fusion = _fusion_candidate(case, idx)
        task_feedback = _task_feedback(case, fusion["feedback_fusion_candidate_id"], idx)
        safety_feedback = _safety_feedback(case, fusion["feedback_fusion_candidate_id"], idx)
        ocr_feedback = _ocr_feedback(case, idx)
        tracking_feedback = _tracking_feedback(case, idx)
        map_memory_feedback = _map_memory_feedback(case, idx)
        conflict_feedback = _conflict_feedback(case, idx)
        view_adjustment_feedback = _active_view_adjustment_feedback(case, idx)
        world_observation_feedback = _world_observation_feedback(case, idx)
        boundary_decision = _boundary_decision(case["scenario_id"])

        task_feedback_total += len(task_feedback)
        safety_feedback_total += len(safety_feedback)
        ocr_feedback_total += len(ocr_feedback)
        tracking_feedback_total += len(tracking_feedback)
        map_memory_feedback_total += len(map_memory_feedback)
        conflict_feedback_total += len(conflict_feedback)
        view_adjustment_feedback_total += len(view_adjustment_feedback)
        world_observation_feedback_total += len(world_observation_feedback)

        case_results.append(
            {
                "dryrun_case": dryrun_case,
                "feedback_fusion_candidate": fusion,
                "task_feedback_candidates": task_feedback,
                "safety_feedback_candidates": safety_feedback,
                "ocr_activation_feedback_candidates": ocr_feedback,
                "tracking_feedback_candidates": tracking_feedback,
                "map_memory_context_feedback_candidates": map_memory_feedback,
                "conflict_correction_feedback_candidates": conflict_feedback,
                "active_view_adjustment_feedback_candidates": view_adjustment_feedback,
                "world_observation_feedback_candidates": world_observation_feedback,
                "dryrun_boundary_decision": boundary_decision,
                "task_feedback_suppressed": case["scenario_id"] == "low_quality_view_requires_hold_still",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    total_feedback_count = (
        task_feedback_total
        + safety_feedback_total
        + ocr_feedback_total
        + tracking_feedback_total
        + map_memory_feedback_total
        + conflict_feedback_total
        + view_adjustment_feedback_total
        + world_observation_feedback_total
    )
    return {
        "results_id": f"{POLICY_ID}_dryrun_results",
        "case_results": case_results,
        "case_count": len(case_results),
        "dryrun_results_generated": True,
        "feedback_candidate_count": total_feedback_count,
        "task_feedback_candidate_count": task_feedback_total,
        "safety_feedback_candidate_count": safety_feedback_total,
        "ocr_activation_feedback_candidate_count": ocr_feedback_total,
        "tracking_feedback_candidate_count": tracking_feedback_total,
        "map_memory_context_feedback_candidate_count": map_memory_feedback_total,
        "conflict_correction_feedback_candidate_count": conflict_feedback_total,
        "active_view_adjustment_feedback_candidate_count": view_adjustment_feedback_total,
        "world_observation_feedback_candidate_count": world_observation_feedback_total,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def run_visual_ocr_map_task_feedback_dryrun_v1(
    *,
    selective_tracking_root: str,
    world_observation_entity_feature_root: str,
    task_aware_visual_focus_root: str,
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
        "selective_tracking_root": selective_tracking_root,
        "world_observation_entity_feature_root": world_observation_entity_feature_root,
        "task_aware_visual_focus_root": task_aware_visual_focus_root,
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

    selective_tracking_summary = _read_json(root_meta["selective_tracking"]["summary_path"]) if root_meta["selective_tracking"]["summary_path"] else {}
    worldobs_summary = _read_json(root_meta["world_observation_entity_feature"]["summary_path"]) if root_meta["world_observation_entity_feature"]["summary_path"] else {}
    visual_focus_summary = _read_json(root_meta["task_aware_visual_focus"]["summary_path"]) if root_meta["task_aware_visual_focus"]["summary_path"] else {}
    midplatform_summary = _read_json(root_meta["midplatform_perception_orchestration"]["summary_path"]) if root_meta["midplatform_perception_orchestration"]["summary_path"] else {}
    planning_summary = _read_json(root_meta["return_to_vision_planning"]["summary_path"]) if root_meta["return_to_vision_planning"]["summary_path"] else {}
    preplan_summary = _read_json(root_meta["preplan_input"]["summary_path"]) if root_meta["preplan_input"]["summary_path"] else {}
    ocr_summary = _read_json(root_meta["ocr_final_closure"]["summary_path"]) if root_meta["ocr_final_closure"]["summary_path"] else {}
    mri_summary = _read_json(root_meta["minimal_runtime_integration_closure"]["summary_path"]) if root_meta["minimal_runtime_integration_closure"]["summary_path"] else {}

    selective_tracking_input_loaded = (
        root_meta["selective_tracking"]["loaded"]
        and selective_tracking_summary.get("final_decision") == SELECTIVE_TRACKING_FINAL_DECISION
        and selective_tracking_summary.get("external_tracking_adapters_future_candidate_only") is True
    )
    world_observation_entity_feature_input_loaded = (
        root_meta["world_observation_entity_feature"]["loaded"]
        and worldobs_summary.get("final_decision") == WORLDOBS_FINAL_DECISION
        and worldobs_summary.get("worldmodel_handoff_candidate_allowed") is True
    )
    task_aware_visual_focus_input_loaded = (
        root_meta["task_aware_visual_focus"]["loaded"]
        and visual_focus_summary.get("final_decision") == VISUAL_FOCUS_FINAL_DECISION
        and visual_focus_summary.get("focus_to_ocr_activation_policy_defined") is True
    )
    midplatform_perception_orchestration_input_loaded = (
        root_meta["midplatform_perception_orchestration"]["loaded"]
        and midplatform_summary.get("final_decision") == MIDPLATFORM_FINAL_DECISION
        and midplatform_summary.get("map_memory_context_hint_policy_defined") is True
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

    worldobs_placeholder = _load_optional_json(root_meta["world_observation_entity_feature"], "worldmodel_memory_library_placeholder_policy.json")
    focus_to_ocr = _load_optional_json(root_meta["task_aware_visual_focus"], "focus_to_ocr_activation_policy.json")
    focus_to_tracking = _load_optional_json(root_meta["task_aware_visual_focus"], "focus_to_tracking_request_policy.json")
    map_memory_hint = _load_optional_json(root_meta["midplatform_perception_orchestration"], "map_memory_context_hint_policy.json")

    dryrun_case_schema = _schema_payload(
        f"{POLICY_ID}_dryrun_case",
        "VisualOcrMapTaskFeedbackDryRunCase",
        CASE_FIELD_SPECS,
        scenario_ids=[row["scenario_id"] for row in SCENARIO_ROWS],
    )
    feedback_fusion_candidate_schema = _schema_payload(
        f"{POLICY_ID}_feedback_fusion_candidate",
        "FeedbackFusionCandidate",
        FUSION_FIELD_SPECS,
        feedback_candidates_require_arbitration=True,
        speech_allowed_false_until_gate=True,
        action_allowed_false=True,
        fact_status_not_fact=True,
    )
    task_feedback_candidate_schema = _schema_payload(
        f"{POLICY_ID}_task_feedback_candidate",
        "TaskFeedbackCandidate",
        TASK_FEEDBACK_FIELD_SPECS,
        feedback_types=TASK_FEEDBACK_TYPES,
        action_allowed_false=True,
    )
    safety_feedback_candidate_schema = _schema_payload(
        f"{POLICY_ID}_safety_feedback_candidate",
        "SafetyFeedbackCandidate",
        SAFETY_FEEDBACK_FIELD_SPECS,
        safety_types=SAFETY_TYPES,
        speech_allowed_false_until_gate=True,
        action_allowed_false=True,
    )
    ocr_activation_feedback_candidate_schema = _schema_payload(
        f"{POLICY_ID}_ocr_activation_feedback_candidate",
        "OCRActivationFeedbackCandidate",
        OCR_ACTIVATION_FIELD_SPECS,
        ocrrequest_submission_allowed=False,
        ocr_provider_allowed=False,
    )
    tracking_feedback_candidate_schema = _schema_payload(
        f"{POLICY_ID}_tracking_feedback_candidate",
        "TrackingFeedbackCandidate",
        TRACKING_FEEDBACK_FIELD_SPECS,
        tracking_runtime_allowed=False,
        full_scene_tracking_allowed=False,
        candidate_only=True,
    )
    map_memory_context_feedback_candidate_schema = _schema_payload(
        f"{POLICY_ID}_map_memory_context_feedback_candidate",
        "MapMemoryContextFeedbackCandidate",
        MAP_MEMORY_FEEDBACK_FIELD_SPECS,
        current_fact_allowed=False,
        action_allowed_false=True,
    )
    conflict_correction_feedback_candidate_schema = _schema_payload(
        f"{POLICY_ID}_conflict_correction_feedback_candidate",
        "ConflictCorrectionFeedbackCandidate",
        CONFLICT_CORRECTION_FIELD_SPECS,
        current_action_allowed_default=False,
    )
    active_view_adjustment_feedback_candidate_schema = _schema_payload(
        f"{POLICY_ID}_active_view_adjustment_feedback_candidate",
        "ActiveViewAdjustmentFeedbackCandidate",
        ACTIVE_VIEW_ADJUSTMENT_FIELD_SPECS,
        speech_gate_required_default=True,
        action_allowed_false=True,
    )
    dryrun_boundary_decision_schema = _schema_payload(
        f"{POLICY_ID}_dryrun_boundary_decision",
        "DryRunBoundaryDecision",
        DRYRUN_BOUNDARY_DECISION_FIELD_SPECS,
        all_boundaries_default_true=True,
    )

    scenario_matrix = {
        "matrix_id": f"{POLICY_ID}_scenario_matrix",
        "scenarios": [
            {
                **row,
                "dryrun_only": True,
                "runtime_allowed_now": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for row in SCENARIO_ROWS
        ],
        "scenario_count": len(SCENARIO_ROWS),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    dryrun_results = _build_dryrun_results()

    feedback_boundary_matrix = {
        "matrix_id": f"{POLICY_ID}_feedback_boundary_matrix",
        "feedback_candidates_require_arbitration": True,
        "speech_allowed_false_until_gate": True,
        "action_allowed_false": True,
        "fact_status_not_fact": True,
        "ocrrequest_submission_allowed": False,
        "ocr_provider_allowed": False,
        "tracking_runtime_allowed": False,
        "crossing_action_instruction_allowed": False,
        "crowd_flow_follow_action_allowed": False,
        "fixed_poi_commit_allowed": False,
        "identity_fact_allowed": False,
        "worldmodel_handoff_candidate_allowed": True,
        "memory_handoff_candidate_allowed": True,
        "library_handoff_placeholder_allowed": True,
        "worldmodel_write_allowed": False,
        "memory_write_allowed": False,
        "library_write_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_register = {
        "register_id": f"{POLICY_ID}_governance_debt",
        "debts": [
            {
                "debt_id": f"debt_{idx:02d}",
                "topic": topic,
                "deferred_reason": "先完成 feedback dry-run 链，再单独进入 Basic Navigation Loop Vision Strengthening / MidPlatform Function Governance。",
                "future_owner_phase": "MidPlatform Function Governance / Navigation Loop Strengthening",
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
        "reason": "视觉 / OCR / 地图 / 记忆 / tracking candidate / 任务反馈 dry-run 链已建立，下一阶段应接回基础导航闭环强化。",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    boundary = _boundary_payload()
    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "selective_tracking_input_loaded": selective_tracking_input_loaded,
        "world_observation_entity_feature_input_loaded": world_observation_entity_feature_input_loaded,
        "task_aware_visual_focus_input_loaded": task_aware_visual_focus_input_loaded,
        "midplatform_perception_orchestration_input_loaded": midplatform_perception_orchestration_input_loaded,
        "return_to_vision_planning_input_loaded": return_to_vision_planning_input_loaded,
        "preplan_input_loaded": preplan_input_loaded,
        "ocr_final_closure_loaded": ocr_final_closure_loaded,
        "minimal_runtime_integration_closure_loaded": minimal_runtime_integration_closure_loaded,
        "dryrun_case_schema_defined": True,
        "feedback_fusion_candidate_schema_defined": True,
        "task_feedback_candidate_schema_defined": True,
        "safety_feedback_candidate_schema_defined": True,
        "ocr_activation_feedback_candidate_schema_defined": True,
        "tracking_feedback_candidate_schema_defined": True,
        "map_memory_context_feedback_candidate_schema_defined": True,
        "conflict_correction_feedback_candidate_schema_defined": True,
        "active_view_adjustment_feedback_candidate_schema_defined": True,
        "dryrun_boundary_decision_schema_defined": True,
        "scenario_matrix_generated": True,
        "scenario_count": len(SCENARIO_ROWS),
        "dryrun_results_generated": True,
        "feedback_candidate_count": dryrun_results["feedback_candidate_count"],
        "task_feedback_candidate_generated": dryrun_results["task_feedback_candidate_count"] > 0,
        "safety_feedback_candidate_generated": dryrun_results["safety_feedback_candidate_count"] > 0,
        "ocr_activation_feedback_candidate_generated": dryrun_results["ocr_activation_feedback_candidate_count"] > 0,
        "tracking_feedback_candidate_generated": dryrun_results["tracking_feedback_candidate_count"] > 0,
        "map_memory_context_feedback_candidate_generated": dryrun_results["map_memory_context_feedback_candidate_count"] > 0,
        "conflict_correction_feedback_candidate_generated": dryrun_results["conflict_correction_feedback_candidate_count"] > 0,
        "active_view_adjustment_feedback_candidate_generated": dryrun_results["active_view_adjustment_feedback_candidate_count"] > 0,
        "feedback_candidates_require_arbitration": True,
        "speech_allowed_false_until_gate": True,
        "action_allowed_false": True,
        "fact_status_not_fact": True,
        "ocrrequest_submission_allowed": False,
        "ocr_provider_allowed": False,
        "tracking_runtime_allowed": False,
        "crossing_action_instruction_allowed": False,
        "crowd_flow_follow_action_allowed": False,
        "fixed_poi_commit_allowed": False,
        "identity_fact_allowed": False,
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
        "dryrun_case_schema": dryrun_case_schema,
        "feedback_fusion_candidate_schema": feedback_fusion_candidate_schema,
        "task_feedback_candidate_schema": task_feedback_candidate_schema,
        "safety_feedback_candidate_schema": safety_feedback_candidate_schema,
        "ocr_activation_feedback_candidate_schema": ocr_activation_feedback_candidate_schema,
        "tracking_feedback_candidate_schema": tracking_feedback_candidate_schema,
        "map_memory_context_feedback_candidate_schema": map_memory_context_feedback_candidate_schema,
        "conflict_correction_feedback_candidate_schema": conflict_correction_feedback_candidate_schema,
        "active_view_adjustment_feedback_candidate_schema": active_view_adjustment_feedback_candidate_schema,
        "dryrun_boundary_decision_schema": dryrun_boundary_decision_schema,
        "visual_ocr_map_task_feedback_scenario_matrix": scenario_matrix,
        "visual_ocr_map_task_feedback_dryrun_results": dryrun_results,
        "feedback_boundary_matrix": feedback_boundary_matrix,
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_runtime_boundary_report": boundary,
        "no_write_boundary_report": boundary,
        "debug_refs": {
            "workspace_root": str(workspace),
            "selective_tracking_final_decision": selective_tracking_summary.get("final_decision"),
            "worldobs_final_decision": worldobs_summary.get("final_decision"),
            "visual_focus_final_decision": visual_focus_summary.get("final_decision"),
            "midplatform_final_decision": midplatform_summary.get("final_decision"),
            "planning_final_decision": planning_summary.get("final_decision"),
            "preplan_ready_flag": preplan_summary.get(PREPLAN_READY_FLAG),
            "ocr_final_decision": ocr_summary.get("final_decision"),
            "minimal_runtime_final_decision": mri_summary.get("final_decision"),
            "focus_to_ocr_policy_loaded": bool(focus_to_ocr.get("policy_id")),
            "focus_to_tracking_policy_loaded": bool(focus_to_tracking.get("policy_id")),
            "map_memory_hint_policy_loaded": bool(map_memory_hint.get("policy_id")),
            "worldobs_placeholder_loaded": bool(worldobs_placeholder.get("policy_id")),
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
