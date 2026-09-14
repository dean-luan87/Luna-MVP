# -*- coding: utf-8 -*-
"""Selective Tracking Adapter Policy v1.

Phase-Selective-Tracking-Adapter-Policy-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Selective-Tracking-Adapter-Policy-v1-001"
POLICY_ID = "stap_v1_001"
POLICY_SCOPE = "selective_tracking_adapter_policy_only"
SOURCE_CHAIN = "selective_tracking_adapter_policy_v1"
FINAL_DECISION = "SELECTIVE_TRACKING_ADAPTER_POLICY_READY_FOR_VISUAL_OCR_MAP_TASK_FEEDBACK_DRYRUN"
NEXT_PHASE = "Phase-Visual-OCR-Map-Task-Feedback-DryRun-v1-001"
WORLDOBS_FINAL_DECISION = "WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY_READY_FOR_SELECTIVE_TRACKING_ADAPTER_POLICY"
VISUAL_FOCUS_FINAL_DECISION = "TASK_AWARE_VISUAL_FOCUS_POLICY_READY_FOR_WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY"
MIDPLATFORM_FINAL_DECISION = "MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY_READY_FOR_TASK_AWARE_VISUAL_FOCUS_POLICY"
PLANNING_FINAL_DECISION = "RETURN_TO_VISION_MAINLINE_PLANNING_READY_FOR_MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY"
PREPLAN_READY_FLAG = "preplan_ready_for_formal_phase_decision"
OCR_FINAL_DECISION = "OCR_MAINLINE_FINAL_CLOSURE_RETURN_TO_VISION_MAINLINE"
MRI_FINAL_DECISION = "MINIMAL_RUNTIME_INTEGRATION_CLOSED_RETURN_TO_VISION_MAINLINE"

ROOT_INPUT_SPECS = [
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
            "focus_to_tracking_request_policy.json",
            "visual_observation_lifecycle_policy.json",
            "visual_focus_feedback_policy.json",
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
    "optical_flow_motion_reuse_review": "docs/architecture/vision/LUNA_OPTICAL_FLOW_MOTION_REUSE_REVIEW_V0.md",
    "vision_frame_trace_stream_registry": "docs/architecture/vision/LUNA_VISION_FRAME_TRACE_STREAM_REGISTRY_V0.md",
    "vision_frame_input_governance": "docs/architecture/vision/LUNA_VISION_FRAME_INPUT_GOVERNANCE_V0.md",
    "vision_roi_proposal_stub": "docs/architecture/vision/LUNA_VISION_FRAME_ROI_PROPOSAL_AND_SEGMENTATION_STUB_V0.md",
    "vision_recognition_evidence_pack": "docs/architecture/vision/LUNA_VISION_RECOGNITION_EVIDENCE_PACK_V0.md",
    "stc_sampling_guidance_policy": "docs/architecture/midplatform/LUNA_STC_SAMPLING_GUIDANCE_POLICY_V1.md",
    "safety_task_arbitration_policy": "docs/architecture/evaluation/LUNA_EVALUATION_SAFETY_TASK_ARBITRATION_POLICY_V1.md",
    "system_health_center_governance": "docs/architecture/evaluation/LUNA_EVALUATION_SYSTEM_HEALTH_CENTER_GOVERNANCE_V0.md",
    "hardware_profile_capability_registry": "docs/architecture/evaluation/LUNA_EVALUATION_HARDWARE_PROFILE_CAPABILITY_REGISTRY_V1.md",
    "ocr_activation_governance_policy": "docs/architecture/midplatform/LUNA_OCR_ACTIVATION_GOVERNANCE_POLICY_V1.md",
    "map_anchor_evidence_schema": "docs/architecture/LUNA_MAP_ANCHOR_EVIDENCE_SCHEMA_V0.md",
    "map_anchor_trust_policy": "docs/architecture/LUNA_MAP_ANCHOR_TRUST_AND_WRITE_READINESS_POLICY_V0.md",
    "worldmodel_unresolved_observation_slot_contract": "docs/architecture/midplatform/LUNA_WORLDMODEL_UNRESOLVED_OBSERVATION_SLOT_CONTRACT_V0.md",
    "worldmodel_lookup_for_reading_framework": "docs/architecture/evaluation/LUNA_EVALUATION_WORLDMODEL_LOOKUP_FOR_READING_FRAMEWORK_V1.md",
    "confirmed_text_evidence_memory_governance_contract": "docs/architecture/evaluation/LUNA_EVALUATION_CONFIRMED_TEXT_EVIDENCE_MEMORY_GOVERNANCE_CONTRACT_V1.md",
}

BOUNDARY_FALSE_FLAGS = {
    "no_runtime_executed": True,
    "no_new_runtime_enabled": True,
    "tracking_runtime_enabled": False,
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
    "sort_invoked": False,
    "botsort_invoked": False,
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
}

ALLOWED_FOCUS_SLOT_TYPES = [
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
]

FORBIDDEN_TRACKING_MODES = [
    "full_scene_tracking",
    "all_moving_objects_tracking",
    "all_person_tracking",
    "all_vehicle_tracking",
    "all_background_motion_tracking",
    "curiosity_only_tracking",
    "emotional_interest_only_tracking",
]

REQUESTED_TARGET_TYPES = [
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
]

TRACKING_REQUEST_FIELD_SPECS = [
    {"name": "tracking_request_candidate_id", "type": "string", "required": True},
    {"name": "source_work_order_id", "type": "string", "required": True},
    {"name": "source_visual_focus_plan_id", "type": "string", "required": True},
    {"name": "source_focus_slot_id", "type": "string", "required": True},
    {"name": "requested_target_type", "type": "enum", "required": True},
    {"name": "requested_tracking_reason", "type": "string", "required": True},
    {"name": "priority", "type": "string", "required": True},
    {"name": "task_relevance", "type": "number", "required": True},
    {"name": "safety_relevance", "type": "number", "required": True},
    {"name": "route_relevance", "type": "number", "required": True},
    {"name": "map_memory_relevance", "type": "number", "required": True},
    {"name": "allowed_adapter_candidates", "type": "list", "required": True},
    {"name": "max_duration", "type": "string", "required": True},
    {"name": "max_tracklets", "type": "number", "required": True},
    {"name": "freshness_requirement", "type": "string", "required": True},
    {"name": "ttl_policy_ref", "type": "string", "required": True},
    {"name": "privacy_filter_required", "type": "boolean", "required": True},
    {"name": "budget_ref", "type": "string", "required": True},
    {"name": "approval_status", "type": "string", "required": True, "default": "not_approved"},
    {"name": "runtime_invocation_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "fact_status", "type": "string", "required": True, "default": "not_fact"},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

TRACK_STATES = [
    "active_candidate",
    "tentative_candidate",
    "lost_candidate",
    "stale_candidate",
    "expired_candidate",
    "archived_candidate",
    "rejected_candidate",
]

TRACKLET_FIELD_SPECS = [
    {"name": "tracklet_candidate_id", "type": "string", "required": True},
    {"name": "source_tracking_request_candidate_id", "type": "string", "required": True},
    {"name": "target_type", "type": "string", "required": True},
    {"name": "target_candidate_ref", "type": "string", "required": False},
    {"name": "track_state", "type": "enum", "required": True},
    {"name": "temporal_span_candidate", "type": "string", "required": True},
    {"name": "spatial_path_candidate", "type": "string", "required": True},
    {"name": "motion_state_candidate", "type": "string", "required": True},
    {"name": "relative_position_candidate", "type": "string", "required": True},
    {"name": "approach_or_departure_candidate", "type": "string", "required": True},
    {"name": "occlusion_status_candidate", "type": "string", "required": True},
    {"name": "stability_score_candidate", "type": "number", "required": True},
    {"name": "confidence", "type": "number", "required": True},
    {"name": "freshness_status", "type": "string", "required": True},
    {"name": "ttl_policy_ref", "type": "string", "required": True},
    {"name": "privacy_tags", "type": "list", "required": True},
    {"name": "current_action_allowed", "type": "boolean", "required": True, "default": False},
    {"name": "feedback_allowed_candidate", "type": "boolean", "required": True},
    {"name": "archive_allowed_candidate", "type": "boolean", "required": True},
    {"name": "worldmodel_handoff_allowed_candidate", "type": "boolean", "required": True, "default": False},
    {"name": "fact_status", "type": "string", "required": True, "default": "not_fact"},
    {"name": "source_chain", "type": "string", "required": True, "default": SOURCE_CHAIN},
]

ALLOWED_TRACKING_TARGETS = [
    "P0 safety target",
    "task-relevant target",
    "route-relevant target",
    "user-feedback target",
    "crossing / traffic safety target",
    "destination confirmation target",
    "temporary facility only if task/safety relevant",
    "world observation target only under low-frequency budget",
]

FORBIDDEN_TRACKING_TARGETS = [
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
]

TRACKING_ADAPTER_CANDIDATES = [
    {
        "adapter_name": "Supervision candidate",
        "adapter_type": "external_tracking_framework",
        "possible_use": "future Detections / tracker bridge candidate",
        "maturity_hint": "reference_only",
        "license_review_required": True,
        "privacy_review_required": True,
        "performance_budget_required": True,
    },
    {
        "adapter_name": "ByteTrack candidate",
        "adapter_type": "multi_object_tracker",
        "possible_use": "future dynamic obstacle / pedestrian / vehicle tracking candidate",
        "maturity_hint": "reference_only",
        "license_review_required": True,
        "privacy_review_required": True,
        "performance_budget_required": True,
    },
    {
        "adapter_name": "OC-SORT candidate",
        "adapter_type": "multi_object_tracker",
        "possible_use": "future occlusion-aware tracking candidate",
        "maturity_hint": "reference_only",
        "license_review_required": True,
        "privacy_review_required": True,
        "performance_budget_required": True,
    },
    {
        "adapter_name": "SORT candidate",
        "adapter_type": "baseline_tracker",
        "possible_use": "future minimal tracklet baseline candidate",
        "maturity_hint": "reference_only",
        "license_review_required": True,
        "privacy_review_required": True,
        "performance_budget_required": True,
    },
    {
        "adapter_name": "BoT-SORT candidate",
        "adapter_type": "multi_object_tracker",
        "possible_use": "future stronger occlusion / re-id aware tracking candidate",
        "maturity_hint": "reference_only",
        "license_review_required": True,
        "privacy_review_required": True,
        "performance_budget_required": True,
    },
    {
        "adapter_name": "Optical Flow candidate",
        "adapter_type": "motion_estimation",
        "possible_use": "future short-term motion / path continuity hint candidate",
        "maturity_hint": "reference_only",
        "license_review_required": False,
        "privacy_review_required": True,
        "performance_budget_required": True,
    },
    {
        "adapter_name": "Frame-diff / motion-score candidate",
        "adapter_type": "lightweight_motion_stub",
        "possible_use": "future low-cost motion change hint candidate",
        "maturity_hint": "reference_only",
        "license_review_required": False,
        "privacy_review_required": True,
        "performance_budget_required": True,
    },
    {
        "adapter_name": "Tracklet stability evaluator candidate",
        "adapter_type": "track_quality_evaluator",
        "possible_use": "future tracklet confidence / stability scoring candidate",
        "maturity_hint": "reference_only",
        "license_review_required": False,
        "privacy_review_required": True,
        "performance_budget_required": True,
    },
]

TRACKING_LIFECYCLE_STATES = [
    "requested",
    "admitted_candidate",
    "active_candidate",
    "tentative_candidate",
    "lost_candidate",
    "stale_candidate",
    "expired_candidate",
    "archived_candidate",
    "rejected_candidate",
]

SCENARIO_ROWS = [
    {
        "scenario_id": "route_surface_tracking_candidate",
        "focus": "路面/可行走路径追踪候选",
        "direct_navigation_allowed": False,
    },
    {
        "scenario_id": "near_field_obstacle_tracking_candidate",
        "focus": "近场障碍安全追踪候选",
        "safety_arbitration_required": True,
    },
    {
        "scenario_id": "pedestrian_approach_safety_candidate",
        "focus": "行人靠近风险",
        "identity_recognition_allowed": False,
    },
    {
        "scenario_id": "vehicle_approach_safety_candidate",
        "focus": "车辆靠近风险",
        "license_plate_recognition_allowed": False,
    },
    {
        "scenario_id": "crowded_path_occluded_surface",
        "focus": "路面遮挡",
        "crowd_flow_fallback_candidate": True,
        "follow_crowd_action_allowed": False,
    },
    {
        "scenario_id": "traffic_light_state_tracking_candidate",
        "focus": "红绿灯变化追踪候选",
        "crossing_action_allowed": False,
    },
    {
        "scenario_id": "shopfront_tracking_for_target_confirmation",
        "focus": "商铺门头/入口作为目标确认追踪候选",
        "ocr_followup_placeholder_allowed": True,
    },
    {
        "scenario_id": "temporary_facility_tracking_candidate",
        "focus": "临时摊位/施工/排队点追踪候选",
        "ttl_required": True,
        "fixed_poi_write_allowed": False,
    },
    {
        "scenario_id": "user_feedback_target_tracking_candidate",
        "focus": "用户说“右边那个”后的 focus slot 调整追踪候选",
        "focus_slot_adjustment_required": True,
    },
    {
        "scenario_id": "low_value_background_tracking_rejected",
        "focus": "背景行人/远处车/低价值移动物体",
        "rejected": True,
        "admission_allowed": False,
    },
]

GOVERNANCE_DEBT_TOPICS = [
    "tracking admission arbitration complexity",
    "tracking budget preemption governance complexity",
    "road surface fallback governance complexity",
    "crowd flow conservative output governance complexity",
    "crossing tracking escalation governance complexity",
    "external tracking adapter review governance complexity",
    "tracking lifecycle archival governance complexity",
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
        "tracking_authority_owner": "MidPlatform",
        "full_scene_tracking_allowed": False,
        "all_moving_objects_tracking_allowed": False,
        "all_person_tracking_allowed": False,
        "all_vehicle_tracking_allowed": False,
        "crowd_flow_follow_action_allowed": False,
        "traffic_light_crossing_action_allowed": False,
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


def run_selective_tracking_adapter_policy_v1(
    *,
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

    worldobs_summary = _read_json(root_meta["world_observation_entity_feature"]["summary_path"]) if root_meta["world_observation_entity_feature"]["summary_path"] else {}
    visual_focus_summary = _read_json(root_meta["task_aware_visual_focus"]["summary_path"]) if root_meta["task_aware_visual_focus"]["summary_path"] else {}
    midplatform_summary = _read_json(root_meta["midplatform_perception_orchestration"]["summary_path"]) if root_meta["midplatform_perception_orchestration"]["summary_path"] else {}
    planning_summary = _read_json(root_meta["return_to_vision_planning"]["summary_path"]) if root_meta["return_to_vision_planning"]["summary_path"] else {}
    preplan_summary = _read_json(root_meta["preplan_input"]["summary_path"]) if root_meta["preplan_input"]["summary_path"] else {}
    ocr_summary = _read_json(root_meta["ocr_final_closure"]["summary_path"]) if root_meta["ocr_final_closure"]["summary_path"] else {}
    mri_summary = _read_json(root_meta["minimal_runtime_integration_closure"]["summary_path"]) if root_meta["minimal_runtime_integration_closure"]["summary_path"] else {}

    worldobs_placeholder = _load_optional_json(root_meta["world_observation_entity_feature"], "worldmodel_memory_library_placeholder_policy.json")
    visual_focus_lifecycle = _load_optional_json(root_meta["task_aware_visual_focus"], "visual_observation_lifecycle_policy.json")
    midplatform_boundary = _load_optional_json(root_meta["midplatform_perception_orchestration"], "worldmodel_memory_library_handoff_boundary.json")
    planning_boundary = _load_optional_json(root_meta["return_to_vision_planning"], "deferred_worldmodel_memory_library_boundary.json")
    preplan_boundary = _load_optional_json(root_meta["preplan_input"], "deferred_worldmodel_memory_library_boundary.json")

    world_observation_entity_feature_input_loaded = (
        root_meta["world_observation_entity_feature"]["loaded"]
        and worldobs_summary.get("final_decision") == WORLDOBS_FINAL_DECISION
        and worldobs_summary.get("worldmodel_handoff_candidate_allowed") is True
    )
    task_aware_visual_focus_input_loaded = (
        root_meta["task_aware_visual_focus"]["loaded"]
        and visual_focus_summary.get("final_decision") == VISUAL_FOCUS_FINAL_DECISION
        and visual_focus_summary.get("tracking_request_candidate_only") is True
    )
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

    selective_tracking_adapter_policy = {
        "policy_id": f"{POLICY_ID}_selective_tracking_adapter",
        "scope": "approved_focus_slot_tracking_candidate_layer",
        "tracking_authority_owner": "MidPlatform",
        "allowed_tracking_sources": [
            "approved MidPlatformPerceptionWorkOrder",
            "approved VisualFocusSlot",
            "task/safety relevant feedback target",
            "temporary facility candidate under explicit budget",
        ],
        "allowed_focus_slot_types": ALLOWED_FOCUS_SLOT_TYPES,
        "forbidden_tracking_modes": FORBIDDEN_TRACKING_MODES,
        "adapter_candidate_registry": "tracking_adapter_candidate_registry.json",
        "tracking_budget_policy_ref": "tracking_budget_policy.json",
        "lifecycle_policy_ref": "tracking_lifecycle_policy.json",
        "arbitration_handoff_policy_ref": "tracking_feedback_policy.json",
        "no_runtime_boundary_ref": "no_runtime_boundary_report.json",
        "no_write_boundary_ref": "no_write_boundary_report.json",
        "tracking_authority_belongs_to_midplatform": True,
        "vision_module_cannot_start_tracking_by_itself": True,
        "detector_cannot_start_tracking_by_itself": True,
        "adapter_cannot_start_tracking_by_itself": True,
        "tracking_requires_approved_visual_focus_slot": True,
        "tracking_requires_midplatform_resource_budget": True,
        "tracking_requires_safety_or_task_relevance": True,
        "tracking_result_candidate_only": True,
        "tracking_result_cannot_directly_trigger_navigation_action": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    tracking_request_candidate_schema = {
        "schema_id": f"{POLICY_ID}_tracking_request_candidate",
        "object_name": "TrackingRequestCandidate",
        "requested_target_types": REQUESTED_TARGET_TYPES,
        "fields": TRACKING_REQUEST_FIELD_SPECS,
        "field_count": len(TRACKING_REQUEST_FIELD_SPECS),
        "non_claims": [
            "TrackingRequestCandidate 不是 runtime invocation。",
            "TrackingRequestCandidate 不等于 tracking 已批准。",
            "TrackingRequestCandidate 不等于导航动作。",
            "TrackingRequestCandidate 不是事实。",
        ],
        "tracking_request_candidate_only": True,
        "runtime_invocation_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    tracklet_candidate_schema = {
        "schema_id": f"{POLICY_ID}_tracklet_candidate",
        "object_name": "TrackletCandidate",
        "track_states": TRACK_STATES,
        "fields": TRACKLET_FIELD_SPECS,
        "field_count": len(TRACKLET_FIELD_SPECS),
        "tracklet_candidate_not_fact": True,
        "current_action_allowed": False,
        "worldmodel_handoff_allowed_candidate_default": False,
        "non_claims": [
            "TrackletCandidate 不等于实时 tracking runtime 输出。",
            "TrackletCandidate 不等于动作指令。",
            "TrackletCandidate 不等于身份事实。",
            "TrackletCandidate 不直接写 WorldModel / Memory / Library。",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    tracking_budget_policy = {
        "tracking_budget_policy_id": f"{POLICY_ID}_tracking_budget",
        "source_resource_budget_ref": "MidPlatformResourceBudgetPolicy",
        "safety_reserved_tracklets": 3,
        "primary_task_tracklets": 3,
        "secondary_task_tracklets": 1,
        "background_observation_tracklets": 0,
        "max_active_tracklets_total": 6,
        "max_tracklets_per_focus_slot": 2,
        "max_track_duration": "short_window_only",
        "max_lost_duration": "brief_recovery_window_only",
        "max_log_events_per_window": 8,
        "drop_low_value_tracklets": True,
        "preempt_by_safety": True,
        "degrade_on_low_hardware_health": True,
        "principles": [
            "P0 safety tracklet budget reserved。",
            "primary task over secondary task。",
            "secondary task cannot consume safety budget。",
            "background world observation tracking limited or disabled。",
            "low-value tracklets dropped。",
            "high privacy low task-value tracklets suppressed。",
            "no unbounded tracking logs。",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    tracking_target_admission_policy = {
        "policy_id": f"{POLICY_ID}_tracking_target_admission",
        "allowed_tracking_targets": ALLOWED_TRACKING_TARGETS,
        "forbidden_tracking_targets": FORBIDDEN_TRACKING_TARGETS,
        "requires_source_chain": True,
        "requires_privacy_filtering": True,
        "requires_midplatform_approval": True,
        "requires_budget": True,
        "full_scene_tracking_allowed": False,
        "all_moving_objects_tracking_allowed": False,
        "all_person_tracking_allowed": False,
        "all_vehicle_tracking_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    road_surface_tracking_policy = {
        "policy_id": f"{POLICY_ID}_road_surface_tracking",
        "covered_candidates": [
            "walkable_surface tracking candidate",
            "road_surface candidate",
            "route_direction candidate",
            "sidewalk_boundary candidate",
            "curb / step candidate",
            "crossing surface candidate",
            "path_continuity candidate",
        ],
        "principles": [
            "路面/可通行路径优先级高于普通对象。",
            "路面不稳定时降级为 route_path_focus + active view adjustment。",
            "路面被人群遮挡时可请求 crowd_flow fallback candidate。",
            "路面追踪结果不得直接导航。",
            "必须进入 Safety/Task arbitration。",
        ],
        "route_surface_direct_navigation_allowed": False,
        "crowd_flow_fallback_allowed": True,
        "arbitration_required": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    pedestrian_vehicle_tracking_policy = {
        "policy_id": f"{POLICY_ID}_pedestrian_vehicle_tracking",
        "covered_candidates": [
            "pedestrian_approach_candidate",
            "vehicle_approach_candidate",
            "bike_or_e_scooter_candidate",
            "crossing_conflict_candidate",
            "near_field_dynamic_obstacle_candidate",
        ],
        "principles": [
            "只追踪与安全/路线/任务相关者。",
            "不追踪所有行人。",
            "不追踪所有车辆。",
            "陌生人身份不识别。",
            "车牌不识别。",
            "只保留运动/风险/空间关系候选。",
            "不写身份事实。",
        ],
        "all_person_tracking_allowed": False,
        "all_vehicle_tracking_allowed": False,
        "identity_recognition_allowed": False,
        "license_plate_recognition_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    crowd_flow_tracking_policy = {
        "policy_id": f"{POLICY_ID}_crowd_flow_tracking",
        "covered_candidates": [
            "crowd_flow_candidate",
            "pedestrian_flow_direction_candidate",
            "crowd_density_candidate",
            "queue_flow_candidate",
            "occluded_path_fallback_candidate",
        ],
        "principles": [
            "人流可作为遮挡场景下的辅助候选。",
            "crowd_flow_follow_candidate 不是导航指令。",
            "人流方向不等于安全路线。",
            "人流不得覆盖地图/任务/安全判断。",
            "crowd flow 必须进入 Safety-Task Arbitration。",
            "crowded path 下必须保持保守输出。",
        ],
        "crowd_flow_follow_action_allowed": False,
        "crowd_flow_overrides_map_or_task_or_safety": False,
        "arbitration_required": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    traffic_light_crossing_tracking_policy = {
        "policy_id": f"{POLICY_ID}_traffic_light_crossing_tracking",
        "covered_candidates": [
            "traffic_light_candidate",
            "traffic_light_state_change_candidate",
            "countdown_text_tracking_candidate placeholder",
            "crosswalk_candidate",
            "vehicle_flow_near_crossing",
            "pedestrian_flow_near_crossing",
        ],
        "principles": [
            "crossing 不在本阶段做行动判断。",
            "traffic light tracking 不等于允许过马路。",
            "OCR countdown 不等于允许过马路。",
            "人流通过不等于允许过马路。",
            "输出必须交给未来 Crossing Decision Governance。",
            "current_action_instruction_allowed=false。",
        ],
        "traffic_light_crossing_action_allowed": False,
        "current_action_instruction_allowed": False,
        "crossing_decision_governance_required": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    tracking_adapter_candidate_registry = {
        "registry_id": f"{POLICY_ID}_adapter_registry",
        "adapters": [
            {
                **item,
                "integration_status": "future_candidate",
                "runtime_invoked": False,
                "allowed_now": False,
                "experiment_branch_required": True,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for item in TRACKING_ADAPTER_CANDIDATES
        ],
        "external_tracking_adapters_future_candidate_only": True,
        "must_not_install_or_import_or_execute_now": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    tracking_lifecycle_policy = {
        "policy_id": f"{POLICY_ID}_tracking_lifecycle",
        "states": [
            {
                "state": state,
                "current_action_allowed": False,
                "feedback_allowed_candidate": state in {"admitted_candidate", "active_candidate", "tentative_candidate", "lost_candidate", "stale_candidate"},
                "archive_allowed_candidate": state in {"lost_candidate", "stale_candidate", "expired_candidate", "archived_candidate", "rejected_candidate"},
                "worldmodel_handoff_allowed_candidate": state in {"archived_candidate", "expired_candidate"},
                "memory_handoff_allowed_candidate": state in {"archived_candidate", "expired_candidate"},
                "ttl_required": True,
                "privacy_filter_required": True,
                "source_chain_required": True,
            }
            for state in TRACKING_LIFECYCLE_STATES
        ],
        "state_count": len(TRACKING_LIFECYCLE_STATES),
        "source_visual_lifecycle_loaded": bool(visual_focus_lifecycle.get("policy_id")),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    tracking_feedback_policy = {
        "policy_id": f"{POLICY_ID}_tracking_feedback",
        "output_candidates": [
            "TrackingFeedbackCandidate",
            "SafetyTrackingFeedbackCandidate",
            "TaskTrackingFeedbackCandidate",
            "RouteTrackingFeedbackCandidate",
            "CrowdFlowFeedbackCandidate",
            "CrossingTrackingFeedbackCandidate",
            "TrackingDegradationFeedbackCandidate",
        ],
        "principles": [
            "feedback candidate 不直接播报。",
            "speech_allowed=false until Speech Gate。",
            "action_allowed=false。",
            "fact_status=not_fact。",
            "requires_arbitration=true。",
            "source_chain required。",
        ],
        "speech_allowed_false_until_gate": True,
        "action_allowed_false": True,
        "fact_status_not_fact": True,
        "requires_arbitration": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    selective_tracking_scenario_matrix = {
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

    selective_tracking_boundary_matrix = {
        "matrix_id": f"{POLICY_ID}_boundary_matrix",
        "tracking_authority_owner": "MidPlatform",
        "full_scene_tracking_allowed": False,
        "all_moving_objects_tracking_allowed": False,
        "all_person_tracking_allowed": False,
        "all_vehicle_tracking_allowed": False,
        "crowd_flow_follow_action_allowed": False,
        "traffic_light_crossing_action_allowed": False,
        "external_tracking_adapters_future_candidate_only": True,
        "tracking_runtime_enabled": False,
        "camera_runtime_allowed": False,
        "map_api_allowed": False,
        "ocr_provider_runtime_allowed": False,
        "ocrrequest_submitted": False,
        "tracking_runtime_allowed": False,
        "optical_flow_runtime_allowed": False,
        "supervision_allowed_now": False,
        "bytetrack_allowed_now": False,
        "ocsort_allowed_now": False,
        "sort_allowed_now": False,
        "botsort_allowed_now": False,
        "entity_resolution_runtime_allowed": False,
        "fact_admission_runtime_allowed": False,
        "memory_consolidation_allowed": False,
        "library_experience_commit_allowed": False,
        "worldmodel_write_allowed": False,
        "memory_write_allowed": False,
        "library_write_allowed": False,
        "fact_write_allowed": False,
        "scene_delta_allowed": False,
        "task_state_commit_allowed": False,
        "navigation_action_allowed": False,
        "speech_gate_allowed": False,
        "vop_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_register = {
        "register_id": f"{POLICY_ID}_governance_debt",
        "debts": [
            {
                "debt_id": f"debt_{idx:02d}",
                "topic": topic,
                "deferred_reason": "先冻结 selective tracking adapter policy，再单独做 MidPlatform Function Governance / Consolidation。",
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
        "reason": "Selective Tracking Adapter Policy 已冻结，下一阶段应进入 Visual-OCR-Map-Task Feedback DryRun 以验证多模态反馈候选串联。",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    boundary = _boundary_payload()
    summary = {
        "phase": PHASE_ID,
        "policy_scope": POLICY_SCOPE,
        "world_observation_entity_feature_input_loaded": world_observation_entity_feature_input_loaded,
        "task_aware_visual_focus_input_loaded": task_aware_visual_focus_input_loaded,
        "midplatform_perception_orchestration_input_loaded": midplatform_perception_orchestration_input_loaded,
        "return_to_vision_planning_input_loaded": return_to_vision_planning_input_loaded,
        "preplan_input_loaded": preplan_input_loaded,
        "ocr_final_closure_loaded": ocr_final_closure_loaded,
        "minimal_runtime_integration_closure_loaded": minimal_runtime_integration_closure_loaded,
        "selective_tracking_adapter_policy_defined": True,
        "tracking_request_candidate_schema_defined": True,
        "tracklet_candidate_schema_defined": True,
        "tracking_budget_policy_defined": True,
        "tracking_target_admission_policy_defined": True,
        "road_surface_tracking_policy_defined": True,
        "pedestrian_vehicle_tracking_policy_defined": True,
        "crowd_flow_tracking_policy_defined": True,
        "traffic_light_crossing_tracking_policy_defined": True,
        "tracking_adapter_candidate_registry_defined": True,
        "tracking_lifecycle_policy_defined": True,
        "tracking_feedback_policy_defined": True,
        "scenario_matrix_generated": True,
        "scenario_count": len(SCENARIO_ROWS),
        "tracking_authority_owner": "MidPlatform",
        "full_scene_tracking_allowed": False,
        "all_moving_objects_tracking_allowed": False,
        "all_person_tracking_allowed": False,
        "all_vehicle_tracking_allowed": False,
        "crowd_flow_follow_action_allowed": False,
        "traffic_light_crossing_action_allowed": False,
        "tracking_request_candidate_only": True,
        "tracklet_candidate_not_fact": True,
        "external_tracking_adapters_future_candidate_only": True,
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
        "selective_tracking_adapter_policy": selective_tracking_adapter_policy,
        "tracking_request_candidate_schema": tracking_request_candidate_schema,
        "tracklet_candidate_schema": tracklet_candidate_schema,
        "tracking_budget_policy": tracking_budget_policy,
        "tracking_target_admission_policy": tracking_target_admission_policy,
        "road_surface_tracking_policy": road_surface_tracking_policy,
        "pedestrian_vehicle_tracking_policy": pedestrian_vehicle_tracking_policy,
        "crowd_flow_tracking_policy": crowd_flow_tracking_policy,
        "traffic_light_crossing_tracking_policy": traffic_light_crossing_tracking_policy,
        "tracking_adapter_candidate_registry": tracking_adapter_candidate_registry,
        "tracking_lifecycle_policy": tracking_lifecycle_policy,
        "tracking_feedback_policy": tracking_feedback_policy,
        "selective_tracking_scenario_matrix": selective_tracking_scenario_matrix,
        "selective_tracking_boundary_matrix": selective_tracking_boundary_matrix,
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_runtime_boundary_report": boundary,
        "no_write_boundary_report": boundary,
        "debug_refs": {
            "workspace_root": str(workspace),
            "worldobs_final_decision": worldobs_summary.get("final_decision"),
            "visual_focus_final_decision": visual_focus_summary.get("final_decision"),
            "midplatform_final_decision": midplatform_summary.get("final_decision"),
            "planning_final_decision": planning_summary.get("final_decision"),
            "preplan_ready_flag": preplan_summary.get(PREPLAN_READY_FLAG),
            "ocr_final_decision": ocr_summary.get("final_decision"),
            "minimal_runtime_final_decision": mri_summary.get("final_decision"),
            "worldobs_placeholder_loaded": bool(worldobs_placeholder.get("policy_id")),
            "midplatform_boundary_loaded": bool(midplatform_boundary.get("boundary_id")),
            "planning_boundary_loaded": bool(planning_boundary.get("boundary_scope")),
            "preplan_boundary_loaded": bool(preplan_boundary.get("boundary_scope")),
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
