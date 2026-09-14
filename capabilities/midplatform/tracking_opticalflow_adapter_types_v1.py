# -*- coding: utf-8 -*-
"""Tracking / Optical Flow adapter types v1."""

from __future__ import annotations

from typing import Dict, Tuple

ADAPTER_INPUT_FIELDS: Tuple[str, ...] = (
    "adapter_input_id", "model_role", "model_ref", "execution_mode", "smoke_run_ref",
    "io_inspection_ref", "frame_input_refs", "object_observation_refs",
    "aligned_observation_refs", "enhanced_field_scene_refs", "field_geometry_refs",
    "session_ref", "authorization_ref", "source_refs", "traceability_refs", "candidate_only",
)

RAW_OUTPUT_FIELDS: Tuple[str, ...] = (
    "raw_output_id", "source_smoke_run_ref", "source_io_inspection_ref", "model_ref",
    "execution_mode", "frame_refs", "timestamp_range", "output_payload_type",
    "raw_track_payload", "raw_bbox_sequence_payload", "raw_motion_payload", "raw_flow_payload",
    "raw_quality_payload", "parseability_status", "warning_codes", "missing_information",
    "source_refs", "traceability_refs", "candidate_only",
)

OBJECT_TRACK_FIELDS: Tuple[str, ...] = (
    "object_track_candidate_id", "source_raw_output_ref", "track_id",
    "source_object_observation_refs", "frame_refs", "timestamp_range", "bbox_sequence",
    "label_hint", "track_confidence", "lifecycle_status", "lost_frame_count",
    "warning_codes", "missing_information", "source_refs", "evidence_refs",
    "traceability_refs", "candidate_only",
)

OBJECT_PERSISTENCE_FIELDS: Tuple[str, ...] = (
    "object_persistence_candidate_id", "source_track_ref", "source_object_observation_refs",
    "candidate_entity_key", "persistence_status", "observation_count", "first_seen_at",
    "last_seen_at", "persistence_confidence", "identity_stability", "conflict_refs",
    "warning_codes", "missing_information", "source_refs", "evidence_refs",
    "traceability_refs", "candidate_only",
)

MOTION_FIELDS: Tuple[str, ...] = (
    "motion_candidate_id", "source_raw_output_ref", "source_track_ref", "frame_refs",
    "timestamp_range", "motion_type", "bbox_delta", "motion_vector_summary",
    "optical_flow_summary", "relative_motion_hint", "motion_confidence", "risk_relevance_hint",
    "warning_codes", "missing_information", "source_refs", "evidence_refs",
    "traceability_refs", "candidate_only",
)

TRACKING_QUALITY_FIELDS: Tuple[str, ...] = (
    "tracking_quality_candidate_id", "source_raw_output_ref", "track_quality", "flow_quality",
    "continuity_quality", "frame_alignment_quality", "identity_switch_risk", "occlusion_risk",
    "quality_status", "blockers", "warnings", "source_refs", "traceability_refs", "candidate_only",
)

ADAPTER_RESULT_FIELDS: Tuple[str, ...] = (
    "adapter_result_id", "adapter_input_ref", "smoke_run_ref", "io_inspection_ref",
    "execution_mode", "object_track_candidates", "object_persistence_candidates",
    "motion_candidates", "tracking_quality_candidates", "accepted_output_count",
    "rejected_output_count", "missing_information", "warning_summary", "conflict_summary",
    "readiness_for_midplatform_task_collaboration",
    "readiness_for_later_world_model_candidate_assembly", "non_execution_flags",
    "source_refs", "traceability_refs", "candidate_only",
)

EXECUTION_MODES: Tuple[str, ...] = (
    "local_real_model", "local_adapter", "cached_output", "adapter_stub",
    "blocked_by_authorization", "blocked_by_missing_dependency", "blocked_by_missing_weight",
    "failed_runtime_error",
)

LIFECYCLE_STATUSES: Tuple[str, ...] = (
    "active", "tentative", "lost", "ended", "unknown",
)

PERSISTENCE_STATUSES: Tuple[str, ...] = (
    "persistent_candidate", "short_lived_candidate", "unstable_candidate",
    "conflict_candidate", "unknown",
)

MOTION_TYPES: Tuple[str, ...] = (
    "static", "moving", "approaching", "receding", "crossing", "unknown",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "no_real_tracking_execution": True,
    "no_real_opticalflow_execution": True,
    "no_model_download": True,
    "no_weight_download": True,
    "no_camera_runtime": True,
    "no_video_stream_runtime": True,
    "no_field_simulation": True,
    "no_task_reasoning": True,
    "no_task_action_output": True,
    "no_navigation_suggestion": True,
    "no_world_model_assembly": True,
    "no_world_model_candidate_generated": True,
    "no_world_model_entry_write": True,
    "no_fact_admission": True,
    "no_new_protocol_without_reason": True,
    "adapter_skeleton_only": True,
    "cached_output_not_marked_as_real_run": True,
    "adapter_stub_not_marked_as_real_run": True,
}

FINAL_DECISION_GO = (
    "MIDPLATFORM_TRACKING_OPTICALFLOW_ADAPTER_SKELETON_READY_FOR_TRACKING_OPTICALFLOW_TASK_COLLABORATION_PLANNING"
)
