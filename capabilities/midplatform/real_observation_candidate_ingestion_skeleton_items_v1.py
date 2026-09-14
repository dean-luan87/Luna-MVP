# -*- coding: utf-8 -*-
"""Real Observation Candidate Ingestion Skeleton — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

SELECTED_NEXT_PHASE = "Phase-Midplatform-Real-Model-Success-Path-DryRun-Planning-v1-001"
SELECTED_NEXT_ROUTE = "Real Model Success Path DryRun Planning"

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "model_download", "weight_download", "large_dependency_install", "yolo_execution",
        "supervision_execution", "real_camera", "real_video_stream", "real_inference",
        "tracking", "ocr", "sam", "slam", "field_simulation", "task_execution",
        "world_model_entry", "memory_candidate", "runtime", "integration_test",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "skeleton_not_real_yolo", "ingestion_not_model_download",
    "observation_candidate_not_world_model_fact", "skeleton_not_production_inference",
)

DETECTOR_OUTPUT_MOCK_CONTRACT: Dict[str, Any] = {
    "contract_id": "detector_output_mock_contract_v1",
    "source_type": "model_detector",
    "detection_fields": ("bbox_xyxy", "class_name", "class_id", "confidence", "tracker_hint_id"),
}

SUPERVISION_NORMALIZED_CONTRACT: Dict[str, Any] = {
    "contract_id": "supervision_normalized_detection_contract_v1",
    "fields": ("normalized_detection_id", "xyxy", "label", "confidence", "normalization_warnings"),
    "candidate_only": True,
}

OBJECT_OBSERVATION_CANDIDATE_CONTRACT: Dict[str, Any] = {
    "contract_id": "object_observation_candidate_contract_v1",
    "source_type": "model_detector",
    "bbox_format": "xyxy",
    "tracker_id_is_hint_not_fact": True,
    "candidate_only": True,
}

INGESTION_MAPPING: Dict[str, Any] = {
    "mapping_id": "detector_to_observation_ingestion_mapping_v1",
    "detector_bbox_xyxy": "observation.bbox",
    "class_name": "observation.label",
    "confidence": "observation.confidence",
}

DEPTH_FALLBACK_EXECUTION: Dict[str, Any] = {
    "policy_id": "depth_missing_fallback_execution_policy_v1",
    "default_depth_source": "unknown",
    "default_depth_confidence": "unknown",
    "depth_error_expected": True,
    "prohibited": ("treat_unknown_as_hardware",),
}

REJECTED_DETECTION_POLICY: Dict[str, Any] = {
    "policy_id": "rejected_detection_policy_v1",
    "reject_on": ("invalid_bbox", "missing_bbox_xyxy", "invalid_bbox_after_clip", "validation_failed"),
    "must_record_reason": True,
}


def _det(detections: tuple, **kw: Any) -> Dict[str, Any]:
    return {
        "detector_output_id": kw.get("id", "det_mock"),
        "model_ref": kw.get("model_ref", "yolo_lightweight_placeholder"),
        "source_type": "model_detector",
        "source_ref": "detector_mock",
        "frame_ref": kw.get("frame_ref", "frame_0"),
        "timestamp": "2026-06-11T00:00:00Z",
        "frame_width": kw.get("fw", 640),
        "frame_height": kw.get("fh", 480),
        "detections": list(detections),
    }


DRYRUN_MOCK_CASES: Tuple[Dict[str, Any], ...] = (
    {
        "case_id": "yolo_like_single_person_detection",
        "detector_output": _det(({"bbox_xyxy": {"x1": 100, "y1": 50, "x2": 200, "y2": 300}, "class_name": "person", "confidence": 0.92},)),
        "expected_accepted_count": 1, "expect_readiness": True,
    },
    {
        "case_id": "multiple_objects_detection",
        "detector_output": _det((
            {"bbox_xyxy": {"x1": 10, "y1": 10, "x2": 60, "y2": 150}, "class_name": "person", "confidence": 0.88},
            {"bbox_xyxy": {"x1": 200, "y1": 100, "x2": 280, "y2": 200}, "class_name": "chair", "confidence": 0.75},
            {"bbox_xyxy": {"x1": 400, "y1": 50, "x2": 480, "y2": 250}, "class_name": "door", "confidence": 0.81},
        )),
        "expected_accepted_count": 3, "expect_readiness": True,
    },
    {
        "case_id": "low_confidence_detection_retained",
        "detector_output": _det(({"bbox_xyxy": {"x1": 50, "y1": 50, "x2": 100, "y2": 120}, "class_name": "sign", "confidence": 0.28},)),
        "expected_accepted_count": 1, "expect_low_confidence_retained": True, "prohibited_silent_drop": True,
    },
    {
        "case_id": "unknown_class_label_fallback",
        "detector_output": _det(({"bbox_xyxy": {"x1": 120, "y1": 80, "x2": 180, "y2": 140}, "class_id": 99, "confidence": 0.55},)),
        "expected_accepted_count": 1, "expect_unknown_label": True,
    },
    {
        "case_id": "invalid_bbox_rejected",
        "detector_output": _det(({"bbox_xyxy": {"x1": 200, "y1": 200, "x2": 100, "y2": 100}, "class_name": "person", "confidence": 0.9},)),
        "expected_accepted_count": 0, "expected_rejected_count": 1, "expect_rejected": True,
    },
    {
        "case_id": "bbox_out_of_frame_warning",
        "detector_output": _det(({"bbox_xyxy": {"x1": 600, "y1": 400, "x2": 700, "y2": 500}, "class_name": "cup", "confidence": 0.7},), fw=640, fh=480),
        "expected_accepted_count": 1,
    },
    {
        "case_id": "depth_missing_fallback_unknown",
        "detector_output": _det(({"bbox_xyxy": {"x1": 30, "y1": 30, "x2": 90, "y2": 120}, "class_name": "person", "confidence": 0.85},)),
        "depth_source": "unknown", "expected_accepted_count": 1, "expect_depth_unknown": True,
    },
    {
        "case_id": "tracker_hint_preserved_as_hint",
        "detector_output": _det(({"bbox_xyxy": {"x1": 150, "y1": 60, "x2": 220, "y2": 280}, "class_name": "person", "confidence": 0.9, "tracker_hint_id": "track_hint_7"},)),
        "expected_accepted_count": 1, "expect_tracker_hint": True,
    },
    {
        "case_id": "supervision_normalized_input_path",
        "use_supervision_normalized_path": True,
        "supervision_output": {
            "source_detector_output_ref": "sup_1", "frame_ref": "frame_1", "timestamp": "2026-06-11T00:00:01Z",
            "frame_width": 640, "frame_height": 480,
            "xyxy": {"x1": 80, "y1": 40, "x2": 160, "y2": 200}, "label": "vehicle", "confidence": 0.87,
        },
        "expected_accepted_count": 1, "expect_readiness": True,
    },
    {
        "case_id": "ready_for_field_first_core",
        "detector_output": _det((
            {"bbox_xyxy": {"x1": 10, "y1": 10, "x2": 60, "y2": 150}, "class_name": "person", "confidence": 0.9},
            {"bbox_xyxy": {"x1": 300, "y1": 200, "x2": 380, "y2": 320}, "class_name": "obstacle", "confidence": 0.8},
        )),
        "expected_accepted_count": 2, "expect_readiness": True,
    },
)
