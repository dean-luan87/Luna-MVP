# -*- coding: utf-8 -*-
"""Depth Observation Candidate Ingestion Skeleton — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

SELECTED_NEXT_PHASE = "Phase-Midplatform-YOLO-Depth-Real-Field-Scene-DryRun-Planning-v1-001"
SELECTED_NEXT_ROUTE = "YOLO + Depth Real Field Scene DryRun Planning"

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "depth_model_download", "weight_download", "large_dependency_install",
        "depth_anything_v2_execution", "unidepth_execution", "metric3d_execution",
        "real_camera", "real_video_stream", "real_depth_inference",
        "slam_runtime", "scene_graph_runtime", "field_simulation",
        "task_execution", "world_model_entry", "memory_candidate",
        "runtime", "integration_test",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "skeleton_not_depth_anything_v2", "ingestion_not_depth_model_download",
    "depth_candidate_not_hardware_fact", "skeleton_not_production_depth_inference",
    "object_depth_hint_not_pseudo_3d_fact",
)

DEPTH_MODEL_OUTPUT_MOCK_CONTRACT: Dict[str, Any] = {
    "contract_id": "depth_model_output_mock_contract_v1",
    "source_type": "model_depth_estimator",
    "fields": (
        "depth_output_id", "model_ref", "frame_ref", "timestamp",
        "frame_width", "frame_height", "depth_map_ref", "depth_map_shape",
        "depth_value_unit", "depth_value_range", "global_depth_confidence",
        "depth_source", "candidate_only",
    ),
}

DEPTH_OBSERVATION_CANDIDATE_CONTRACT: Dict[str, Any] = {
    "contract_id": "depth_observation_candidate_contract_v1",
    "source_type": "model_depth_estimator",
    "depth_error_expected": True,
    "no_hardware_fact": True,
    "candidate_only": True,
}

OBJECT_DEPTH_HINT_CANDIDATE_CONTRACT: Dict[str, Any] = {
    "contract_id": "object_depth_hint_candidate_contract_v1",
    "bbox_sampling_policy": "center_median_sample",
    "depth_buckets": ("near", "middle", "far", "unknown"),
    "field_zone_hints": ("inner_zone", "working_zone", "forecast_zone", "unknown"),
    "candidate_only": True,
}

DEPTH_SAMPLING_POLICY: Dict[str, Any] = {
    "policy_id": "depth_sampling_policy_v1",
    "default_method": "center_median_sample",
    "fallback_method": "center_mean_sample",
    "invalid_bbox_reject": True,
    "alignment_keys": ("frame_ref", "timestamp"),
}

DEPTH_RELIABILITY_POLICY: Dict[str, Any] = {
    "policy_id": "depth_reliability_policy_v1",
    "estimated_depth_error_expected": True,
    "no_hardware_fact": True,
    "unreliable_confidence_threshold": 0.4,
    "missing_depth_bucket": "unknown",
    "relative_depth_confidence_cap": "medium",
}

YOLO_DEPTH_ALIGNMENT_POLICY: Dict[str, Any] = {
    "policy_id": "yolo_depth_alignment_policy_v1",
    "required_alignment": ("frame_ref", "timestamp", "frame_width", "frame_height"),
    "frame_ref_mismatch_action": "reject_object_depth_hint",
    "timestamp_gap_threshold_sec": 1.0,
    "timestamp_gap_action": "warning_and_confidence_downgrade",
    "bbox_sampling": "bbox_center_on_depth_map",
}

DEPTH_MISSING_FALLBACK_EXECUTION: Dict[str, Any] = {
    "policy_id": "depth_missing_fallback_execution_policy_v1",
    "when_depth_missing": {
        "object_depth_hint": None,
        "depth_bucket": "unknown",
        "field_zone_hint": "unknown",
        "depth_source": "unknown",
        "depth_confidence": "unknown",
        "depth_error_expected": True,
        "object_not_dropped": True,
    },
    "when_depth_unreliable": {
        "depth_confidence": "low",
        "depth_error_expected": True,
        "object_depth_hint": "retain_with_warning",
        "high_confidence_pseudo_3d_blocked": True,
    },
    "when_depth_estimated": {
        "depth_source": "estimated",
        "depth_error_expected": True,
        "not_hardware_fact": True,
    },
    "prohibited": ("treat_estimated_as_hardware", "silent_drop_object_on_unknown_depth"),
}


def _depth(**kw: Any) -> Dict[str, Any]:
    return {
        "depth_output_id": kw.get("id", "depth_mock"),
        "model_ref": kw.get("model_ref", "depth_anything_v2_placeholder"),
        "source_type": "model_depth_estimator",
        "frame_ref": kw.get("frame_ref", "frame_0"),
        "timestamp": kw.get("timestamp", "2026-06-11T00:00:00Z"),
        "frame_width": kw.get("fw", 640),
        "frame_height": kw.get("fh", 480),
        "depth_map_ref": kw.get("depth_map_ref", "depth_map_mock_0"),
        "depth_map_shape": kw.get("shape", [480, 640]),
        "depth_value_unit": kw.get("unit", "relative"),
        "depth_value_range": kw.get("dr", [0.5, 10.0]),
        "global_depth_confidence": kw.get("conf", 0.72),
        "depth_source": "estimated",
        "depth_map_samples": kw.get("samples", {}),
        "candidate_only": True,
    }


def _obs(obs_id: str, label: str, bbox: Dict[str, float], **kw: Any) -> Dict[str, Any]:
    return {
        "observation_id": obs_id,
        "frame_ref": kw.get("frame_ref", "frame_0"),
        "timestamp": kw.get("timestamp", "2026-06-11T00:00:00Z"),
        "label": label,
        "confidence": kw.get("confidence", 0.9),
        "bbox": dict(bbox),
        "bbox_format": "xyxy",
        "frame_width": kw.get("fw", 640),
        "frame_height": kw.get("fh", 480),
        "source_refs": [obs_id],
        "candidate_only": True,
    }


DRYRUN_MOCK_CASES: Tuple[Dict[str, Any], ...] = (
    {
        "case_id": "depth_output_valid_single_object",
        "depth_output": _depth(samples={"150_175": 2.0}),
        "object_observations": [_obs("obs_p1", "person", {"x1": 100, "y1": 50, "x2": 200, "y2": 300})],
        "expected_hint_count": 1, "expect_readiness": True, "expect_depth_bucket": "near",
        "expect_field_zone": "inner_zone",
    },
    {
        "case_id": "multiple_objects_depth_hints",
        "depth_output": _depth(samples={"150_175": 2.0, "240_150": 5.5, "440_150": 8.5}),
        "object_observations": [
            _obs("obs_m1", "person", {"x1": 100, "y1": 50, "x2": 200, "y2": 300}),
            _obs("obs_m2", "chair", {"x1": 200, "y1": 100, "x2": 280, "y2": 200}),
            _obs("obs_m3", "door", {"x1": 400, "y1": 50, "x2": 480, "y2": 250}),
        ],
        "expected_hint_count": 3, "expect_readiness": True,
    },
    {
        "case_id": "depth_map_missing_fallback",
        "depth_output": _depth(depth_map_ref=None, samples={}),
        "object_observations": [_obs("obs_d1", "person", {"x1": 50, "y1": 50, "x2": 120, "y2": 200})],
        "expected_hint_count": 1, "expect_depth_missing": True,
        "expect_object_not_blocked": True, "prohibited_drop_on_unknown": True,
    },
    {
        "case_id": "depth_unit_relative_warning",
        "depth_output": _depth(unit="relative", conf=0.95, samples={"150_175": 3.0}),
        "object_observations": [_obs("obs_r1", "cup", {"x1": 100, "y1": 50, "x2": 200, "y2": 300})],
        "expected_hint_count": 1, "expect_relative_warning": True,
    },
    {
        "case_id": "depth_unit_metric_allowed_but_estimated",
        "depth_output": _depth(unit="metric", dr=[0.5, 5.0], samples={"150_175": 2.5}),
        "object_observations": [_obs("obs_met1", "person", {"x1": 100, "y1": 50, "x2": 200, "y2": 300})],
        "expected_hint_count": 1, "expect_metric_estimated": True, "expect_readiness": True,
    },
    {
        "case_id": "bbox_invalid_rejected_for_depth_hint",
        "depth_output": _depth(samples={"150_175": 2.0}),
        "object_observations": [_obs("obs_inv", "person", {"x1": 200, "y1": 200, "x2": 100, "y2": 100})],
        "expected_hint_count": 0, "expected_rejected_count": 1, "expect_rejected": True,
    },
    {
        "case_id": "frame_ref_mismatch_rejected",
        "depth_output": _depth(frame_ref="frame_0", samples={"150_175": 2.0}),
        "object_observations": [_obs("obs_fm", "person", {"x1": 100, "y1": 50, "x2": 200, "y2": 300}, frame_ref="frame_1")],
        "expected_hint_count": 0, "expected_rejected_count": 1, "expect_frame_mismatch": True,
    },
    {
        "case_id": "timestamp_gap_warning",
        "depth_output": _depth(timestamp="2026-06-11T00:00:00Z", samples={"150_175": 2.0}),
        "object_observations": [_obs("obs_ts", "person", {"x1": 100, "y1": 50, "x2": 200, "y2": 300}, timestamp="2026-06-11T00:00:03Z")],
        "expected_hint_count": 1, "expect_timestamp_warning": True,
    },
    {
        "case_id": "unreliable_depth_confidence_downgrade",
        "depth_output": _depth(conf=0.25, samples={"150_175": 2.0}),
        "object_observations": [_obs("obs_unr", "person", {"x1": 100, "y1": 50, "x2": 200, "y2": 300})],
        "expected_hint_count": 1, "expect_unreliable_downgrade": True,
    },
    {
        "case_id": "field_zone_hint_assignment",
        "depth_output": _depth(dr=[0.0, 10.0], samples={"150_175": 1.0, "240_150": 5.0, "440_150": 9.0}),
        "object_observations": [
            _obs("obs_z1", "near_obj", {"x1": 100, "y1": 50, "x2": 200, "y2": 300}),
            _obs("obs_z2", "mid_obj", {"x1": 200, "y1": 100, "x2": 280, "y2": 200}),
            _obs("obs_z3", "far_obj", {"x1": 400, "y1": 50, "x2": 480, "y2": 250}),
        ],
        "expected_hint_count": 3, "expect_readiness": True,
    },
    {
        "case_id": "unknown_depth_does_not_block_object",
        "depth_output": _depth(depth_map_ref=None),
        "object_observations": [
            _obs("obs_u1", "person", {"x1": 10, "y1": 10, "x2": 60, "y2": 150}),
            _obs("obs_u2", "obstacle", {"x1": 300, "y1": 200, "x2": 380, "y2": 320}),
        ],
        "expected_hint_count": 2, "expect_depth_missing": True,
        "expect_object_not_blocked": True, "prohibited_drop_on_unknown": True,
    },
    {
        "case_id": "ready_for_field_geometry_true",
        "depth_output": _depth(samples={"150_175": 3.5, "240_150": 6.0}),
        "object_observations": [
            _obs("obs_g1", "person", {"x1": 100, "y1": 50, "x2": 200, "y2": 300}),
            _obs("obs_g2", "vehicle", {"x1": 200, "y1": 100, "x2": 280, "y2": 200}),
        ],
        "expected_hint_count": 2, "expect_readiness": True, "expect_no_hardware_fact": True,
    },
)
