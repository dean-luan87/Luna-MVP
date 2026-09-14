# -*- coding: utf-8 -*-
"""Basic Navigation Loop Vision Strengthening DryRun v1.

Phase-Basic-Navigation-Loop-Vision-Strengthening-DryRun-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Basic-Navigation-Loop-Vision-Strengthening-DryRun-v1-001"
POLICY_ID = "bnlvsd_v1_001"
DRYRUN_SCOPE = "basic_navigation_loop_vision_strengthening_dryrun_only"
SOURCE_CHAIN = "basic_navigation_loop_vision_strengthening_dryrun_v1"
FINAL_DECISION = "BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Basic-Navigation-Loop-Vision-Strengthening-Post-DryRun-Review-v1-001"
VISUAL_FEEDBACK_FINAL_DECISION = "VISUAL_OCR_MAP_TASK_FEEDBACK_DRYRUN_READY_FOR_BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING"
SELECTIVE_TRACKING_FINAL_DECISION = "SELECTIVE_TRACKING_ADAPTER_POLICY_READY_FOR_VISUAL_OCR_MAP_TASK_FEEDBACK_DRYRUN"
WORLDOBS_FINAL_DECISION = "WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY_READY_FOR_SELECTIVE_TRACKING_ADAPTER_POLICY"
VISUAL_FOCUS_FINAL_DECISION = "TASK_AWARE_VISUAL_FOCUS_POLICY_READY_FOR_WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY"
MIDPLATFORM_FINAL_DECISION = "MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY_READY_FOR_TASK_AWARE_VISUAL_FOCUS_POLICY"
PLANNING_FINAL_DECISION = "RETURN_TO_VISION_MAINLINE_PLANNING_READY_FOR_MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY"
PREPLAN_READY_FLAG = "preplan_ready_for_formal_phase_decision"
OCR_FINAL_DECISION = "OCR_MAINLINE_FINAL_CLOSURE_RETURN_TO_VISION_MAINLINE"
MRI_FINAL_DECISION = "MINIMAL_RUNTIME_INTEGRATION_CLOSED_RETURN_TO_VISION_MAINLINE"
BASIC_NAV_STABILIZATION_FINAL_DECISION = "BASIC_NAVIGATION_GUIDANCE_LOOP_STABILIZATION_READY_FOR_MINIMAL_RUNTIME_INTEGRATION_TRIAL"

ROOT_INPUT_SPECS = [
    {
        "intake_id": "visual_ocr_map_task_feedback",
        "path_arg": "visual_ocr_map_task_feedback_root",
        "label": "Visual OCR Map Task Feedback DryRun v1",
        "required": True,
        "summary_file": "summary.json",
        "extra_artifacts": [
            "visual_ocr_map_task_feedback_dryrun_results.json",
            "feedback_boundary_matrix.json",
            "task_feedback_candidate_schema.json",
        ],
    },
    {
        "intake_id": "selective_tracking",
        "path_arg": "selective_tracking_root",
        "label": "Selective Tracking Adapter Policy v1",
        "required": True,
        "summary_file": "summary.json",
        "extra_artifacts": [
            "tracking_feedback_candidate_schema.json",
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
            "active_view_adjustment_candidate_schema.json",
        ],
    },
    {
        "intake_id": "midplatform_perception_orchestration",
        "path_arg": "midplatform_perception_orchestration_root",
        "label": "MidPlatform Perception Orchestration Policy v1",
        "required": True,
        "summary_file": "summary.json",
        "extra_artifacts": [
            "map_memory_context_hint_policy.json",
            "perception_feedback_candidate_policy.json",
        ],
    },
    {
        "intake_id": "basic_navigation_loop_stabilization",
        "path_arg": "basic_navigation_loop_stabilization_root",
        "label": "Basic Navigation Guidance Loop Stabilization Test v1",
        "required": True,
        "summary_file": "summary.json",
        "extra_artifacts": [
            "stabilization_decision_candidates.json",
            "handoff_boundary_matrix.json",
        ],
    },
    {
        "intake_id": "safety_task_arbitration_policy",
        "path_arg": "safety_task_arbitration_policy_root",
        "label": "Safety Task Arbitration Policy v1",
        "required": True,
        "summary_file": "safety_task_arbitration_policy_v1_summary.json",
        "extra_artifacts": [
            "safety_task_arbitration_boundary_report_v1.json",
            "safety_task_arbitration_final_decision_v1.json",
        ],
    },
    {
        "intake_id": "minimal_runtime_integration_closure",
        "path_arg": "minimal_runtime_integration_closure_root",
        "label": "Minimal Runtime Integration Closure v1",
        "required": True,
        "summary_file": "summary.json",
        "extra_artifacts": [
            "vision_mainline_handoff_plan.json",
            "minimal_runtime_integration_closure_report.json",
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
]

OPTIONAL_ROOT_SPECS = [
    {
        "intake_id": "basic_navigation_guidance_loop_dryrun",
        "path_arg": "basic_navigation_guidance_loop_dryrun_root",
        "label": "Basic Navigation Guidance Loop DryRun v1",
        "required": False,
        "summary_file": "basic_navigation_guidance_loop_dryrun_v1_summary.json",
        "extra_artifacts": [
            "basic_navigation_guidance_decision_candidate_collection_v1.json",
        ],
    },
    {
        "intake_id": "navigation_guidance_speech_adapter",
        "path_arg": "navigation_guidance_speech_adapter_root",
        "label": "Navigation Guidance Speech Adapter v1",
        "required": False,
        "summary_file": "summary.json",
        "extra_artifacts": [],
    },
    {
        "intake_id": "voice_interruption_governance_dryrun",
        "path_arg": "voice_interruption_governance_dryrun_root",
        "label": "Voice Interruption Governance DryRun v1",
        "required": False,
        "summary_file": "summary.json",
        "extra_artifacts": [
            "interruption_decision_candidates.json",
        ],
    },
    {
        "intake_id": "voice_command_ownership_gate_policy",
        "path_arg": "voice_command_ownership_gate_policy_root",
        "label": "Voice Command Ownership Gate Policy v1",
        "required": False,
        "summary_file": "voice_command_ownership_gate_policy_v1_summary.json",
        "extra_artifacts": [
            "voice_command_ownership_gate_decision_candidates_v1.json",
        ],
    },
    {
        "intake_id": "text_only_output_post_trial_review",
        "path_arg": "text_only_output_post_trial_review_root",
        "label": "Text-Only Output Post Trial Review v1",
        "required": False,
        "summary_file": "summary.json",
        "extra_artifacts": [
            "text_only_output_post_trial_review_report.json",
            "output_mode_boundary_review.json",
        ],
    },
]

REQUIRED_DOCS = {
    "visual_ocr_map_task_feedback_doc": "docs/architecture/vision/LUNA_VISUAL_OCR_MAP_TASK_FEEDBACK_DRYRUN_V1.md",
    "selective_tracking_doc": "docs/architecture/vision/LUNA_SELECTIVE_TRACKING_ADAPTER_POLICY_V1.md",
    "world_observation_entity_feature_doc": "docs/architecture/vision/LUNA_WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY_V1.md",
    "task_aware_visual_focus_doc": "docs/architecture/vision/LUNA_TASK_AWARE_VISUAL_FOCUS_POLICY_V1.md",
    "midplatform_perception_orchestration_doc": "docs/architecture/midplatform/LUNA_MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY_V1.md",
    "basic_navigation_loop_stabilization_doc": "docs/architecture/midplatform/LUNA_BASIC_NAVIGATION_GUIDANCE_LOOP_STABILIZATION_TEST_V1.md",
    "safety_task_arbitration_doc": "docs/architecture/midplatform/LUNA_SAFETY_TASK_ARBITRATION_POLICY_V1.md",
    "minimal_runtime_integration_closure_doc": "docs/architecture/midplatform/LUNA_MINIMAL_RUNTIME_INTEGRATION_CLOSURE_V1.md",
    "ocr_final_closure_doc": "docs/architecture/ocr/LUNA_OCR_MAINLINE_FINAL_CLOSURE_V1.md",
    "ocr_phase_verdict_table": "docs/architecture/evaluation/LUNA_EVALUATION_OCR_PHASE_VERDICT_STATUS_TABLE_V0.md",
}

OPTIONAL_DOCS = {
    "basic_navigation_guidance_loop_dryrun_doc": "docs/architecture/midplatform/LUNA_BASIC_NAVIGATION_GUIDANCE_LOOP_DRYRUN_V1.md",
    "navigation_guidance_to_speech_adapter_doc": "docs/architecture/midplatform/LUNA_NAVIGATION_GUIDANCE_TO_SPEECH_CANDIDATE_ADAPTER_V1.md",
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
    "safety_task_arbitration_runtime_invoked": False,
    "speech_gate_invoked": False,
    "vop_invoked": False,
    "tts_invoked": False,
    "user_heard_assumed": False,
    "task_state_committed_now": False,
    "navigation_action_triggered": False,
    "route_modified": False,
    "scene_delta_generated": False,
    "world_model_written": False,
    "memory_written": False,
    "library_written": False,
    "fact_written": False,
    "entity_resolution_runtime_invoked": False,
    "fact_admission_runtime_invoked": False,
    "memory_consolidation_invoked": False,
    "library_experience_commit_invoked": False,
}

CASE_FIELD_SPECS = [
    {"name": "dryrun_case_id", "type": "string", "required": True},
    {"name": "case_type", "type": "string", "required": True},
    {"name": "source_feedback_case_ref", "type": "string", "required": True},
    {"name": "related_task_id", "type": "string", "required": True},
    {"name": "task_phase", "type": "string", "required": True},
    {"name": "incoming_feedback_candidates", "type": "list", "required": True},
    {"name": "safety_feedback_refs", "type": "list", "required": True},
    {"name": "task_feedback_refs", "type": "list", "required": True},
    {"name": "ocr_activation_feedback_refs", "type": "list", "required": True},
    {"name": "tracking_feedback_refs", "type": "list", "required": True},
    {"name": "map_memory_context_feedback_refs", "type": "list", "required": True},
    {"name": "conflict_correction_feedback_refs", "type": "list", "required": True},
    {"name": "active_view_adjustment_feedback_refs", "type": "list", "required": True},
    {"name": "expected_arbitration_path", "type": "string", "required": True},
    {"name": "expected_guidance_candidate", "type": "string", "required": True},
    {"name": "expected_output_candidate", "type": "string", "required": True},
    {"name": "expected_boundary_flags", "type": "object", "required": True},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

INTAKE_FIELD_SPECS = [
    {"name": "intake_candidate_id", "type": "string", "required": True},
    {"name": "source_dryrun_case_id", "type": "string", "required": True},
    {"name": "feedback_refs", "type": "list", "required": True},
    {"name": "intake_status", "type": "string", "required": True},
    {"name": "accepted_feedback_types", "type": "list", "required": True},
    {"name": "delayed_feedback_types", "type": "list", "required": True},
    {"name": "suppressed_feedback_types", "type": "list", "required": True},
    {"name": "requires_safety_task_arbitration", "type": "boolean", "required": True},
    {"name": "requires_user_confirmation", "type": "boolean", "required": True},
    {"name": "requires_view_adjustment", "type": "boolean", "required": True},
    {"name": "requires_ocr_later", "type": "boolean", "required": True},
    {"name": "requires_tracking_later", "type": "boolean", "required": True},
    {"name": "fact_status", "type": "string", "required": True, "default": "not_fact"},
    {"name": "action_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

GUIDANCE_TYPES = [
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
    "temporary_route_caution_candidate",
    "reobserve_or_confirm_candidate",
]

GUIDANCE_FIELD_SPECS = [
    {"name": "guidance_candidate_id", "type": "string", "required": True},
    {"name": "source_intake_candidate_id", "type": "string", "required": True},
    {"name": "guidance_type", "type": "enum", "required": True},
    {"name": "related_task_id", "type": "string", "required": True},
    {"name": "task_phase", "type": "string", "required": True},
    {"name": "safety_priority", "type": "string", "required": True},
    {"name": "evidence_refs", "type": "list", "required": True},
    {"name": "map_memory_hint_refs", "type": "list", "required": True},
    {"name": "visual_feedback_refs", "type": "list", "required": True},
    {"name": "ocr_feedback_refs", "type": "list", "required": True},
    {"name": "tracking_feedback_refs", "type": "list", "required": True},
    {"name": "confidence", "type": "number", "required": True},
    {"name": "uncertainty", "type": "number", "required": True},
    {"name": "allowed_output_mode", "type": "string", "required": True},
    {"name": "requires_safety_task_arbitration", "type": "boolean", "required": True},
    {"name": "requires_speech_gate", "type": "boolean", "required": True},
    {"name": "action_instruction_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "navigation_action_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "fact_status", "type": "string", "required": True, "default": "not_fact"},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

ARBITRATION_BRIDGE_FIELD_SPECS = [
    {"name": "bridge_candidate_id", "type": "string", "required": True},
    {"name": "source_guidance_candidate_id", "type": "string", "required": True},
    {"name": "safety_feedback_refs", "type": "list", "required": True},
    {"name": "task_feedback_refs", "type": "list", "required": True},
    {"name": "arbitration_priority", "type": "string", "required": True},
    {"name": "suppress_task_guidance", "type": "boolean", "required": True},
    {"name": "delay_task_guidance", "type": "boolean", "required": True},
    {"name": "allow_safety_guidance_candidate", "type": "boolean", "required": True},
    {"name": "requires_confirmation", "type": "boolean", "required": True},
    {"name": "requires_reobserve", "type": "boolean", "required": True},
    {"name": "fact_status", "type": "string", "required": True, "default": "not_fact"},
    {"name": "action_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

OUTPUT_MODES = [
    "TEXT_ONLY_DRY_PREVIEW",
    "STRUCTURED_LOG_ONLY",
    "DRY_SPEECH_PREVIEW",
    "NO_OUTPUT_SUPPRESSED",
    "SAFETY_HOLD_PROMPT_CANDIDATE",
    "ACTIVE_VIEW_ADJUSTMENT_PROMPT_CANDIDATE",
]

OUTPUT_FIELD_SPECS = [
    {"name": "output_candidate_id", "type": "string", "required": True},
    {"name": "source_guidance_candidate_id", "type": "string", "required": True},
    {"name": "output_mode", "type": "enum", "required": True},
    {"name": "user_visible_text_candidate", "type": "string", "required": False},
    {"name": "speech_gate_required", "type": "boolean", "required": True},
    {"name": "speech_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "tts_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "vop_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "user_heard_assumed", "type": "boolean", "required": True, "default": False},
    {"name": "action_instruction_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "fact_status", "type": "string", "required": True, "default": "not_fact"},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

BOUNDARY_DECISION_FIELD_SPECS = [
    {"name": "case_id", "type": "string", "required": True},
    {"name": "intake_boundary_ok", "type": "boolean", "required": True},
    {"name": "arbitration_boundary_ok", "type": "boolean", "required": True},
    {"name": "guidance_boundary_ok", "type": "boolean", "required": True},
    {"name": "output_boundary_ok", "type": "boolean", "required": True},
    {"name": "runtime_boundary_ok", "type": "boolean", "required": True},
    {"name": "write_boundary_ok", "type": "boolean", "required": True},
    {"name": "speech_boundary_ok", "type": "boolean", "required": True},
    {"name": "action_boundary_ok", "type": "boolean", "required": True},
    {"name": "violations", "type": "list", "required": True},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

SCENARIO_ROWS = [
    {
        "scenario_id": "route_walking_clear_path_guidance",
        "source_feedback_case_ref": "navigation_route_walking_clear_path",
        "task_phase": "ROUTE_WALKING",
        "incoming_feedback": ["route_alignment_feedback"],
        "safety_feedback": [],
        "task_feedback": ["route_alignment_feedback"],
        "ocr_feedback": [],
        "tracking_feedback": [],
        "map_memory_feedback": ["route_segment_forward_hint"],
        "conflict_feedback": [],
        "view_adjustment_feedback": [],
        "expected_arbitration_path": "task_guidance_direct_candidate",
        "expected_guidance_candidate": "continue_walking_candidate",
        "expected_output_candidate": "TEXT_ONLY_DRY_PREVIEW",
    },
    {
        "scenario_id": "route_walking_near_field_obstacle",
        "source_feedback_case_ref": "navigation_route_walking_clear_path",
        "task_phase": "ROUTE_WALKING",
        "incoming_feedback": ["near_field_obstacle", "route_alignment_feedback"],
        "safety_feedback": ["near_field_obstacle"],
        "task_feedback": ["route_alignment_feedback"],
        "ocr_feedback": [],
        "tracking_feedback": [],
        "map_memory_feedback": [],
        "conflict_feedback": [],
        "view_adjustment_feedback": [],
        "expected_arbitration_path": "safety_priority_delay_task",
        "expected_guidance_candidate": "slow_down_candidate",
        "expected_output_candidate": "SAFETY_HOLD_PROMPT_CANDIDATE",
    },
    {
        "scenario_id": "approaching_destination_signage_candidate",
        "source_feedback_case_ref": "navigation_approaching_destination_with_signage",
        "task_phase": "APPROACHING_TARGET",
        "incoming_feedback": ["destination_approach_feedback", "ocr_activation_needed"],
        "safety_feedback": [],
        "task_feedback": ["destination_approach_feedback"],
        "ocr_feedback": ["ocr_activation_needed"],
        "tracking_feedback": [],
        "map_memory_feedback": ["destination_nearby_hint"],
        "conflict_feedback": [],
        "view_adjustment_feedback": [],
        "expected_arbitration_path": "task_guidance_plus_ocr_later",
        "expected_guidance_candidate": "destination_approach_hint",
        "expected_output_candidate": "TEXT_ONLY_DRY_PREVIEW",
    },
    {
        "scenario_id": "shop_search_right_side_view_adjustment",
        "source_feedback_case_ref": "shop_search_right_side_storefront",
        "task_phase": "SHOP_SEARCH",
        "incoming_feedback": ["shopfront_search_feedback", "view_adjustment_needed", "ocr_activation_needed"],
        "safety_feedback": [],
        "task_feedback": ["shopfront_search_feedback"],
        "ocr_feedback": ["ocr_activation_needed"],
        "tracking_feedback": [],
        "map_memory_feedback": ["right_side_storefront_hint"],
        "conflict_feedback": [],
        "view_adjustment_feedback": ["center_target"],
        "expected_arbitration_path": "view_adjustment_before_task_confirmation",
        "expected_guidance_candidate": "active_view_adjustment_hint",
        "expected_output_candidate": "ACTIVE_VIEW_ADJUSTMENT_PROMPT_CANDIDATE",
    },
    {
        "scenario_id": "object_search_home_privacy_sensitive",
        "source_feedback_case_ref": "object_search_home_keys",
        "task_phase": "OBJECT_SEARCH",
        "incoming_feedback": ["object_search_feedback"],
        "safety_feedback": [],
        "task_feedback": ["object_search_feedback"],
        "ocr_feedback": [],
        "tracking_feedback": [],
        "map_memory_feedback": ["tabletop_bag_area_hint"],
        "conflict_feedback": [],
        "view_adjustment_feedback": [],
        "expected_arbitration_path": "task_guidance_privacy_preserved",
        "expected_guidance_candidate": "target_search_hint",
        "expected_output_candidate": "TEXT_ONLY_DRY_PREVIEW",
    },
    {
        "scenario_id": "crowded_path_crowd_flow_caution",
        "source_feedback_case_ref": "crowded_path_occluded_surface",
        "task_phase": "ROUTE_WALKING",
        "incoming_feedback": ["route_surface_occluded", "crowd_flow_risk", "tracking_needed"],
        "safety_feedback": ["route_surface_occluded", "crowd_flow_risk"],
        "task_feedback": ["tracking_needed"],
        "ocr_feedback": [],
        "tracking_feedback": ["tracking_needed"],
        "map_memory_feedback": ["crowded_corridor_history_hint"],
        "conflict_feedback": [],
        "view_adjustment_feedback": [],
        "expected_arbitration_path": "safety_priority_crowd_caution",
        "expected_guidance_candidate": "crowd_flow_caution_hint",
        "expected_output_candidate": "TEXT_ONLY_DRY_PREVIEW",
    },
    {
        "scenario_id": "crossing_uncertain_red_green_light",
        "source_feedback_case_ref": "crossing_uncertain_traffic_light",
        "task_phase": "CROSSING_APPROACH",
        "incoming_feedback": ["crossing_uncertain", "traffic_light_uncertain", "tracking_needed"],
        "safety_feedback": ["crossing_uncertain", "traffic_light_uncertain"],
        "task_feedback": ["tracking_needed"],
        "ocr_feedback": [],
        "tracking_feedback": ["tracking_needed"],
        "map_memory_feedback": ["intersection_ahead_hint"],
        "conflict_feedback": [],
        "view_adjustment_feedback": [],
        "expected_arbitration_path": "crossing_uncertain_hold_guidance",
        "expected_guidance_candidate": "crossing_uncertain_hint",
        "expected_output_candidate": "SAFETY_HOLD_PROMPT_CANDIDATE",
    },
    {
        "scenario_id": "visual_map_memory_conflict_navigation",
        "source_feedback_case_ref": "visual_map_memory_conflict",
        "task_phase": "APPROACHING_TARGET",
        "incoming_feedback": ["map_memory_conflict_feedback", "conflict_correction_feedback"],
        "safety_feedback": [],
        "task_feedback": ["map_memory_conflict_feedback"],
        "ocr_feedback": [],
        "tracking_feedback": [],
        "map_memory_feedback": ["map_says_shop_right", "memory_says_previous_left"],
        "conflict_feedback": ["visual_vs_map_vs_memory"],
        "view_adjustment_feedback": [],
        "expected_arbitration_path": "conflict_reobserve_before_guidance",
        "expected_guidance_candidate": "map_visual_conflict_hint",
        "expected_output_candidate": "STRUCTURED_LOG_ONLY",
    },
    {
        "scenario_id": "low_quality_view_hold_still",
        "source_feedback_case_ref": "low_quality_view_requires_hold_still",
        "task_phase": "GENERAL_SCAN",
        "incoming_feedback": ["view_quality_poor", "view_adjustment_needed"],
        "safety_feedback": ["view_quality_poor"],
        "task_feedback": [],
        "ocr_feedback": [],
        "tracking_feedback": [],
        "map_memory_feedback": [],
        "conflict_feedback": [],
        "view_adjustment_feedback": ["hold_still"],
        "expected_arbitration_path": "safety_hold_suppress_task_visual",
        "expected_guidance_candidate": "hold_still_candidate",
        "expected_output_candidate": "ACTIVE_VIEW_ADJUSTMENT_PROMPT_CANDIDATE",
    },
    {
        "scenario_id": "temporary_facility_route_impact",
        "source_feedback_case_ref": "temporary_mobile_vendor_near_route",
        "task_phase": "ROUTE_WALKING",
        "incoming_feedback": ["temporary_facility_task_feedback", "world_observation_handoff_feedback"],
        "safety_feedback": [],
        "task_feedback": ["temporary_facility_task_feedback"],
        "ocr_feedback": [],
        "tracking_feedback": [],
        "map_memory_feedback": ["route_side_activity_hint"],
        "conflict_feedback": [],
        "view_adjustment_feedback": [],
        "expected_arbitration_path": "temporary_route_caution_candidate",
        "expected_guidance_candidate": "temporary_route_caution_candidate",
        "expected_output_candidate": "TEXT_ONLY_DRY_PREVIEW",
    },
    {
        "scenario_id": "tracking_later_needed_dynamic_obstacle",
        "source_feedback_case_ref": "crowded_path_occluded_surface",
        "task_phase": "ROUTE_WALKING",
        "incoming_feedback": ["tracking_needed", "route_alignment_feedback"],
        "safety_feedback": ["near_field_obstacle"],
        "task_feedback": ["tracking_needed"],
        "ocr_feedback": [],
        "tracking_feedback": ["tracking_needed"],
        "map_memory_feedback": ["route_segment_forward_hint"],
        "conflict_feedback": [],
        "view_adjustment_feedback": [],
        "expected_arbitration_path": "tracking_later_without_runtime",
        "expected_guidance_candidate": "tracking_later_needed_hint",
        "expected_output_candidate": "TEXT_ONLY_DRY_PREVIEW",
    },
    {
        "scenario_id": "ocr_later_needed_readable_sign",
        "source_feedback_case_ref": "navigation_approaching_destination_with_signage",
        "task_phase": "APPROACHING_TARGET",
        "incoming_feedback": ["ocr_activation_needed"],
        "safety_feedback": [],
        "task_feedback": [],
        "ocr_feedback": ["ocr_activation_needed"],
        "tracking_feedback": [],
        "map_memory_feedback": ["destination_nearby_hint"],
        "conflict_feedback": [],
        "view_adjustment_feedback": [],
        "expected_arbitration_path": "ocr_later_without_submission",
        "expected_guidance_candidate": "ocr_later_needed_hint",
        "expected_output_candidate": "TEXT_ONLY_DRY_PREVIEW",
    },
]

GOVERNANCE_DEBT_TOPICS = [
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


def _boundary_payload() -> Dict[str, Any]:
    return {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        **BOUNDARY_FALSE_FLAGS,
        "feedback_candidates_require_arbitration": True,
        "speech_allowed_false_until_gate": True,
        "action_allowed_false": True,
        "navigation_action_allowed": False,
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


def _load_optional_json(root_meta: Dict[str, Any], filename: str) -> Dict[str, Any]:
    root = root_meta.get("root")
    path = root / filename if root else None
    if path and path.is_file():
        return _read_json(path)
    return {}


def _task_id(idx: int) -> str:
    return f"nav_task_{idx:02d}"


def _guidance_mode_for_scenario(scenario_id: str) -> str:
    mapping = {
        "route_walking_clear_path_guidance": "TEXT_ONLY_DRY_PREVIEW",
        "route_walking_near_field_obstacle": "SAFETY_HOLD_PROMPT_CANDIDATE",
        "approaching_destination_signage_candidate": "TEXT_ONLY_DRY_PREVIEW",
        "shop_search_right_side_view_adjustment": "ACTIVE_VIEW_ADJUSTMENT_PROMPT_CANDIDATE",
        "object_search_home_privacy_sensitive": "TEXT_ONLY_DRY_PREVIEW",
        "crowded_path_crowd_flow_caution": "TEXT_ONLY_DRY_PREVIEW",
        "crossing_uncertain_red_green_light": "SAFETY_HOLD_PROMPT_CANDIDATE",
        "visual_map_memory_conflict_navigation": "STRUCTURED_LOG_ONLY",
        "low_quality_view_hold_still": "ACTIVE_VIEW_ADJUSTMENT_PROMPT_CANDIDATE",
        "temporary_facility_route_impact": "TEXT_ONLY_DRY_PREVIEW",
        "tracking_later_needed_dynamic_obstacle": "TEXT_ONLY_DRY_PREVIEW",
        "ocr_later_needed_readable_sign": "TEXT_ONLY_DRY_PREVIEW",
    }
    return mapping[scenario_id]


def _guidance_text_for_scenario(scenario_id: str) -> str:
    mapping = {
        "route_walking_clear_path_guidance": "前方路径候选保持清晰，可继续按当前方向谨慎前进。",
        "route_walking_near_field_obstacle": "前方近场存在障碍候选，请先减速并保持保守观察。",
        "approaching_destination_signage_candidate": "接近目标候选，但仍需后续文字确认，暂不判定已到达。",
        "shop_search_right_side_view_adjustment": "右侧店面候选需要进一步观察，请先把视角对准右侧门头。",
        "object_search_home_privacy_sensitive": "优先在记忆提示的桌面和包附近区域继续搜索。",
        "crowded_path_crowd_flow_caution": "前方路径被遮挡且人流复杂，请保持保守通过策略。",
        "crossing_uncertain_red_green_light": "当前过街状态不确定，请先保持等待并继续观察。",
        "visual_map_memory_conflict_navigation": "地图、记忆和当前视觉存在冲突，需要重新观察或进一步确认。",
        "low_quality_view_hold_still": "当前画面质量较差，请先保持不动以稳定视图。",
        "temporary_facility_route_impact": "路线附近存在临时设施候选，请对通过路径保持谨慎。",
        "tracking_later_needed_dynamic_obstacle": "动态障碍仍需后续 tracking 候选支持，当前不启动 runtime。",
        "ocr_later_needed_readable_sign": "该标识适合后续 OCR 候选处理，当前不提交 OCRRequest。",
    }
    return mapping[scenario_id]


def _build_results() -> Dict[str, Any]:
    case_results: List[Dict[str, Any]] = []
    safety_priority_cases = 0
    task_guidance_cases = 0
    active_view_adjustment_cases = 0
    ocr_later_needed_cases = 0
    tracking_later_needed_cases = 0
    map_visual_conflict_cases = 0
    crossing_uncertain_cases = 0

    for idx, row in enumerate(SCENARIO_ROWS, start=1):
        task_id = _task_id(idx)
        case_id = row["scenario_id"]
        intake_candidate_id = f"intake_{idx:02d}"
        guidance_candidate_id = f"guidance_{idx:02d}"

        requires_safety = len(row["safety_feedback"]) > 0
        requires_ocr_later = len(row["ocr_feedback"]) > 0
        requires_tracking_later = len(row["tracking_feedback"]) > 0
        requires_view_adjustment = len(row["view_adjustment_feedback"]) > 0
        requires_user_confirmation = case_id in {"visual_map_memory_conflict_navigation", "crossing_uncertain_red_green_light"}
        delayed_feedback_types = row["task_feedback"] if case_id in {"route_walking_near_field_obstacle", "low_quality_view_hold_still"} else []
        suppressed_feedback_types = row["task_feedback"] if case_id == "low_quality_view_hold_still" else []
        accepted_feedback_types = [*row["safety_feedback"], *row["task_feedback"], *row["ocr_feedback"], *row["tracking_feedback"]]

        dryrun_case = {
            "dryrun_case_id": case_id,
            "case_type": case_id,
            "source_feedback_case_ref": row["source_feedback_case_ref"],
            "related_task_id": task_id,
            "task_phase": row["task_phase"],
            "incoming_feedback_candidates": row["incoming_feedback"],
            "safety_feedback_refs": row["safety_feedback"],
            "task_feedback_refs": row["task_feedback"],
            "ocr_activation_feedback_refs": row["ocr_feedback"],
            "tracking_feedback_refs": row["tracking_feedback"],
            "map_memory_context_feedback_refs": row["map_memory_feedback"],
            "conflict_correction_feedback_refs": row["conflict_feedback"],
            "active_view_adjustment_feedback_refs": row["view_adjustment_feedback"],
            "expected_arbitration_path": row["expected_arbitration_path"],
            "expected_guidance_candidate": row["expected_guidance_candidate"],
            "expected_output_candidate": row["expected_output_candidate"],
            "expected_boundary_flags": {
                "runtime_boundary_ok": True,
                "write_boundary_ok": True,
                "speech_boundary_ok": True,
                "action_boundary_ok": True,
            },
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }

        intake_candidate = {
            "intake_candidate_id": intake_candidate_id,
            "source_dryrun_case_id": case_id,
            "feedback_refs": row["incoming_feedback"],
            "intake_status": "accepted_with_arbitration" if requires_safety or requires_user_confirmation else "accepted_candidate",
            "accepted_feedback_types": accepted_feedback_types,
            "delayed_feedback_types": delayed_feedback_types,
            "suppressed_feedback_types": suppressed_feedback_types,
            "requires_safety_task_arbitration": requires_safety,
            "requires_user_confirmation": requires_user_confirmation,
            "requires_view_adjustment": requires_view_adjustment,
            "requires_ocr_later": requires_ocr_later,
            "requires_tracking_later": requires_tracking_later,
            "fact_status": "not_fact",
            "action_allowed": False,
            "source_chain": SOURCE_CHAIN,
        }

        guidance_candidate = {
            "guidance_candidate_id": guidance_candidate_id,
            "source_intake_candidate_id": intake_candidate_id,
            "guidance_type": row["expected_guidance_candidate"],
            "related_task_id": task_id,
            "task_phase": row["task_phase"],
            "safety_priority": "P0" if requires_safety else "P2",
            "evidence_refs": row["incoming_feedback"],
            "map_memory_hint_refs": row["map_memory_feedback"],
            "visual_feedback_refs": row["task_feedback"],
            "ocr_feedback_refs": row["ocr_feedback"],
            "tracking_feedback_refs": row["tracking_feedback"],
            "confidence": 0.73,
            "uncertainty": 0.18,
            "allowed_output_mode": _guidance_mode_for_scenario(case_id),
            "requires_safety_task_arbitration": requires_safety or case_id in {"visual_map_memory_conflict_navigation", "crossing_uncertain_red_green_light"},
            "requires_speech_gate": True,
            "action_instruction_allowed": False,
            "navigation_action_allowed": False,
            "fact_status": "not_fact",
            "source_chain": SOURCE_CHAIN,
        }

        bridge_candidate = {
            "bridge_candidate_id": f"bridge_{idx:02d}",
            "source_guidance_candidate_id": guidance_candidate_id,
            "safety_feedback_refs": row["safety_feedback"],
            "task_feedback_refs": row["task_feedback"],
            "arbitration_priority": row["expected_arbitration_path"],
            "suppress_task_guidance": case_id in {"low_quality_view_hold_still"},
            "delay_task_guidance": case_id in {"route_walking_near_field_obstacle", "low_quality_view_hold_still"},
            "allow_safety_guidance_candidate": requires_safety,
            "requires_confirmation": requires_user_confirmation,
            "requires_reobserve": case_id in {"visual_map_memory_conflict_navigation", "crossing_uncertain_red_green_light"},
            "fact_status": "not_fact",
            "action_allowed": False,
            "source_chain": SOURCE_CHAIN,
        }

        output_candidate = {
            "output_candidate_id": f"output_{idx:02d}",
            "source_guidance_candidate_id": guidance_candidate_id,
            "output_mode": row["expected_output_candidate"],
            "user_visible_text_candidate": _guidance_text_for_scenario(case_id),
            "speech_gate_required": True,
            "speech_allowed": False,
            "tts_allowed": False,
            "vop_allowed": False,
            "user_heard_assumed": False,
            "action_instruction_allowed": False,
            "fact_status": "not_fact",
            "source_chain": SOURCE_CHAIN,
        }

        boundary_decision = {
            "case_id": case_id,
            "intake_boundary_ok": True,
            "arbitration_boundary_ok": True,
            "guidance_boundary_ok": True,
            "output_boundary_ok": True,
            "runtime_boundary_ok": True,
            "write_boundary_ok": True,
            "speech_boundary_ok": True,
            "action_boundary_ok": True,
            "violations": [],
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }

        if requires_safety:
            safety_priority_cases += 1
        if row["task_feedback"]:
            task_guidance_cases += 1
        if requires_view_adjustment:
            active_view_adjustment_cases += 1
        if requires_ocr_later:
            ocr_later_needed_cases += 1
        if requires_tracking_later:
            tracking_later_needed_cases += 1
        if case_id == "visual_map_memory_conflict_navigation":
            map_visual_conflict_cases += 1
        if case_id == "crossing_uncertain_red_green_light":
            crossing_uncertain_cases += 1

        case_results.append(
            {
                "navigation_vision_strengthening_dryrun_case": dryrun_case,
                "navigation_feedback_intake_candidate": intake_candidate,
                "vision_aware_navigation_guidance_candidate": guidance_candidate,
                "navigation_safety_arbitration_bridge_candidate": bridge_candidate,
                "navigation_output_candidate_dryrun": output_candidate,
                "navigation_vision_strengthening_boundary_decision": boundary_decision,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    return {
        "results_id": f"{POLICY_ID}_dryrun_results",
        "case_results": case_results,
        "case_count": len(case_results),
        "dryrun_results_generated": True,
        "guidance_candidate_count": len(case_results),
        "output_candidate_count": len(case_results),
        "safety_priority_cases_generated": safety_priority_cases > 0,
        "task_guidance_cases_generated": task_guidance_cases > 0,
        "active_view_adjustment_cases_generated": active_view_adjustment_cases > 0,
        "ocr_later_needed_cases_generated": ocr_later_needed_cases > 0,
        "tracking_later_needed_cases_generated": tracking_later_needed_cases > 0,
        "map_visual_conflict_cases_generated": map_visual_conflict_cases > 0,
        "crossing_uncertain_cases_generated": crossing_uncertain_cases > 0,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def run_basic_navigation_loop_vision_strengthening_dryrun_v1(
    *,
    visual_ocr_map_task_feedback_root: str,
    selective_tracking_root: str,
    world_observation_entity_feature_root: str,
    task_aware_visual_focus_root: str,
    midplatform_perception_orchestration_root: str,
    basic_navigation_loop_stabilization_root: str,
    safety_task_arbitration_policy_root: str,
    minimal_runtime_integration_closure_root: str,
    ocr_final_closure_root: str,
    basic_navigation_guidance_loop_dryrun_root: Optional[str] = None,
    navigation_guidance_speech_adapter_root: Optional[str] = None,
    voice_interruption_governance_dryrun_root: Optional[str] = None,
    voice_command_ownership_gate_policy_root: Optional[str] = None,
    text_only_output_post_trial_review_root: Optional[str] = None,
    workspace_root: str = "",
) -> Dict[str, Any]:
    repo_root = Path(__file__).resolve().parents[2]
    workspace = Path(workspace_root).expanduser().resolve() if workspace_root else Path.cwd()

    root_arg_values = {
        "visual_ocr_map_task_feedback_root": visual_ocr_map_task_feedback_root,
        "selective_tracking_root": selective_tracking_root,
        "world_observation_entity_feature_root": world_observation_entity_feature_root,
        "task_aware_visual_focus_root": task_aware_visual_focus_root,
        "midplatform_perception_orchestration_root": midplatform_perception_orchestration_root,
        "basic_navigation_loop_stabilization_root": basic_navigation_loop_stabilization_root,
        "safety_task_arbitration_policy_root": safety_task_arbitration_policy_root,
        "minimal_runtime_integration_closure_root": minimal_runtime_integration_closure_root,
        "ocr_final_closure_root": ocr_final_closure_root,
        "basic_navigation_guidance_loop_dryrun_root": basic_navigation_guidance_loop_dryrun_root,
        "navigation_guidance_speech_adapter_root": navigation_guidance_speech_adapter_root,
        "voice_interruption_governance_dryrun_root": voice_interruption_governance_dryrun_root,
        "voice_command_ownership_gate_policy_root": voice_command_ownership_gate_policy_root,
        "text_only_output_post_trial_review_root": text_only_output_post_trial_review_root,
    }

    all_specs = [*ROOT_INPUT_SPECS, *OPTIONAL_ROOT_SPECS]
    root_meta = {
        spec["intake_id"]: _load_root(root_arg_values[spec["path_arg"]], spec["summary_file"])
        for spec in all_specs
    }

    input_root_rows: List[Dict[str, Any]] = []
    for spec in all_specs:
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

    visual_feedback_summary = _read_json(root_meta["visual_ocr_map_task_feedback"]["summary_path"]) if root_meta["visual_ocr_map_task_feedback"]["summary_path"] else {}
    selective_tracking_summary = _read_json(root_meta["selective_tracking"]["summary_path"]) if root_meta["selective_tracking"]["summary_path"] else {}
    worldobs_summary = _read_json(root_meta["world_observation_entity_feature"]["summary_path"]) if root_meta["world_observation_entity_feature"]["summary_path"] else {}
    visual_focus_summary = _read_json(root_meta["task_aware_visual_focus"]["summary_path"]) if root_meta["task_aware_visual_focus"]["summary_path"] else {}
    midplatform_summary = _read_json(root_meta["midplatform_perception_orchestration"]["summary_path"]) if root_meta["midplatform_perception_orchestration"]["summary_path"] else {}
    basic_nav_stabilization_summary = _read_json(root_meta["basic_navigation_loop_stabilization"]["summary_path"]) if root_meta["basic_navigation_loop_stabilization"]["summary_path"] else {}
    safety_arbitration_summary = _read_json(root_meta["safety_task_arbitration_policy"]["summary_path"]) if root_meta["safety_task_arbitration_policy"]["summary_path"] else {}
    minimal_runtime_summary = _read_json(root_meta["minimal_runtime_integration_closure"]["summary_path"]) if root_meta["minimal_runtime_integration_closure"]["summary_path"] else {}
    ocr_summary = _read_json(root_meta["ocr_final_closure"]["summary_path"]) if root_meta["ocr_final_closure"]["summary_path"] else {}
    basic_nav_dryrun_summary = _read_json(root_meta["basic_navigation_guidance_loop_dryrun"]["summary_path"]) if root_meta["basic_navigation_guidance_loop_dryrun"]["summary_path"] else {}
    voice_interrupt_summary = _read_json(root_meta["voice_interruption_governance_dryrun"]["summary_path"]) if root_meta["voice_interruption_governance_dryrun"]["summary_path"] else {}
    voice_ownership_summary = _read_json(root_meta["voice_command_ownership_gate_policy"]["summary_path"]) if root_meta["voice_command_ownership_gate_policy"]["summary_path"] else {}
    text_only_summary = _read_json(root_meta["text_only_output_post_trial_review"]["summary_path"]) if root_meta["text_only_output_post_trial_review"]["summary_path"] else {}

    visual_ocr_map_task_feedback_input_loaded = (
        root_meta["visual_ocr_map_task_feedback"]["loaded"]
        and visual_feedback_summary.get("final_decision") == VISUAL_FEEDBACK_FINAL_DECISION
        and visual_feedback_summary.get("feedback_candidate_count", 0) >= 10
    )
    selective_tracking_input_loaded = (
        root_meta["selective_tracking"]["loaded"]
        and selective_tracking_summary.get("final_decision") == SELECTIVE_TRACKING_FINAL_DECISION
        and selective_tracking_summary.get("tracking_request_candidate_only") is True
    )
    world_observation_entity_feature_input_loaded = (
        root_meta["world_observation_entity_feature"]["loaded"]
        and worldobs_summary.get("final_decision") == WORLDOBS_FINAL_DECISION
        and worldobs_summary.get("worldmodel_handoff_candidate_allowed") is True
    )
    task_aware_visual_focus_input_loaded = (
        root_meta["task_aware_visual_focus"]["loaded"]
        and visual_focus_summary.get("final_decision") == VISUAL_FOCUS_FINAL_DECISION
        and visual_focus_summary.get("focus_to_tracking_request_policy_defined") is True
    )
    midplatform_perception_orchestration_input_loaded = (
        root_meta["midplatform_perception_orchestration"]["loaded"]
        and midplatform_summary.get("final_decision") == MIDPLATFORM_FINAL_DECISION
        and midplatform_summary.get("map_memory_context_hint_policy_defined") is True
    )
    basic_navigation_loop_stabilization_input_loaded = (
        root_meta["basic_navigation_loop_stabilization"]["loaded"]
        and basic_nav_stabilization_summary.get("final_decision") == BASIC_NAV_STABILIZATION_FINAL_DECISION
        and basic_nav_stabilization_summary.get("boundary_ok") is True
    )
    safety_task_arbitration_policy_input_loaded = (
        root_meta["safety_task_arbitration_policy"]["loaded"]
        and safety_arbitration_summary.get("phase") == "Safety-Task-Arbitration-Policy-v1-001"
        and safety_arbitration_summary.get("arbitration_schema_defined") is True
        and safety_arbitration_summary.get("baseline_safety_loop_supported") is True
    )
    minimal_runtime_integration_closure_loaded = (
        root_meta["minimal_runtime_integration_closure"]["loaded"]
        and minimal_runtime_summary.get("final_decision") == MRI_FINAL_DECISION
    )
    ocr_final_closure_loaded = (
        root_meta["ocr_final_closure"]["loaded"]
        and ocr_summary.get("final_decision") == OCR_FINAL_DECISION
    )

    dryrun_case_schema = _schema_payload(
        f"{POLICY_ID}_dryrun_case",
        "NavigationVisionStrengtheningDryRunCase",
        CASE_FIELD_SPECS,
        scenario_ids=[row["scenario_id"] for row in SCENARIO_ROWS],
    )
    navigation_feedback_intake_candidate_schema = _schema_payload(
        f"{POLICY_ID}_feedback_intake",
        "NavigationFeedbackIntakeCandidate",
        INTAKE_FIELD_SPECS,
        action_allowed_false=True,
    )
    vision_aware_navigation_guidance_candidate_schema = _schema_payload(
        f"{POLICY_ID}_guidance_candidate",
        "VisionAwareNavigationGuidanceCandidate",
        GUIDANCE_FIELD_SPECS,
        guidance_types=GUIDANCE_TYPES,
        speech_allowed_false_until_gate=True,
        navigation_action_allowed=False,
    )
    navigation_safety_arbitration_bridge_candidate_schema = _schema_payload(
        f"{POLICY_ID}_arbitration_bridge",
        "NavigationSafetyArbitrationBridgeCandidate",
        ARBITRATION_BRIDGE_FIELD_SPECS,
        action_allowed_false=True,
    )
    navigation_output_candidate_dryrun_schema = _schema_payload(
        f"{POLICY_ID}_output_candidate",
        "NavigationOutputCandidateDryRun",
        OUTPUT_FIELD_SPECS,
        output_modes=OUTPUT_MODES,
        speech_allowed_false_until_gate=True,
        tts_allowed=False,
        vop_allowed=False,
        user_heard_assumed=False,
        action_instruction_allowed=False,
    )
    boundary_decision_schema = _schema_payload(
        f"{POLICY_ID}_boundary_decision",
        "NavigationVisionStrengtheningBoundaryDecision",
        BOUNDARY_DECISION_FIELD_SPECS,
        all_boundary_dimensions_defined=True,
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

    dryrun_results = _build_results()

    boundary = _boundary_payload()
    navigation_loop_vision_strengthening_boundary_matrix = {
        "matrix_id": f"{POLICY_ID}_boundary_matrix",
        "feedback_candidates_require_arbitration": True,
        "speech_allowed_false_until_gate": True,
        "action_allowed_false": True,
        "navigation_action_allowed": False,
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
                "deferred_reason": "先完成视觉增强导航闭环 dry-run，再进入 post-dryrun review 做收口与裁剪。",
                "future_owner_phase": "Basic Navigation Loop Vision Strengthening Post-DryRun Review",
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
        "reason": "第一轮视觉增强导航闭环 dry-run 已完成，下一阶段应只做 Post-DryRun Review，不进入 runtime。",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "visual_ocr_map_task_feedback_input_loaded": visual_ocr_map_task_feedback_input_loaded,
        "selective_tracking_input_loaded": selective_tracking_input_loaded,
        "world_observation_entity_feature_input_loaded": world_observation_entity_feature_input_loaded,
        "task_aware_visual_focus_input_loaded": task_aware_visual_focus_input_loaded,
        "midplatform_perception_orchestration_input_loaded": midplatform_perception_orchestration_input_loaded,
        "basic_navigation_loop_stabilization_input_loaded": basic_navigation_loop_stabilization_input_loaded,
        "safety_task_arbitration_policy_input_loaded": safety_task_arbitration_policy_input_loaded,
        "minimal_runtime_integration_closure_loaded": minimal_runtime_integration_closure_loaded,
        "ocr_final_closure_loaded": ocr_final_closure_loaded,
        "navigation_vision_strengthening_dryrun_case_schema_defined": True,
        "navigation_feedback_intake_candidate_schema_defined": True,
        "vision_aware_navigation_guidance_candidate_schema_defined": True,
        "navigation_safety_arbitration_bridge_candidate_schema_defined": True,
        "navigation_output_candidate_dryrun_schema_defined": True,
        "boundary_decision_schema_defined": True,
        "scenario_matrix_generated": True,
        "scenario_count": len(SCENARIO_ROWS),
        "dryrun_results_generated": True,
        "guidance_candidate_count": dryrun_results["guidance_candidate_count"],
        "output_candidate_count": dryrun_results["output_candidate_count"],
        "safety_priority_cases_generated": dryrun_results["safety_priority_cases_generated"],
        "task_guidance_cases_generated": dryrun_results["task_guidance_cases_generated"],
        "active_view_adjustment_cases_generated": dryrun_results["active_view_adjustment_cases_generated"],
        "ocr_later_needed_cases_generated": dryrun_results["ocr_later_needed_cases_generated"],
        "tracking_later_needed_cases_generated": dryrun_results["tracking_later_needed_cases_generated"],
        "map_visual_conflict_cases_generated": dryrun_results["map_visual_conflict_cases_generated"],
        "crossing_uncertain_cases_generated": dryrun_results["crossing_uncertain_cases_generated"],
        "feedback_candidates_require_arbitration": True,
        "speech_allowed_false_until_gate": True,
        "action_allowed_false": True,
        "navigation_action_allowed": False,
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
        "navigation_vision_strengthening_dryrun_case_schema": dryrun_case_schema,
        "navigation_feedback_intake_candidate_schema": navigation_feedback_intake_candidate_schema,
        "vision_aware_navigation_guidance_candidate_schema": vision_aware_navigation_guidance_candidate_schema,
        "navigation_safety_arbitration_bridge_candidate_schema": navigation_safety_arbitration_bridge_candidate_schema,
        "navigation_output_candidate_dryrun_schema": navigation_output_candidate_dryrun_schema,
        "navigation_vision_strengthening_boundary_decision_schema": boundary_decision_schema,
        "navigation_loop_vision_strengthening_scenario_matrix": scenario_matrix,
        "navigation_loop_vision_strengthening_dryrun_results": dryrun_results,
        "navigation_loop_vision_strengthening_boundary_matrix": navigation_loop_vision_strengthening_boundary_matrix,
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_runtime_boundary_report": boundary,
        "no_write_boundary_report": boundary,
        "debug_refs": {
            "visual_feedback_final_decision": visual_feedback_summary.get("final_decision"),
            "selective_tracking_final_decision": selective_tracking_summary.get("final_decision"),
            "worldobs_final_decision": worldobs_summary.get("final_decision"),
            "visual_focus_final_decision": visual_focus_summary.get("final_decision"),
            "midplatform_final_decision": midplatform_summary.get("final_decision"),
            "basic_nav_stabilization_final_decision": basic_nav_stabilization_summary.get("final_decision"),
            "safety_arbitration_policy_scope": safety_arbitration_summary.get("policy_scope"),
            "basic_nav_dryrun_loaded": bool(basic_nav_dryrun_summary.get("phase")),
            "voice_interrupt_loaded": bool(voice_interrupt_summary.get("phase")),
            "voice_ownership_loaded": bool(voice_ownership_summary.get("phase")),
            "text_only_post_review_loaded": bool(text_only_summary.get("phase")),
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
