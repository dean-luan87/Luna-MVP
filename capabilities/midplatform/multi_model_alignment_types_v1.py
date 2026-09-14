# -*- coding: utf-8 -*-
"""Multi-Model Alignment — types v1."""

from __future__ import annotations

from typing import Dict, Tuple

ALIGNMENT_INPUT_FIELDS: Tuple[str, ...] = (
    "input_package_id", "object_observations", "depth_observation", "optional_observations",
)

MODEL_OBSERVATION_REF_FIELDS: Tuple[str, ...] = (
    "observation_ref", "model_role", "frame_ref", "timestamp",
)

ALIGNMENT_SIGNAL_FIELDS: Tuple[str, ...] = (
    "signal_id", "frame_ref_score", "timestamp_score", "camera_ref_score",
    "frame_size_score", "model_role_presence", "overall_strength",
)

ALIGNED_OBSERVATION_FIELDS: Tuple[str, ...] = (
    "aligned_candidate_id", "alignment_group_id", "frame_ref", "timestamp", "camera_ref",
    "primary_object_observation_ref", "depth_observation_ref", "optional_observation_refs",
    "alignment_status", "alignment_confidence", "alignment_strength", "aligned_model_roles",
    "missing_model_roles", "rejected_model_outputs", "conflict_refs", "warning_codes",
    "degradation_reason_codes", "source_refs", "evidence_refs", "traceability_refs", "candidate_only",
)

ALIGNMENT_RESULT_FIELDS: Tuple[str, ...] = (
    "alignment_result_id", "aligned_candidates", "rejected_outputs",
    "missing_model_roles_summary", "conflict_summary", "warning_summary",
    "readiness_for_depth_object_fusion", "non_execution_flags", "candidate_only",
)

DRYRUN_RESULT_FIELDS: Tuple[str, ...] = (
    "case_id", "expected_aligned_count", "actual_aligned_count",
    "expected_rejected_count", "actual_rejected_count",
    "prohibited_behavior_absent", "case_passed", "reason_codes",
)

ALIGNMENT_STATUSES: Tuple[str, ...] = (
    "aligned_strong", "aligned_weak", "aligned_degraded",
    "rejected_frame_mismatch", "rejected_timestamp_gap", "rejected_camera_mismatch",
    "insufficient_alignment",
)

ALIGNMENT_STRENGTHS: Tuple[str, ...] = ("strong", "medium", "weak", "rejected")

TIMESTAMP_STRONG_GAP_SEC: float = 0.5
TIMESTAMP_WEAK_GAP_SEC: float = 1.0
TIMESTAMP_REJECT_GAP_SEC: float = 2.0

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "no_world_model_fact": True,
    "no_persistent_memory": True,
    "no_model_download": True,
    "no_weight_download": True,
    "no_real_inference_execution": True,
    "no_runtime_execution": True,
    "no_depth_object_fusion": True,
    "no_field_geometry_generation": True,
    "no_field_scene_assembly": True,
    "no_large_dependency_install": True,
}

FINAL_DECISION_GO = (
    "MIDPLATFORM_MULTI_MODEL_ALIGNMENT_SKELETON_READY_FOR_DEPTH_OBJECT_FUSION_SKELETON"
)
