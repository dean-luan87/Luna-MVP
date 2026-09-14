# -*- coding: utf-8 -*-
"""Tracking / Optical Flow adapter input builder v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional


def build_tracking_opticalflow_adapter_input_package(
    *,
    frame_inputs: List[Dict[str, Any]],
    object_observations: List[Dict[str, Any]],
    session_ref: str,
    smoke_run: Dict[str, Any],
    io_inspection: Dict[str, Any],
    aligned_observations: Optional[List[Dict[str, Any]]] = None,
    enhanced_field_scenes: Optional[List[Dict[str, Any]]] = None,
    field_geometries: Optional[List[Dict[str, Any]]] = None,
    authorization_ref: str = "tracking_opticalflow_authorization_v1",
) -> Dict[str, Any]:
    """Build adapter input from smoke IO inspection artifacts."""
    execution_mode = smoke_run.get("execution_mode", "adapter_stub")
    traceability: List[str] = [
        session_ref,
        smoke_run.get("smoke_run_id", ""),
        io_inspection.get("io_inspection_id", ""),
    ]
    source_refs: List[str] = [session_ref, smoke_run.get("smoke_run_id", "")]
    frame_refs: List[str] = []
    for f in frame_inputs:
        fid = f.get("frame_input_id")
        frame_refs.append(fid)
        traceability.extend([fid, f.get("frame_ref")])
        source_refs.append(fid)

    obs_refs: List[str] = []
    for obs in object_observations:
        oid = obs.get("object_observation_id") or obs.get("observation_id")
        if oid:
            obs_refs.append(oid)
            traceability.append(oid)

    aligned_refs: List[str] = []
    for al in aligned_observations or []:
        aid = al.get("aligned_observation_id") or al.get("multi_model_aligned_observation_id")
        if aid:
            aligned_refs.append(aid)

    scene_refs: List[str] = []
    for sc in enhanced_field_scenes or []:
        sid = sc.get("field_scene_id")
        if sid:
            scene_refs.append(sid)
            traceability.append(sid)

    geom_refs: List[str] = []
    for g in field_geometries or []:
        gid = g.get("geometry_candidate_id") or g.get("field_geometry_candidate_id")
        if gid:
            geom_refs.append(gid)

    return {
        "adapter_input_id": f"toai_{uuid.uuid4().hex[:12]}",
        "model_role": "tracking_optical_flow",
        "model_ref": smoke_run.get("model_ref", "tracking_opticalflow_inspection_v1"),
        "execution_mode": execution_mode,
        "smoke_run_ref": smoke_run.get("smoke_run_id"),
        "io_inspection_ref": io_inspection.get("io_inspection_id"),
        "frame_input_refs": frame_refs,
        "object_observation_refs": obs_refs,
        "aligned_observation_refs": aligned_refs,
        "enhanced_field_scene_refs": scene_refs,
        "field_geometry_refs": geom_refs,
        "session_ref": session_ref,
        "authorization_ref": authorization_ref,
        "source_refs": [r for r in source_refs if r],
        "traceability_refs": [t for t in traceability if t],
        "candidate_only": True,
        "_frame_packages": frame_inputs,
        "_object_observations": object_observations,
        "_aligned_observations": aligned_observations or [],
        "_scene_packages": enhanced_field_scenes or [],
        "_geometry_packages": field_geometries or [],
        "_smoke_run": smoke_run,
        "_io_inspection": io_inspection,
    }
