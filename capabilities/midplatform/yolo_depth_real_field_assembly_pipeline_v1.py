# -*- coding: utf-8 -*-
"""YOLO + Depth real field assembly pipeline v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.depth_object_fusion_core_v1 import run_depth_object_fusion
from capabilities.midplatform.field_assembly_core_v1 import run_field_assembly
from capabilities.midplatform.field_geometry_candidate_core_v1 import run_field_geometry_generation
from capabilities.midplatform.multi_model_alignment_core_v1 import run_multi_model_alignment


def run_real_field_assembly_pipeline(
    *,
    frame_pkg: Dict[str, Any],
    yolo_pkg: Dict[str, Any],
    depth_pkg: Optional[Dict[str, Any]],
    objects: List[Dict[str, Any]],
    depth_obs: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """Reuse alignment → fusion → geometry → assembly modules."""
    alignment_input = {
        "input_package_id": f"align_{uuid.uuid4().hex[:8]}",
        "object_observations": objects,
        "depth_observation": depth_obs,
        "optional_observations": [],
    }
    alignment_result = run_multi_model_alignment(alignment_input)
    aligned = alignment_result.get("aligned_candidates") or []

    fusion_input = {
        "fusion_input_id": f"fusion_{uuid.uuid4().hex[:8]}",
        "aligned_candidates": aligned,
        "object_observations": objects,
        "depth_observations": [depth_obs] if depth_obs else [],
        "alignment_result_ref": alignment_result.get("alignment_result_id"),
    }
    fusion_result = run_depth_object_fusion(fusion_input)
    hints = fusion_result.get("object_depth_hint_candidates") or []

    geometry_input = {
        "geometry_input_id": f"geom_{uuid.uuid4().hex[:8]}",
        "object_observations": objects,
        "object_depth_hints": hints,
        "depth_object_fusion_result_ref": fusion_result.get("fusion_result_id"),
    }
    geometry_result = run_field_geometry_generation(geometry_input)
    geometries = geometry_result.get("field_geometry_candidates") or []
    spatials = geometry_result.get("object_spatial_state_candidates") or []

    assembly_input = {
        "assembly_input_id": f"asm_{uuid.uuid4().hex[:8]}",
        "object_observations": objects,
        "object_depth_hints": hints,
        "object_spatial_states": spatials,
        "field_geometry_candidates": geometries,
        "alignment_result_ref": alignment_result.get("alignment_result_id"),
        "fusion_result_ref": fusion_result.get("fusion_result_id"),
        "geometry_result_ref": geometry_result.get("geometry_generation_result_id"),
        "frame_ref": frame_pkg.get("frame_ref"),
        "timestamp": frame_pkg.get("timestamp"),
        "source_refs": [frame_pkg.get("frame_input_id"), yolo_pkg.get("detector_run_id")],
    }
    assembly_result = run_field_assembly(assembly_input)

    return {
        "alignment_result": alignment_result,
        "fusion_result": fusion_result,
        "geometry_result": geometry_result,
        "assembly_result": assembly_result,
        "aligned_candidates": aligned,
        "object_depth_hints": hints,
        "field_geometry_candidates": geometries,
        "enhanced_field_scene": assembly_result.get("enhanced_field_scene_candidate"),
    }
