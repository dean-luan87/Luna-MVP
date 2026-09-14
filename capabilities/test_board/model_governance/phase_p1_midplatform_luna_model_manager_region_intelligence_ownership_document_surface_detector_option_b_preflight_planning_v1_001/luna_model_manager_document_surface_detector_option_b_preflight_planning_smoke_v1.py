# -*- coding: utf-8 -*-
"""Luna Document Surface — Option B preflight planning smoke v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_option_b_preflight_planning_processor_v1 import (
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
from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_option_b_preflight_planning_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    SMOKE_CASE_IDS,
)


def _wrap(case_id: str, result: Dict[str, Any], checks: Dict[str, bool]) -> Dict[str, Any]:
    return {"case_id": case_id, "passed": all(checks.values()), "result": result, "checks": checks}


def run_smoke_cases() -> Dict[str, Any]:
    ra, rb, rc, rd, re, rf, rg, rh = run_case_a(), run_case_b(), run_case_c(), run_case_d(), run_case_e(), run_case_f(), run_case_g(), run_case_h()
    cases = [
        _wrap("case_a_preflight_candidate_scope", ra, {"c2": ra["count_2"], "blk": ra["blocked_excluded"], "na": ra["no_active"]}),
        _wrap("case_b_dependency_weight_license_planning", rb, {"dep": rb["dep"], "w": rb["weight"], "lic": rb["license"], "ni": rb["no_install"], "nd": rb["no_download"]}),
        _wrap("case_c_input_output_boundary_planning", rc, {"img": rc["no_image"], "meta": rc["metadata"], "out": rc["tmp_out"], "reg": rc["no_active_reg"]}),
        _wrap("case_d_raw_output_normalization_planning", rd, {"ds": rd["no_downstream"], "w": rd["wrapper_abort"], "cap": rd["caption"]}),
        _wrap("case_e_candidate_schema_leak_planning", re, {"al": re["allowed_6"], "fb": re["forbidden"], "lk": re["leak_abort"]}),
        _wrap("case_f_runtime_trace_planning", rf, {"fld": rf["fields"], "ex": rf["no_exec"], "seg": rf["no_seg"], "am": rf["no_active"]}),
        _wrap("case_g_abort_rollback_planning", rg, {"ab": rg["abort_16"], "nr": rg["no_registry"], "nf": rg["no_fallback"], "na": rg["no_option_a"]}),
        _wrap("case_h_protocol_compliance", rh, {"pr": rh["protocol"], "ct": rh["contract"], "ch": rh["chain"], "br": rh["branch"], "nx": rh["next_dryrun"], "ne": rh["no_exec"]}),
    ]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    planning = run_processor()
    fd = FINAL_BLOCKED if failed else planning.get("final_decision", FINAL_BLOCKED)
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Preflight-Planning-v1-001",
        "preflight_planning_only": True,
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "failed_checks": failed,
        "final_decision": fd,
        "planning_final_decision": planning.get("final_decision"),
        "recommended_next_phase": planning.get("recommended_next_phase"),
    }
