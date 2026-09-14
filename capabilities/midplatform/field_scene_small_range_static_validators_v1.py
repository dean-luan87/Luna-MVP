# -*- coding: utf-8 -*-
"""Field Scene Small Range Construction — static validators v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.field_scene_small_range_types_v1 import (
    CAMERA_STATE_REQUIRED,
    DEPTH_SOURCES,
    FACT_STATUS_CANDIDATE,
    FIELD_ENTITY_CANDIDATE_FIELDS,
    FIELD_SCENE_CANDIDATE_FIELDS,
    FIELD_ZONES,
    OBJECT_OBSERVATION_REQUIRED,
    USER_STATE_REQUIRED,
)


def validate_object_observation(obs: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for f in OBJECT_OBSERVATION_REQUIRED:
        if not obs.get(f):
            issues.append(f"missing_{f}")
    bbox = obs.get("bbox") or {}
    if not all(k in bbox for k in ("x1", "y1", "x2", "y2")):
        issues.append("invalid_bbox")
    return len(issues) == 0, issues


def validate_field_entity(entity: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for f in FIELD_ENTITY_CANDIDATE_FIELDS:
        if f not in entity:
            issues.append(f"missing_{f}")
    if entity.get("fact_status") != FACT_STATUS_CANDIDATE:
        issues.append("fact_status_not_candidate")
    if entity.get("field_zone") not in FIELD_ZONES:
        issues.append("invalid_field_zone")
    if entity.get("depth_source") not in DEPTH_SOURCES:
        issues.append("invalid_depth_source")
    depth_hint = entity.get("depth_hint")
    if depth_hint is None and entity.get("depth_unknown") is not True:
        if "depth_hint" not in entity and "depth_unknown" not in entity:
            issues.append("missing_depth_hint_or_unknown")
    pseudo = entity.get("pseudo_3d_position") or {}
    if pseudo.get("status") not in ("estimated", "pseudo_3d_unknown"):
        issues.append("invalid_pseudo_3d")
    if entity.get("depth_source") == "estimated" and entity.get("depth_error_expected") is not True:
        issues.append("estimated_depth_must_mark_error_expected")
    if entity.get("depth_source") == "hardware" and entity.get("depth_error_expected") is True:
        issues.append("hardware_depth_should_not_mark_error_as_fact")
    return len(issues) == 0, issues


def validate_field_scene(scene: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for f in FIELD_SCENE_CANDIDATE_FIELDS:
        if f not in scene:
            issues.append(f"missing_{f}")
    flags = scene.get("non_execution_flags") or {}
    if flags.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if flags.get("no_world_model_fact") is not True:
        issues.append("no_world_model_fact_required")
    if flags.get("no_persistent_memory") is not True:
        issues.append("no_persistent_memory_required")
    return len(issues) == 0, issues


def validate_camera_state(cam: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in CAMERA_STATE_REQUIRED if not cam.get(f)]
    return len(issues) == 0, issues


def validate_user_state(user: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{f}" for f in USER_STATE_REQUIRED if not user.get(f)]
    return len(issues) == 0, issues
