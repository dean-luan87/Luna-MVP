# -*- coding: utf-8 -*-
"""FreeSpace candidate builder v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional


def build_freespace_candidates(
    *,
    adapter_input: Dict[str, Any],
    raw_output: Dict[str, Any],
    case_overrides: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """Build FreeSpaceCandidate from free space mask / polygon. No navigation suggestion."""
    overrides = case_overrides or {}
    if raw_output.get("_blocked"):
        return []

    raw_freespace = raw_output.get("raw_freespace_payload")
    subtype = raw_output.get("_inspect_subtype", "grounded_sam")
    if not raw_freespace and subtype != "freespace":
        return []

    fs_data = raw_freespace or {}
    execution_mode = adapter_input.get("execution_mode", "adapter_stub")
    geoms = adapter_input.get("_geometry_packages") or []
    geom_refs = [g.get("field_geometry_candidate_id") for g in geoms if g]
    has_geometry = bool(geom_refs) and not overrides.get("no_geometry_ref")

    pass_conf = "medium" if has_geometry else "low"
    if execution_mode in ("cached_output", "adapter_stub") and pass_conf == "high":
        pass_conf = "medium"
    if not has_geometry:
        pass_conf = "low"

    region_type = overrides.get("region_type", fs_data.get("region_type", "floor"))
    if region_type == "walkable_floor":
        region_type = "floor"

    fs_id = f"fsc_{uuid.uuid4().hex[:12]}"
    return [{
        "freespace_candidate_id": fs_id,
        "source_raw_output_ref": raw_output.get("raw_output_id"),
        "frame_ref": (adapter_input.get("_frame_packages") or [{}])[0].get("frame_ref"),
        "freespace_region_ref": fs_data.get("free_space_mask"),
        "passable_area_polygon": fs_data.get("passable_area"),
        "passable_area_mask_ref": fs_data.get("free_space_mask"),
        "region_type": region_type,
        "passability_confidence": pass_conf,
        "geometry_refs": geom_refs,
        "warning_codes": ["no_navigation_suggestion", "passability_not_action_permission"],
        "missing_information": [] if has_geometry else ["no_geometry_ref_freespace_degraded"],
        "source_refs": [adapter_input.get("adapter_input_id"), raw_output.get("raw_output_id")],
        "evidence_refs": [adapter_input.get("model_ref")],
        "traceability_refs": list(adapter_input.get("traceability_refs") or []) + [fs_id],
        "candidate_only": True,
    }]
