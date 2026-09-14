# -*- coding: utf-8 -*-
"""Controlled Frame Input Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Controlled-Frame-Input-Planning-v1-001"
PLANNING_ID = "cfip_v1_001"
PLANNING_SCOPE = "controlled_frame_input_planning_only"
SOURCE_CHAIN = "controlled_frame_input_planning_v1"
FINAL_DECISION = "CONTROLLED_FRAME_INPUT_PLANNING_READY_FOR_CONTROLLED_FRAME_INPUT_DRYRUN"
NEXT_PHASE = "Phase-Controlled-Frame-Input-DryRun-v1-001"

MAP_LOCATION_FINAL_DECISION = "MAP_LOCATION_READONLY_CONTEXT_POLICY_READY_FOR_CONTROLLED_FRAME_INPUT_PLANNING"
ROADMAP_DECISION = "POST_VISION_STRENGTHENING_ROADMAP_DECISION_READY_FOR_MAP_LOCATION_READONLY_CONTEXT_POLICY"
VISION_STRENGTHENING_CLOSURE_DECISION = "BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_CLOSED_FOR_CURRENT_MAINLINE"
FEEDBACK_DRYRUN_DECISION = "VISUAL_OCR_MAP_TASK_FEEDBACK_DRYRUN_READY_FOR_BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING"
VISUAL_FOCUS_DECISION = "TASK_AWARE_VISUAL_FOCUS_POLICY_READY_FOR_WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY"
MIDPLATFORM_DECISION = "MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY_READY_FOR_TASK_AWARE_VISUAL_FOCUS_POLICY"
MRI_DECISION = "MINIMAL_RUNTIME_INTEGRATION_CLOSED_RETURN_TO_VISION_MAINLINE"
OCR_DECISION = "OCR_MAINLINE_FINAL_CLOSURE_RETURN_TO_VISION_MAINLINE"

ROOT_SPECS = [
    {
        "id": "map_location_readonly_context",
        "arg": "map_location_readonly_context_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "map_location_readonly_context_policy.json", "map_location_boundary_matrix.json"],
    },
    {
        "id": "post_vision_strengthening_roadmap_decision",
        "arg": "post_vision_strengthening_roadmap_decision_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "recommended_next_phase_decision.json"],
    },
    {
        "id": "vision_strengthening_closure",
        "arg": "vision_strengthening_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "vision_strengthening_closure_summary.json"],
    },
    {
        "id": "visual_ocr_map_task_feedback",
        "arg": "visual_ocr_map_task_feedback_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "task_feedback_candidate_schema.json"],
    },
    {
        "id": "task_aware_visual_focus",
        "arg": "task_aware_visual_focus_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "focus_to_ocr_activation_policy.json", "focus_to_tracking_request_policy.json"],
    },
    {
        "id": "midplatform_perception_orchestration",
        "arg": "midplatform_perception_orchestration_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "perception_work_order_schema.json"],
    },
    {
        "id": "minimal_runtime_integration_closure",
        "arg": "minimal_runtime_integration_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "minimal_runtime_integration_closure_report.json"],
    },
    {
        "id": "ocr_final_closure",
        "arg": "ocr_final_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "ocr_mainline_final_closure_report.json"],
    },
    {
        "id": "vision_frame_trace_stream_registry",
        "arg": "vision_frame_trace_stream_registry_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "vision_frame_input_governance",
        "arg": "vision_frame_input_governance_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "vision_roi_proposal_stub",
        "arg": "vision_roi_proposal_stub_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "hardware_profile_capability_registry",
        "arg": "hardware_profile_capability_registry_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "system_health_center_governance",
        "arg": "system_health_center_governance_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "simulation_lab_profile",
        "arg": "simulation_lab_profile_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
]

FRAME_SOURCE_TYPES = [
    "static_test_image",
    "pre_recorded_video_frame",
    "simulation_frame",
    "synthetic_frame",
    "archived_frame_candidate",
    "controlled_uploaded_frame",
    "live_camera_placeholder",
    "device_camera_placeholder",
    "external_stream_placeholder",
]

CHANNEL_ROLE_TYPES = [
    "safety_world_lane_primary",
    "safety_world_lane_backup",
    "task_focus_lane_primary",
    "task_focus_lane_backup",
    "shared_fallback_channel",
]

QUALITY_LEVELS = {
    "GOOD": {
        "scene_sketch_allowed_candidate": True,
        "visual_focus_allowed_candidate": True,
        "ocr_activation_allowed_candidate": True,
        "tracking_request_allowed_candidate": True,
        "world_observation_allowed_candidate": True,
        "active_view_adjustment_recommended": False,
        "safety_only_recommended": False,
        "reject_reason": "",
    },
    "DEGRADED": {
        "scene_sketch_allowed_candidate": True,
        "visual_focus_allowed_candidate": True,
        "ocr_activation_allowed_candidate": False,
        "tracking_request_allowed_candidate": False,
        "world_observation_allowed_candidate": True,
        "active_view_adjustment_recommended": True,
        "safety_only_recommended": False,
        "reject_reason": "quality degraded; suppress precision-dependent downstream",
    },
    "POOR": {
        "scene_sketch_allowed_candidate": False,
        "visual_focus_allowed_candidate": False,
        "ocr_activation_allowed_candidate": False,
        "tracking_request_allowed_candidate": False,
        "world_observation_allowed_candidate": False,
        "active_view_adjustment_recommended": True,
        "safety_only_recommended": True,
        "reject_reason": "quality too poor for task-grade downstream",
    },
    "BLOCKED": {
        "scene_sketch_allowed_candidate": False,
        "visual_focus_allowed_candidate": False,
        "ocr_activation_allowed_candidate": False,
        "tracking_request_allowed_candidate": False,
        "world_observation_allowed_candidate": False,
        "active_view_adjustment_recommended": False,
        "safety_only_recommended": False,
        "reject_reason": "frame blocked by source or privacy gate",
    },
    "UNKNOWN_MARKED": {
        "scene_sketch_allowed_candidate": False,
        "visual_focus_allowed_candidate": False,
        "ocr_activation_allowed_candidate": False,
        "tracking_request_allowed_candidate": False,
        "world_observation_allowed_candidate": False,
        "active_view_adjustment_recommended": False,
        "safety_only_recommended": False,
        "reject_reason": "quality unknown but explicitly marked",
    },
}

PRIVACY_TAGS = [
    "human_face_visible",
    "bystander_presence",
    "license_plate_visible",
    "private_space_candidate",
    "home_context_candidate",
    "medical_context_candidate",
    "school_or_child_context_candidate",
    "workplace_context_candidate",
    "screen_or_document_visible",
    "personal_item_visible",
    "commercial_sensitive_candidate",
]

SCENARIO_MATRIX = [
    {
        "scenario_id": "static_test_image_allowed_for_schema_test",
        "source_type": "static_test_image",
        "allowed_for_future_dryrun": True,
        "privacy_tags_required": True,
        "runtime_required": False,
        "notes": "static test image 允许作为后续 schema/dry-run 输入候选",
    },
    {
        "scenario_id": "pre_recorded_video_frame_allowed_for_controlled_dryrun",
        "source_type": "pre_recorded_video_frame",
        "allowed_for_future_dryrun": True,
        "privacy_tags_required": True,
        "runtime_required": False,
        "notes": "预录帧允许但必须带 timestamp/source_chain",
    },
    {
        "scenario_id": "simulation_frame_allowed_for_sim_lab",
        "source_type": "simulation_frame",
        "allowed_for_future_dryrun": True,
        "privacy_tags_required": True,
        "runtime_required": False,
        "notes": "仿真帧允许作为受控输入，必须标明 simulation context",
    },
    {
        "scenario_id": "uploaded_frame_requires_privacy_tags",
        "source_type": "controlled_uploaded_frame",
        "allowed_for_future_dryrun": True,
        "privacy_tags_required": True,
        "runtime_required": False,
        "notes": "uploaded frame 若缺少 privacy tags，则 downstream blocked",
    },
    {
        "scenario_id": "live_camera_placeholder_blocked_now",
        "source_type": "live_camera_placeholder",
        "allowed_for_future_dryrun": False,
        "privacy_tags_required": True,
        "runtime_required": True,
        "notes": "live camera placeholder 当前 blocked",
    },
    {
        "scenario_id": "external_stream_placeholder_blocked_now",
        "source_type": "external_stream_placeholder",
        "allowed_for_future_dryrun": False,
        "privacy_tags_required": True,
        "runtime_required": True,
        "notes": "external stream placeholder 当前 blocked",
    },
    {
        "scenario_id": "low_quality_frame_degraded",
        "source_type": "pre_recorded_video_frame",
        "allowed_for_future_dryrun": True,
        "privacy_tags_required": True,
        "runtime_required": False,
        "notes": "quality=POOR 时任务视觉 suppressed，仅可建议 active view adjustment",
    },
    {
        "scenario_id": "privacy_sensitive_home_frame_restricted",
        "source_type": "controlled_uploaded_frame",
        "allowed_for_future_dryrun": True,
        "privacy_tags_required": True,
        "runtime_required": False,
        "notes": "home/private frame 任务使用受限，长时写入 blocked",
    },
    {
        "scenario_id": "stale_frame_archive_candidate_only",
        "source_type": "archived_frame_candidate",
        "allowed_for_future_dryrun": True,
        "privacy_tags_required": True,
        "runtime_required": False,
        "notes": "stale/expired frame current_action_allowed=false，archive_candidate_allowed=true",
    },
    {
        "scenario_id": "frame_to_ocr_requires_visual_focus",
        "source_type": "static_test_image",
        "allowed_for_future_dryrun": True,
        "privacy_tags_required": True,
        "runtime_required": False,
        "notes": "frame contains text; OCR activation only through VisualFocus, never direct OCR provider",
    },
]

DEBT_TOPICS = [
    "frame source trust calibration debt",
    "privacy tag completeness debt",
    "quality grade calibration debt",
    "stc and ttl reuse mapping debt",
    "simulation-to-real source gap debt",
    "midplatform frame ownership debt",
    "frame storage policy debt",
    "downstream eligibility matrix complexity",
    "hardware profile coupling debt",
    "schema consolidation risk",
    "双设备设计被误解为当前硬件 runtime",
    "双模型设计导致双治理系统",
    "failover 被误解为自动行动授权",
    "device health placeholder 被误写成设备事实",
    "多输入一致性候选被误写成事实",
    "硬件阶段职责提前侵入当前视觉主线",
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _read_json(path: Path) -> Any:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def _load_root(path_str: Optional[str], summary_file: str, artifacts: List[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    loaded = bool(root and root.is_dir() and all((root / name).is_file() for name in artifacts))
    return {
        "root": root,
        "loaded": loaded,
        "summary": _read_json(root / summary_file) if root and (root / summary_file).is_file() else {},
    }


def _field(name: str, field_type: str, required: bool, **extras: Any) -> Dict[str, Any]:
    payload = {"name": name, "type": field_type, "required": required}
    payload.update(extras)
    return payload


def _boundary_payload() -> Dict[str, Any]:
    return {
        "planning_scope": PLANNING_SCOPE,
        "live_camera_allowed": False,
        "device_camera_allowed": False,
        "external_stream_allowed": False,
        "dual_device_runtime_allowed": False,
        "dual_model_runtime_allowed": False,
        "failover_runtime_allowed": False,
        "automatic_hardware_switch_allowed": False,
        "hardware_stage_deferred": True,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "camera_invoked": False,
        "camera_opened": False,
        "video_capture_invoked": False,
        "visual_model_invoked": False,
        "map_api_invoked": False,
        "gaode_api_invoked": False,
        "gps_runtime_invoked": False,
        "ocr_provider_invoked": False,
        "ocrrequest_submitted": False,
        "tracking_runtime_invoked": False,
        "optical_flow_runtime_invoked": False,
        "supervision_invoked": False,
        "bytetrack_invoked": False,
        "ocsort_invoked": False,
        "speech_gate_invoked": False,
        "vop_invoked": False,
        "tts_invoked": False,
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
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def run_controlled_frame_input_planning_v1(
    *,
    map_location_readonly_context_root: str,
    post_vision_strengthening_roadmap_decision_root: str,
    vision_strengthening_closure_root: str,
    visual_ocr_map_task_feedback_root: str,
    task_aware_visual_focus_root: str,
    midplatform_perception_orchestration_root: str,
    minimal_runtime_integration_closure_root: str,
    ocr_final_closure_root: str,
    vision_frame_trace_stream_registry_root: Optional[str] = None,
    vision_frame_input_governance_root: Optional[str] = None,
    vision_roi_proposal_stub_root: Optional[str] = None,
    hardware_profile_capability_registry_root: Optional[str] = None,
    system_health_center_governance_root: Optional[str] = None,
    simulation_lab_profile_root: Optional[str] = None,
) -> Dict[str, Any]:
    args = locals().copy()
    roots = {spec["id"]: _load_root(args[spec["arg"]], spec["summary"], spec["artifacts"]) for spec in ROOT_SPECS}

    input_rows = []
    for spec in ROOT_SPECS:
        meta = roots[spec["id"]]
        input_rows.append(
            {
                "intake_id": spec["id"],
                "path": str(meta["root"]) if meta["root"] else "(not_provided)",
                "loaded": meta["loaded"],
                "required": spec["required"],
                "status": "loaded" if meta["loaded"] else ("missing_required" if spec["required"] else "optional_missing"),
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    summaries = {key: roots[key]["summary"] for key in roots}

    map_location_readonly_context_input_loaded = (
        roots["map_location_readonly_context"]["loaded"]
        and summaries["map_location_readonly_context"].get("final_decision") == MAP_LOCATION_FINAL_DECISION
    )
    post_vision_strengthening_roadmap_decision_input_loaded = (
        roots["post_vision_strengthening_roadmap_decision"]["loaded"]
        and summaries["post_vision_strengthening_roadmap_decision"].get("final_decision") == ROADMAP_DECISION
    )
    vision_strengthening_closure_input_loaded = (
        roots["vision_strengthening_closure"]["loaded"]
        and summaries["vision_strengthening_closure"].get("final_decision") == VISION_STRENGTHENING_CLOSURE_DECISION
    )
    visual_ocr_map_task_feedback_input_loaded = (
        roots["visual_ocr_map_task_feedback"]["loaded"]
        and summaries["visual_ocr_map_task_feedback"].get("final_decision") == FEEDBACK_DRYRUN_DECISION
    )
    task_aware_visual_focus_input_loaded = (
        roots["task_aware_visual_focus"]["loaded"]
        and summaries["task_aware_visual_focus"].get("final_decision") == VISUAL_FOCUS_DECISION
    )
    midplatform_perception_orchestration_input_loaded = (
        roots["midplatform_perception_orchestration"]["loaded"]
        and summaries["midplatform_perception_orchestration"].get("final_decision") == MIDPLATFORM_DECISION
    )
    minimal_runtime_integration_closure_loaded = (
        roots["minimal_runtime_integration_closure"]["loaded"]
        and summaries["minimal_runtime_integration_closure"].get("final_decision") == MRI_DECISION
    )
    ocr_final_closure_loaded = (
        roots["ocr_final_closure"]["loaded"]
        and summaries["ocr_final_closure"].get("final_decision") == OCR_DECISION
    )

    controlled_frame_input_planning_policy = {
        "policy_id": PLANNING_ID,
        "policy_scope": PLANNING_SCOPE,
        "allowed_frame_sources": [
            "static_test_image",
            "pre_recorded_video_frame",
            "simulation_frame",
            "synthetic_frame",
            "archived_frame_candidate",
            "controlled_uploaded_frame",
        ],
        "forbidden_frame_sources": [
            "live_camera_placeholder",
            "device_camera_placeholder",
            "external_stream_placeholder",
        ],
        "frame_intake_boundary_ref": "frame_intake_gate_policy.json",
        "frame_quality_gate_ref": "frame_quality_gate_policy.json",
        "privacy_filtering_policy_ref": "frame_privacy_tagging_policy.json",
        "stc_freshness_policy_ref": "frame_stc_freshness_policy.json",
        "source_chain_policy_ref": "controlled_frame_input_boundary_matrix.json",
        "downstream_handoff_policy_ref": "frame_downstream_handoff_policy.json",
        "no_runtime_boundary_ref": "no_runtime_boundary_report.json",
        "no_write_boundary_ref": "no_write_boundary_report.json",
        "source_chain": SOURCE_CHAIN,
        "non_claims": [
            "controlled frame input planning 不等于 camera runtime",
            "当前不读取 live camera",
            "当前不读取用户设备摄像头",
            "当前不调用视觉模型",
            "当前只定义未来受控 frame 输入的规则",
        ],
        **_not_fact(),
    }

    frame_source_candidate_schema = {
        "schema_name": "FrameSourceCandidate",
        "source_type_enum": FRAME_SOURCE_TYPES,
        "field_specs": [
            _field("frame_source_candidate_id", "string", True),
            _field("source_type", "enum", True, allowed_values=FRAME_SOURCE_TYPES),
            _field("source_origin", "string", True),
            _field("source_trust_level", "string", True),
            _field("frame_access_mode", "string", True),
            _field("allowed_now", "boolean", True),
            _field("runtime_required", "boolean", True),
            _field("privacy_risk", "string", True),
            _field("test_only", "boolean", True),
            _field("task_use_allowed_candidate", "boolean", True),
            _field("world_observation_use_allowed_candidate", "boolean", True),
            _field("fact_status", "string", True, default="not_fact"),
            _field("source_chain", "string", True, default=SOURCE_CHAIN),
        ],
        "source_defaults": {
            "live_camera_placeholder": {"allowed_now": False, "runtime_required": True},
            "device_camera_placeholder": {"allowed_now": False, "runtime_required": True},
            "external_stream_placeholder": {"allowed_now": False, "runtime_required": True},
            "static_test_image": {"allowed_now": True, "runtime_required": False},
            "pre_recorded_video_frame": {"allowed_now": True, "runtime_required": False},
            "simulation_frame": {"allowed_now": True, "runtime_required": False},
        },
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    controlled_frame_input_candidate_schema = {
        "schema_name": "ControlledFrameInputCandidate",
        "downstream_allowed_targets_enum": [
            "view_quality_candidate",
            "scene_sketch_candidate",
            "visual_focus_plan_candidate",
            "ocr_activation_candidate",
            "tracking_request_candidate",
            "world_observation_candidate",
            "debug_visualization_candidate",
        ],
        "field_specs": [
            _field("frame_input_candidate_id", "string", True),
            _field("frame_source_candidate_ref", "string", True),
            _field("frame_id", "string", True),
            _field("frame_timestamp", "string", True),
            _field("monotonic_seq", "integer", True),
            _field("source_time_ref", "string", True),
            _field("location_context_ref", "string", False),
            _field("pose_or_view_context_ref", "string", False),
            _field("device_context_ref", "string", False),
            _field("task_context_ref", "string", False),
            _field("privacy_tags", "list", True),
            _field("quality_status_candidate", "string", True),
            _field("freshness_status", "string", True),
            _field("ttl_policy_ref", "string", True),
            _field("frame_hash_placeholder", "string", True),
            _field("storage_policy", "string", True),
            _field("downstream_allowed_targets", "list", True),
            _field("runtime_action_allowed", "boolean", True, default=False),
            _field("fact_status", "string", True, default="not_fact"),
            _field("source_chain", "string", True, default=SOURCE_CHAIN),
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    frame_intake_gate_policy = {
        "policy_name": "FrameIntakeGatePolicy",
        "allow_conditions": [
            "source allowed",
            "source_chain present",
            "timestamp present",
            "privacy tags present",
            "task context present or explicitly taskless background context",
            "quality status computable or unknown-but-marked",
            "no live runtime required",
            "no write side effect",
            "no direct output side effect",
        ],
        "reject_conditions": [
            "unknown source",
            "missing source_chain",
            "missing timestamp",
            "live camera attempt",
            "external stream attempt",
            "privacy tags missing",
            "task context missing without background policy",
            "frame tries to trigger runtime",
            "frame tries to write fact",
            "frame tries to bypass MidPlatform",
        ],
        "source_chain_required": True,
        "timestamp_required": True,
        "privacy_tags_required_for_downstream": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    frame_quality_gate_policy = {
        "policy_name": "FrameQualityGatePolicy",
        "quality_dimensions": [
            "blur",
            "brightness",
            "exposure",
            "occlusion",
            "motion_blur",
            "camera_shake",
            "target_distance",
            "angle_quality",
            "resolution_sufficiency",
            "frame_stability",
            "privacy_sensitivity",
        ],
        "quality_levels": QUALITY_LEVELS,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    frame_privacy_tagging_policy = {
        "policy_name": "FramePrivacyTaggingPolicy",
        "privacy_tags": PRIVACY_TAGS,
        "principles": [
            "privacy tag missing -> frame blocked from downstream",
            "privacy filtering owned by MidPlatform",
            "frame collection != frame long-term storage",
            "frame usable for task != frame eligible for WorldModel/Memory",
            "private/home/medical/school/workplace contexts require restricted policy",
            "no face recognition",
            "no identity inference",
            "no emotional inference",
        ],
        "restricted_contexts": [
            "private_space_candidate",
            "home_context_candidate",
            "medical_context_candidate",
            "school_or_child_context_candidate",
            "workplace_context_candidate",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    frame_stc_freshness_policy = {
        "policy_name": "FrameSTCFreshnessPolicy",
        "timestamp_required": True,
        "monotonic_seq_required": True,
        "location_context_optional_but_marked": True,
        "pose_or_view_context_optional_but_marked": True,
        "freshness_status_values": ["fresh", "stale", "expired", "unknown_marked"],
        "ttl_policy_ref": "controlled_frame_input_boundary_matrix.json",
        "stale_handling": "stale frame may degrade to archive/debug or review-only candidate",
        "expired_handling": "expired frame blocks current task-grade downstream and keeps archive candidate only",
        "current_action_allowed_when_stale": False,
        "archive_candidate_allowed": True,
        "source_chain_required": True,
        "stc_freshness_reuse_required": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    frame_downstream_handoff_policy = {
        "policy_name": "FrameDownstreamHandoffPolicy",
        "allowed_handoffs": [
            "Frame -> ViewQualityCandidate",
            "Frame -> SceneSketchCandidate",
            "Frame -> VisualFocusPlan candidate",
            "Frame -> OCRActivationCandidate only via VisualFocus",
            "Frame -> TrackingRequestCandidate only via VisualFocus/MidPlatform",
            "Frame -> WorldObservationCandidate only via WorldObservation policy",
            "Frame -> Debug/Review artifact if no privacy conflict",
        ],
        "forbidden_handoffs": [
            "Frame -> OCR provider directly",
            "Frame -> tracking runtime directly",
            "Frame -> map API",
            "Frame -> NavigationAction",
            "Frame -> SpeechOutput",
            "Frame -> WorldModel write",
            "Frame -> Memory write",
            "Frame -> Fact write",
            "Frame -> SceneDelta",
        ],
        "frame_to_ocr_requires_visual_focus": True,
        "frame_to_tracking_requires_visual_focus": True,
        "frame_to_world_observation_requires_policy": True,
        "frame_to_navigation_action_allowed": False,
        "frame_to_speech_output_allowed": False,
        "frame_to_worldmodel_write_allowed": False,
        "frame_to_memory_write_allowed": False,
        "frame_to_fact_write_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    dual_device_redundant_perception_placeholder = {
        "placeholder_name": "Dual-Device / Dual-Lane Redundant Perception Placeholder",
        "placeholder_scope": "future_hardware_stage_only",
        "current_stage_behavior": "placeholder_schema_stub_future_hook_only",
        "design_positioning": [
            "当前不接真实硬件",
            "当前不接真实 camera",
            "当前不定义最终设备形态",
            "当前不绑定具体模型",
            "当前不执行 failover",
            "当前不做 dual-camera runtime",
            "当前不做 dual-model runtime",
            "当前不做多输入融合",
            "当前只预留字段和边界",
        ],
        "future_candidate_directions": [
            "主输入设备 + 备份输入设备",
            "Safety-World Lane 输入设备 + Task-Focus Lane 输入设备",
            "低功耗安全观察设备 + 高精度任务观察设备",
            "RGB + depth / ToF / wide-angle / secondary camera 等组合",
            "主模型 + 备份模型",
            "轻量安全模型 + 重型任务模型",
        ],
        "perception_input_channel_placeholder": {
            "schema_name": "PerceptionInputChannelPlaceholder",
            "channel_role_enum": CHANNEL_ROLE_TYPES,
            "field_specs": [
                _field("input_channel_id", "string", True),
                _field("channel_role", "enum", True, allowed_values=CHANNEL_ROLE_TYPES),
                _field("lane_assignment_candidate", "string", True),
                _field("primary_or_backup_candidate", "string", True),
                _field("device_type_placeholder", "string", True),
                _field("model_assignment_placeholder", "string", True),
                _field("health_status_ref_placeholder", "string", False),
                _field("frame_source_candidate_ref", "string", False),
                _field("failover_role_candidate", "string", False),
                _field("degraded_mode_candidate", "string", False),
                _field("runtime_allowed", "boolean", True, default=False),
                _field("fact_status", "string", True, default="not_fact"),
                _field("source_chain", "string", True, default=SOURCE_CHAIN),
            ],
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        "perception_device_health_placeholder": {
            "schema_name": "PerceptionDeviceHealthPlaceholder",
            "field_specs": [
                _field("device_health_placeholder_id", "string", True),
                _field("input_channel_id", "string", True),
                _field("availability_candidate", "string", True),
                _field("latency_candidate", "string", True),
                _field("frame_drop_candidate", "string", True),
                _field("quality_candidate", "string", True),
                _field("power_state_candidate", "string", True),
                _field("thermal_state_candidate", "string", True),
                _field("failure_reason_candidate", "string", False),
                _field("health_fact_allowed", "boolean", True, default=False),
                _field("runtime_allowed", "boolean", True, default=False),
                _field("source_chain", "string", True, default=SOURCE_CHAIN),
            ],
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        "perception_lane_failover_placeholder": {
            "schema_name": "PerceptionLaneFailoverPlaceholder",
            "field_specs": [
                _field("failover_placeholder_id", "string", True),
                _field("failed_channel_ref", "string", True),
                _field("backup_channel_ref", "string", True),
                _field("failover_condition_candidate", "string", True),
                _field("degraded_mode_candidate", "string", True),
                _field("minimum_safety_capability_candidate", "string", True),
                _field("task_suspension_policy_candidate", "string", True),
                _field("user_notice_candidate", "string", False),
                _field("automatic_action_allowed", "boolean", True, default=False),
                _field("runtime_allowed", "boolean", True, default=False),
                _field("source_chain", "string", True, default=SOURCE_CHAIN),
            ],
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        "dual_input_consistency_placeholder": {
            "schema_name": "DualInputConsistencyPlaceholder",
            "field_specs": [
                _field("consistency_placeholder_id", "string", True),
                _field("input_a_ref", "string", True),
                _field("input_b_ref", "string", True),
                _field("agreement_level_candidate", "string", True),
                _field("conflict_type_candidate", "string", False),
                _field("confidence_delta_candidate", "string", True),
                _field("reobserve_required_candidate", "boolean", True),
                _field("arbitration_required", "boolean", True, default=True),
                _field("fact_status", "string", True, default="not_fact"),
                _field("runtime_allowed", "boolean", True, default=False),
                _field("source_chain", "string", True, default=SOURCE_CHAIN),
            ],
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        "boundaries": {
            "dual_device_runtime_allowed": False,
            "dual_model_runtime_allowed": False,
            "failover_runtime_allowed": False,
            "device_health_fact_allowed": False,
            "lane_failover_action_allowed": False,
            "automatic_hardware_switch_allowed": False,
            "multi_input_fusion_runtime_allowed": False,
            "hardware_stage_deferred": True,
        },
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    controlled_frame_input_readiness_gate = {
        "go_conditions": [
            "source policy defined",
            "frame candidate schema defined",
            "intake gate defined",
            "quality gate defined",
            "privacy tagging defined",
            "STC/freshness policy defined",
            "downstream handoff policy defined",
            "no live camera runtime",
            "no model runtime",
            "no write",
            "next phase clear",
        ],
        "no_go_conditions": [
            "live camera attempted",
            "unknown frame source allowed",
            "missing source_chain allowed",
            "privacy tags optional for downstream",
            "OCR provider allowed directly",
            "tracking runtime allowed directly",
            "WorldModel/Memory/Fact write allowed",
            "NavigationAction allowed",
            "Speech output allowed",
        ],
        "ready_for_next_phase": True,
        "verdict": "GO",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    controlled_frame_input_planning_scenario_matrix = {
        "scenarios": [
            {
                **item,
                "source_chain": SOURCE_CHAIN,
                "fact_status": "not_fact",
                "runtime_action_allowed": False,
                **_not_fact(),
            }
            for item in SCENARIO_MATRIX
        ],
        "scenario_count": len(SCENARIO_MATRIX),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    controlled_frame_input_boundary_matrix = {
        "planning_scope": PLANNING_SCOPE,
        "live_camera_allowed": False,
        "device_camera_allowed": False,
        "external_stream_allowed": False,
        "dual_device_runtime_allowed": False,
        "dual_model_runtime_allowed": False,
        "failover_runtime_allowed": False,
        "device_health_fact_allowed": False,
        "lane_failover_action_allowed": False,
        "automatic_hardware_switch_allowed": False,
        "multi_input_fusion_runtime_allowed": False,
        "hardware_stage_deferred": True,
        "static_test_image_allowed_candidate": True,
        "prerecorded_video_frame_allowed_candidate": True,
        "simulation_frame_allowed_candidate": True,
        "frame_to_ocr_requires_visual_focus": True,
        "frame_to_tracking_requires_visual_focus": True,
        "frame_to_world_observation_requires_policy": True,
        "frame_to_navigation_action_allowed": False,
        "frame_to_speech_output_allowed": False,
        "frame_to_worldmodel_write_allowed": False,
        "frame_to_memory_write_allowed": False,
        "frame_to_fact_write_allowed": False,
        "privacy_tags_required_for_downstream": True,
        "source_chain_required": True,
        "timestamp_required": True,
        "stc_freshness_reuse_required": True,
        "current_stage_runtime_forbidden": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_register = {
        "carryover_topics": [
            {
                "topic": topic,
                "impact": "must remain visible before controlled frame input dryrun and midplatform function governance",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for topic in DEBT_TOPICS
        ],
        "future_midplatform_function_governance_required": True,
        "no_duplicate_governance_module_allowed": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE,
        "final_decision": FINAL_DECISION,
        "reason": "controlled frame intake rules are defined; next step is dryrun with static / prerecorded / simulation inputs only",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers = []
    if not all(
        [
            map_location_readonly_context_input_loaded,
            post_vision_strengthening_roadmap_decision_input_loaded,
            vision_strengthening_closure_input_loaded,
            visual_ocr_map_task_feedback_input_loaded,
            task_aware_visual_focus_input_loaded,
            midplatform_perception_orchestration_input_loaded,
            minimal_runtime_integration_closure_loaded,
            ocr_final_closure_loaded,
        ]
    ):
        blockers.append("required_root_missing_or_invalid")

    controlled_frame_input_readiness_gate["ready_for_next_phase"] = not blockers
    controlled_frame_input_readiness_gate["verdict"] = "GO" if not blockers else "NO_GO"

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "map_location_readonly_context_input_loaded": map_location_readonly_context_input_loaded,
        "post_vision_strengthening_roadmap_decision_input_loaded": post_vision_strengthening_roadmap_decision_input_loaded,
        "vision_strengthening_closure_input_loaded": vision_strengthening_closure_input_loaded,
        "visual_ocr_map_task_feedback_input_loaded": visual_ocr_map_task_feedback_input_loaded,
        "task_aware_visual_focus_input_loaded": task_aware_visual_focus_input_loaded,
        "midplatform_perception_orchestration_input_loaded": midplatform_perception_orchestration_input_loaded,
        "minimal_runtime_integration_closure_loaded": minimal_runtime_integration_closure_loaded,
        "ocr_final_closure_loaded": ocr_final_closure_loaded,
        "controlled_frame_input_planning_policy_defined": True,
        "frame_source_candidate_schema_defined": True,
        "controlled_frame_input_candidate_schema_defined": True,
        "frame_intake_gate_policy_defined": True,
        "frame_quality_gate_policy_defined": True,
        "frame_privacy_tagging_policy_defined": True,
        "frame_stc_freshness_policy_defined": True,
        "frame_downstream_handoff_policy_defined": True,
        "controlled_frame_input_readiness_gate_generated": True,
        "scenario_matrix_generated": True,
        "governance_debt_register_generated": True,
        "dual_device_redundant_perception_placeholder_defined": True,
        "perception_input_channel_placeholder_defined": True,
        "perception_device_health_placeholder_defined": True,
        "perception_lane_failover_placeholder_defined": True,
        "dual_input_consistency_placeholder_defined": True,
        "scenario_count": len(SCENARIO_MATRIX),
        "static_test_image_allowed_candidate": True,
        "prerecorded_video_frame_allowed_candidate": True,
        "simulation_frame_allowed_candidate": True,
        "live_camera_allowed": False,
        "device_camera_allowed": False,
        "external_stream_allowed": False,
        "dual_device_runtime_allowed": False,
        "dual_model_runtime_allowed": False,
        "failover_runtime_allowed": False,
        "automatic_hardware_switch_allowed": False,
        "hardware_stage_deferred": True,
        "frame_to_ocr_requires_visual_focus": True,
        "frame_to_tracking_requires_visual_focus": True,
        "frame_to_world_observation_requires_policy": True,
        "frame_to_navigation_action_allowed": False,
        "frame_to_speech_output_allowed": False,
        "frame_to_worldmodel_write_allowed": False,
        "frame_to_memory_write_allowed": False,
        "frame_to_fact_write_allowed": False,
        "privacy_tags_required_for_downstream": True,
        "source_chain_required": True,
        "timestamp_required": True,
        "stc_freshness_reuse_required": True,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "camera_invoked": False,
        "camera_opened": False,
        "video_capture_invoked": False,
        "visual_model_invoked": False,
        "map_api_invoked": False,
        "gaode_api_invoked": False,
        "gps_runtime_invoked": False,
        "ocr_provider_invoked": False,
        "ocrrequest_submitted": False,
        "tracking_runtime_invoked": False,
        "optical_flow_runtime_invoked": False,
        "supervision_invoked": False,
        "bytetrack_invoked": False,
        "ocsort_invoked": False,
        "speech_gate_invoked": False,
        "vop_invoked": False,
        "tts_invoked": False,
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
        "boundary_ok": True,
        "violations": [],
        "final_decision": FINAL_DECISION if not blockers else "CONTROLLED_FRAME_INPUT_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if not blockers else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "controlled_frame_input_planning_policy": controlled_frame_input_planning_policy,
        "frame_source_candidate_schema": frame_source_candidate_schema,
        "controlled_frame_input_candidate_schema": controlled_frame_input_candidate_schema,
        "frame_intake_gate_policy": frame_intake_gate_policy,
        "frame_quality_gate_policy": frame_quality_gate_policy,
        "frame_privacy_tagging_policy": frame_privacy_tagging_policy,
        "frame_stc_freshness_policy": frame_stc_freshness_policy,
        "frame_downstream_handoff_policy": frame_downstream_handoff_policy,
        "dual_device_redundant_perception_placeholder": dual_device_redundant_perception_placeholder,
        "controlled_frame_input_readiness_gate": controlled_frame_input_readiness_gate,
        "controlled_frame_input_planning_scenario_matrix": controlled_frame_input_planning_scenario_matrix,
        "controlled_frame_input_boundary_matrix": controlled_frame_input_boundary_matrix,
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_runtime_boundary_report": _boundary_payload(),
        "no_write_boundary_report": _boundary_payload(),
    }
