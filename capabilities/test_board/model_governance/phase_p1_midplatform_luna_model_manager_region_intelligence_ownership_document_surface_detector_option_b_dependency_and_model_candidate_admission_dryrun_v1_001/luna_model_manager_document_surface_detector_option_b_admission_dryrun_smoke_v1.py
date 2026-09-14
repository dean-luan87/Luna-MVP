# -*- coding: utf-8 -*-
"""Luna Document Surface — Option B admission dryrun smoke v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_option_b_admission_dryrun_processor_v1 import (
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
from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_option_b_admission_dryrun_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    SMOKE_CASE_IDS,
)


def _wrap(case_id: str, result: Dict[str, Any], checks: Dict[str, bool]) -> Dict[str, Any]:
    return {"case_id": case_id, "passed": all(checks.values()), "result": result, "checks": checks}


def run_smoke_cases() -> Dict[str, Any]:
    ra, rb, rc, rd, re, rf, rg, rh = run_case_a(), run_case_b(), run_case_c(), run_case_d(), run_case_e(), run_case_f(), run_case_g(), run_case_h()
    cases = [
        _wrap("case_a_candidate_fixtures_completeness", ra, {
            "count": ra["count"],
            "registry": ra["registry_complete"],
            "active": ra["active_false"],
        }),
        _wrap("case_b_admitted_to_preflight_only", rb, {
            "a1": rb["a1_admitted"],
            "c1": rb["c1_admitted"],
            "no_exec": rb["no_execution"],
            "no_active": rb["no_active"],
        }),
        _wrap("case_c_dependency_block", rc, {
            "blocked": rc["blocked"],
            "no_install": rc["no_install"],
            "no_download": rc["no_download"],
            "no_exec": rc["no_execution"],
        }),
        _wrap("case_d_license_weight_block", rd, {
            "b1": rd["b1_weight"],
            "b2": rd["b2_license"],
            "d1": rd["d1_hardware"],
        }),
        _wrap("case_e_output_contract_block", re, {
            "blocked": re["blocked"],
            "no_fact": re["no_fact_downstream"],
        }),
        _wrap("case_f_wrapper_requirement", rf, {
            "status": rf["blocked_or_wrapper"],
            "wrapper": rf["wrapper_required"],
            "raw": rf["raw_not_downstream"],
            "not_preflight": rf["not_direct_preflight"],
            "missing": rf["wrapper_missing_blocked"],
        }),
        _wrap("case_g_abort_rollback", rg, {
            "count": rg["blocked_count"],
            "abort": rg["abort_complete"],
            "rollback": rg["rollback_complete"],
        }),
        _wrap("case_h_protocol_compliance", rh, {
            "protocol": rh["protocol"],
            "chain": rh["chain"],
            "branch": rh["branch"],
            "co": rh["co"],
            "nf": rh["nf"],
            "next": rh["next_not_execution"],
        }),
    ]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    dryrun = run_processor()
    fd = FINAL_BLOCKED if failed else dryrun.get("final_decision", FINAL_BLOCKED)
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Dependency-And-Model-Candidate-Admission-DryRun-v1-001",
        "admission_dryrun_only": True,
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "failed_checks": failed,
        "final_decision": fd,
        "dryrun_final_decision": dryrun.get("final_decision"),
        "recommended_next_phase": dryrun.get("recommended_next_phase"),
    }
