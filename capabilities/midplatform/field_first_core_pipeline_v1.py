# -*- coding: utf-8 -*-
"""Field-First Core Logic — pipeline helpers v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional


def scene_to_tracking_summary(scene: Dict[str, Any]) -> Dict[str, Any]:
    entities: List[Dict[str, Any]] = []
    for e in scene.get("entity_candidates") or []:
        entities.append({
            "entity_candidate_id": e.get("entity_candidate_id"),
            "label": e.get("label"),
            "bbox": e.get("bbox"),
            "pseudo_3d_position": e.get("pseudo_3d_position"),
            "field_zone": e.get("field_zone", "unknown"),
            "confidence": e.get("confidence", 0.0),
            "risk_hint": e.get("risk_hint"),
            "depth_source": e.get("depth_source"),
            "depth_unknown": e.get("depth_unknown"),
        })
    return {"field_scene_id": scene.get("field_scene_id", "fs_unknown"), "entities": entities}


def scene_to_continuity_summary(scene: Dict[str, Any]) -> Dict[str, Any]:
    labels = [e.get("label") for e in scene.get("entity_candidates") or []]
    return {
        "field_scene_id": scene.get("field_scene_id"),
        "entity_labels": labels,
        "entity_count": len(labels),
        "active_zones": scene.get("active_zones") or [],
    }


def derive_continuity_evaluation_context(
    *,
    previous_scene: Optional[Dict[str, Any]],
    current_scene: Dict[str, Any],
    override: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    if override:
        return dict(override)
    prev = scene_to_continuity_summary(previous_scene) if previous_scene else {"entity_labels": [], "entity_count": 0}
    curr = scene_to_continuity_summary(current_scene)
    prev_labels = prev.get("entity_labels") or []
    curr_labels = curr.get("entity_labels") or []
    overlap = len(set(prev_labels) & set(curr_labels))
    return {
        "location_prev": "mock_loc",
        "location_curr": "mock_loc",
        "entity_labels_prev": prev_labels,
        "entity_labels_curr": curr_labels,
        "entity_count_prev": len(prev_labels),
        "entity_count_curr": len(curr_labels),
        "layout_hash_prev": "_".join(sorted(prev_labels)) or "empty",
        "layout_hash_curr": "_".join(sorted(curr_labels)) or "empty",
        "overlap_count": overlap,
        "time_gap_s": 0.5,
        "heading_prev": 0,
        "heading_curr": 0,
    }


def infer_depth_source_from_scene(scene: Dict[str, Any]) -> str:
    sources = [e.get("depth_source") for e in scene.get("entity_candidates") or []]
    if any(s == "unknown" for s in sources):
        return "unknown"
    if any(s == "estimated" for s in sources):
        return "estimated"
    return "hardware"
