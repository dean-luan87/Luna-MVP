# -*- coding: utf-8 -*-
"""Depth-Object Fusion Skeleton — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

SELECTED_NEXT_PHASE = "Phase-Midplatform-Field-Geometry-Candidate-Skeleton-v1-001"
SELECTED_NEXT_ROUTE = "Field Geometry Candidate Skeleton"

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "field_geometry_generation", "pseudo_3d_position_generation", "field_scene_assembly",
        "model_download", "weight_download", "yolo_execution", "depth_model_execution",
        "real_depth_inference", "real_multi_model_runtime", "slam_runtime",
        "field_simulation", "task_execution", "world_model_entry", "memory_candidate",
        "runtime", "integration_test",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "fusion_not_geometry", "depth_hint_not_pseudo_3d",
    "object_depth_hint_not_world_model_fact", "fusion_not_field_assembly",
)

FUSION_INPUT_CONTRACT: Dict[str, Any] = {
    "contract_id": "depth_object_fusion_input_contract_v1",
    "inputs": ("MultiModelAlignedObservationCandidate", "ObjectObservationCandidate", "DepthObservationCandidate"),
    "primary_anchor": "MultiModelAlignedObservationCandidate",
    "candidate_only": True,
}

OBJECT_DEPTH_HINT_CANDIDATE_REGISTRY: Dict[str, Any] = {
    "registry_id": "object_depth_hint_candidate_registry_v1",
    "candidate_type": "ObjectDepthHintCandidate",
    "candidate_only": True,
}

FUSION_RESULT_CANDIDATE_REGISTRY: Dict[str, Any] = {
    "registry_id": "depth_object_fusion_result_candidate_registry_v1",
    "outputs": (
        "object_depth_hint_candidates", "rejected_fusion_count", "missing_depth_count",
        "readiness_for_field_geometry",
    ),
    "candidate_only": True,
}

DEPTH_BUCKET_FIELD_ZONE_HINT_POLICY: Dict[str, Any] = {
    "policy_id": "depth_bucket_field_zone_hint_policy_v1",
    "metric_buckets": (
        {"range_m": "0-3", "depth_bucket": "near", "field_zone_hint": "inner_zone"},
        {"range_m": "3-10", "depth_bucket": "middle", "field_zone_hint": "working_zone"},
        {"range_m": "10-20", "depth_bucket": "far", "field_zone_hint": "forecast_zone"},
        {"range_m": "20+", "depth_bucket": "unknown", "field_zone_hint": "unknown"},
    ),
    "relative_buckets": (
        {"norm": "0-0.33", "depth_bucket": "near", "field_zone_hint": "inner_zone", "weak_hint": True},
        {"norm": "0.33-0.66", "depth_bucket": "middle", "field_zone_hint": "working_zone", "weak_hint": True},
        {"norm": "0.66-1.0", "depth_bucket": "far", "field_zone_hint": "forecast_zone", "weak_hint": True},
    ),
    "unknown_unit": {"depth_bucket": "unknown", "field_zone_hint": "unknown"},
    "relative_warning": "relative_depth_not_metric",
}

FUSION_FALLBACK_POLICY: Dict[str, Any] = {
    "policy_id": "depth_object_fusion_fallback_policy_v1",
    "missing_depth": {"depth_bucket": "unknown", "field_zone_hint": "unknown", "fusion_confidence": "low"},
    "unreliable_depth": {"fusion_confidence": "low", "retain_candidate": True},
    "relative_depth": {"warning": "relative_depth_not_metric", "fusion_confidence_not_high": True},
    "rejected_alignment": {"no_fusion": True},
    "degraded_alignment": {"fusion_confidence_downgrade": True},
}


def _aligned(aid: str, obs_id: str, depth_id: str | None, **kw: Any) -> Dict[str, Any]:
    return {
        "aligned_candidate_id": aid,
        "alignment_group_id": kw.get("group", "ag_1"),
        "frame_ref": kw.get("frame_ref", "frame_0"),
        "timestamp": kw.get("timestamp", "2026-06-11T00:00:00Z"),
        "camera_ref": kw.get("camera_ref"),
        "primary_object_observation_ref": obs_id,
        "depth_observation_ref": depth_id,
        "optional_observation_refs": kw.get("optional_refs", []),
        "alignment_status": kw.get("status", "aligned_strong"),
        "alignment_confidence": kw.get("align_conf", "high"),
        "alignment_strength": kw.get("strength", "strong"),
        "aligned_model_roles": kw.get("roles", ["detector_yolo", "depth_model"]),
        "missing_model_roles": kw.get("missing_roles", []),
        "rejected_model_outputs": [],
        "conflict_refs": kw.get("conflicts", []),
        "warning_codes": kw.get("warnings", []),
        "degradation_reason_codes": kw.get("degradation", []),
        "source_refs": [aid, obs_id] + ([depth_id] if depth_id else []),
        "evidence_refs": [obs_id],
        "traceability_refs": [kw.get("frame_ref", "frame_0")],
        "candidate_only": True,
    }


def _obj(obs_id: str, **kw: Any) -> Dict[str, Any]:
    return {
        "observation_id": obs_id,
        "source_type": "model_detector",
        "model_ref": "yolo_lightweight_placeholder",
        "frame_ref": kw.get("frame_ref", "frame_0"),
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


def _depth(did: str, **kw: Any) -> Dict[str, Any]:
    center_x = kw.get("cx", 150)
    center_y = kw.get("cy", 175)
    samples = kw.get("samples") or {f"{center_x}_{center_y}": kw.get("depth_val", 2.0)}
    return {
        "depth_observation_id": did,
        "source_type": "model_depth_estimator",
        "model_ref": "depth_anything_v2_placeholder",
        "frame_ref": kw.get("frame_ref", "frame_0"),
        "timestamp": kw.get("timestamp", "2026-06-11T00:00:00Z"),
        "frame_width": kw.get("fw", 640),
        "frame_height": kw.get("fh", 480),
        "depth_map_ref": kw.get("depth_map_ref", "depth_map_mock"),
        "depth_map_shape": kw.get("shape", [480, 640]),
        "depth_map_samples": samples,
        "depth_value_unit": kw.get("unit", "metric"),
        "depth_source": "estimated",
        "depth_confidence": kw.get("conf", "medium"),
        "depth_error_expected": True,
        "reliability_level": kw.get("reliability", "medium"),
        "source_refs": [did],
        "evidence_refs": [did],
        "candidate_only": True,
    }


def _fusion(aligned: tuple, objects: tuple, depths: tuple, **kw: Any) -> Dict[str, Any]:
    return {
        "fusion_input_id": kw.get("id", "fusion_mock"),
        "aligned_candidates": list(aligned),
        "object_observations": list(objects),
        "depth_observations": list(depths),
        "alignment_result_ref": kw.get("align_ref", "mar_mock"),
    }


DRYRUN_MOCK_CASES: Tuple[Dict[str, Any], ...] = (
    {
        "case_id": "aligned_object_depth_metric_near",
        "fusion_input": _fusion(
            (_aligned("mac_n1", "obs_n1", "depth_n1"),),
            (_obj("obs_n1", bbox={"x1": 100, "y1": 50, "x2": 200, "y2": 300}),),
            (_depth("depth_n1", depth_val=2.0, cx=150, cy=175),),
        ),
        "expected_hint_count": 1, "expected_rejected_count": 0,
        "expect_near": True, "expect_readiness": True, "prohibited_geometry": True,
    },
    {
        "case_id": "aligned_object_depth_metric_middle",
        "fusion_input": _fusion(
            (_aligned("mac_m1", "obs_m1", "depth_m1"),),
            (_obj("obs_m1"),),
            (_depth("depth_m1", depth_val=5.0, cx=150, cy=175),),
        ),
        "expected_hint_count": 1, "expect_middle": True, "expect_readiness": True,
    },
    {
        "case_id": "aligned_object_depth_metric_far",
        "fusion_input": _fusion(
            (_aligned("mac_f1", "obs_f1", "depth_f1"),),
            (_obj("obs_f1"),),
            (_depth("depth_f1", depth_val=15.0, cx=150, cy=175),),
        ),
        "expected_hint_count": 1, "expect_far": True, "expect_readiness": True,
    },
    {
        "case_id": "relative_depth_generates_weak_hint",
        "fusion_input": _fusion(
            (_aligned("mac_r1", "obs_r1", "depth_r1"),),
            (_obj("obs_r1"),),
            (_depth("depth_r1", unit="relative", depth_val=0.2, cx=150, cy=175),),
        ),
        "expected_hint_count": 1, "expect_relative_weak": True, "expect_readiness": True,
    },
    {
        "case_id": "missing_depth_generates_unknown_hint",
        "fusion_input": _fusion(
            (_aligned("mac_u1", "obs_u1", None, missing_roles=["depth_model"], status="aligned_degraded"),),
            (_obj("obs_u1"),),
            (),
        ),
        "expected_hint_count": 1, "expect_missing_unknown": True, "expect_not_ready": True,
    },
    {
        "case_id": "rejected_alignment_no_fusion",
        "fusion_input": _fusion(
            (_aligned("mac_rej", "obs_rej", "depth_rej", status="rejected_frame_mismatch", strength="rejected"),),
            (_obj("obs_rej"),),
            (_depth("depth_rej", frame_ref="frame_1"),),
        ),
        "expected_hint_count": 0, "expected_rejected_count": 1, "expect_rejected_alignment": True,
    },
    {
        "case_id": "degraded_alignment_confidence_downgrade",
        "fusion_input": _fusion(
            (_aligned("mac_d1", "obs_d1", "depth_d1", status="aligned_degraded", align_conf="medium"),),
            (_obj("obs_d1"),),
            (_depth("depth_d1", depth_val=2.0),),
        ),
        "expected_hint_count": 1, "expect_degraded_fusion": True, "expect_readiness": True,
    },
    {
        "case_id": "invalid_bbox_rejected",
        "fusion_input": _fusion(
            (_aligned("mac_inv", "obs_inv", "depth_inv"),),
            (_obj("obs_inv", bbox={"x1": 200, "y1": 200, "x2": 100, "y2": 100}),),
            (_depth("depth_inv", depth_val=2.0),),
        ),
        "expected_hint_count": 0, "expected_rejected_count": 1, "expect_invalid_bbox": True,
    },
    {
        "case_id": "depth_map_shape_mismatch_warning",
        "fusion_input": _fusion(
            (_aligned("mac_sm", "obs_sm", "depth_sm"),),
            (_obj("obs_sm"),),
            (_depth("depth_sm", shape=[600, 800], depth_val=2.0),),
        ),
        "expected_hint_count": 1, "expect_shape_mismatch": True, "expect_readiness": True,
    },
    {
        "case_id": "low_depth_confidence_downgrade",
        "fusion_input": _fusion(
            (_aligned("mac_lc", "obs_lc", "depth_lc"),),
            (_obj("obs_lc"),),
            (_depth("depth_lc", conf="low", depth_val=2.0),),
        ),
        "expected_hint_count": 1, "expect_low_confidence": True, "expect_readiness": True,
    },
    {
        "case_id": "multiple_objects_same_depth_map",
        "fusion_input": _fusion(
            (
                _aligned("mac_mu1", "obs_mu1", "depth_mu"),
                _aligned("mac_mu2", "obs_mu2", "depth_mu"),
            ),
            (
                _obj("obs_mu1", label="person"),
                _obj("obs_mu2", label="chair", bbox={"x1": 200, "y1": 100, "x2": 280, "y2": 200}),
            ),
            (_depth("depth_mu", samples={"150_175": 2.0, "240_150": 5.0}, depth_val=2.0),),
        ),
        "expected_hint_count": 2, "expect_multiple": True, "expect_readiness": True,
    },
    {
        "case_id": "field_geometry_readiness_true",
        "fusion_input": _fusion(
            (_aligned("mac_rd", "obs_rd", "depth_rd"),),
            (_obj("obs_rd"),),
            (_depth("depth_rd", depth_val=4.0),),
        ),
        "expected_hint_count": 1, "expect_readiness": True, "prohibited_geometry": True,
    },
    {
        "case_id": "all_depth_missing_geometry_not_ready",
        "fusion_input": _fusion(
            (
                _aligned("mac_nr1", "obs_nr1", None, missing_roles=["depth_model"], status="aligned_degraded"),
                _aligned("mac_nr2", "obs_nr2", None, missing_roles=["depth_model"], status="aligned_degraded"),
            ),
            (_obj("obs_nr1"), _obj("obs_nr2", bbox={"x1": 200, "y1": 100, "x2": 280, "y2": 200})),
            (),
        ),
        "expected_hint_count": 2, "expect_missing_unknown": True, "expect_not_ready": True,
    },
)
