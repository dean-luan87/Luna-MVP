# -*- coding: utf-8 -*-
"""Field Geometry Candidate Skeleton — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

SELECTED_NEXT_PHASE = "Phase-Midplatform-Field-Assembly-Skeleton-v1-001"
SELECTED_NEXT_ROUTE = "Field Assembly Skeleton"

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "field_scene_assembly", "field_entity_merge", "scene_relation_generation",
        "model_download", "weight_download", "yolo_execution", "depth_model_execution",
        "real_depth_inference", "slam_runtime", "scene_graph_runtime",
        "field_simulation", "task_execution", "world_model_entry", "memory_candidate",
        "runtime", "integration_test",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "geometry_not_field_scene", "pseudo_3d_not_world_model_fact",
    "field_geometry_candidate_not_field_assembly", "spatial_state_not_slam",
)

OBJECT_SPATIAL_STATE_CANDIDATE_REGISTRY: Dict[str, Any] = {
    "registry_id": "object_spatial_state_candidate_registry_v1",
    "candidate_type": "ObjectSpatialStateCandidate",
    "candidate_only": True,
}

FIELD_GEOMETRY_CANDIDATE_REGISTRY: Dict[str, Any] = {
    "registry_id": "field_geometry_candidate_registry_v1",
    "candidate_type": "FieldGeometryCandidate",
    "candidate_only": True,
}

FIELD_GEOMETRY_GENERATION_RESULT_REGISTRY: Dict[str, Any] = {
    "registry_id": "field_geometry_generation_result_registry_v1",
    "outputs": (
        "object_spatial_state_candidates", "field_geometry_candidates",
        "readiness_for_field_assembly",
    ),
    "candidate_only": True,
}


def _obj(obs_id: str, **kw: Any) -> Dict[str, Any]:
    o: Dict[str, Any] = {
        "observation_id": obs_id,
        "frame_ref": kw.get("frame_ref", "frame_0"),
        "timestamp": kw.get("timestamp", "2026-06-11T00:00:00Z"),
        "label": kw.get("label", "person"),
        "confidence": kw.get("confidence", 0.9),
        "bbox": kw.get("bbox", {"x1": 100, "y1": 50, "x2": 200, "y2": 300}),
        "bbox_format": "xyxy",
        "source_refs": [obs_id],
        "evidence_refs": [obs_id],
        "candidate_only": True,
    }
    if "fw" in kw:
        o["frame_width"] = kw["fw"]
    elif "frame_width" in kw:
        o["frame_width"] = kw["frame_width"]
    else:
        o["frame_width"] = 640
    if "fh" in kw:
        o["frame_height"] = kw["fh"]
    elif "frame_height" in kw:
        o["frame_height"] = kw["frame_height"]
    else:
        o["frame_height"] = 480
    return o


def _hint(hid: str, obs_id: str, **kw: Any) -> Dict[str, Any]:
    depth_val = kw.get("depth_val")
    unit = kw.get("unit", "metric")
    bucket = kw.get("bucket", "near")
    zone = kw.get("zone", "inner_zone")
    return {
        "object_depth_hint_id": hid,
        "object_observation_ref": obs_id,
        "depth_observation_ref": kw.get("depth_ref", f"depth_{obs_id}"),
        "frame_ref": kw.get("frame_ref", "frame_0"),
        "timestamp": kw.get("timestamp", "2026-06-11T00:00:00Z"),
        "label": kw.get("label", "person"),
        "bbox": kw.get("bbox", {"x1": 100, "y1": 50, "x2": 200, "y2": 300}),
        "object_depth_hint": depth_val,
        "sampled_depth_value": depth_val,
        "depth_value_unit": unit,
        "depth_bucket": bucket if depth_val is not None else "unknown",
        "field_zone_hint": zone if depth_val is not None else "unknown",
        "depth_source": kw.get("depth_source", "estimated"),
        "depth_confidence": kw.get("depth_conf", "medium"),
        "depth_error_expected": True,
        "fusion_confidence": kw.get("fusion_conf", "medium"),
        "alignment_confidence": kw.get("align_conf", "high"),
        "depth_reliability_reasons": kw.get("reasons", []),
        "missing_information": kw.get("missing", []),
        "warning_codes": kw.get("warnings", []),
        "conflict_refs": kw.get("conflicts", []),
        "source_refs": [hid, obs_id],
        "evidence_refs": [obs_id],
        "candidate_only": True,
    }


def _geom_input(objects: Tuple[Dict[str, Any], ...], hints: Tuple[Dict[str, Any], ...]) -> Dict[str, Any]:
    return {
        "geometry_input_id": "fgi_mock",
        "object_observations": list(objects),
        "object_depth_hints": list(hints),
        "depth_object_fusion_result_ref": "dof_mock",
    }


DRYRUN_MOCK_CASES: Tuple[Dict[str, Any], ...] = (
    {
        "case_id": "metric_near_generates_inner_zone_geometry",
        "geometry_input": _geom_input(
            (_obj("obs_n1"),),
            (_hint("hint_n1", "obs_n1", depth_val=2.0, bucket="near", zone="inner_zone"),),
        ),
        "expected_spatial_count": 1, "expected_geometry_count": 1,
        "expect_inner_zone": True, "expect_readiness": True,
    },
    {
        "case_id": "metric_middle_generates_working_zone_geometry",
        "geometry_input": _geom_input(
            (_obj("obs_m1"),),
            (_hint("hint_m1", "obs_m1", depth_val=5.0, bucket="middle", zone="working_zone"),),
        ),
        "expected_spatial_count": 1, "expected_geometry_count": 1,
        "expect_working_zone": True, "expect_readiness": True,
    },
    {
        "case_id": "metric_far_generates_forecast_zone_geometry",
        "geometry_input": _geom_input(
            (_obj("obs_f1"),),
            (_hint("hint_f1", "obs_f1", depth_val=15.0, bucket="far", zone="forecast_zone"),),
        ),
        "expected_spatial_count": 1, "expected_geometry_count": 1,
        "expect_forecast_zone": True, "expect_readiness": True,
    },
    {
        "case_id": "relative_depth_generates_weak_geometry",
        "geometry_input": _geom_input(
            (_obj("obs_r1"),),
            (_hint("hint_r1", "obs_r1", depth_val=0.2, unit="relative", bucket="near", zone="inner_zone",
                   warnings=["relative_depth_not_metric"]),),
        ),
        "expected_spatial_count": 1, "expected_geometry_count": 1,
        "expect_weak_geometry": True, "expect_readiness": True,
    },
    {
        "case_id": "unknown_depth_generates_geometry_unknown",
        "geometry_input": _geom_input(
            (_obj("obs_u1"),),
            (_hint("hint_u1", "obs_u1", depth_val=None, unit="unknown", bucket="unknown", zone="unknown",
                   depth_conf="unknown", fusion_conf="low", missing=["depth_map_missing"]),),
        ),
        "expected_spatial_count": 1, "expected_geometry_count": 1,
        "expect_geometry_unknown": True,
    },
    {
        "case_id": "invalid_bbox_geometry_rejected",
        "geometry_input": _geom_input(
            (_obj("obs_inv", bbox={"x1": 200, "y1": 200, "x2": 100, "y2": 100}),),
            (_hint("hint_inv", "obs_inv", depth_val=2.0),),
        ),
        "expected_spatial_count": 0, "expected_geometry_count": 0,
        "expected_rejected_count": 1, "expect_geometry_rejected": True,
    },
    {
        "case_id": "frame_size_missing_confidence_downgrade",
        "geometry_input": _geom_input(
            (_obj("obs_fs", fw=None, fh=None),),
            (_hint("hint_fs", "obs_fs", depth_val=2.0),),
        ),
        "expected_spatial_count": 1, "expected_geometry_count": 1,
        "expect_confidence_low": True, "expect_readiness": True,
    },
    {
        "case_id": "low_object_confidence_downgrade",
        "geometry_input": _geom_input(
            (_obj("obs_lc", confidence=0.3),),
            (_hint("hint_lc", "obs_lc", depth_val=2.0),),
        ),
        "expected_spatial_count": 1, "expected_geometry_count": 1,
        "expect_confidence_low": True,
    },
    {
        "case_id": "degraded_fusion_confidence_downgrade",
        "geometry_input": _geom_input(
            (_obj("obs_df"),),
            (_hint("hint_df", "obs_df", depth_val=2.0, fusion_conf="low", reasons=["alignment_degraded"]),),
        ),
        "expected_spatial_count": 1, "expected_geometry_count": 1,
        "expect_confidence_low": True, "expect_readiness": True,
    },
    {
        "case_id": "out_of_range_depth_warning",
        "geometry_input": _geom_input(
            (_obj("obs_or"),),
            (_hint("hint_or", "obs_or", depth_val=25.0, bucket="unknown", zone="unknown",
                   warnings=["depth_out_of_range"]),),
        ),
        "expected_spatial_count": 1, "expected_geometry_count": 1,
        "expect_out_of_range": True,
    },
    {
        "case_id": "multiple_objects_geometry_generated",
        "geometry_input": _geom_input(
            (_obj("obs_mu1"), _obj("obs_mu2", bbox={"x1": 300, "y1": 100, "x2": 400, "y2": 350})),
            (
                _hint("hint_mu1", "obs_mu1", depth_val=2.0),
                _hint("hint_mu2", "obs_mu2", depth_val=8.0, bucket="middle", zone="working_zone"),
            ),
        ),
        "expected_spatial_count": 2, "expected_geometry_count": 2,
        "expect_multiple": True, "expect_readiness": True,
    },
    {
        "case_id": "missing_depth_does_not_drop_object_spatial_state",
        "geometry_input": _geom_input(
            (_obj("obs_md"),),
            (_hint("hint_md", "obs_md", depth_val=None, unit="unknown", bucket="unknown", zone="unknown",
                   depth_conf="unknown", fusion_conf="low"),),
        ),
        "expected_spatial_count": 1, "expected_geometry_count": 1,
        "expect_spatial_unknown_kept": True,
    },
    {
        "case_id": "readiness_for_field_assembly_true",
        "geometry_input": _geom_input(
            (_obj("obs_rd"),),
            (_hint("hint_rd", "obs_rd", depth_val=2.0, bucket="near", zone="inner_zone"),),
        ),
        "expected_spatial_count": 1, "expected_geometry_count": 1,
        "expect_readiness": True, "expect_inner_zone": True,
    },
)
