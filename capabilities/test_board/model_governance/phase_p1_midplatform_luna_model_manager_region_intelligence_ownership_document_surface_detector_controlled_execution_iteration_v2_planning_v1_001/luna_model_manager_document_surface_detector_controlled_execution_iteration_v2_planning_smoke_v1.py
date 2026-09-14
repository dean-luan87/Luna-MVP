# -*- coding: utf-8 -*-
"""Luna Document Surface Detector — iteration v2 planning smoke v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_controlled_execution_iteration_v2_planning_processor_v1 import (
    run_case_a,
    run_case_b,
    run_case_c,
    run_case_d,
    run_case_e,
    run_case_f,
    run_case_g,
    run_case_h,
    run_planning_processor,
)
from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_controlled_execution_iteration_v2_planning_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    SMOKE_CASE_IDS,
)


def _wrap(case_id: str, result: Dict[str, Any], checks: Dict[str, bool]) -> Dict[str, Any]:
    return {"case_id": case_id, "passed": all(checks.values()), "result": result, "checks": checks}


def smoke_case_a() -> Dict[str, Any]:
    r = run_case_a()
    return _wrap("case_a_option_a_limitation_review", r, {
        "st": r.get("strengths") is True,
        "lm": r.get("limits") is True,
        "ks": r.get("keep_scope") is True,
        "ns": r.get("not_sufficient") is True,
        "na": r.get("activation_not_allowed") is True,
    })


def smoke_case_b() -> Dict[str, Any]:
    r = run_case_b()
    return _wrap("case_b_option_b_candidate_route_planning", r, {
        "cr": r.get("candidate_route_only") is True,
        "nm": r.get("no_active_model") is True,
        "nd": r.get("no_download") is True,
        "ne": r.get("no_execution") is True,
        "nt": r.get("no_training") is True,
    })


def smoke_case_c() -> Dict[str, Any]:
    r = run_case_c()
    return _wrap("case_c_ab_relationship", r, {
        "sf": r.get("not_silent_fallback") is True,
        "as": r.get("not_auto_substitute") is True,
        "vr": r.get("validation_review_on_conflict") is True,
        "nc": r.get("no_confidence_override") is True,
    })


def smoke_case_d() -> Dict[str, Any]:
    r = run_case_d()
    return _wrap("case_d_case_mapping", r, {
        "am": r.get("all_mapped") is True,
        "h": r.get("has_case_h") is True,
        "hm": r.get("h_fixture_mismatch") is True,
    })


def smoke_case_e() -> Dict[str, Any]:
    r = run_case_e()
    return _wrap("case_e_fixture_plan_v2_1", r, {
        "c8": r.get("count_ge_8") is True,
        "rt": r.get("has_route_target") is True,
        "sy": r.get("synthetic_marked") is True,
    })


def smoke_case_f() -> Dict[str, Any]:
    r = run_case_f()
    return _wrap("case_f_metrics_v2", r, {
        "rm": r.get("route_metrics") is True,
        "rg": r.get("retained_governance") is True,
    })


def smoke_case_g() -> Dict[str, Any]:
    r = run_case_g()
    return _wrap("case_g_option_b_admission_constraints", r, {
        "cr": r.get("candidate_route_only") is True,
        "ex": r.get("execution_forbidden") is True,
        "ad": r.get("admission_required") is True,
        "pb": r.get("planning_before_execution") is True,
    })


def smoke_case_h() -> Dict[str, Any]:
    r = run_case_h()
    return _wrap("case_h_protocol_compliance", r, {
        "pr": r.get("protocol_required") is True,
        "ce": r.get("chain_extension") is True,
        "nb": r.get("not_new_branch") is True,
        "co": r.get("candidate_only") is True,
        "nf": r.get("not_fact") is True,
    })


def run_smoke_cases() -> Dict[str, Any]:
    cases = [
        smoke_case_a(), smoke_case_b(), smoke_case_c(), smoke_case_d(),
        smoke_case_e(), smoke_case_f(), smoke_case_g(), smoke_case_h(),
    ]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    planning = run_planning_processor()
    fd = FINAL_BLOCKED if failed else planning.get("final_decision", FINAL_BLOCKED)
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Controlled-Execution-Iteration-v2-Planning-v1-001",
        "iteration_v2_planning_only": True,
        "detector_execution_forbidden": True,
        "runtime_activation": False,
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "smoke_case_count": len(cases),
        "failed_checks": failed,
        "final_decision": fd,
        "planning_final_decision": planning.get("final_decision"),
        "recommended_next_phase": planning.get("recommended_next_phase"),
        "route_verdict": planning.get("route_verdict"),
    }
