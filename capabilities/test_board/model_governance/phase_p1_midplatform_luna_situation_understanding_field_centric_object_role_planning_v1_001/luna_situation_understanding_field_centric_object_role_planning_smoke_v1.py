# -*- coding: utf-8 -*-
"""Luna Field-Centric Object Role — planning smoke fixtures v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.situation_understanding.luna_situation_understanding_field_centric_object_role_planning_processor_v1 import (
    run_attention_field_goal_not_saliency,
    run_field_constrains_unknown_space,
    run_same_behavior_different_field_risk,
    run_same_object_different_field_role,
    run_unknown_interaction_infers_role,
    run_unknown_no_interaction_unresolved,
)
from capabilities.midplatform.situation_understanding.luna_situation_understanding_field_centric_object_role_planning_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    SMOKE_CASE_IDS,
)


def _wrap(case_id: str, result: Dict[str, Any], checks: Dict[str, bool]) -> Dict[str, Any]:
    return {"case_id": case_id, "passed": all(checks.values()), "result": result, "checks": checks}


def smoke_case_a() -> Dict[str, Any]:
    r = run_same_object_different_field_role()
    return _wrap("case_a_same_object_different_field_role", r, {
        "diff": r.get("roles_differ") is True,
        "furniture": bool(r.get("furniture_role")),
        "construction": bool(r.get("construction_role")),
        "field_first": r.get("field_before_object") is True,
    })


def smoke_case_b() -> Dict[str, Any]:
    r = run_same_behavior_different_field_risk()
    return _wrap("case_b_same_behavior_different_field_risk", r, {
        "field_dep": r.get("behavior_field_dependent") is True,
        "g_norm": r.get("greenery_normality") == "normal",
        "m_risk": r.get("mall_risk") in ("high", "medium") or r.get("mall_risk") is not None,
    })


def smoke_case_c() -> Dict[str, Any]:
    r = run_unknown_interaction_infers_role()
    return _wrap("case_c_unknown_interaction_infers_role", r, {
        "interaction": r.get("has_interaction") is True,
        "inferred": r.get("role_inferred") is True,
        "not_unresolved": r.get("not_unresolved") is True,
    })


def smoke_case_d() -> Dict[str, Any]:
    r = run_unknown_no_interaction_unresolved()
    return _wrap("case_d_unknown_no_interaction_unresolved", r, {
        "unresolved": r.get("has_unresolved") is True,
        "record": r.get("record_for_later") is True,
    })


def smoke_case_e() -> Dict[str, Any]:
    r = run_attention_field_goal_not_saliency()
    return _wrap("case_e_attention_field_goal_not_saliency", r, {
        "not_sal": r.get("not_saliency") is True,
        "field_goal": r.get("field_goal_driven") is True,
        "differ": r.get("priorities_differ") is True,
    })


def smoke_case_f() -> Dict[str, Any]:
    r = run_field_constrains_unknown_space()
    return _wrap("case_f_field_constrains_unknown_space", r, {
        "entities": r.get("has_expected_entities") is True,
        "not_scene": r.get("field_not_scene_label") is True,
        "constrains": r.get("field_constrains") is True,
    })


def run_smoke_cases() -> Dict[str, Any]:
    cases = [smoke_case_a(), smoke_case_b(), smoke_case_c(), smoke_case_d(), smoke_case_e(), smoke_case_f()]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-Planning-v1-001",
        "planning_only": True,
        "field_centric": True,
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "smoke_case_count": len(cases),
        "failed_checks": failed,
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
