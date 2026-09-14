# -*- coding: utf-8 -*-
"""Field Assembly Skeleton — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

SELECTED_NEXT_PHASE = "Phase-Midplatform-YOLO-Depth-Real-Field-Assembly-DryRun-Planning-v1-001"
SELECTED_NEXT_ROUTE = "YOLO Depth Real Field Assembly DryRun Planning"

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "field_simulation", "task_reasoning", "scene_relation_generation", "scene_graph_runtime",
        "slam_runtime", "model_download", "weight_download", "yolo_execution", "depth_model_execution",
        "real_multi_model_runtime", "world_model_entry", "memory_candidate", "runtime",
        "integration_test", "candidate_lifecycle_manager", "module_handoff_contract",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "assembly_not_simulation", "field_scene_not_world_model_fact",
    "enhanced_entity_not_memory", "assembly_not_task_execution",
)

ENHANCED_FIELD_ENTITY_CANDIDATE_REGISTRY: Dict[str, Any] = {
    "registry_id": "enhanced_field_entity_candidate_registry_v1",
    "candidate_type": "EnhancedFieldEntityCandidate",
    "fact_status": "candidate",
    "candidate_only": True,
}

ENHANCED_FIELD_SCENE_CANDIDATE_REGISTRY: Dict[str, Any] = {
    "registry_id": "enhanced_field_scene_candidate_registry_v1",
    "candidate_type": "EnhancedFieldSceneCandidate",
    "candidate_only": True,
}

FIELD_ASSEMBLY_RESULT_CANDIDATE_REGISTRY: Dict[str, Any] = {
    "registry_id": "field_assembly_result_candidate_registry_v1",
    "outputs": (
        "enhanced_field_scene_candidate", "enhanced_entity_candidates",
        "readiness_for_field_first_core", "readiness_for_real_model_success_path",
    ),
    "candidate_only": True,
}


def _obj(obs_id: str, **kw: Any) -> Dict[str, Any]:
    return {
        "observation_id": obs_id,
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


def _hint(hid: str, obs_id: str, **kw: Any) -> Dict[str, Any]:
    dv = kw.get("depth_val", 2.0)
    return {
        "object_depth_hint_id": hid,
        "object_observation_ref": obs_id,
        "object_depth_hint": dv,
        "depth_value_unit": kw.get("unit", "metric"),
        "depth_bucket": kw.get("bucket", "near"),
        "field_zone_hint": kw.get("zone", "inner_zone"),
        "depth_source": kw.get("depth_source", "estimated"),
        "depth_confidence": kw.get("depth_conf", "medium"),
        "depth_error_expected": True,
        "fusion_confidence": kw.get("fusion_conf", "medium"),
        "warning_codes": kw.get("warnings", []),
        "missing_information": kw.get("missing", []),
        "candidate_only": True,
    }


def _spatial(sid: str, obs_id: str, **kw: Any) -> Dict[str, Any]:
    zone = kw.get("zone", "inner_zone")
    return {
        "object_spatial_state_id": sid,
        "object_observation_ref": obs_id,
        "object_depth_hint_ref": kw.get("hint_ref"),
        "bbox_center": kw.get("center", {"x": 150, "y": 175}),
        "depth_hint": kw.get("depth_val", 2.0),
        "pseudo_3d_position": kw.get("pseudo", {"x_norm": 0.23, "y_norm": 0.36, "z_hint": 2.0, "coordinate_mode": "normalized_image_depth_hint"}),
        "pseudo_3d_status": kw.get("pseudo_status", "pseudo_3d_estimated"),
        "distance_bucket": kw.get("bucket", "near"),
        "field_zone": zone,
        "spatial_confidence": kw.get("conf", "medium"),
        "spatial_reliability_reasons": [],
        "candidate_only": True,
    }


def _geometry(gid: str, obs_id: str, sid: str, **kw: Any) -> Dict[str, Any]:
    zone = kw.get("zone", "inner_zone")
    status = kw.get("status", "geometry_estimated")
    return {
        "geometry_candidate_id": gid,
        "object_spatial_state_ref": sid,
        "object_observation_ref": obs_id,
        "object_depth_hint_ref": kw.get("hint_ref"),
        "pseudo_3d_position": kw.get("pseudo", {"x_norm": 0.23, "y_norm": 0.36, "z_hint": kw.get("depth_val", 2.0), "coordinate_mode": "normalized_image_depth_hint"}),
        "field_zone": zone,
        "distance_bucket": kw.get("bucket", "near"),
        "geometry_confidence": kw.get("conf", "medium"),
        "geometry_status": status,
        "geometry_reliability_reasons": [],
        "warning_codes": kw.get("warnings", []),
        "missing_information": kw.get("missing", []),
        "depth_error_expected": True,
        "candidate_only": True,
    }


def _asm(objects=(), hints=(), spatials=(), geometries=(), **kw: Any) -> Dict[str, Any]:
    return {
        "assembly_input_id": kw.get("aid", "asm_mock"),
        "object_observations": list(objects),
        "object_depth_hints": list(hints),
        "object_spatial_states": list(spatials),
        "field_geometry_candidates": list(geometries),
        "alignment_result_ref": kw.get("align_ref", "mar_mock"),
        "fusion_result_ref": kw.get("fusion_ref", "dof_mock"),
        "geometry_result_ref": kw.get("geom_ref", "fgr_mock"),
        "frame_ref": kw.get("frame_ref", "frame_0"),
        "timestamp": kw.get("timestamp", "2026-06-11T00:00:00Z"),
    }


DRYRUN_MOCK_CASES: Tuple[Dict[str, Any], ...] = (
    {
        "case_id": "single_geometry_enhanced_entity",
        "assembly_input": _asm(
            (_obj("obs_s1"),),
            (_hint("h_s1", "obs_s1"),),
            (_spatial("sp_s1", "obs_s1"),),
            (_geometry("g_s1", "obs_s1", "sp_s1"),),
        ),
        "expected_entity_count": 1, "expect_geometry_enhanced": True,
        "expect_estimated_depth_error": True, "expect_readiness_core": True,
    },
    {
        "case_id": "multiple_entities_zone_summary",
        "assembly_input": _asm(
            (
                _obj("obs_i", label="person"),
                _obj("obs_w", label="chair", bbox={"x1": 200, "y1": 100, "x2": 300, "y2": 350}),
                _obj("obs_f", label="door", bbox={"x1": 400, "y1": 80, "x2": 500, "y2": 400}),
                _obj("obs_u", label="sign", bbox={"x1": 50, "y1": 20, "x2": 120, "y2": 100}),
            ),
            (
                _hint("h_i", "obs_i", depth_val=2.0),
                _hint("h_w", "obs_w", depth_val=5.0, bucket="middle", zone="working_zone"),
                _hint("h_f", "obs_f", depth_val=15.0, bucket="far", zone="forecast_zone"),
                _hint("h_u", "obs_u", depth_val=None, unit="unknown", bucket="unknown", zone="unknown"),
            ),
            (
                _spatial("sp_i", "obs_i", zone="inner_zone"),
                _spatial("sp_w", "obs_w", zone="working_zone", bucket="middle", depth_val=5.0),
                _spatial("sp_f", "obs_f", zone="forecast_zone", bucket="far", depth_val=15.0),
                _spatial("sp_u", "obs_u", zone="unknown", bucket="unknown", depth_val=None, pseudo_status="pseudo_3d_unknown"),
            ),
            (
                _geometry("g_i", "obs_i", "sp_i", zone="inner_zone"),
                _geometry("g_w", "obs_w", "sp_w", zone="working_zone", bucket="middle", depth_val=5.0),
                _geometry("g_f", "obs_f", "sp_f", zone="forecast_zone", bucket="far", depth_val=15.0),
                _geometry("g_u", "obs_u", "sp_u", zone="unknown", bucket="unknown", status="geometry_unknown"),
            ),
        ),
        "expected_entity_count": 4, "expect_multiple_zones": True, "min_active_zones": 3,
        "expect_zone_counts": {
            "inner_zone_entity_count": 1, "working_zone_entity_count": 1,
            "forecast_zone_entity_count": 1, "unknown_zone_entity_count": 1,
        },
    },
    {
        "case_id": "missing_depth_entity_2d_only",
        "assembly_input": _asm((_obj("obs_2d"),), (), (), ()),
        "expected_entity_count": 1, "expect_2d_only": True,
    },
    {
        "case_id": "unknown_geometry_entity_geometry_unknown",
        "assembly_input": _asm(
            (_obj("obs_unk"),),
            (_hint("h_unk", "obs_unk", depth_val=None, unit="unknown", bucket="unknown", zone="unknown"),),
            (_spatial("sp_unk", "obs_unk", zone="unknown", pseudo_status="pseudo_3d_unknown", depth_val=None),),
            (_geometry("g_unk", "obs_unk", "sp_unk", zone="unknown", status="geometry_unknown"),),
        ),
        "expected_entity_count": 1, "expect_geometry_unknown": True,
    },
    {
        "case_id": "low_confidence_object_retained",
        "assembly_input": _asm(
            (_obj("obs_lc", confidence=0.35),),
            (_hint("h_lc", "obs_lc"),),
            (_spatial("sp_lc", "obs_lc"),),
            (_geometry("g_lc", "obs_lc", "sp_lc"),),
        ),
        "expected_entity_count": 1, "expect_low_confidence_retained": True, "expect_geometry_enhanced": True,
    },
    {
        "case_id": "duplicate_labels_not_merged",
        "assembly_input": _asm(
            (_obj("obs_c1", label="cup"), _obj("obs_c2", label="cup", bbox={"x1": 300, "y1": 100, "x2": 380, "y2": 250})),
            (_hint("h_c1", "obs_c1"), _hint("h_c2", "obs_c2", depth_val=4.0, bucket="middle", zone="working_zone")),
            (_spatial("sp_c1", "obs_c1"), _spatial("sp_c2", "obs_c2", zone="working_zone", bucket="middle", depth_val=4.0)),
            (_geometry("g_c1", "obs_c1", "sp_c1"), _geometry("g_c2", "obs_c2", "sp_c2", zone="working_zone", bucket="middle", depth_val=4.0)),
        ),
        "expected_entity_count": 2, "expect_duplicate_not_merged": True,
    },
    {
        "case_id": "depth_only_no_entity",
        "assembly_input": _asm(
            (),
            (_hint("h_orphan", "obs_missing", depth_val=2.0),),
            (), (),
        ),
        "expected_entity_count": 0, "expected_rejected_count": 0, "expect_depth_only_no_entity": True,
    },
    {
        "case_id": "geometry_without_object_rejected",
        "assembly_input": _asm(
            (),
            (), (),
            (_geometry("g_orph", "obs_missing", "sp_missing"),),
        ),
        "expected_entity_count": 0, "expected_rejected_count": 1, "expect_geometry_rejected": True,
    },
    {
        "case_id": "estimated_depth_not_hardware_fact",
        "assembly_input": _asm(
            (_obj("obs_est"),),
            (_hint("h_est", "obs_est", depth_source="estimated"),),
            (_spatial("sp_est", "obs_est"),),
            (_geometry("g_est", "obs_est", "sp_est"),),
        ),
        "expected_entity_count": 1, "expect_estimated_depth_error": True, "expect_geometry_enhanced": True,
    },
    {
        "case_id": "zone_summary_counts_correct",
        "assembly_input": _asm(
            (_obj("obs_z1"), _obj("obs_z2", label="box", bbox={"x1": 250, "y1": 80, "x2": 350, "y2": 280})),
            (_hint("h_z1", "obs_z1"), _hint("h_z2", "obs_z2", depth_val=6.0, bucket="middle", zone="working_zone")),
            (_spatial("sp_z1", "obs_z1"), _spatial("sp_z2", "obs_z2", zone="working_zone", bucket="middle", depth_val=6.0)),
            (_geometry("g_z1", "obs_z1", "sp_z1"), _geometry("g_z2", "obs_z2", "sp_z2", zone="working_zone", bucket="middle", depth_val=6.0)),
        ),
        "expected_entity_count": 2,
        "expect_zone_counts": {"inner_zone_entity_count": 1, "working_zone_entity_count": 1, "forecast_zone_entity_count": 0, "unknown_zone_entity_count": 0},
    },
    {
        "case_id": "quality_summary_degraded_by_missing_geometry",
        "assembly_input": _asm(
            (_obj("obs_q1"), _obj("obs_q2", label="box"), _obj("obs_q3", label="bag")),
            (
                _hint("h_q1", "obs_q1", depth_val=None, unit="unknown", bucket="unknown", zone="unknown"),
                _hint("h_q2", "obs_q2", depth_val=None, unit="unknown", bucket="unknown", zone="unknown"),
                _hint("h_q3", "obs_q3", depth_val=None, unit="unknown", bucket="unknown", zone="unknown"),
            ),
            (
                _spatial("sp_q1", "obs_q1", zone="unknown", pseudo_status="pseudo_3d_unknown", depth_val=None),
                _spatial("sp_q2", "obs_q2", zone="unknown", pseudo_status="pseudo_3d_unknown", depth_val=None),
                _spatial("sp_q3", "obs_q3", zone="unknown", pseudo_status="pseudo_3d_unknown", depth_val=None),
            ),
            (
                _geometry("g_q1", "obs_q1", "sp_q1", zone="unknown", status="geometry_unknown"),
                _geometry("g_q2", "obs_q2", "sp_q2", zone="unknown", status="geometry_unknown"),
                _geometry("g_q3", "obs_q3", "sp_q3", zone="unknown", status="geometry_unknown"),
            ),
        ),
        "expected_entity_count": 3, "expect_geometry_quality_degraded": True,
    },
    {
        "case_id": "readiness_for_core_pipeline_true",
        "assembly_input": _asm(
            (_obj("obs_rd"),),
            (_hint("h_rd", "obs_rd"),),
            (_spatial("sp_rd", "obs_rd"),),
            (_geometry("g_rd", "obs_rd", "sp_rd"),),
        ),
        "expected_entity_count": 1, "expect_readiness_core": True,
        "expect_readiness_real_path": True, "expect_geometry_enhanced": True,
    },
    {
        "case_id": "no_scene_relation_generated",
        "assembly_input": _asm(
            (_obj("obs_nr"),),
            (_hint("h_nr", "obs_nr"),),
            (_spatial("sp_nr", "obs_nr"),),
            (_geometry("g_nr", "obs_nr", "sp_nr"),),
        ),
        "expected_entity_count": 1, "prohibited_scene_relation": True,
    },
)
