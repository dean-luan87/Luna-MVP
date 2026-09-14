# -*- coding: utf-8 -*-
"""Field Scene Small Range Construction — candidate type definitions v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

FIELD_ZONES: Tuple[str, ...] = ("inner_zone", "working_zone", "forecast_zone", "unknown")
DEPTH_SOURCES: Tuple[str, ...] = ("estimated", "hardware", "unknown")
FACT_STATUS_CANDIDATE = "candidate"

OBJECT_OBSERVATION_REQUIRED: Tuple[str, ...] = (
    "observation_id", "timestamp", "source_ref", "label", "confidence", "bbox",
)
DEPTH_OBSERVATION_REQUIRED: Tuple[str, ...] = (
    "observation_id", "frame_ref", "timestamp", "depth_source", "depth_confidence",
)
CAMERA_STATE_REQUIRED: Tuple[str, ...] = ("camera_ref", "timestamp", "frame_width", "frame_height")
USER_STATE_REQUIRED: Tuple[str, ...] = ("user_ref", "timestamp")

FIELD_SCENE_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "field_scene_id", "field_session_ref", "timestamp", "user_ref", "camera_ref",
    "field_origin", "field_radius_m", "active_zones", "entity_candidates",
    "scene_quality_summary", "depth_quality_summary", "construction_status",
    "missing_information", "traceability_refs", "governance_refs", "non_execution_flags",
)

FIELD_ENTITY_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "entity_candidate_id", "field_scene_ref", "observation_refs", "entity_type", "label",
    "confidence", "bbox", "depth_hint", "depth_source", "depth_confidence",
    "depth_error_expected", "pseudo_3d_position", "field_zone", "static_dynamic_hint",
    "task_relevance_hint", "risk_hint", "source_refs", "evidence_refs", "fact_status",
)

CONSTRUCTION_RESULT_FIELDS: Tuple[str, ...] = (
    "result_id", "input_observation_count", "entity_candidate_count",
    "constructed_field_scene_ref", "construction_pass", "reason_codes",
    "warnings", "missing_information", "non_execution_flags",
)


def bbox_center(bbox: Dict[str, Any]) -> Dict[str, float]:
    x1, y1 = float(bbox.get("x1", 0)), float(bbox.get("y1", 0))
    x2, y2 = float(bbox.get("x2", 0)), float(bbox.get("y2", 0))
    return {"x": (x1 + x2) / 2.0, "y": (y1 + y2) / 2.0}


def pseudo_3d_from_bbox_center(center: Dict[str, float], depth_hint: Optional[float]) -> Dict[str, Any]:
    if depth_hint is None:
        return {"status": "pseudo_3d_unknown", "x": None, "y": None, "z": None}
    return {
        "status": "estimated",
        "x": center["x"],
        "y": center["y"],
        "z": float(depth_hint),
    }
