# -*- coding: utf-8 -*-
"""Luna Document Surface — Option B preflight closure smoke v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_option_b_preflight_closure_processor_v1 import (
    run_case_a,
    run_case_b,
    run_case_c,
    run_case_d,
    run_case_e,
    run_case_f,
    run_case_g,
    run_case_h,
    run_processor,
)
from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_option_b_preflight_closure_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    SMOKE_CASE_IDS,
)


def _wrap(case_id: str, result: Dict[str, Any], checks: Dict[str, bool]) -> Dict[str, Any]:
    return {"case_id": case_id, "passed": all(checks.values()), "result": result, "checks": checks}


def run_smoke_cases() -> Dict[str, Any]:
    ra, rb, rc, rd, re, rf, rg, rh = run_case_a(), run_case_b(), run_case_c(), run_case_d(), run_case_e(), run_case_f(), run_case_g(), run_case_h()
    cases = [
        _wrap("case_a_preflight_candidate_scope", ra, {"c": ra["count"], "b": ra["blocked"], "na": ra["no_active"]}),
        _wrap("case_b_dependency_availability_dryrun", rb, {"r": rb["has_results"], "ni": rb["no_install"], "nd": rb["no_download"]}),
        _wrap("case_c_weight_license_dryrun", rc, {"w": rc["weight"], "l": rc["license"], "nd": rc["no_dl"]}),
        _wrap("case_d_input_output_boundary_dryrun", rd, {"img": rd["no_image"], "out": rd["tmp_out"], "reg": rd["no_reg"]}),
        _wrap("case_e_raw_output_normalization_dryrun", re, {"ds": re["no_ds"], "ok": re["ok"]}),
        _wrap("case_f_schema_leak_dryrun", rf, {"sc": rf["schema"], "lk": rf["no_leak"]}),
        _wrap("case_g_trace_abort_rollback_dryrun", rg, {"tr": rg["trace"], "ex": rg["no_exec"], "seg": rg["no_seg"], "am": rg["no_active"]}),
        _wrap("case_h_protocol_compliance", rh, {"pl": rh["planning"], "dr": rh["dryrun"], "po": rh["post"], "ch": rh["chain"], "nx": rh["next_ce"], "ne": rh["no_exec"]}),
    ]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    closure = run_processor()
    fd = FINAL_BLOCKED if failed else closure.get("final_decision", FINAL_BLOCKED)
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Preflight-Closure-v1-001",
        "preflight_closure_only": True,
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "failed_checks": failed,
        "final_decision": fd,
        "closure_final_decision": closure.get("final_decision"),
        "recommended_next_phase": closure.get("recommended_next_phase"),
    }
