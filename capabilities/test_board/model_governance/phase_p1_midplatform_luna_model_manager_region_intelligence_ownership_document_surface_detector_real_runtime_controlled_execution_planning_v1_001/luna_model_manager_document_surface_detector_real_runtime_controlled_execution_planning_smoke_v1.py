# -*- coding: utf-8 -*-
"""Luna Document Surface Detector — controlled execution planning smoke v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_real_runtime_controlled_execution_planning_processor_v1 import (
    run_abort_condition_planning,
    run_controlled_smoke_plan_case,
    run_cv2_dependency_admission_planning,
    run_input_output_boundary_planning,
    run_next_phase_gate,
    run_protocol_compliance_retained,
    run_trace_schema_planning,
)
from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_real_runtime_controlled_execution_planning_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    SMOKE_CASE_IDS,
)


def _wrap(case_id: str, result: Dict[str, Any], checks: Dict[str, bool]) -> Dict[str, Any]:
    return {"case_id": case_id, "passed": all(checks.values()), "result": result, "checks": checks}


def smoke_case_a() -> Dict[str, Any]:
    r = run_cv2_dependency_admission_planning()
    return _wrap("case_a_cv2_dependency_admission_planning", r, {
        "na": r.get("not_admitted") is True,
        "ph": r.get("phase_only") is True,
        "ni": r.get("no_import") is True,
        "ns": r.get("no_silent") is True,
    })


def smoke_case_b() -> Dict[str, Any]:
    r = run_input_output_boundary_planning()
    return _wrap("case_b_input_output_boundary_planning", r, {
        "in": r.get("input_defined") is True,
        "out": r.get("output_restricted") is True,
        "na": r.get("no_arbitrary") is True,
    })


def smoke_case_c() -> Dict[str, Any]:
    r = run_abort_condition_planning()
    return _wrap("case_c_abort_condition_planning", r, {
        "cnt": r.get("at_least_12") is True,
        "ok": r.get("complete") is True,
    })


def smoke_case_d() -> Dict[str, Any]:
    r = run_trace_schema_planning()
    return _wrap("case_d_trace_schema_planning", r, {
        "fld": r.get("fields_complete") is True,
        "ocr": r.get("ocr_false") is True,
        "fb": r.get("no_fallback") is True,
    })


def smoke_case_e() -> Dict[str, Any]:
    r = run_controlled_smoke_plan_case()
    return _wrap("case_e_controlled_smoke_plan", r, {
        "six": r.get("at_least_6") is True,
        "no": r.get("no_exec") is True,
    })


def smoke_case_f() -> Dict[str, Any]:
    r = run_protocol_compliance_retained()
    return _wrap("case_f_protocol_compliance_retained", r, {
        "ext": r.get("chain_ext") is True,
        "nb": r.get("not_new_branch") is True,
        "req": r.get("required") is True,
    })


def smoke_case_g() -> Dict[str, Any]:
    r = run_next_phase_gate()
    return _wrap("case_g_next_phase_gate", r, {
        "off": r.get("real_off") is True,
        "pf": r.get("preflight") is True,
        "nd": r.get("not_direct") is True,
    })


def run_smoke_cases() -> Dict[str, Any]:
    cases = [smoke_case_a(), smoke_case_b(), smoke_case_c(), smoke_case_d(), smoke_case_e(), smoke_case_f(), smoke_case_g()]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Controlled-Execution-Planning-v1-001",
        "controlled_execution_planning_only": True,
        "real_execution_enabled": False,
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "smoke_case_count": len(cases),
        "failed_checks": failed,
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
