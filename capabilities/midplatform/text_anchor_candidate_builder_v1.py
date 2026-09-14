# -*- coding: utf-8 -*-
"""Text anchor candidate builder v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional


def build_text_anchor_candidates(
    *,
    adapter_input: Dict[str, Any],
    raw_output: Dict[str, Any],
    observations: List[Dict[str, Any]],
    regions: List[Dict[str, Any]],
    case_overrides: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """Build TextAnchorCandidate from text + region + spatial refs."""
    overrides = case_overrides or {}
    if raw_output.get("_blocked"):
        return []

    results: List[Dict[str, Any]] = []
    execution_mode = adapter_input.get("execution_mode", "adapter_stub")
    geoms = adapter_input.get("_geometry_packages") or []
    anchors = adapter_input.get("_spatial_anchors") or []
    has_spatial = bool(geoms or anchors) and not overrides.get("no_spatial_ref")

    for obs in observations:
        region = regions[0] if regions else None
        anchor_id = f"tac_{uuid.uuid4().hex[:12]}"
        anchor_conf = "medium" if has_spatial else "low"
        spatial_rel = "reliable" if has_spatial and len(geoms) >= 1 else "unreliable"
        if execution_mode in ("cached_output", "adapter_stub") and anchor_conf == "high":
            anchor_conf = "medium"
        if not has_spatial:
            spatial_rel = "unreliable"
            anchor_conf = "low"

        anchor_type = overrides.get("anchor_type", "storefront_text_anchor")
        if obs.get("text_type_hint") == "floor_indicator":
            anchor_type = "floor_text_anchor"

        results.append({
            "text_anchor_candidate_id": anchor_id,
            "source_text_observation_ref": obs.get("text_observation_candidate_id"),
            "source_text_region_ref": (region or {}).get("text_region_candidate_id"),
            "associated_spatial_anchor_refs": [a.get("spatial_anchor_candidate_id") for a in anchors if a],
            "associated_field_geometry_refs": [g.get("field_geometry_candidate_id") for g in geoms if g],
            "anchor_text": obs.get("text", ""),
            "normalized_anchor_text": obs.get("normalized_text"),
            "anchor_type": anchor_type,
            "anchor_confidence": anchor_conf,
            "spatial_reliability": spatial_rel,
            "observation_count": overrides.get("observation_count", 1),
            "warning_codes": obs.get("warning_codes") or [],
            "missing_information": [] if has_spatial else ["no_spatial_ref_anchor_degraded"],
            "source_refs": [obs.get("text_observation_candidate_id"), adapter_input.get("adapter_input_id")],
            "evidence_refs": [adapter_input.get("model_ref")],
            "traceability_refs": list(obs.get("traceability_refs") or []) + [anchor_id],
            "candidate_only": True,
        })
    return results
