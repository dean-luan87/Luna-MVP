# -*- coding: utf-8 -*-
"""Controlled Frame Input DryRun v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Controlled-Frame-Input-DryRun-v1-001"
DRYRUN_ID = "cfid_v1_001"
DRYRUN_SCOPE = "controlled_frame_input_dryrun_only"
SOURCE_CHAIN = "controlled_frame_input_dryrun_v1"
FINAL_DECISION = "CONTROLLED_FRAME_INPUT_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Controlled-Frame-Input-Post-DryRun-Review-v1-001"

PLANNING_DECISION = "CONTROLLED_FRAME_INPUT_PLANNING_READY_FOR_CONTROLLED_FRAME_INPUT_DRYRUN"
MAP_LOCATION_FINAL_DECISION = "MAP_LOCATION_READONLY_CONTEXT_POLICY_READY_FOR_CONTROLLED_FRAME_INPUT_PLANNING"
ROADMAP_DECISION = "POST_VISION_STRENGTHENING_ROADMAP_DECISION_READY_FOR_MAP_LOCATION_READONLY_CONTEXT_POLICY"
VISION_STRENGTHENING_CLOSURE_DECISION = "BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_CLOSED_FOR_CURRENT_MAINLINE"
VISUAL_FOCUS_DECISION = "TASK_AWARE_VISUAL_FOCUS_POLICY_READY_FOR_WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY"
MIDPLATFORM_DECISION = "MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY_READY_FOR_TASK_AWARE_VISUAL_FOCUS_POLICY"
MRI_DECISION = "MINIMAL_RUNTIME_INTEGRATION_CLOSED_RETURN_TO_VISION_MAINLINE"
OCR_DECISION = "OCR_MAINLINE_FINAL_CLOSURE_RETURN_TO_VISION_MAINLINE"

ROOT_SPECS = [
    {
        "id": "controlled_frame_input_planning",
        "arg": "controlled_frame_input_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "controlled_frame_input_planning_policy.json",
            "frame_source_candidate_schema.json",
            "controlled_frame_input_candidate_schema.json",
            "frame_intake_gate_policy.json",
            "frame_quality_gate_policy.json",
            "frame_privacy_tagging_policy.json",
            "frame_stc_freshness_policy.json",
            "frame_downstream_handoff_policy.json",
            "dual_device_redundant_perception_placeholder.json",
            "controlled_frame_input_boundary_matrix.json",
        ],
    },
    {
        "id": "map_location_readonly_context",
        "arg": "map_location_readonly_context_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "map_location_readonly_context_policy.json"],
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

DRYRUN_CASES = [
    {
        "dryrun_case_id": "case_static_test_image_good_quality",
        "scenario_id": "static_test_image_good_quality",
        "case_type": "good_quality_frame",
        "source_type": "static_test_image",
        "source_origin": "controlled_schema_fixture",
        "task_context_ref": "task.search_shopfront",
        "location_context_ref": "loc.target_zone_a",
        "pose_or_view_context_ref": "pose.front_view",
        "device_context_ref": "device.simulated_viewer",
        "privacy_tags": ["commercial_sensitive_candidate"],
        "quality_level": "GOOD",
        "freshness_status": "fresh",
        "ttl_policy_ref": "ttl.standard.short",
        "storage_policy_candidate": "ephemeral_review_only",
        "source_chain_present": True,
        "timestamp_present": True,
        "accepted_for_downstream": True,
        "restricted_use_required": False,
        "archive_only": False,
        "allow_scene_sketch": True,
        "allow_visual_focus": True,
        "allow_ocr_via_focus": False,
        "allow_tracking_via_focus": False,
        "allow_world_observation": True,
        "debug_artifact_allowed": True,
    },
    {
        "dryrun_case_id": "case_prerecorded_degraded_quality",
        "scenario_id": "prerecorded_video_frame_degraded_quality",
        "case_type": "degraded_quality_frame",
        "source_type": "pre_recorded_video_frame",
        "source_origin": "controlled_video_fixture",
        "task_context_ref": "task.follow_route_segment",
        "location_context_ref": "loc.segment_b",
        "pose_or_view_context_ref": "pose.side_view",
        "device_context_ref": "device.simulated_body_cam",
        "privacy_tags": ["bystander_presence"],
        "quality_level": "DEGRADED",
        "freshness_status": "fresh",
        "ttl_policy_ref": "ttl.standard.short",
        "storage_policy_candidate": "ephemeral_review_only",
        "source_chain_present": True,
        "timestamp_present": True,
        "accepted_for_downstream": True,
        "restricted_use_required": False,
        "archive_only": False,
        "allow_scene_sketch": True,
        "allow_visual_focus": True,
        "allow_ocr_via_focus": False,
        "allow_tracking_via_focus": False,
        "allow_world_observation": True,
        "debug_artifact_allowed": True,
    },
    {
        "dryrun_case_id": "case_simulation_frame_allowed",
        "scenario_id": "simulation_frame_allowed",
        "case_type": "simulation_frame",
        "source_type": "simulation_frame",
        "source_origin": "simulation_lab_profile",
        "task_context_ref": "task.navigation_probe",
        "location_context_ref": "sim.map.block_c",
        "pose_or_view_context_ref": "sim.pose.overview",
        "device_context_ref": "sim.device.virtual_sensor",
        "privacy_tags": ["commercial_sensitive_candidate"],
        "quality_level": "GOOD",
        "freshness_status": "fresh",
        "ttl_policy_ref": "ttl.simulation.short",
        "storage_policy_candidate": "simulation_ephemeral",
        "source_chain_present": True,
        "timestamp_present": True,
        "accepted_for_downstream": True,
        "restricted_use_required": False,
        "archive_only": False,
        "allow_scene_sketch": True,
        "allow_visual_focus": True,
        "allow_ocr_via_focus": False,
        "allow_tracking_via_focus": False,
        "allow_world_observation": True,
        "debug_artifact_allowed": True,
    },
    {
        "dryrun_case_id": "case_controlled_uploaded_privacy_sensitive",
        "scenario_id": "controlled_uploaded_frame_privacy_sensitive",
        "case_type": "privacy_sensitive_frame",
        "source_type": "controlled_uploaded_frame",
        "source_origin": "user_uploaded_placeholder",
        "task_context_ref": "task.find_notice",
        "location_context_ref": "loc.private_home_candidate",
        "pose_or_view_context_ref": "pose.near_screen",
        "device_context_ref": "device.uploaded_file",
        "privacy_tags": ["home_context_candidate", "private_space_candidate", "screen_or_document_visible"],
        "quality_level": "GOOD",
        "freshness_status": "fresh",
        "ttl_policy_ref": "ttl.upload.short",
        "storage_policy_candidate": "restricted_ephemeral_only",
        "source_chain_present": True,
        "timestamp_present": True,
        "accepted_for_downstream": True,
        "restricted_use_required": True,
        "archive_only": False,
        "allow_scene_sketch": False,
        "allow_visual_focus": False,
        "allow_ocr_via_focus": False,
        "allow_tracking_via_focus": False,
        "allow_world_observation": False,
        "debug_artifact_allowed": False,
    },
    {
        "dryrun_case_id": "case_missing_source_chain_rejected",
        "scenario_id": "missing_source_chain_rejected",
        "case_type": "missing_required_field",
        "source_type": "static_test_image",
        "source_origin": "broken_fixture",
        "task_context_ref": "task.schema_probe",
        "location_context_ref": "loc.none",
        "pose_or_view_context_ref": "pose.none",
        "device_context_ref": "device.test_harness",
        "privacy_tags": ["commercial_sensitive_candidate"],
        "quality_level": "GOOD",
        "freshness_status": "fresh",
        "ttl_policy_ref": "ttl.standard.short",
        "storage_policy_candidate": "ephemeral_review_only",
        "source_chain_present": False,
        "timestamp_present": True,
        "accepted_for_downstream": False,
        "restricted_use_required": False,
        "archive_only": False,
        "allow_scene_sketch": False,
        "allow_visual_focus": False,
        "allow_ocr_via_focus": False,
        "allow_tracking_via_focus": False,
        "allow_world_observation": False,
        "debug_artifact_allowed": False,
    },
    {
        "dryrun_case_id": "case_missing_timestamp_rejected",
        "scenario_id": "missing_timestamp_rejected",
        "case_type": "missing_required_field",
        "source_type": "simulation_frame",
        "source_origin": "broken_sim_fixture",
        "task_context_ref": "task.schema_probe",
        "location_context_ref": "loc.sim.none",
        "pose_or_view_context_ref": "pose.none",
        "device_context_ref": "device.test_harness",
        "privacy_tags": ["commercial_sensitive_candidate"],
        "quality_level": "GOOD",
        "freshness_status": "unknown_marked",
        "ttl_policy_ref": "ttl.standard.short",
        "storage_policy_candidate": "ephemeral_review_only",
        "source_chain_present": True,
        "timestamp_present": False,
        "accepted_for_downstream": False,
        "restricted_use_required": False,
        "archive_only": False,
        "allow_scene_sketch": False,
        "allow_visual_focus": False,
        "allow_ocr_via_focus": False,
        "allow_tracking_via_focus": False,
        "allow_world_observation": False,
        "debug_artifact_allowed": False,
    },
    {
        "dryrun_case_id": "case_missing_privacy_tags_rejected",
        "scenario_id": "missing_privacy_tags_rejected",
        "case_type": "missing_required_field",
        "source_type": "controlled_uploaded_frame",
        "source_origin": "broken_upload_fixture",
        "task_context_ref": "task.notice_read",
        "location_context_ref": "loc.upload_zone",
        "pose_or_view_context_ref": "pose.upload",
        "device_context_ref": "device.upload",
        "privacy_tags": [],
        "quality_level": "GOOD",
        "freshness_status": "fresh",
        "ttl_policy_ref": "ttl.upload.short",
        "storage_policy_candidate": "restricted_ephemeral_only",
        "source_chain_present": True,
        "timestamp_present": True,
        "accepted_for_downstream": False,
        "restricted_use_required": False,
        "archive_only": False,
        "allow_scene_sketch": False,
        "allow_visual_focus": False,
        "allow_ocr_via_focus": False,
        "allow_tracking_via_focus": False,
        "allow_world_observation": False,
        "debug_artifact_allowed": False,
    },
    {
        "dryrun_case_id": "case_live_camera_attempt_blocked",
        "scenario_id": "live_camera_attempt_blocked",
        "case_type": "runtime_blocked_source",
        "source_type": "live_camera_placeholder",
        "source_origin": "runtime_request_placeholder",
        "task_context_ref": "task.runtime_probe",
        "location_context_ref": "loc.none",
        "pose_or_view_context_ref": "pose.none",
        "device_context_ref": "device.camera0",
        "privacy_tags": ["bystander_presence"],
        "quality_level": "UNKNOWN_MARKED",
        "freshness_status": "unknown_marked",
        "ttl_policy_ref": "ttl.none",
        "storage_policy_candidate": "blocked",
        "source_chain_present": True,
        "timestamp_present": True,
        "accepted_for_downstream": False,
        "restricted_use_required": False,
        "archive_only": False,
        "allow_scene_sketch": False,
        "allow_visual_focus": False,
        "allow_ocr_via_focus": False,
        "allow_tracking_via_focus": False,
        "allow_world_observation": False,
        "debug_artifact_allowed": False,
    },
    {
        "dryrun_case_id": "case_device_camera_attempt_blocked",
        "scenario_id": "device_camera_attempt_blocked",
        "case_type": "runtime_blocked_source",
        "source_type": "device_camera_placeholder",
        "source_origin": "device_camera_placeholder",
        "task_context_ref": "task.runtime_probe",
        "location_context_ref": "loc.none",
        "pose_or_view_context_ref": "pose.none",
        "device_context_ref": "device.camera_user",
        "privacy_tags": ["bystander_presence"],
        "quality_level": "UNKNOWN_MARKED",
        "freshness_status": "unknown_marked",
        "ttl_policy_ref": "ttl.none",
        "storage_policy_candidate": "blocked",
        "source_chain_present": True,
        "timestamp_present": True,
        "accepted_for_downstream": False,
        "restricted_use_required": False,
        "archive_only": False,
        "allow_scene_sketch": False,
        "allow_visual_focus": False,
        "allow_ocr_via_focus": False,
        "allow_tracking_via_focus": False,
        "allow_world_observation": False,
        "debug_artifact_allowed": False,
    },
    {
        "dryrun_case_id": "case_external_stream_attempt_blocked",
        "scenario_id": "external_stream_attempt_blocked",
        "case_type": "runtime_blocked_source",
        "source_type": "external_stream_placeholder",
        "source_origin": "external_stream_placeholder",
        "task_context_ref": "task.runtime_probe",
        "location_context_ref": "loc.none",
        "pose_or_view_context_ref": "pose.none",
        "device_context_ref": "device.external_stream",
        "privacy_tags": ["bystander_presence"],
        "quality_level": "UNKNOWN_MARKED",
        "freshness_status": "unknown_marked",
        "ttl_policy_ref": "ttl.none",
        "storage_policy_candidate": "blocked",
        "source_chain_present": True,
        "timestamp_present": True,
        "accepted_for_downstream": False,
        "restricted_use_required": False,
        "archive_only": False,
        "allow_scene_sketch": False,
        "allow_visual_focus": False,
        "allow_ocr_via_focus": False,
        "allow_tracking_via_focus": False,
        "allow_world_observation": False,
        "debug_artifact_allowed": False,
    },
    {
        "dryrun_case_id": "case_stale_frame_archive_only",
        "scenario_id": "stale_frame_archive_only",
        "case_type": "stale_frame",
        "source_type": "archived_frame_candidate",
        "source_origin": "archive_placeholder",
        "task_context_ref": "task.review_old_frame",
        "location_context_ref": "loc.old_segment",
        "pose_or_view_context_ref": "pose.archive",
        "device_context_ref": "device.archive",
        "privacy_tags": ["commercial_sensitive_candidate"],
        "quality_level": "GOOD",
        "freshness_status": "expired",
        "ttl_policy_ref": "ttl.archive.expired",
        "storage_policy_candidate": "archive_only",
        "source_chain_present": True,
        "timestamp_present": True,
        "accepted_for_downstream": True,
        "restricted_use_required": False,
        "archive_only": True,
        "allow_scene_sketch": False,
        "allow_visual_focus": False,
        "allow_ocr_via_focus": False,
        "allow_tracking_via_focus": False,
        "allow_world_observation": False,
        "debug_artifact_allowed": True,
    },
    {
        "dryrun_case_id": "case_frame_with_text_requires_visual_focus_for_ocr",
        "scenario_id": "frame_with_text_requires_visual_focus_for_ocr",
        "case_type": "text_hint_frame",
        "source_type": "static_test_image",
        "source_origin": "text_placeholder_fixture",
        "task_context_ref": "task.read_signage",
        "location_context_ref": "loc.signage_zone",
        "pose_or_view_context_ref": "pose.front_sign",
        "device_context_ref": "device.test_fixture",
        "privacy_tags": ["commercial_sensitive_candidate"],
        "quality_level": "GOOD",
        "freshness_status": "fresh",
        "ttl_policy_ref": "ttl.standard.short",
        "storage_policy_candidate": "ephemeral_review_only",
        "source_chain_present": True,
        "timestamp_present": True,
        "accepted_for_downstream": True,
        "restricted_use_required": False,
        "archive_only": False,
        "allow_scene_sketch": True,
        "allow_visual_focus": True,
        "allow_ocr_via_focus": True,
        "allow_tracking_via_focus": False,
        "allow_world_observation": True,
        "debug_artifact_allowed": True,
    },
    {
        "dryrun_case_id": "case_frame_with_motion_requires_visual_focus_for_tracking",
        "scenario_id": "frame_with_motion_requires_visual_focus_for_tracking",
        "case_type": "motion_hint_frame",
        "source_type": "pre_recorded_video_frame",
        "source_origin": "motion_placeholder_fixture",
        "task_context_ref": "task.track_moving_target",
        "location_context_ref": "loc.route_edge",
        "pose_or_view_context_ref": "pose.follow_side",
        "device_context_ref": "device.test_fixture",
        "privacy_tags": ["bystander_presence"],
        "quality_level": "GOOD",
        "freshness_status": "fresh",
        "ttl_policy_ref": "ttl.standard.short",
        "storage_policy_candidate": "ephemeral_review_only",
        "source_chain_present": True,
        "timestamp_present": True,
        "accepted_for_downstream": True,
        "restricted_use_required": False,
        "archive_only": False,
        "allow_scene_sketch": True,
        "allow_visual_focus": True,
        "allow_ocr_via_focus": False,
        "allow_tracking_via_focus": True,
        "allow_world_observation": True,
        "debug_artifact_allowed": True,
    },
    {
        "dryrun_case_id": "case_dual_device_placeholder_review_only",
        "scenario_id": "dual_device_placeholder_review_only",
        "case_type": "placeholder_review_only",
        "source_type": "simulation_frame",
        "source_origin": "placeholder_review",
        "task_context_ref": "task.placeholder_review",
        "location_context_ref": "loc.none",
        "pose_or_view_context_ref": "pose.none",
        "device_context_ref": "device.placeholder",
        "privacy_tags": ["commercial_sensitive_candidate"],
        "quality_level": "UNKNOWN_MARKED",
        "freshness_status": "unknown_marked",
        "ttl_policy_ref": "ttl.none",
        "storage_policy_candidate": "review_only",
        "source_chain_present": True,
        "timestamp_present": True,
        "accepted_for_downstream": False,
        "restricted_use_required": False,
        "archive_only": False,
        "allow_scene_sketch": False,
        "allow_visual_focus": False,
        "allow_ocr_via_focus": False,
        "allow_tracking_via_focus": False,
        "allow_world_observation": False,
        "debug_artifact_allowed": True,
    },
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
        "dryrun_scope": DRYRUN_SCOPE,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "frame_content_loaded": False,
        "actual_image_read": False,
        "live_camera_allowed": False,
        "device_camera_allowed": False,
        "external_stream_allowed": False,
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
        "dual_device_runtime_invoked": False,
        "dual_model_runtime_invoked": False,
        "failover_runtime_invoked": False,
        "multi_input_fusion_runtime_invoked": False,
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


def _schema(name: str, fields: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"schema_name": name, "field_specs": fields, "source_chain": SOURCE_CHAIN, **_not_fact()}


def _simulated_metadata(case: Dict[str, Any]) -> Dict[str, Any]:
    frame_timestamp = f"2026-05-26T16:{len(case['dryrun_case_id']) % 60:02d}:00Z" if case["timestamp_present"] else ""
    source_chain = SOURCE_CHAIN if case["source_chain_present"] else ""
    return {
        "frame_id": f"{case['scenario_id']}_frame_001",
        "source_type": case["source_type"],
        "source_origin": case["source_origin"],
        "frame_timestamp": frame_timestamp,
        "monotonic_seq": len(case["scenario_id"]),
        "source_chain": source_chain,
        "privacy_tags": case["privacy_tags"],
        "task_context_ref": case["task_context_ref"],
        "location_context_ref": case["location_context_ref"],
        "pose_or_view_context_ref": case["pose_or_view_context_ref"],
        "device_context_ref": case["device_context_ref"],
        "simulated_quality_profile": case["quality_level"],
        "freshness_profile": case["freshness_status"],
        "ttl_policy_ref": case["ttl_policy_ref"],
        "storage_policy_candidate": case["storage_policy_candidate"],
        "frame_content_loaded": False,
        "actual_image_read": False,
        "visual_model_invoked": False,
        **_not_fact(),
    }


def _intake_status(case: Dict[str, Any], metadata: Dict[str, Any]) -> str:
    if case["source_type"] == "live_camera_placeholder":
        return "rejected_live_camera"
    if case["source_type"] == "device_camera_placeholder":
        return "rejected_device_camera"
    if case["source_type"] == "external_stream_placeholder":
        return "rejected_external_stream"
    if case["source_type"] not in {
        "static_test_image",
        "pre_recorded_video_frame",
        "simulation_frame",
        "controlled_uploaded_frame",
        "archived_frame_candidate",
    } and case["case_type"] != "placeholder_review_only":
        return "rejected_unknown_source"
    if not metadata["source_chain"]:
        return "rejected_missing_source_chain"
    if not metadata["frame_timestamp"]:
        return "rejected_missing_timestamp"
    if not metadata["privacy_tags"]:
        return "rejected_missing_privacy_tags"
    return "accepted_candidate"


def _quality_decision(case: Dict[str, Any], intake_status: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
    if intake_status != "accepted_candidate":
        level = "BLOCKED"
    else:
        level = case["quality_level"]
    presets = {
        "GOOD": dict(
            scene_sketch_allowed_candidate=case["allow_scene_sketch"],
            visual_focus_allowed_candidate=case["allow_visual_focus"],
            ocr_activation_allowed_candidate=False,
            tracking_request_allowed_candidate=False,
            world_observation_allowed_candidate=case["allow_world_observation"],
            active_view_adjustment_recommended=False,
            safety_only_recommended=False,
            reject_reason="",
        ),
        "DEGRADED": dict(
            scene_sketch_allowed_candidate=case["allow_scene_sketch"],
            visual_focus_allowed_candidate=case["allow_visual_focus"],
            ocr_activation_allowed_candidate=False,
            tracking_request_allowed_candidate=False,
            world_observation_allowed_candidate=case["allow_world_observation"],
            active_view_adjustment_recommended=True,
            safety_only_recommended=False,
            reject_reason="quality degraded; precision downstream suppressed",
        ),
        "POOR": dict(
            scene_sketch_allowed_candidate=False,
            visual_focus_allowed_candidate=False,
            ocr_activation_allowed_candidate=False,
            tracking_request_allowed_candidate=False,
            world_observation_allowed_candidate=False,
            active_view_adjustment_recommended=True,
            safety_only_recommended=True,
            reject_reason="quality poor; task downstream blocked",
        ),
        "BLOCKED": dict(
            scene_sketch_allowed_candidate=False,
            visual_focus_allowed_candidate=False,
            ocr_activation_allowed_candidate=False,
            tracking_request_allowed_candidate=False,
            world_observation_allowed_candidate=False,
            active_view_adjustment_recommended=False,
            safety_only_recommended=False,
            reject_reason="frame blocked before quality downstream",
        ),
        "UNKNOWN_MARKED": dict(
            scene_sketch_allowed_candidate=False,
            visual_focus_allowed_candidate=False,
            ocr_activation_allowed_candidate=False,
            tracking_request_allowed_candidate=False,
            world_observation_allowed_candidate=False,
            active_view_adjustment_recommended=False,
            safety_only_recommended=False,
            reject_reason="quality unknown but marked",
        ),
    }
    return {
        "quality_decision_id": f"{case['scenario_id']}_quality",
        "source_case_id": case["dryrun_case_id"],
        "frame_id": metadata["frame_id"],
        "quality_level": level,
        **presets[level],
        "fact_status": "not_fact",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _privacy_decision(case: Dict[str, Any], intake_status: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
    tags = set(metadata["privacy_tags"])
    tags_present = bool(tags)
    restricted = bool(
        tags
        & {
            "private_space_candidate",
            "home_context_candidate",
            "medical_context_candidate",
            "school_or_child_context_candidate",
            "workplace_context_candidate",
            "screen_or_document_visible",
        }
    )
    downstream_allowed = intake_status == "accepted_candidate" and tags_present and not restricted
    risk_level = "HIGH" if restricted else ("MEDIUM" if tags_present else "BLOCKED")
    return {
        "privacy_decision_id": f"{case['scenario_id']}_privacy",
        "source_case_id": case["dryrun_case_id"],
        "frame_id": metadata["frame_id"],
        "privacy_tags_present": tags_present,
        "privacy_risk_level": risk_level,
        "downstream_allowed_candidate": downstream_allowed,
        "restricted_use_required": restricted,
        "long_term_storage_allowed": False,
        "worldmodel_handoff_allowed_candidate": False,
        "memory_handoff_allowed_candidate": False,
        "fact_status": "not_fact",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _freshness_decision(case: Dict[str, Any], metadata: Dict[str, Any]) -> Dict[str, Any]:
    freshness = case["freshness_status"]
    current_action_allowed = False
    archive_allowed = freshness in {"stale", "expired"}
    stale_blocks = freshness in {"stale", "expired"}
    expired_blocks = freshness == "expired"
    return {
        "freshness_decision_id": f"{case['scenario_id']}_freshness",
        "source_case_id": case["dryrun_case_id"],
        "frame_id": metadata["frame_id"],
        "freshness_status": freshness,
        "ttl_policy_ref": case["ttl_policy_ref"],
        "current_action_allowed": current_action_allowed,
        "archive_candidate_allowed": archive_allowed,
        "stale_blocks_task_feedback": stale_blocks,
        "expired_blocks_current_action": expired_blocks,
        "fact_status": "not_fact",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _downstream_handoff(
    case: Dict[str, Any],
    metadata: Dict[str, Any],
    intake_status: str,
    quality: Dict[str, Any],
    privacy: Dict[str, Any],
    freshness: Dict[str, Any],
) -> Dict[str, Any]:
    accepted = intake_status == "accepted_candidate"
    base_allowed = accepted and privacy["downstream_allowed_candidate"] and not freshness["expired_blocks_current_action"]
    visual_focus_allowed = base_allowed and quality["visual_focus_allowed_candidate"]
    scene_sketch_allowed = base_allowed and quality["scene_sketch_allowed_candidate"]
    world_observation_allowed = base_allowed and quality["world_observation_allowed_candidate"] and case["allow_world_observation"]
    ocr_allowed = visual_focus_allowed and case["allow_ocr_via_focus"]
    tracking_allowed = visual_focus_allowed and case["allow_tracking_via_focus"]
    debug_allowed = accepted and case["debug_artifact_allowed"]
    if case["archive_only"]:
        scene_sketch_allowed = False
        visual_focus_allowed = False
        world_observation_allowed = False
        ocr_allowed = False
        tracking_allowed = False
    blocked = []
    for name, flag in (
        ("view_quality_candidate", accepted),
        ("scene_sketch_input", scene_sketch_allowed),
        ("visual_focus_input", visual_focus_allowed),
        ("ocr_activation_input", ocr_allowed),
        ("tracking_request_input", tracking_allowed),
        ("world_observation_input", world_observation_allowed),
        ("debug_review_artifact", debug_allowed),
    ):
        if not flag:
            blocked.append(name)
    return {
        "handoff_candidate_id": f"{case['scenario_id']}_handoff",
        "source_case_id": case["dryrun_case_id"],
        "frame_id": metadata["frame_id"],
        "view_quality_candidate_allowed": accepted,
        "scene_sketch_input_allowed": scene_sketch_allowed,
        "visual_focus_input_allowed": visual_focus_allowed,
        "ocr_activation_input_allowed": ocr_allowed,
        "tracking_request_input_allowed": tracking_allowed,
        "world_observation_input_allowed": world_observation_allowed,
        "debug_review_artifact_allowed": debug_allowed,
        "blocked_downstream_targets": blocked,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def run_controlled_frame_input_dryrun_v1(
    *,
    controlled_frame_input_planning_root: str,
    map_location_readonly_context_root: str,
    post_vision_strengthening_roadmap_decision_root: str,
    vision_strengthening_closure_root: str,
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
    controlled_frame_input_planning_input_loaded = (
        roots["controlled_frame_input_planning"]["loaded"]
        and summaries["controlled_frame_input_planning"].get("final_decision") == PLANNING_DECISION
    )
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

    planning_placeholder = (
        _read_json(roots["controlled_frame_input_planning"]["root"] / "dual_device_redundant_perception_placeholder.json")
        if roots["controlled_frame_input_planning"]["root"]
        else {}
    )

    dryrun_case_schema = _schema(
        "ControlledFrameInputDryRunCase",
        [
            _field("dryrun_case_id", "string", True),
            _field("case_type", "string", True),
            _field("simulated_frame_source", "string", True),
            _field("simulated_frame_metadata", "object", True),
            _field("expected_intake_decision", "string", True),
            _field("expected_quality_decision", "string", True),
            _field("expected_privacy_decision", "string", True),
            _field("expected_freshness_decision", "string", True),
            _field("expected_downstream_handoff", "object", True),
            _field("expected_boundary_flags", "object", True),
            _field("source_chain", "string", True, default=SOURCE_CHAIN),
        ],
    )
    simulated_frame_metadata_schema = _schema(
        "SimulatedFrameMetadata",
        [
            _field("frame_id", "string", True),
            _field("source_type", "string", True),
            _field("source_origin", "string", True),
            _field("frame_timestamp", "string", True),
            _field("monotonic_seq", "integer", True),
            _field("source_chain", "string", True),
            _field("privacy_tags", "list", True),
            _field("task_context_ref", "string", True),
            _field("location_context_ref", "string", True),
            _field("pose_or_view_context_ref", "string", True),
            _field("device_context_ref", "string", True),
            _field("simulated_quality_profile", "string", True),
            _field("freshness_profile", "string", True),
            _field("ttl_policy_ref", "string", True),
            _field("storage_policy_candidate", "string", True),
            _field("frame_content_loaded", "boolean", True, default=False),
            _field("actual_image_read", "boolean", True, default=False),
            _field("visual_model_invoked", "boolean", True, default=False),
        ],
    )
    frame_intake_decision_candidate_schema = _schema(
        "FrameIntakeDecisionCandidate",
        [
            _field("intake_decision_id", "string", True),
            _field("source_case_id", "string", True),
            _field("frame_id", "string", True),
            _field("intake_status", "string", True),
            _field("accepted_for_downstream_candidate", "boolean", True),
            _field("blocked_reason", "string", False),
            _field("required_missing_fields", "list", True),
            _field("live_runtime_blocked", "boolean", True),
            _field("privacy_gate_required", "boolean", True),
            _field("source_chain_valid", "boolean", True),
            _field("timestamp_valid", "boolean", True),
            _field("fact_status", "string", True, default="not_fact"),
            _field("source_chain", "string", True, default=SOURCE_CHAIN),
        ],
    )
    frame_quality_decision_candidate_schema = _schema(
        "FrameQualityDecisionCandidate",
        [
            _field("quality_decision_id", "string", True),
            _field("source_case_id", "string", True),
            _field("frame_id", "string", True),
            _field("quality_level", "string", True),
            _field("scene_sketch_allowed_candidate", "boolean", True),
            _field("visual_focus_allowed_candidate", "boolean", True),
            _field("ocr_activation_allowed_candidate", "boolean", True),
            _field("tracking_request_allowed_candidate", "boolean", True),
            _field("world_observation_allowed_candidate", "boolean", True),
            _field("active_view_adjustment_recommended", "boolean", True),
            _field("safety_only_recommended", "boolean", True),
            _field("reject_reason", "string", False),
            _field("fact_status", "string", True, default="not_fact"),
            _field("source_chain", "string", True, default=SOURCE_CHAIN),
        ],
    )
    frame_privacy_decision_candidate_schema = _schema(
        "FramePrivacyDecisionCandidate",
        [
            _field("privacy_decision_id", "string", True),
            _field("source_case_id", "string", True),
            _field("frame_id", "string", True),
            _field("privacy_tags_present", "boolean", True),
            _field("privacy_risk_level", "string", True),
            _field("downstream_allowed_candidate", "boolean", True),
            _field("restricted_use_required", "boolean", True),
            _field("long_term_storage_allowed", "boolean", True, default=False),
            _field("worldmodel_handoff_allowed_candidate", "boolean", True),
            _field("memory_handoff_allowed_candidate", "boolean", True),
            _field("fact_status", "string", True, default="not_fact"),
            _field("source_chain", "string", True, default=SOURCE_CHAIN),
        ],
    )
    frame_freshness_decision_candidate_schema = _schema(
        "FrameFreshnessDecisionCandidate",
        [
            _field("freshness_decision_id", "string", True),
            _field("source_case_id", "string", True),
            _field("frame_id", "string", True),
            _field("freshness_status", "string", True),
            _field("ttl_policy_ref", "string", True),
            _field("current_action_allowed", "boolean", True, default=False),
            _field("archive_candidate_allowed", "boolean", True),
            _field("stale_blocks_task_feedback", "boolean", True),
            _field("expired_blocks_current_action", "boolean", True),
            _field("fact_status", "string", True, default="not_fact"),
            _field("source_chain", "string", True, default=SOURCE_CHAIN),
        ],
    )
    frame_downstream_handoff_candidate_schema = _schema(
        "FrameDownstreamHandoffCandidate",
        [
            _field("handoff_candidate_id", "string", True),
            _field("source_case_id", "string", True),
            _field("frame_id", "string", True),
            _field("view_quality_candidate_allowed", "boolean", True),
            _field("scene_sketch_input_allowed", "boolean", True),
            _field("visual_focus_input_allowed", "boolean", True),
            _field("ocr_activation_input_allowed", "boolean", True),
            _field("tracking_request_input_allowed", "boolean", True),
            _field("world_observation_input_allowed", "boolean", True),
            _field("debug_review_artifact_allowed", "boolean", True),
            _field("blocked_downstream_targets", "list", True),
            _field("source_chain", "string", True, default=SOURCE_CHAIN),
        ],
    )
    controlled_frame_input_dryrun_result_schema = _schema(
        "ControlledFrameInputDryRunResult",
        [
            _field("result_id", "string", True),
            _field("source_case_id", "string", True),
            _field("intake_decision_ref", "string", True),
            _field("quality_decision_ref", "string", True),
            _field("privacy_decision_ref", "string", True),
            _field("freshness_decision_ref", "string", True),
            _field("downstream_handoff_ref", "string", True),
            _field("boundary_decision_ref", "string", True),
            _field("dryrun_status", "string", True),
            _field("violations", "list", True),
            _field("source_chain", "string", True, default=SOURCE_CHAIN),
        ],
    )

    scenario_rows = []
    intake_rows = []
    quality_rows = []
    privacy_rows = []
    freshness_rows = []
    handoff_rows = []
    result_rows = []

    for case in DRYRUN_CASES:
        metadata = _simulated_metadata(case)
        intake_status = _intake_status(case, metadata)
        missing_fields = []
        if not metadata["source_chain"]:
            missing_fields.append("source_chain")
        if not metadata["frame_timestamp"]:
            missing_fields.append("frame_timestamp")
        if not metadata["privacy_tags"]:
            missing_fields.append("privacy_tags")
        blocked_reason = intake_status if intake_status != "accepted_candidate" else ""
        intake = {
            "intake_decision_id": f"{case['scenario_id']}_intake",
            "source_case_id": case["dryrun_case_id"],
            "frame_id": metadata["frame_id"],
            "intake_status": intake_status,
            "accepted_for_downstream_candidate": intake_status == "accepted_candidate",
            "blocked_reason": blocked_reason,
            "required_missing_fields": missing_fields,
            "live_runtime_blocked": case["source_type"] in {"live_camera_placeholder", "device_camera_placeholder", "external_stream_placeholder"},
            "privacy_gate_required": True,
            "source_chain_valid": bool(metadata["source_chain"]),
            "timestamp_valid": bool(metadata["frame_timestamp"]),
            "fact_status": "not_fact",
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }
        quality = _quality_decision(case, intake_status, metadata)
        privacy = _privacy_decision(case, intake_status, metadata)
        freshness = _freshness_decision(case, metadata)
        handoff = _downstream_handoff(case, metadata, intake_status, quality, privacy, freshness)

        if case["case_type"] == "placeholder_review_only":
            dryrun_status = "review_only_candidate"
        elif intake_status != "accepted_candidate":
            dryrun_status = "rejected_candidate"
        elif privacy["restricted_use_required"]:
            dryrun_status = "restricted_candidate"
        elif case["archive_only"]:
            dryrun_status = "archive_only_candidate"
        else:
            dryrun_status = "accepted_candidate"

        result = {
            "result_id": f"{case['scenario_id']}_result",
            "source_case_id": case["dryrun_case_id"],
            "intake_decision_ref": intake["intake_decision_id"],
            "quality_decision_ref": quality["quality_decision_id"],
            "privacy_decision_ref": privacy["privacy_decision_id"],
            "freshness_decision_ref": freshness["freshness_decision_id"],
            "downstream_handoff_ref": handoff["handoff_candidate_id"],
            "boundary_decision_ref": "controlled_frame_input_boundary_matrix.json",
            "dryrun_status": dryrun_status,
            "violations": [],
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }

        scenario_rows.append(
            {
                "dryrun_case_id": case["dryrun_case_id"],
                "case_type": case["case_type"],
                "simulated_frame_source": case["source_type"],
                "simulated_frame_metadata": metadata,
                "expected_intake_decision": intake_status,
                "expected_quality_decision": quality["quality_level"],
                "expected_privacy_decision": privacy["privacy_risk_level"],
                "expected_freshness_decision": freshness["freshness_status"],
                "expected_downstream_handoff": {
                    "view_quality_candidate_allowed": handoff["view_quality_candidate_allowed"],
                    "scene_sketch_input_allowed": handoff["scene_sketch_input_allowed"],
                    "visual_focus_input_allowed": handoff["visual_focus_input_allowed"],
                    "ocr_activation_input_allowed": handoff["ocr_activation_input_allowed"],
                    "tracking_request_input_allowed": handoff["tracking_request_input_allowed"],
                    "world_observation_input_allowed": handoff["world_observation_input_allowed"],
                    "debug_review_artifact_allowed": handoff["debug_review_artifact_allowed"],
                },
                "expected_boundary_flags": {
                    "frame_content_loaded": False,
                    "actual_image_read": False,
                    "visual_model_invoked": False,
                    "navigation_action_triggered": False,
                    "world_model_written": False,
                },
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
        intake_rows.append(intake)
        quality_rows.append(quality)
        privacy_rows.append(privacy)
        freshness_rows.append(freshness)
        handoff_rows.append(handoff)
        result_rows.append(result)

    dual_device_placeholder_dryrun_review = {
        "dual_device_placeholder_loaded": bool(planning_placeholder),
        "perception_input_channel_placeholder_present": bool(planning_placeholder.get("perception_input_channel_placeholder")),
        "perception_device_health_placeholder_present": bool(planning_placeholder.get("perception_device_health_placeholder")),
        "perception_lane_failover_placeholder_present": bool(planning_placeholder.get("perception_lane_failover_placeholder")),
        "dual_input_consistency_placeholder_present": bool(planning_placeholder.get("dual_input_consistency_placeholder")),
        "dual_device_runtime_allowed": False,
        "dual_model_runtime_allowed": False,
        "failover_runtime_allowed": False,
        "automatic_hardware_switch_allowed": False,
        "multi_input_fusion_runtime_allowed": False,
        "hardware_stage_deferred": True,
        "verdict": "GO" if planning_placeholder else "NO_GO",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    accepted_candidate_count = sum(1 for row in result_rows if row["dryrun_status"] == "accepted_candidate")
    rejected_candidate_count = sum(1 for row in result_rows if row["dryrun_status"] == "rejected_candidate")
    restricted_candidate_count = sum(1 for row in result_rows if row["dryrun_status"] == "restricted_candidate")
    stale_archive_only_candidate_count = sum(1 for row in result_rows if row["dryrun_status"] == "archive_only_candidate")

    controlled_frame_input_dryrun_results = {
        "results": result_rows,
        "intake_decisions": intake_rows,
        "quality_decisions": quality_rows,
        "privacy_decisions": privacy_rows,
        "freshness_decisions": freshness_rows,
        "downstream_handoffs": handoff_rows,
        "result_count": len(result_rows),
        "accepted_candidate_count": accepted_candidate_count,
        "rejected_candidate_count": rejected_candidate_count,
        "restricted_candidate_count": restricted_candidate_count,
        "stale_archive_only_candidate_count": stale_archive_only_candidate_count,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    controlled_frame_input_boundary_matrix = {
        "dryrun_scope": DRYRUN_SCOPE,
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
        "live_camera_allowed": False,
        "device_camera_allowed": False,
        "external_stream_allowed": False,
        "dual_device_runtime_allowed": False,
        "dual_model_runtime_allowed": False,
        "failover_runtime_allowed": False,
        "automatic_hardware_switch_allowed": False,
        "multi_input_fusion_runtime_allowed": False,
        "hardware_stage_deferred": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_register = {
        "carryover_topics": [
            {
                "topic": topic,
                "impact": "must remain visible before post-dryrun review and any narrower real-file trial discussion",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for topic in [
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
                "dual-device placeholder misuse risk",
            ]
        ],
        "future_midplatform_function_governance_required": True,
        "no_duplicate_governance_module_allowed": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE,
        "final_decision": FINAL_DECISION,
        "reason": "controlled frame metadata dryrun chain is validated; next step is post-dryrun review only",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers = []
    if not all(
        [
            controlled_frame_input_planning_input_loaded,
            map_location_readonly_context_input_loaded,
            post_vision_strengthening_roadmap_decision_input_loaded,
            vision_strengthening_closure_input_loaded,
            task_aware_visual_focus_input_loaded,
            midplatform_perception_orchestration_input_loaded,
            minimal_runtime_integration_closure_loaded,
            ocr_final_closure_loaded,
            dual_device_placeholder_dryrun_review["dual_device_placeholder_loaded"],
        ]
    ):
        blockers.append("required_root_missing_or_invalid")

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "controlled_frame_input_planning_input_loaded": controlled_frame_input_planning_input_loaded,
        "map_location_readonly_context_input_loaded": map_location_readonly_context_input_loaded,
        "post_vision_strengthening_roadmap_decision_input_loaded": post_vision_strengthening_roadmap_decision_input_loaded,
        "vision_strengthening_closure_input_loaded": vision_strengthening_closure_input_loaded,
        "task_aware_visual_focus_input_loaded": task_aware_visual_focus_input_loaded,
        "midplatform_perception_orchestration_input_loaded": midplatform_perception_orchestration_input_loaded,
        "minimal_runtime_integration_closure_loaded": minimal_runtime_integration_closure_loaded,
        "ocr_final_closure_loaded": ocr_final_closure_loaded,
        "dryrun_case_schema_defined": True,
        "simulated_frame_metadata_schema_defined": True,
        "frame_intake_decision_candidate_schema_defined": True,
        "frame_quality_decision_candidate_schema_defined": True,
        "frame_privacy_decision_candidate_schema_defined": True,
        "frame_freshness_decision_candidate_schema_defined": True,
        "frame_downstream_handoff_candidate_schema_defined": True,
        "controlled_frame_input_dryrun_result_schema_defined": True,
        "dual_device_placeholder_dryrun_review_generated": True,
        "scenario_matrix_generated": True,
        "scenario_count": len(DRYRUN_CASES),
        "dryrun_results_generated": True,
        "accepted_candidate_count": accepted_candidate_count,
        "rejected_candidate_count": rejected_candidate_count,
        "restricted_candidate_count": restricted_candidate_count,
        "stale_archive_only_candidate_count": stale_archive_only_candidate_count,
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
        "live_camera_allowed": False,
        "device_camera_allowed": False,
        "external_stream_allowed": False,
        "dual_device_redundant_perception_placeholder_loaded": dual_device_placeholder_dryrun_review["dual_device_placeholder_loaded"],
        "dual_device_runtime_allowed": False,
        "dual_model_runtime_allowed": False,
        "failover_runtime_allowed": False,
        "automatic_hardware_switch_allowed": False,
        "multi_input_fusion_runtime_allowed": False,
        "hardware_stage_deferred": True,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "frame_content_loaded": False,
        "actual_image_read": False,
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
        "dual_device_runtime_invoked": False,
        "dual_model_runtime_invoked": False,
        "failover_runtime_invoked": False,
        "multi_input_fusion_runtime_invoked": False,
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
        "final_decision": FINAL_DECISION if not blockers else "CONTROLLED_FRAME_INPUT_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if not blockers else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "dryrun_case_schema": dryrun_case_schema,
        "simulated_frame_metadata_schema": simulated_frame_metadata_schema,
        "frame_intake_decision_candidate_schema": frame_intake_decision_candidate_schema,
        "frame_quality_decision_candidate_schema": frame_quality_decision_candidate_schema,
        "frame_privacy_decision_candidate_schema": frame_privacy_decision_candidate_schema,
        "frame_freshness_decision_candidate_schema": frame_freshness_decision_candidate_schema,
        "frame_downstream_handoff_candidate_schema": frame_downstream_handoff_candidate_schema,
        "controlled_frame_input_dryrun_result_schema": controlled_frame_input_dryrun_result_schema,
        "dual_device_placeholder_dryrun_review": dual_device_placeholder_dryrun_review,
        "controlled_frame_input_dryrun_scenario_matrix": {"scenarios": scenario_rows, "scenario_count": len(scenario_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "controlled_frame_input_dryrun_results": controlled_frame_input_dryrun_results,
        "controlled_frame_input_boundary_matrix": controlled_frame_input_boundary_matrix,
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_runtime_boundary_report": _boundary_payload(),
        "no_write_boundary_report": _boundary_payload(),
    }
