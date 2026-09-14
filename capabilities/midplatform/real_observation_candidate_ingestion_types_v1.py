# -*- coding: utf-8 -*-
"""Real Observation Candidate Ingestion — types v1."""

from __future__ import annotations

from typing import Dict, Tuple

DETECTOR_OUTPUT_MOCK_FIELDS: Tuple[str, ...] = (
    "detector_output_id", "model_ref", "source_type", "frame_ref", "image_ref",
    "timestamp", "frame_width", "frame_height", "detections",
)

NORMALIZED_DETECTION_FIELDS: Tuple[str, ...] = (
    "normalized_detection_id", "source_detector_output_ref", "frame_ref", "timestamp",
    "xyxy", "label", "confidence", "class_id", "tracker_hint_id",
    "normalization_warnings", "candidate_only",
)

OBJECT_OBSERVATION_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "observation_id", "source_type", "source_ref", "model_ref", "frame_ref", "timestamp",
    "label", "confidence", "bbox", "bbox_format", "frame_width", "frame_height",
    "mask_ref", "tracker_hint_id", "tracker_id_is_hint_not_fact",
    "depth_hint", "depth_source", "depth_confidence", "depth_error_expected",
    "task_relevance_hint", "risk_hint", "validation_status", "missing_information",
    "warning_codes", "source_refs", "evidence_refs", "traceability_refs", "candidate_only",
)

INGESTION_RESULT_FIELDS: Tuple[str, ...] = (
    "ingestion_result_id", "accepted_candidates", "rejected_detections",
    "warning_summary", "missing_information", "readiness_for_field_first_core",
    "non_execution_flags",
)

DRYRUN_RESULT_FIELDS: Tuple[str, ...] = (
    "case_id", "expected_accepted_count", "actual_accepted_count",
    "expected_rejected_count", "actual_rejected_count",
    "prohibited_behavior_absent", "case_passed", "reason_codes",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "no_world_model_fact": True,
    "no_persistent_memory": True,
    "no_model_download": True,
    "no_weight_download": True,
    "no_real_inference_execution": True,
    "no_runtime_execution": True,
    "no_large_dependency_install": True,
    "tracker_id_is_hint_not_fact": True,
}

FINAL_DECISION_GO = (
    "MIDPLATFORM_REAL_OBSERVATION_CANDIDATE_INGESTION_SKELETON_READY_FOR_REAL_MODEL_SUCCESS_PATH_DRYRUN_PLANNING"
)
