# -*- coding: utf-8 -*-
"""Object Role Inference — 场 + 交互 → role candidate v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

ROLE_BY_FIELD_OBJECT: Dict[str, Dict[str, Dict[str, Any]]] = {
    "home_furniture_store": {
        "metal_rack": {"role_candidate": "folding_furniture_display_rack", "confidence": 0.88},
    },
    "construction_site": {
        "metal_rack": {"role_candidate": "scaffolding_structure", "confidence": 0.86},
    },
    "shopping_mall_public_area": {
        "uniform_person": {"role_candidate": "security_or_staff", "confidence": 0.82},
        "glowing_screen": {"role_candidate": "advertisement_or_info_display", "confidence": 0.80},
        "crowd": {"role_candidate": "shopping_crowd", "normality": "normal", "confidence": 0.85},
        "red_device": {"role_candidate": "decorative_art_installation", "confidence": 0.78},
        "person_with_machine": {"role_candidate": "unusual_behavior_near_crowd", "normality": "abnormal", "risk_level": "high", "confidence": 0.83},
    },
    "hospital_public_area": {
        "uniform_person": {"role_candidate": "medical_or_care_staff", "confidence": 0.84},
    },
    "greenery_maintenance_zone": {
        "scissor_machine": {"role_candidate": "pruning_tool", "normality": "normal", "confidence": 0.90},
        "person_with_machine": {"role_candidate": "landscaping_worker", "normality": "normal", "risk_level": "low", "confidence": 0.88},
    },
    "barber_shop": {
        "scissor_machine": {"role_candidate": "haircut_tool", "normality": "normal", "confidence": 0.91},
    },
    "subway_platform": {
        "glowing_screen": {"role_candidate": "wayfinding_display", "confidence": 0.92},
    },
    "restaurant_dining": {
        "glowing_screen": {"role_candidate": "ordering_screen", "confidence": 0.89},
    },
    "street_intersection": {
        "crowd": {"role_candidate": "pedestrian_congestion", "normality": "risk", "risk_level": "medium", "confidence": 0.87},
        "person_with_machine": {"role_candidate": "unusual_behavior_near_crowd", "normality": "abnormal", "risk_level": "high", "confidence": 0.83},
    },
    "fire_safety_zone": {
        "red_device": {"role_candidate": "fire_safety_equipment", "confidence": 0.93},
    },
}

INTERACTION_ROLE_INFERENCE: Dict[str, Dict[str, Any]] = {
    "unknown_sculpture_touch": {
        "unknown_sculpture": {
            "role_candidate": "interactive_art_exhibit",
            "inferred_from": "interaction",
            "confidence": 0.75,
        },
    },
}


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def infer_object_roles(
    *,
    field_key: str,
    object_ids: List[str],
    interaction_graph: Dict[str, Any],
    interaction_fixture_key: str = "",
) -> Dict[str, Any]:
    """
    Object Role Candidate — 同一物体在不同场中不同 role。
    行为意义 = 动作 + 场 + 作用对象 + 结果
    """
    field_roles = ROLE_BY_FIELD_OBJECT.get(field_key, {})
    interaction_roles = INTERACTION_ROLE_INFERENCE.get(interaction_fixture_key, {})
    roles: List[Dict[str, Any]] = []

    for oid in object_ids:
        if oid in interaction_roles:
            entry = interaction_roles[oid]
            roles.append({
                "role_id": _uid("role"),
                "object_id": oid,
                "role_candidate": entry.get("role_candidate"),
                "inferred_from": entry.get("inferred_from", "field_and_interaction"),
                "confidence": entry.get("confidence", 0.0),
                "candidate_only": True,
                "not_fact": True,
            })
        elif oid in field_roles:
            entry = field_roles[oid]
            roles.append({
                "role_id": _uid("role"),
                "object_id": oid,
                "role_candidate": entry.get("role_candidate"),
                "normality": entry.get("normality"),
                "risk_level": entry.get("risk_level"),
                "inferred_from": "field_context",
                "confidence": entry.get("confidence", 0.0),
                "candidate_only": True,
                "not_fact": True,
            })
        else:
            roles.append({
                "role_id": _uid("role"),
                "object_id": oid,
                "role_candidate": "unresolved",
                "inferred_from": "field_constrained_unknown",
                "candidate_only": True,
            })

    same_object_different_field = len(set(r.get("role_candidate") for r in roles if r.get("role_candidate") != "unresolved")) >= 1

    return {
        "inference_id": _uid("ori"),
        "object_role_candidates": roles,
        "field_before_object_role": True,
        "not_object_first": True,
        "candidate_only": True,
    }
