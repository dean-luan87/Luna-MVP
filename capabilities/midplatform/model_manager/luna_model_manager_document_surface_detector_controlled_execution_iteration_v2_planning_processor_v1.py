# -*- coding: utf-8 -*-
"""Luna Document Surface Detector — iteration v2 planning processor v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_v2_planning.document_surface_iteration_v2_planning_adapter_v1 import (
    run_iteration_v2_planning,
)


def run_planning_processor() -> Dict[str, Any]:
    return run_iteration_v2_planning(write_outputs=False)


def run_case_a() -> Dict[str, Any]:
    r = run_iteration_v2_planning(write_outputs=False)
    a = r.get("option_a_limit_review") or {}
    return {
        "strengths": bool(a.get("option_a_strengths")),
        "limits": bool(a.get("option_a_limitations")),
        "keep_scope": bool(a.get("option_a_keep_scope")),
        "not_sufficient": bool(a.get("option_a_not_sufficient_for")),
        "activation_not_allowed": a.get("option_a_activation_status") == "not_allowed",
    }


def run_case_b() -> Dict[str, Any]:
    r = run_iteration_v2_planning(write_outputs=False)
    b = r.get("option_b_candidate_route") or {}
    return {
        "candidate_route_only": b.get("option_b_status") == "candidate_route_only",
        "no_active_model": b.get("active_model_specified") is False,
        "no_download": b.get("model_download_planned") is False,
        "no_execution": b.get("model_execution_planned") is False,
        "no_training": b.get("training_planned") is False,
    }


def run_case_c() -> Dict[str, Any]:
    r = run_iteration_v2_planning(write_outputs=False)
    c = r.get("option_a_b_comparison") or {}
    return {
        "not_silent_fallback": c.get("silent_fallback") is False,
        "not_auto_substitute": c.get("auto_substitute") is False,
        "validation_review_on_conflict": c.get("conflict_resolution") == "validation_review",
        "no_confidence_override": c.get("confidence_auto_override") is False,
    }


def run_case_d() -> Dict[str, Any]:
    r = run_iteration_v2_planning(write_outputs=False)
    m = r.get("case_mapping") or {}
    cases = {x["case_id"] for x in (m.get("mappings") or [])}
    h = next((x for x in (m.get("mappings") or []) if x.get("case_id") == "case_h_screen_control"), {})
    return {
        "all_mapped": m.get("all_required_cases_covered") is True,
        "has_case_h": "case_h_screen_control" in cases,
        "h_fixture_mismatch": h.get("attribution") == "fixture_semantic_mismatch_not_detector_failure",
    }


def run_case_e() -> Dict[str, Any]:
    r = run_iteration_v2_planning(write_outputs=False)
    f = r.get("fixture_plan") or {}
    fixtures = f.get("fixtures") or []
    return {
        "count_ge_8": len(fixtures) >= 8,
        "has_route_target": all(fx.get("target_route") for fx in fixtures),
        "synthetic_marked": any(fx.get("not_real_world_benchmark") for fx in fixtures),
    }


def run_case_f() -> Dict[str, Any]:
    r = run_iteration_v2_planning(write_outputs=False)
    mp = r.get("metrics_plan") or {}
    return {
        "route_metrics": mp.get("route_level_metrics_complete") is True,
        "retained_governance": len(mp.get("retained_governance_metrics") or []) >= 7,
    }


def run_case_g() -> Dict[str, Any]:
    r = run_iteration_v2_planning(write_outputs=False)
    c = r.get("option_b_admission_constraints") or {}
    return {
        "candidate_route_only": c.get("option_b_status") == "candidate_route_only",
        "execution_forbidden": c.get("execution_allowed") is False,
        "admission_required": c.get("dependency_admission_required") is True,
        "planning_before_execution": c.get("controlled_execution_planning_required_before_any_execution") is True,
    }


def run_case_h() -> Dict[str, Any]:
    r = run_iteration_v2_planning(write_outputs=False)
    return {
        "protocol_required": r.get("protocol_compliance_check") == "required",
        "chain_extension": r.get("existing_midplatform_protocol_chain_extension") is True,
        "not_new_branch": r.get("protocol_patch_not_new_branch") is True,
        "candidate_only": r.get("candidate_only") is True,
        "not_fact": r.get("not_fact") is True,
    }
