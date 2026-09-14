# -*- coding: utf-8 -*-
"""Enhanced FieldEntity builder v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.field_scene_small_range_types_v1 import bbox_center


def _entity_confidence(obj_conf: float, geom_conf: str | None, depth_conf: str | None) -> str:
    if obj_conf < 0.5:
        return "low"
    if geom_conf == "low" or depth_conf in ("low", "unknown"):
        return "low"
    if geom_conf in ("medium", "low") or depth_conf == "medium":
        return "medium"
    return "medium"


def build_enhanced_field_entity_candidates(
    assembly_input: Dict[str, Any],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Build EnhancedFieldEntityCandidate list from assembly input."""
    objects = {o["observation_id"]: o for o in (assembly_input.get("object_observations") or [])}
    hints = {h["object_observation_ref"]: h for h in (assembly_input.get("object_depth_hints") or []) if h.get("object_observation_ref")}
    spatials = {s["object_observation_ref"]: s for s in (assembly_input.get("object_spatial_states") or []) if s.get("object_observation_ref")}
    geometries = {g["object_observation_ref"]: g for g in (assembly_input.get("field_geometry_candidates") or []) if g.get("object_observation_ref")}

    entities: List[Dict[str, Any]] = []
    rejected: List[Dict[str, Any]] = []

    # geometry without object anchor
    for geom in assembly_input.get("field_geometry_candidates") or []:
        obs_ref = geom.get("object_observation_ref")
        if obs_ref and obs_ref not in objects:
            rejected.append({
                "field_geometry_ref": geom.get("geometry_candidate_id"),
                "object_observation_ref": obs_ref,
                "reason": "geometry_without_object_anchor",
            })

    for obs_id, obj in objects.items():
        if not obj.get("observation_id"):
            rejected.append({"object_observation_ref": obs_id, "reason": "invalid_object_missing_id"})
            continue

        hint = hints.get(obs_id)
        spatial = spatials.get(obs_id)
        geometry = geometries.get(obs_id)

        bbox = dict(obj.get("bbox") or {})
        try:
            center = bbox_center(bbox) if bbox else None
        except (TypeError, ValueError):
            center = None

        obj_conf = float(obj.get("confidence", 0.5))
        warnings: List[str] = []
        missing: List[str] = list(obj.get("missing_information") or [])
        conflicts: List[str] = []

        if obj_conf < 0.5:
            warnings.append("low_object_confidence")

        if geometry and geometry.get("geometry_status") in ("geometry_estimated", "geometry_weak_estimated"):
            entity_status = "entity_geometry_enhanced"
            if geometry.get("geometry_status") == "geometry_weak_estimated":
                entity_status = "entity_degraded"
        elif geometry and geometry.get("geometry_status") == "geometry_unknown":
            entity_status = "entity_geometry_unknown"
        elif hint and hint.get("object_depth_hint") is not None:
            entity_status = "entity_degraded"
        elif hint or spatial:
            entity_status = "entity_geometry_unknown"
        else:
            entity_status = "entity_2d_only"
            missing.append("depth_and_geometry_missing")

        if hint:
            warnings.extend(hint.get("warning_codes") or [])
            missing.extend(hint.get("missing_information") or [])
            conflicts.extend(hint.get("conflict_refs") or [])
        if geometry:
            warnings.extend(geometry.get("warning_codes") or [])
            missing.extend(geometry.get("missing_information") or [])
            conflicts.extend(geometry.get("conflict_refs") or [])

        depth_hint = None
        depth_source = "unknown"
        depth_conf = "unknown"
        depth_error = True
        pseudo_pos = None
        pseudo_status = "pseudo_3d_unknown"
        field_zone = "unknown"
        dist_bucket = "unknown"
        geom_conf = None

        if geometry:
            pseudo_pos = geometry.get("pseudo_3d_position")
            field_zone = geometry.get("field_zone", "unknown")
            dist_bucket = geometry.get("distance_bucket", "unknown")
            geom_conf = geometry.get("geometry_confidence")
            pseudo_status = (spatial or {}).get("pseudo_3d_status", "pseudo_3d_estimated")
        elif spatial:
            pseudo_pos = spatial.get("pseudo_3d_position")
            pseudo_status = spatial.get("pseudo_3d_status", "pseudo_3d_unknown")
            field_zone = spatial.get("field_zone", "unknown")
            dist_bucket = spatial.get("distance_bucket", "unknown")
            geom_conf = spatial.get("spatial_confidence")
        elif hint:
            field_zone = hint.get("field_zone_hint", "unknown")
            dist_bucket = hint.get("depth_bucket", "unknown")

        if hint:
            depth_hint = hint.get("object_depth_hint")
            depth_source = hint.get("depth_source", "estimated")
            depth_conf = hint.get("depth_confidence", "unknown")
            depth_error = hint.get("depth_error_expected", True) is True
        elif spatial:
            depth_hint = spatial.get("depth_hint")
            depth_error = True

        if entity_status == "entity_2d_only":
            field_zone = "unknown"

        ent_conf = _entity_confidence(obj_conf, geom_conf, depth_conf)
        if warnings and ent_conf == "medium":
            ent_conf = "low"

        entity = {
            "entity_candidate_id": f"efc_{uuid.uuid4().hex[:12]}",
            "field_scene_ref": None,
            "object_observation_ref": obs_id,
            "object_depth_hint_ref": hint.get("object_depth_hint_id") if hint else None,
            "object_spatial_state_ref": spatial.get("object_spatial_state_id") if spatial else None,
            "field_geometry_ref": geometry.get("geometry_candidate_id") if geometry else None,
            "label": obj.get("label", "unknown_object"),
            "confidence": obj_conf,
            "bbox": bbox,
            "bbox_center": center or (spatial or {}).get("bbox_center"),
            "depth_hint": depth_hint,
            "depth_source": depth_source,
            "depth_confidence": depth_conf,
            "depth_error_expected": depth_error,
            "pseudo_3d_position": pseudo_pos,
            "pseudo_3d_status": pseudo_status,
            "field_zone": field_zone,
            "distance_bucket": dist_bucket,
            "geometry_confidence": geom_conf,
            "entity_confidence": ent_conf,
            "entity_status": entity_status,
            "source_refs": [obs_id] + ([hint["object_depth_hint_id"]] if hint else []) + ([geometry["geometry_candidate_id"]] if geometry else []),
            "evidence_refs": list(obj.get("evidence_refs") or []),
            "traceability_refs": [obj.get("frame_ref", "frame_0")],
            "conflict_refs": sorted(set(conflicts)),
            "warning_codes": sorted(set(warnings)),
            "missing_information": sorted(set(missing)),
            "fact_status": "candidate",
            "candidate_only": True,
        }
        entities.append(entity)

    return entities, rejected
