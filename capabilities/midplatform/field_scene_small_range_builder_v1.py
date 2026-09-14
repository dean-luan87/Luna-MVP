# -*- coding: utf-8 -*-
"""Field Scene Small Range Construction — builder v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.field_scene_small_range_static_validators_v1 import (
    validate_field_entity,
    validate_field_scene,
    validate_object_observation,
)
from capabilities.midplatform.field_scene_small_range_types_v1 import (
    FACT_STATUS_CANDIDATE,
    bbox_center,
    pseudo_3d_from_bbox_center,
)

INNER_MAX_M = 3.0
WORKING_MAX_M = 10.0
FORECAST_MAX_M = 20.0
DEFAULT_FIELD_RADIUS_M = 20.0

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "no_world_model_fact": True,
    "no_persistent_memory": True,
    "no_runtime_execution": True,
    "no_semantic_attachment": True,
    "no_tracking_execution": True,
    "no_trajectory_simulation": True,
}


def assign_field_zone(depth_hint: Optional[float]) -> str:
    if depth_hint is None:
        return "unknown"
    if depth_hint <= INNER_MAX_M:
        return "inner_zone"
    if depth_hint <= WORKING_MAX_M:
        return "working_zone"
    if depth_hint <= FORECAST_MAX_M:
        return "forecast_zone"
    return "unknown"


def attach_depth_hint(
    obs: Dict[str, Any],
    depth_candidate: Optional[Dict[str, Any]] = None,
) -> Tuple[Optional[float], str, float, bool, bool]:
    """Return depth_hint, depth_source, depth_confidence, depth_error_expected, depth_unknown."""
    if obs.get("depth_hint") is not None:
        src = obs.get("depth_source") or "estimated"
        conf = float(obs.get("depth_confidence", 0.5))
        err = src == "estimated" or obs.get("depth_error_expected", src == "estimated")
        return float(obs["depth_hint"]), src, conf, err, False
    hints = (depth_candidate or {}).get("object_depth_hints") or {}
    oid = obs.get("observation_id")
    if oid in hints:
        return float(hints[oid]), "estimated", float((depth_candidate or {}).get("depth_confidence", 0.4)), True, False
    return None, "unknown", 0.0, True, True


def normalize_spatial_payload(
    obs: Dict[str, Any],
    frame_width: int = 640,
    frame_height: int = 480,
) -> Dict[str, Any]:
    bbox = dict(obs.get("bbox") or {})
    center = bbox_center(bbox)
    return {
        **obs,
        "bbox": bbox,
        "bbox_center": center,
        "frame_ref": obs.get("frame_ref", "frame_0"),
        "frame_width": obs.get("frame_width", frame_width),
        "frame_height": obs.get("frame_height", frame_height),
    }


def build_field_entity_candidate(
    obs: Dict[str, Any],
    field_scene_id: str,
    depth_candidate: Optional[Dict[str, Any]] = None,
) -> Tuple[Dict[str, Any], List[str]]:
    warnings: List[str] = []
    depth_hint, depth_source, depth_conf, depth_err, depth_unknown = attach_depth_hint(obs, depth_candidate)
    center = obs.get("bbox_center") or bbox_center(obs["bbox"])
    pseudo = pseudo_3d_from_bbox_center(center, depth_hint)
    zone = assign_field_zone(depth_hint)
    conf = float(obs.get("confidence", 0.0))
    if conf < 0.4:
        warnings.append("low_confidence_object_retained")
    entity = {
        "entity_candidate_id": f"fec_{uuid.uuid4().hex[:12]}",
        "field_scene_ref": field_scene_id,
        "observation_refs": [obs["observation_id"]],
        "entity_type": obs.get("source_type", "object"),
        "label": obs["label"],
        "confidence": conf,
        "bbox": obs["bbox"],
        "mask_ref": obs.get("mask_ref"),
        "depth_hint": depth_hint,
        "depth_unknown": depth_unknown,
        "depth_source": depth_source,
        "depth_confidence": depth_conf,
        "depth_error_expected": depth_err,
        "pseudo_3d_position": pseudo,
        "field_zone": zone,
        "static_dynamic_hint": obs.get("static_dynamic_hint", "static"),
        "task_relevance_hint": obs.get("task_relevance_hint"),
        "risk_hint": obs.get("risk_hint"),
        "source_refs": [obs.get("source_ref", "mock_source")],
        "evidence_refs": [obs["observation_id"]],
        "fact_status": FACT_STATUS_CANDIDATE,
    }
    ok, issues = validate_field_entity(entity)
    if not ok:
        warnings.extend(issues)
    return entity, warnings


def assemble_field_scene_candidate(
    *,
    field_scene_id: str,
    field_session_ref: str,
    timestamp: str,
    user_ref: str,
    camera_ref: str,
    entities: List[Dict[str, Any]],
    missing_information: List[str],
    camera_state: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    zones = sorted({e["field_zone"] for e in entities})
    active = [z for z in zones if z in ("inner_zone", "working_zone")]
    depth_sources = [e.get("depth_source") for e in entities]
    scene = {
        "field_scene_id": field_scene_id,
        "field_session_ref": field_session_ref,
        "timestamp": timestamp,
        "user_ref": user_ref,
        "camera_ref": camera_ref,
        "field_origin": "self_centered",
        "field_radius_m": DEFAULT_FIELD_RADIUS_M,
        "active_zones": active or ["inner_zone", "working_zone"],
        "entity_candidates": entities,
        "scene_quality_summary": {
            "entity_count": len(entities),
            "zones_present": zones,
            "camera_heading_present": bool((camera_state or {}).get("heading_hint")),
        },
        "depth_quality_summary": {
            "estimated_count": depth_sources.count("estimated"),
            "unknown_count": depth_sources.count("unknown"),
            "hardware_count": depth_sources.count("hardware"),
        },
        "construction_status": "constructed",
        "missing_information": missing_information,
        "traceability_refs": [field_session_ref, camera_ref],
        "governance_refs": ["field_scene_small_range_construction_v1"],
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
    }
    return scene


def emit_construction_result(
    *,
    field_scene: Dict[str, Any],
    input_count: int,
    warnings: List[str],
    missing_information: List[str],
    construction_pass: bool,
) -> Dict[str, Any]:
    return {
        "result_id": f"fscr_{uuid.uuid4().hex[:12]}",
        "input_observation_count": input_count,
        "entity_candidate_count": len(field_scene.get("entity_candidates") or []),
        "constructed_field_scene_ref": field_scene["field_scene_id"],
        "construction_pass": construction_pass,
        "reason_codes": ["small_range_field_scene_built"] if construction_pass else ["construction_incomplete"],
        "warnings": warnings,
        "missing_information": missing_information,
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
    }


def construct_small_range_field_scene(
    *,
    observations: List[Dict[str, Any]],
    user_state: Dict[str, Any],
    camera_state: Dict[str, Any],
    depth_candidate: Optional[Dict[str, Any]] = None,
    field_session_ref: str = "fs_session_mock",
) -> Dict[str, Any]:
    """Full 10-step pipeline for small range field scene construction."""
    warnings: List[str] = []
    missing: List[str] = []
    valid_obs: List[Dict[str, Any]] = []

    for obs in observations:
        ok, issues = validate_object_observation(obs)
        if not ok:
            warnings.extend([f"invalid_obs:{obs.get('observation_id')}:{i}" for i in issues])
            continue
        valid_obs.append(obs)

    fw = int(camera_state.get("frame_width", 640))
    fh = int(camera_state.get("frame_height", 480))
    normalized = [normalize_spatial_payload(o, fw, fh) for o in valid_obs]

    if not camera_state.get("heading_hint"):
        missing.append("camera_heading_hint_missing")

    field_scene_id = f"fs_{uuid.uuid4().hex[:12]}"
    entities: List[Dict[str, Any]] = []
    for obs in normalized:
        entity, ew = build_field_entity_candidate(obs, field_scene_id, depth_candidate)
        entities.append(entity)
        warnings.extend(ew)

    timestamp = camera_state.get("timestamp") or user_state.get("timestamp", "2026-06-11T00:00:00Z")
    scene = assemble_field_scene_candidate(
        field_scene_id=field_scene_id,
        field_session_ref=field_session_ref,
        timestamp=timestamp,
        user_ref=user_state.get("user_ref", "user_self_ref"),
        camera_ref=camera_state.get("camera_ref", "camera_ref"),
        entities=entities,
        missing_information=missing,
        camera_state=camera_state,
    )
    scene_ok, scene_issues = validate_field_scene(scene)
    if not scene_ok:
        warnings.extend(scene_issues)
    construction_pass = scene_ok and len(entities) >= 1
    result = emit_construction_result(
        field_scene=scene,
        input_count=len(observations),
        warnings=warnings,
        missing_information=missing,
        construction_pass=construction_pass,
    )
    return {
        "field_scene": scene,
        "entities": entities,
        "construction_result": result,
        "warnings": warnings,
        "construction_pass": construction_pass,
    }
