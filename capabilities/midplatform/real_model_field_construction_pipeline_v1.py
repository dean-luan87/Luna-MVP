# -*- coding: utf-8 -*-
"""Real model field construction pipeline v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from capabilities.midplatform.real_model_candidate_conversion_v1 import (
    convert_depth_output_to_depth_observation_candidate,
    convert_yolo_output_to_object_observation_candidates,
)
from capabilities.midplatform.yolo_depth_real_field_assembly_pipeline_v1 import (
    run_real_field_assembly_pipeline,
)


def run_real_model_field_construction_pipeline(
    *,
    frame_pkg: Dict[str, Any],
    yolo_pkg: Dict[str, Any],
    depth_pkg: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """Run full field construction pipeline reusing existing modules."""
    objects, _ = convert_yolo_output_to_object_observation_candidates(yolo_pkg, frame_pkg)
    depth_obs, _ = convert_depth_output_to_depth_observation_candidate(depth_pkg, frame_pkg)
    if not objects:
        return {
            "pipeline_status": "failed_no_detection",
            "object_observation_candidates": [],
            "depth_observation_candidate": depth_obs,
            "alignment_result_ref": None,
            "fusion_result_ref": None,
            "geometry_result_ref": None,
            "field_assembly_result_ref": None,
            "enhanced_field_scene_candidate": None,
        }

    pipeline = run_real_field_assembly_pipeline(
        frame_pkg=frame_pkg,
        yolo_pkg=yolo_pkg,
        depth_pkg=depth_pkg,
        objects=objects,
        depth_obs=depth_obs,
    )
    scene = pipeline.get("enhanced_field_scene") or pipeline.get("enhanced_field_scene_candidate")
    return {
        "pipeline_status": "pass" if scene and scene.get("field_scene_id") else "failed_field_assembly",
        "object_observation_candidates": objects,
        "depth_observation_candidate": depth_obs,
        "alignment_result_ref": (pipeline.get("alignment_result") or {}).get("alignment_result_id"),
        "fusion_result_ref": (pipeline.get("fusion_result") or {}).get("fusion_result_id"),
        "geometry_result_ref": (pipeline.get("geometry_result") or {}).get("geometry_result_id"),
        "field_assembly_result_ref": (pipeline.get("field_assembly_result") or {}).get("field_assembly_result_id"),
        "enhanced_field_scene_candidate": scene,
        "pipeline_detail": pipeline,
    }
