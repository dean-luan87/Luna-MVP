# -*- coding: utf-8 -*-
"""Luna Field-Centric Object Role — planning processor v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.situation_understanding.field_centric.planning.field_centric_adapter_v1 import (
    run_field_centric_object_role_planning,
)


def _role(result: Dict[str, Any], object_id: str) -> str:
    roles = (result.get("object_role_inference") or {}).get("object_role_candidates") or []
    entry = next((r for r in roles if r.get("object_id") == object_id), {})
    return entry.get("role_candidate", "")


def run_same_object_different_field_role() -> Dict[str, Any]:
    """Case A: metal_rack 在家居店 vs 工地 → 不同 role."""
    furniture = run_field_centric_object_role_planning(fixture_key="metal_rack_furniture")
    construction = run_field_centric_object_role_planning(fixture_key="metal_rack_construction")
    return {
        "scenario": "case_a_same_object_different_field_role",
        "furniture_result": furniture,
        "construction_result": construction,
        "furniture_role": _role(furniture, "metal_rack"),
        "construction_role": _role(construction, "metal_rack"),
        "roles_differ": _role(furniture, "metal_rack") != _role(construction, "metal_rack"),
        "field_before_object": furniture.get("field_before_object_role") is True,
    }


def run_same_behavior_different_field_risk() -> Dict[str, Any]:
    """Case B: 人持机器在绿化带正常 vs 商场近人群 → 不同 risk."""
    greenery = run_field_centric_object_role_planning(fixture_key="person_machine_greenery")
    mall = run_field_centric_object_role_planning(fixture_key="person_machine_mall")
    g_roles = (greenery.get("object_role_inference") or {}).get("object_role_candidates") or []
    m_roles = (mall.get("object_role_inference") or {}).get("object_role_candidates") or []
    g_person = next((r for r in g_roles if r.get("object_id") == "person_with_machine"), {})
    m_person = next((r for r in m_roles if r.get("object_id") == "person_with_machine"), {})
    return {
        "scenario": "case_b_same_behavior_different_field_risk",
        "greenery_result": greenery,
        "mall_result": mall,
        "greenery_normality": g_person.get("normality"),
        "mall_risk": m_person.get("risk_level"),
        "behavior_field_dependent": g_person.get("normality") != m_person.get("normality"),
    }


def run_unknown_interaction_infers_role() -> Dict[str, Any]:
    """Case C: unknown_sculpture 有交互 → 从交互推断 role."""
    result = run_field_centric_object_role_planning(fixture_key="unknown_sculpture_interaction")
    role = next(
        (r for r in (result.get("object_role_inference") or {}).get("object_role_candidates") or []),
        {},
    )
    return {
        **result,
        "scenario": "case_c_unknown_interaction_infers_role",
        "has_interaction": (result.get("interaction_graph") or {}).get("has_interaction") is True,
        "role_inferred": role.get("inferred_from") in ("interaction", "field_and_interaction"),
        "not_unresolved": role.get("role_candidate") != "unresolved",
        "interactive_art": "art" in (role.get("role_candidate") or "") or "exhibit" in (role.get("role_candidate") or ""),
    }


def run_unknown_no_interaction_unresolved() -> Dict[str, Any]:
    """Case D: 无交互 + 外部查询无果 + 任务无关 → unresolved memory."""
    result = run_field_centric_object_role_planning(fixture_key="unknown_no_interaction")
    unresolved = (result.get("unresolved_object_memory") or {}).get("unresolved_objects") or []
    return {
        **result,
        "scenario": "case_d_unknown_no_interaction_unresolved",
        "has_unresolved": len(unresolved) > 0,
        "record_for_later": any(u.get("action") == "record_for_later" for u in unresolved),
        "not_goal_relevant": all(not u.get("goal_relevant") for u in unresolved),
    }


def run_attention_field_goal_not_saliency() -> Dict[str, Any]:
    """Case E: 同 goal 不同场 → 不同 attention 优先级."""
    subway = run_field_centric_object_role_planning(fixture_key="attention_subway_exit")
    mall = run_field_centric_object_role_planning(fixture_key="attention_mall_exit")
    s_attn = (subway.get("attention_from_field") or {}).get("attention_priorities") or []
    m_attn = (mall.get("attention_from_field") or {}).get("attention_priorities") or []
    s_types = {a.get("information_type") for a in s_attn}
    m_types = {a.get("information_type") for a in m_attn}
    return {
        "scenario": "case_e_attention_field_goal_not_saliency",
        "subway_result": subway,
        "mall_result": mall,
        "not_saliency": (subway.get("attention_from_field") or {}).get("not_saliency_driven") is True,
        "field_goal_driven": (subway.get("attention_from_field") or {}).get("attention_from_field_and_goal") is True,
        "priorities_differ": s_types != m_types or s_attn != m_attn,
    }


def run_field_constrains_unknown_space() -> Dict[str, Any]:
    """Case F: Field profile 约束 unknown object 候选空间."""
    result = run_field_centric_object_role_planning(fixture_key="unknown_no_interaction")
    field = result.get("field_understanding") or {}
    unresolved = result.get("unresolved_object_memory") or {}
    return {
        **result,
        "scenario": "case_f_field_constrains_unknown_space",
        "has_expected_entities": len(field.get("expected_entity_profile") or []) > 0,
        "has_risk_profile": len(field.get("risk_pattern_profile") or []) > 0,
        "field_not_scene_label": field.get("field_not_scene_label") is True,
        "field_constrains": unresolved.get("field_constrains_unknown_space") is True,
    }
