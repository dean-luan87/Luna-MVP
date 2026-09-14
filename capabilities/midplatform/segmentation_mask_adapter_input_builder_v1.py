# -*- coding: utf-8 -*-
"""Segmentation / Mask adapter input builder v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional


def build_segmentation_mask_adapter_input_package(
    *,
    frame_inputs: List[Dict[str, Any]],
    session_ref: str,
    smoke_run: Dict[str, Any],
    io_inspection: Dict[str, Any],
    object_observations: Optional[List[Dict[str, Any]]] = None,
    aligned_observations: Optional[List[Dict[str, Any]]] = None,
    enhanced_field_scenes: Optional[List[Dict[str, Any]]] = None,
    field_geometries: Optional[List[Dict[str, Any]]] = None,
    text_regions: Optional[List[Dict[str, Any]]] = None,
    prompt_refs: Optional[List[str]] = None,
    authorization_ref: str = "segmentation_mask_authorization_v1",
) -> Dict[str, Any]:
    """Build adapter input from smoke IO inspection artifacts."""
    execution_mode = smoke_run.get("execution_mode", "adapter_stub")
    traceability: List[str] = [
        session_ref, smoke_run.get("smoke_run_id", ""), io_inspection.get("io_inspection_id", ""),
    ]
    source_refs: List[str] = [session_ref, smoke_run.get("smoke_run_id", "")]
    frame_refs: List[str] = []
    for f in frame_inputs:
        fid = f.get("frame_input_id")
        frame_refs.append(fid)
        traceability.extend([fid, f.get("frame_ref")])
        source_refs.append(fid)

    obs_refs: List[str] = []
    for obs in object_observations or []:
        oid = obs.get("object_observation_id") or obs.get("observation_id")
        if oid:
            obs_refs.append(oid)
            traceability.append(oid)

    aligned_refs = [
        al.get("multi_model_aligned_observation_id") or al.get("aligned_observation_id")
        for al in (aligned_observations or []) if al
    ]
    scene_refs = [sc.get("field_scene_id") for sc in (enhanced_field_scenes or []) if sc.get("field_scene_id")]
    geom_refs = [
        g.get("geometry_candidate_id") or g.get("field_geometry_candidate_id")
        for g in (field_geometries or []) if g
    ]
    text_refs = [
        t.get("text_region_candidate_id") for t in (text_regions or []) if t.get("text_region_candidate_id")
    ]

    return {
        "adapter_input_id": f"smai_{uuid.uuid4().hex[:12]}",
        "model_role": "segmentation_mask_model",
        "model_ref": smoke_run.get("model_ref", "segmentation_mask_inspection_v1"),
        "execution_mode": execution_mode,
        "smoke_run_ref": smoke_run.get("smoke_run_id"),
        "io_inspection_ref": io_inspection.get("io_inspection_id"),
        "frame_input_refs": frame_refs,
        "object_observation_refs": obs_refs,
        "aligned_observation_refs": [r for r in aligned_refs if r],
        "enhanced_field_scene_refs": scene_refs,
        "field_geometry_refs": geom_refs,
        "text_region_refs": text_refs,
        "prompt_refs": list(prompt_refs or []),
        "session_ref": session_ref,
        "authorization_ref": authorization_ref,
        "source_refs": [r for r in source_refs if r],
        "traceability_refs": [t for t in traceability if t],
        "candidate_only": True,
        "_frame_packages": frame_inputs,
        "_object_observations": object_observations or [],
        "_aligned_observations": aligned_observations or [],
        "_scene_packages": enhanced_field_scenes or [],
        "_geometry_packages": field_geometries or [],
        "_text_regions": text_regions or [],
        "_smoke_run": smoke_run,
        "_io_inspection": io_inspection,
    }
