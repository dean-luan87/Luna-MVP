# -*- coding: utf-8 -*-
"""Luna Document Surface Detector — controlled execution preflight smoke v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_real_runtime_controlled_execution_preflight_processor_v1 import (
    run_abort_policy_case,
    run_blocked_invalid_input_path_case,
    run_controlled_input_registry_case,
    run_cv2_dependency_preflight_case,
    run_output_boundary_case,
    run_protocol_compliance_retained_case,
    run_real_execution_remains_disabled_case,
    run_trace_schema_case,
)
from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_real_runtime_controlled_execution_preflight_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    FINAL_GO_WITH_DEPENDENCY_BLOCKED,
    SMOKE_CASE_IDS,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_preflight.document_surface_cv2_preflight_check_v1 import (
    run_cv2_preflight_check,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_preflight.document_surface_preflight_adapter_v1 import (
    run_controlled_execution_preflight,
)


def _wrap(case_id: str, result: Dict[str, Any], checks: Dict[str, bool]) -> Dict[str, Any]:
    return {"case_id": case_id, "passed": all(checks.values()), "result": result, "checks": checks}


def smoke_case_a() -> Dict[str, Any]:
    r = run_cv2_dependency_preflight_case()
    return _wrap("case_a_cv2_dependency_preflight", r, {
        "ia": r.get("import_attempted") is True,
        "np": r.get("no_processing") is True,
        "ns": r.get("no_silent_install") is True,
        "bm": r.get("blocked_if_missing") is True,
    })


def smoke_case_b() -> Dict[str, Any]:
    r = run_controlled_input_registry_case()
    return _wrap("case_b_controlled_input_registry", r, {
        "de": r.get("dir_exists") is True,
        "sv": r.get("schema_valid") is True,
        "po": r.get("paths_ok") is True,
        "nr": r.get("no_content_read") is True,
    })


def smoke_case_c() -> Dict[str, Any]:
    r = run_blocked_invalid_input_path_case()
    return _wrap("case_c_blocked_invalid_input_path", r, {
        "ab": r.get("input_not_in_registry_abort_defined") is True,
        "br": r.get("bad_path_not_in_registry") is True,
        "na": r.get("abort_has_next_action") is True,
    })


def smoke_case_d() -> Dict[str, Any]:
    r = run_output_boundary_case()
    return _wrap("case_d_output_boundary", r, {
        "tr": r.get("tmp_root") is True,
        "np": r.get("no_prod") is True,
        "nt": r.get("no_training") is True,
        "nf": r.get("no_fact") is True,
    })


def smoke_case_e() -> Dict[str, Any]:
    r = run_trace_schema_case()
    return _wrap("case_e_trace_schema", r, {
        "fl": r.get("fields") is True,
        "ocr": r.get("ocr_off") is True,
        "vlm": r.get("vlm_off") is True,
        "fb": r.get("fallback_off") is True,
    })


def smoke_case_f() -> Dict[str, Any]:
    r = run_abort_policy_case()
    return _wrap("case_f_abort_policy", r, {
        "c13": r.get("count_13") is True,
        "ok": r.get("complete") is True,
    })


def smoke_case_g() -> Dict[str, Any]:
    r = run_protocol_compliance_retained_case()
    return _wrap("case_g_protocol_compliance_retained", r, {
        "pc": r.get("passed") is True,
        "ext": r.get("chain_ext") is True,
        "nb": r.get("not_new_branch") is True,
    })


def smoke_case_h() -> Dict[str, Any]:
    r = run_real_execution_remains_disabled_case()
    return _wrap("case_h_real_execution_remains_disabled", r, {
        "det": r.get("detector_off") is True,
        "real": r.get("real_off") is True,
        "ctrl": r.get("controlled_next") is True,
        "nu": r.get("not_uncontrolled") is True,
    })


def run_smoke_cases() -> Dict[str, Any]:
    cases = [
        smoke_case_a(), smoke_case_b(), smoke_case_c(), smoke_case_d(),
        smoke_case_e(), smoke_case_f(), smoke_case_g(), smoke_case_h(),
    ]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    cv2 = run_cv2_preflight_check()
    preflight = run_controlled_execution_preflight(write_outputs=False)
    fd = preflight.get("final_decision")
    if failed:
        fd = FINAL_BLOCKED
    elif not cv2.get("cv2_available_candidate") and fd not in (FINAL_GO_WITH_DEPENDENCY_BLOCKED, FINAL_GO):
        fd = FINAL_GO_WITH_DEPENDENCY_BLOCKED if not failed else FINAL_BLOCKED
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Controlled-Execution-Preflight-v1-001",
        "controlled_execution_preflight_only": True,
        "detector_execution_enabled": False,
        "real_execution_enabled": False,
        "cv2_available_candidate": cv2.get("cv2_available_candidate"),
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "smoke_case_count": len(cases),
        "failed_checks": failed,
        "final_decision": fd,
        "recommended_next_phase": preflight.get("recommended_next_phase"),
    }
