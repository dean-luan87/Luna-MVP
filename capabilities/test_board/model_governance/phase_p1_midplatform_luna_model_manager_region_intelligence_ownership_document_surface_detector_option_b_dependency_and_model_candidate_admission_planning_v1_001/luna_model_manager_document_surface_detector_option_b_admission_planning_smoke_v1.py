# -*- coding: utf-8 -*-
"""Luna Document Surface — Option B admission planning smoke v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_option_b_admission_planning_processor_v1 import (
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
from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_option_b_admission_planning_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    SMOKE_CASE_IDS,
)


def _wrap(case_id: str, result: Dict[str, Any], checks: Dict[str, bool]) -> Dict[str, Any]:
    return {"case_id": case_id, "passed": all(checks.values()), "result": result, "checks": checks}


def run_smoke_cases() -> Dict[str, Any]:
    ra, rb, rc, rd, re, rf, rg, rh = run_case_a(), run_case_b(), run_case_c(), run_case_d(), run_case_e(), run_case_f(), run_case_g(), run_case_h()
    cases = [
        _wrap("case_a_candidate_family_evaluation", ra, {"ab": ra["abcd"], "na": ra["no_active"], "ne": ra["no_exec"]}),
        _wrap("case_b_registry_schema", rb, {"sc": rb["schema"], "af": rb["active_false"], "pf": rb["preflight"], "ce": rb["controlled"]}),
        _wrap("case_c_dependency_admission_policy", rc, {"in": rc["install"], "dl": rc["download"], "ex": rc["exec"], "si": rc["silent"]}),
        _wrap("case_d_license_weight_policy", rd, {"ct": rd["count"], "na": rd["has_next_action"], "fw": rd["has_forbidden"]}),
        _wrap("case_e_output_contract_compatibility", re, {"al": re["allowed"], "fb": re["forbidden"], "wr": re["wrapper"]}),
        _wrap("case_f_preflight_requirements", rf, {"cp": rf["complete"], "sk": rf["skip_forbidden"]}),
        _wrap("case_g_abort_rollback_planning", rg, {"ac": rg["abort_count"], "nr": rg["no_registry"], "no": rg["no_ocr_fallback"]}),
        _wrap("case_h_protocol_compliance", rh, {"pr": rh["protocol"], "ce": rh["chain"], "nb": rh["branch"], "co": rh["co"], "nf": rh["nf"]}),
    ]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    planning = run_processor()
    fd = FINAL_BLOCKED if failed else planning.get("final_decision", FINAL_BLOCKED)
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Dependency-And-Model-Candidate-Admission-Planning-v1-001",
        "admission_planning_only": True,
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "failed_checks": failed,
        "final_decision": fd,
        "planning_final_decision": planning.get("final_decision"),
        "recommended_next_phase": planning.get("recommended_next_phase"),
    }
