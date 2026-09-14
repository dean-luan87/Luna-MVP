# -*- coding: utf-8 -*-
"""Spatial mapping adapter input builder v1 — based on smoke IO inspection."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional


def build_spatial_mapping_adapter_input_package(
    *,
    frame_inputs: List[Dict[str, Any]],
    session_ref: str,
    smoke_run: Dict[str, Any],
    io_inspection: Dict[str, Any],
    enhanced_field_scenes: Optional[List[Dict[str, Any]]] = None,
    field_geometries: Optional[List[Dict[str, Any]]] = None,
    authorization_ref: str = "spatial_mapping_authorization_v1",
) -> Dict[str, Any]:
    """Build adapter input from smoke IO inspection artifacts. Reuses RealFrameInputPackage."""
    execution_mode = smoke_run.get("execution_mode", "adapter_stub")
    traceability: List[str] = [session_ref, smoke_run.get("smoke_run_id", ""), io_inspection.get("io_inspection_id", "")]
    source_refs: List[str] = [session_ref, smoke_run.get("smoke_run_id", "")]
    for f in frame_inputs:
        traceability.extend([f.get("frame_input_id"), f.get("frame_ref")])
        source_refs.append(f.get("frame_input_id", ""))
    scene_refs = []
    for sc in enhanced_field_scenes or []:
        scene_refs.append(sc.get("field_scene_id"))
        traceability.append(sc.get("field_scene_id"))
    geom_refs = []
    for g in field_geometries or []:
        gid = g.get("geometry_candidate_id") or g.get("field_geometry_candidate_id")
        if gid:
            geom_refs.append(gid)

    return {
        "adapter_input_id": f"smai_{uuid.uuid4().hex[:12]}",
        "model_role": "slam_spatial_mapping",
        "model_ref": smoke_run.get("model_ref", "slam_spatial_mapping_inspection_v1"),
        "execution_mode": execution_mode,
        "smoke_run_ref": smoke_run.get("smoke_run_id"),
        "io_inspection_ref": io_inspection.get("io_inspection_id"),
        "frame_inputs": [f.get("frame_input_id") for f in frame_inputs],
        "enhanced_field_scene_refs": scene_refs,
        "field_geometry_refs": geom_refs,
        "session_ref": session_ref,
        "authorization_ref": authorization_ref,
        "source_refs": [r for r in source_refs if r],
        "traceability_refs": [t for t in traceability if t],
        "candidate_only": True,
        "_frame_packages": frame_inputs,
        "_scene_packages": enhanced_field_scenes or [],
        "_geometry_packages": field_geometries or [],
        "_smoke_run": smoke_run,
        "_io_inspection": io_inspection,
    }
