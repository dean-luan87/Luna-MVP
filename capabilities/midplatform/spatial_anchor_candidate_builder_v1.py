# -*- coding: utf-8 -*-
"""Spatial anchor candidate builder v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional


def build_spatial_anchor_candidates(
    *,
    adapter_input: Dict[str, Any],
    raw_output: Dict[str, Any],
    poses: List[Dict[str, Any]],
    case_overrides: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """Build spatial anchor candidates from raw output and stable entity hints."""
    overrides = case_overrides or {}
    if raw_output.get("_blocked"):
        return []
    anchors: List[Dict[str, Any]] = []
    raw_ref = raw_output.get("raw_output_id")
    scenes = adapter_input.get("_scene_packages") or []
    raw_anchor = raw_output.get("raw_anchor_payload")

    if raw_anchor:
        aid = f"sac_{uuid.uuid4().hex[:12]}"
        anchors.append({
            "spatial_anchor_candidate_id": aid,
            "source_raw_output_ref": raw_ref,
            "anchor_type": raw_anchor.get("anchor_type", "unknown_anchor"),
            "source_frame_refs": raw_anchor.get("source_frame_refs") or [],
            "associated_field_entity_refs": raw_anchor.get("entity_refs") or [],
            "associated_geometry_refs": [],
            "position_candidate": raw_anchor.get("position") or {"x": 0.0, "y": 0.0, "z": 0.0},
            "coordinate_mode": "session_local_candidate",
            "stability_score": raw_anchor.get("stability_score", "medium"),
            "observation_count": raw_anchor.get("observation_count", 1),
            "first_seen_at": raw_anchor.get("first_seen_at"),
            "last_seen_at": raw_anchor.get("last_seen_at"),
            "conflict_refs": [],
            "warning_codes": [],
            "missing_information": [],
            "source_refs": [adapter_input.get("adapter_input_id"), raw_ref],
            "evidence_refs": [adapter_input.get("model_ref")],
            "traceability_refs": list(adapter_input.get("traceability_refs") or []) + [aid],
            "candidate_only": True,
        })

    for scene in scenes:
        for ent in scene.get("entity_candidates") or []:
            label = (ent.get("label") or "").lower()
            obs_count = overrides.get("observation_count", ent.get("observation_count", 1))
            stability = "high" if obs_count >= 3 else ("medium" if obs_count >= 2 else "low")
            if obs_count < 2 and overrides.get("require_high_stability"):
                continue
            anchor_type = "static_object_anchor"
            if label in ("door",):
                anchor_type = "doorway_anchor"
            elif label in ("wall", "floor"):
                anchor_type = "wall_floor_anchor"
            elif label in ("sign",):
                anchor_type = "structural_anchor"
            elif label in ("table", "chair"):
                anchor_type = "static_object_anchor"

            aid = f"sac_{uuid.uuid4().hex[:12]}"
            anchors.append({
                "spatial_anchor_candidate_id": aid,
                "source_raw_output_ref": raw_ref,
                "anchor_type": overrides.get("anchor_type", anchor_type),
                "source_frame_refs": [scene.get("frame_ref")],
                "associated_field_entity_refs": [ent.get("entity_id") or ent.get("observation_id")],
                "associated_geometry_refs": [],
                "position_candidate": ent.get("position_candidate") or {"x": 1.0, "y": 0.5, "z": 2.0},
                "coordinate_mode": "session_local_candidate",
                "stability_score": stability,
                "observation_count": obs_count,
                "first_seen_at": scene.get("timestamp"),
                "last_seen_at": scene.get("timestamp"),
                "conflict_refs": [],
                "warning_codes": ["text_anchor_reserved_not_ocr"] if overrides.get("text_anchor_reserved") else [],
                "missing_information": [],
                "source_refs": [scene.get("field_scene_id"), adapter_input.get("adapter_input_id"), raw_ref],
                "evidence_refs": [ent.get("observation_id") or ent.get("entity_id")],
                "traceability_refs": list(adapter_input.get("traceability_refs") or []) + [aid],
                "candidate_only": True,
            })
    return anchors
