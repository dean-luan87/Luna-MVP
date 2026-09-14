# -*- coding: utf-8 -*-
"""Luna Document Surface — Option B protocol alignment planning smoke v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_option_b_protocol_alignment_planning_processor_v1 import (
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
from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_option_b_protocol_alignment_planning_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    SMOKE_CASE_IDS,
)


def _wrap(case_id: str, result: Dict[str, Any], checks: Dict[str, bool]) -> Dict[str, Any]:
    return {"case_id": case_id, "passed": all(checks.values()), "result": result, "checks": checks}


def run_smoke_cases() -> Dict[str, Any]:
    ra, rb, rc, rd, re, rf, rg, rh = run_case_a(), run_case_b(), run_case_c(), run_case_d(), run_case_e(), run_case_f(), run_case_g(), run_case_h()
    cases = [
        _wrap("case_a_contract_mapping", ra, {"primary": ra["primary"], "mounted": ra["mounted"], "not_replace": ra["not_replace"], "refs": ra["refs"]}),
        _wrap("case_b_registry_alignment", rb, {"count": rb["count"], "no_active": rb["no_active"], "not_model": rb["not_model_admitted"]}),
        _wrap("case_c_dependency_protocol_mapping", rc, {"install": rc["install"], "download": rc["download"], "exec": rc["exec"]}),
        _wrap("case_d_output_contract_protocol_mapping", rd, {"no_fact": rd["no_fact"], "no_ocr": rd["no_ocr"], "allowed": rd["allowed"]}),
        _wrap("case_e_permission_runtime_boundary", re, {"runtime": re["runtime"], "controlled": re["controlled"], "admission": re["admission_req"]}),
        _wrap("case_f_change_control_freeze", rf, {"frozen": rf["frozen"], "pipeline": rf["pipeline"], "skip": rf["skip_forbidden"]}),
        _wrap("case_g_frozen_state", rg, {"mr": rg["model_route"], "sr": rg["skill_route"], "am": rg["no_active_model"], "as": rg["no_active_skill"], "pf": rg["preflight"]}),
        _wrap("case_h_protocol_compliance", rh, {"protocol": rh["protocol"], "chain": rh["chain"], "branch": rh["branch"], "review": rh["review"], "next": rh["next_dryrun"]}),
    ]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    planning = run_processor()
    fd = FINAL_BLOCKED if failed else planning.get("final_decision", FINAL_BLOCKED)
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Model-Skill-Admission-Protocol-Alignment-Planning-v1-001",
        "protocol_alignment_planning_only": True,
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "failed_checks": failed,
        "final_decision": fd,
        "planning_final_decision": planning.get("final_decision"),
        "recommended_next_phase": planning.get("recommended_next_phase"),
    }
