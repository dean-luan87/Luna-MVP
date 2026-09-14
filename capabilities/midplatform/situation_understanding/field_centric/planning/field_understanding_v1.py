# -*- coding: utf-8 -*-
"""Field Understanding — 场理解，非 scene label v1."""

from __future__ import annotations

from typing import Any, Dict
from uuid import uuid4

from capabilities.midplatform.situation_understanding.field_centric.planning.field_profiles_v1 import (
    get_field_profile,
)


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def understand_field(*, field_key: str) -> Dict[str, Any]:
    """
    Field Understanding — 先问「在什么场」，再问「是什么物体」。
    NOT: scene = mall
    """
    profile = get_field_profile(field_key)
    props = profile.get("field_properties") or {}

    return {
        "understanding_id": _uid("fld"),
        "layer": "field_understanding",
        "field_candidate": profile.get("field_candidate"),
        "field_properties": props,
        "expected_entity_profile": props.get("expected_entities") or [],
        "expected_behavior_profile": props.get("expected_behaviors") or [],
        "expected_information_profile": props.get("expected_information") or [],
        "risk_pattern_profile": props.get("risk_patterns") or [],
        "field_not_scene_label": profile.get("field_not_scene_label") is True,
        "field_before_object": True,
        "candidate_only": True,
        "not_fact": True,
    }
