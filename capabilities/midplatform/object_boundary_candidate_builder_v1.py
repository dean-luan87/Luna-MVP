# -*- coding: utf-8 -*-
"""Object boundary candidate builder v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional


def build_object_boundary_candidates(
    *,
    adapter_input: Dict[str, Any],
    raw_output: Dict[str, Any],
    masks: List[Dict[str, Any]],
    case_overrides: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """Build ObjectBoundaryCandidate from polygon / contour / bbox-linked mask."""
    overrides = case_overrides or {}
    if raw_output.get("_blocked"):
        return []

    results: List[Dict[str, Any]] = []
    execution_mode = adapter_input.get("execution_mode", "adapter_stub")
    obs = adapter_input.get("_object_observations") or []
    obs_refs = [o.get("object_observation_id") for o in obs if o]
    has_object = bool(obs_refs) and not overrides.get("no_object_ref")
    raw_boundary = raw_output.get("raw_boundary_payload") or raw_output.get("raw_polygon_payload") or {}
    raw_mask = raw_output.get("raw_mask_payload") or {}

    if not raw_boundary and not raw_mask.get("polygon") and not raw_mask.get("bbox"):
        return results

    boundary_id = f"obc_{uuid.uuid4().hex[:12]}"
    boundary_conf = "medium" if has_object else "low"
    boundary_quality = "usable" if has_object else "degraded"
    if execution_mode in ("cached_output", "adapter_stub") and boundary_conf == "high":
        boundary_conf = "medium"
    if not has_object:
        boundary_conf = "low"
        boundary_quality = "degraded"

    mask_refs = [m.get("mask_ref") or m.get("mask_observation_candidate_id") for m in masks if m]

    results.append({
        "object_boundary_candidate_id": boundary_id,
        "source_raw_output_ref": raw_output.get("raw_output_id"),
        "frame_ref": (adapter_input.get("_frame_packages") or [{}])[0].get("frame_ref"),
        "associated_object_observation_refs": obs_refs,
        "associated_mask_refs": [r for r in mask_refs if r],
        "bbox": raw_boundary.get("bbox") or raw_mask.get("bbox"),
        "polygon": raw_boundary.get("polygon") or raw_mask.get("polygon"),
        "contour": overrides.get("contour"),
        "boundary_confidence": boundary_conf,
        "boundary_quality": boundary_quality,
        "warning_codes": masks[0].get("warning_codes") if masks else [],
        "missing_information": [] if has_object else ["no_object_ref_boundary_degraded"],
        "source_refs": [adapter_input.get("adapter_input_id"), raw_output.get("raw_output_id")],
        "evidence_refs": [adapter_input.get("model_ref")],
        "traceability_refs": list(adapter_input.get("traceability_refs") or []) + [boundary_id],
        "candidate_only": True,
    })
    return results
