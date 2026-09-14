# -*- coding: utf-8 -*-
"""Multi-Model Alignment Skeleton — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

SELECTED_NEXT_PHASE = "Phase-Midplatform-Depth-Object-Fusion-Skeleton-v1-001"
SELECTED_NEXT_ROUTE = "Depth + Object Fusion Skeleton"

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "depth_object_fusion", "field_geometry_generation", "field_scene_assembly",
        "model_download", "weight_download", "yolo_execution", "depth_model_execution",
        "ocr_execution", "tracking_execution", "segmentation_execution", "slam_runtime",
        "real_multi_model_runtime", "field_simulation", "task_execution",
        "world_model_entry", "memory_candidate", "runtime", "integration_test",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "alignment_not_fusion", "alignment_not_field_assembly",
    "aligned_candidate_not_world_model_fact", "optional_model_ref_not_fact",
)

ALIGNMENT_INPUT_CONTRACT: Dict[str, Any] = {
    "contract_id": "multi_model_alignment_input_contract_v1",
    "inputs": ("ObjectObservationCandidate", "DepthObservationCandidate", "OptionalModelObservationMock"),
    "primary_anchor": "ObjectObservationCandidate",
    "alignment_keys": ("frame_ref", "timestamp", "camera_ref", "frame_width", "frame_height"),
    "candidate_only": True,
}

ALIGNMENT_SIGNAL_REGISTRY: Dict[str, Any] = {
    "registry_id": "alignment_signal_registry_v1",
    "signals": (
        "score_frame_ref_alignment", "score_timestamp_alignment",
        "score_camera_ref_alignment", "score_frame_size_alignment", "score_model_role_presence",
    ),
    "alignment_statuses": (
        "aligned_strong", "aligned_weak", "aligned_degraded",
        "rejected_frame_mismatch", "rejected_timestamp_gap", "rejected_camera_mismatch",
        "insufficient_alignment",
    ),
    "alignment_strengths": ("strong", "medium", "weak", "rejected"),
}

ALIGNED_OBSERVATION_CANDIDATE_REGISTRY: Dict[str, Any] = {
    "registry_id": "multi_model_aligned_observation_candidate_registry_v1",
    "contract_ref": "multi_model_aligned_observation_candidate_contract_v1",
    "candidate_only": True,
}

ALIGNMENT_RESULT_CANDIDATE_REGISTRY: Dict[str, Any] = {
    "registry_id": "multi_model_alignment_result_candidate_registry_v1",
    "outputs": (
        "aligned_candidates", "rejected_outputs", "missing_model_roles_summary",
        "conflict_summary", "warning_summary", "readiness_for_depth_object_fusion",
    ),
    "candidate_only": True,
}

REJECTED_ALIGNMENT_POLICY: Dict[str, Any] = {
    "policy_id": "rejected_alignment_policy_v1",
    "reject_on": (
        "frame_ref_mismatch", "timestamp_gap_exceeds_threshold", "camera_ref_mismatch_strict",
    ),
    "degrade_on": ("timestamp_small_gap", "camera_ref_mismatch", "frame_size_mismatch"),
    "must_record": ("rejected_model_outputs", "conflict_refs", "degradation_reason_codes"),
    "missing_depth_not_reject": True,
}

MISSING_MODEL_ROLES_SUMMARY: Dict[str, Any] = {
    "summary_id": "missing_model_roles_summary_v1",
    "rules": (
        "missing_depth_keeps_object_alignment",
        "depth_without_object_insufficient_alignment",
        "optional_roles_missing_not_blocking",
    ),
}


def _obj(obs_id: str, **kw: Any) -> Dict[str, Any]:
    return {
        "observation_id": obs_id,
        "source_type": "model_detector",
        "model_ref": kw.get("model_ref", "yolo_lightweight_placeholder"),
        "frame_ref": kw.get("frame_ref", "frame_0"),
        "camera_ref": kw.get("camera_ref"),
        "timestamp": kw.get("timestamp", "2026-06-11T00:00:00Z"),
        "label": kw.get("label", "person"),
        "confidence": kw.get("confidence", 0.9),
        "bbox": kw.get("bbox", {"x1": 100, "y1": 50, "x2": 200, "y2": 300}),
        "bbox_format": "xyxy",
        "frame_width": kw.get("fw", 640),
        "frame_height": kw.get("fh", 480),
        "source_refs": [obs_id],
        "evidence_refs": [obs_id],
        "candidate_only": True,
    }


def _depth(depth_id: str, **kw: Any) -> Dict[str, Any]:
    return {
        "depth_observation_id": depth_id,
        "source_type": "model_depth_estimator",
        "model_ref": kw.get("model_ref", "depth_anything_v2_placeholder"),
        "frame_ref": kw.get("frame_ref", "frame_0"),
        "camera_ref": kw.get("camera_ref"),
        "timestamp": kw.get("timestamp", "2026-06-11T00:00:00Z"),
        "frame_width": kw.get("fw", 640),
        "frame_height": kw.get("fh", 480),
        "depth_map_ref": kw.get("depth_map_ref", "depth_map_mock_0"),
        "depth_map_shape": [480, 640],
        "depth_value_unit": "relative",
        "depth_source": "estimated",
        "depth_confidence": "medium",
        "depth_error_expected": True,
        "source_refs": [depth_id],
        "evidence_refs": [depth_id],
        "candidate_only": True,
    }


def _opt(opt_id: str, role: str, **kw: Any) -> Dict[str, Any]:
    return {
        "optional_observation_id": opt_id,
        "model_role": role,
        "frame_ref": kw.get("frame_ref", "frame_0"),
        "camera_ref": kw.get("camera_ref"),
        "timestamp": kw.get("timestamp", "2026-06-11T00:00:00Z"),
        "payload_ref": kw.get("payload_ref"),
        "source_refs": [opt_id],
        "candidate_only": True,
    }


def _pkg(objects: tuple, depth: Dict[str, Any] | None = None, optional: tuple = (), **kw: Any) -> Dict[str, Any]:
    return {
        "input_package_id": kw.get("id", "pkg_mock"),
        "object_observations": list(objects),
        "depth_observation": depth,
        "optional_observations": list(optional),
        "alignment_group_id": kw.get("group_id"),
    }


DRYRUN_MOCK_CASES: Tuple[Dict[str, Any], ...] = (
    {
        "case_id": "yolo_depth_same_frame_strong_alignment",
        "input_package": _pkg((_obj("obs_s1",),), _depth("depth_s1")),
        "expected_aligned_count": 1, "expected_rejected_count": 0,
        "expect_strong": True, "expect_readiness": True, "prohibited_fusion": True,
    },
    {
        "case_id": "frame_ref_mismatch_rejected",
        "input_package": _pkg((_obj("obs_f1", frame_ref="frame_0"),), _depth("depth_f1", frame_ref="frame_1")),
        "expected_aligned_count": 0, "expected_rejected_count": 1, "expect_frame_reject": True,
    },
    {
        "case_id": "timestamp_small_gap_weak_alignment",
        "input_package": _pkg((_obj("obs_t1", timestamp="2026-06-11T00:00:00Z"),), _depth("depth_t1", timestamp="2026-06-11T00:00:00.7Z")),
        "expected_aligned_count": 1, "expected_rejected_count": 0, "expect_ts_weak": True,
    },
    {
        "case_id": "timestamp_large_gap_rejected",
        "input_package": _pkg((_obj("obs_t2", timestamp="2026-06-11T00:00:00Z"),), _depth("depth_t2", timestamp="2026-06-11T00:00:03Z")),
        "expected_aligned_count": 0, "expected_rejected_count": 1, "expect_ts_reject": True,
    },
    {
        "case_id": "camera_ref_mismatch_degraded",
        "input_package": _pkg((_obj("obs_c1", camera_ref="cam_a"),), _depth("depth_c1", camera_ref="cam_b")),
        "expected_aligned_count": 1, "expected_rejected_count": 0, "expect_camera_degraded": True,
    },
    {
        "case_id": "frame_size_mismatch_warning",
        "input_package": _pkg((_obj("obs_fs1", fw=640, fh=480),), _depth("depth_fs1", fw=800, fh=600)),
        "expected_aligned_count": 1, "expected_rejected_count": 0, "expect_frame_size_warning": True,
    },
    {
        "case_id": "missing_depth_keeps_object_alignment",
        "input_package": _pkg((_obj("obs_md1",),), None),
        "expected_aligned_count": 1, "expected_rejected_count": 0, "expect_missing_depth": True,
    },
    {
        "case_id": "depth_without_object_insufficient_alignment",
        "input_package": _pkg((), _depth("depth_do1")),
        "expected_aligned_count": 1, "expected_rejected_count": 0, "expect_depth_only_insufficient": True,
    },
    {
        "case_id": "multiple_objects_one_depth_map",
        "input_package": _pkg((
            _obj("obs_m1", label="person"),
            _obj("obs_m2", label="chair", bbox={"x1": 200, "y1": 100, "x2": 280, "y2": 200}),
        ), _depth("depth_m1")),
        "expected_aligned_count": 2, "expected_rejected_count": 0, "expect_multiple_aligned": True, "expect_readiness": True,
    },
    {
        "case_id": "optional_tracking_hint_attached",
        "input_package": _pkg((_obj("obs_tr1",),), _depth("depth_tr1"), (_opt("opt_tr1", "tracking"),)),
        "expected_aligned_count": 1, "expected_rejected_count": 0, "expect_optional_tracking": True,
    },
    {
        "case_id": "optional_ocr_same_frame_attached",
        "input_package": _pkg((_obj("obs_ocr1",),), _depth("depth_ocr1"), (_opt("opt_ocr1", "ocr"),)),
        "expected_aligned_count": 1, "expected_rejected_count": 0, "expect_optional_ocr": True,
    },
    {
        "case_id": "conflict_summary_generated",
        "input_package": _pkg((_obj("obs_cf1", frame_ref="frame_0"),), _depth("depth_cf1", frame_ref="frame_1")),
        "expected_aligned_count": 0, "expected_rejected_count": 1, "expect_conflict_summary": True,
    },
)
