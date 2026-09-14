# -*- coding: utf-8 -*-
"""FieldGeometryCandidate builder v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.field_zone_assignment_policy_v1 import assign_field_zone_from_depth_hint
from capabilities.midplatform.geometry_confidence_policy_v1 import compute_geometry_confidence
from capabilities.midplatform.pseudo_3d_projection_policy_v1 import (
    compute_bbox_center,
    estimate_pseudo_3d_position,
)


def _geometry_status_from_pseudo(pseudo_status: str) -> str:
    return {
        "pseudo_3d_estimated": "geometry_estimated",
        "pseudo_3d_weak_estimated": "geometry_weak_estimated",
        "pseudo_3d_unknown": "geometry_unknown",
        "pseudo_3d_rejected": "geometry_rejected",
    }.get(pseudo_status, "geometry_unknown")


def build_object_spatial_state_and_geometry(
    obj: Dict[str, Any],
    hint: Dict[str, Any],
) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """Build ObjectSpatialStateCandidate + FieldGeometryCandidate or rejection."""
    obs_ref = obj.get("observation_id")
    hint_ref = hint.get("object_depth_hint_id")
    bbox = dict(obj.get("bbox") or hint.get("bbox") or {})

    fw = obj.get("frame_width")
    fh = obj.get("frame_height")
    frame_size_missing = fw is None or fh is None
    fw_int = int(fw) if fw is not None else 640
    fh_int = int(fh) if fh is not None else 480

    center, bbox_valid, bbox_reason = compute_bbox_center(bbox, frame_width=fw_int, frame_height=fh_int)

    depth_hint_val = hint.get("object_depth_hint")
    if depth_hint_val is None:
        depth_hint_val = hint.get("sampled_depth_value")
    unit = hint.get("depth_value_unit", "unknown")

    pseudo_pos, pseudo_status = estimate_pseudo_3d_position(
        bbox_center_pt=center or {"x": 0, "y": 0},
        frame_width=fw_int,
        frame_height=fh_int,
        depth_hint=float(depth_hint_val) if depth_hint_val is not None else None,
        depth_value_unit=unit,
        bbox_valid=bbox_valid,
    )

    dist_bucket, field_zone, zone_warnings = assign_field_zone_from_depth_hint(hint)
    warnings = list(set(list(hint.get("warning_codes") or []) + zone_warnings))
    missing = list(hint.get("missing_information") or [])
    if frame_size_missing:
        missing = missing + [k for k in ("frame_width", "frame_height") if obj.get(k) is None]

    obj_conf = float(obj.get("confidence", 0.5))
    geom_conf, geom_reasons = compute_geometry_confidence(
        object_confidence=obj_conf,
        depth_confidence=hint.get("depth_confidence", "unknown"),
        fusion_confidence=hint.get("fusion_confidence", "unknown"),
        depth_value_unit=unit,
        missing_information=missing,
        warning_codes=warnings,
        conflict_refs=list(hint.get("conflict_refs") or []),
        alignment_confidence=hint.get("alignment_confidence"),
        frame_size_missing=frame_size_missing,
        pseudo_3d_status=pseudo_status,
    )

    spatial_reasons = list(hint.get("depth_reliability_reasons") or []) + geom_reasons
    geometry_status = _geometry_status_from_pseudo(pseudo_status)

    if not bbox_valid:
        rejection = {
            "object_observation_ref": obs_ref,
            "object_depth_hint_ref": hint_ref,
            "reason": bbox_reason,
            "geometry_status": "geometry_rejected",
        }
        return None, None, rejection

    spatial_id = f"oss_{uuid.uuid4().hex[:12]}"
    spatial = {
        "object_spatial_state_id": spatial_id,
        "object_observation_ref": obs_ref,
        "object_depth_hint_ref": hint_ref,
        "frame_ref": obj.get("frame_ref", hint.get("frame_ref", "frame_0")),
        "timestamp": obj.get("timestamp", hint.get("timestamp", "2026-06-11T00:00:00Z")),
        "label": obj.get("label", hint.get("label", "unknown_object")),
        "bbox": bbox,
        "bbox_center": center,
        "depth_hint": depth_hint_val,
        "depth_value_unit": unit,
        "pseudo_3d_position": pseudo_pos,
        "pseudo_3d_status": pseudo_status,
        "distance_bucket": dist_bucket,
        "field_zone": field_zone,
        "spatial_confidence": geom_conf,
        "spatial_reliability_reasons": spatial_reasons,
        "depth_error_expected": hint.get("depth_error_expected", True),
        "geometry_warning_codes": warnings,
        "missing_information": sorted(set(missing)),
        "source_refs": [obs_ref, hint_ref],
        "evidence_refs": list(obj.get("evidence_refs") or []) + list(hint.get("evidence_refs") or []),
        "traceability_refs": [obj.get("frame_ref", "frame_0")],
        "candidate_only": True,
    }

    geom_id = f"fgc_{uuid.uuid4().hex[:12]}"
    geometry = {
        "geometry_candidate_id": geom_id,
        "object_spatial_state_ref": spatial_id,
        "object_observation_ref": obs_ref,
        "object_depth_hint_ref": hint_ref,
        "frame_ref": spatial["frame_ref"],
        "timestamp": spatial["timestamp"],
        "label": spatial["label"],
        "bbox": bbox,
        "bbox_center": center,
        "pseudo_3d_position": pseudo_pos,
        "field_zone": field_zone,
        "distance_bucket": dist_bucket,
        "geometry_confidence": geom_conf,
        "geometry_status": geometry_status,
        "geometry_reliability_reasons": geom_reasons,
        "depth_error_expected": hint.get("depth_error_expected", True),
        "warning_codes": warnings,
        "missing_information": sorted(set(missing)),
        "conflict_refs": list(hint.get("conflict_refs") or []),
        "source_refs": [obs_ref, hint_ref, spatial_id],
        "evidence_refs": spatial["evidence_refs"],
        "traceability_refs": spatial["traceability_refs"],
        "candidate_only": True,
    }
    return spatial, geometry, None


def build_field_geometry_from_input(
    geometry_input: Dict[str, Any],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Return spatial states, geometry candidates, rejected items."""
    objects_by_id = {o["observation_id"]: o for o in (geometry_input.get("object_observations") or [])}
    hints_by_obs = {}
    for h in geometry_input.get("object_depth_hints") or []:
        ref = h.get("object_observation_ref")
        if ref:
            hints_by_obs[ref] = h

    spatials: List[Dict[str, Any]] = []
    geometries: List[Dict[str, Any]] = []
    rejected: List[Dict[str, Any]] = []

    for obs_id, obj in objects_by_id.items():
        hint = hints_by_obs.get(obs_id)
        if not hint:
            rejected.append({"object_observation_ref": obs_id, "reason": "missing_depth_hint"})
            continue
        spatial, geometry, rej = build_object_spatial_state_and_geometry(obj, hint)
        if rej:
            rejected.append(rej)
            continue
        if spatial:
            spatials.append(spatial)
        if geometry:
            geometries.append(geometry)

    return spatials, geometries, rejected
