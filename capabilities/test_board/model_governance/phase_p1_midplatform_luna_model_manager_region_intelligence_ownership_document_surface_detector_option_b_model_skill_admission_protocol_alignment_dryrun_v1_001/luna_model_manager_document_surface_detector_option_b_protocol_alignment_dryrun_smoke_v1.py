# -*- coding: utf-8 -*-
"""Luna Document Surface — Option B protocol alignment dryrun smoke v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_option_b_protocol_alignment_dryrun_processor_v1 import (
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
from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_option_b_protocol_alignment_dryrun_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    SMOKE_CASE_IDS,
)


def _wrap(case_id: str, result: Dict[str, Any], checks: Dict[str, bool]) -> Dict[str, Any]:
    return {"case_id": case_id, "passed": all(checks.values()), "result": result, "checks": checks}


def run_smoke_cases() -> Dict[str, Any]:
    ra, rb, rc, rd, re, rf, rg, rh = run_case_a(), run_case_b(), run_case_c(), run_case_d(), run_case_e(), run_case_f(), run_case_g(), run_case_h()
    cases = [
        _wrap("case_a_model_skill_contract_mapping", ra, {"count": ra["count"], "mapped": ra["all_mapped"], "pf": ra["preflight"], "blk": ra["blocked"]}),
        _wrap("case_b_registry_alignment", rb, {"am": rb["no_active_model"], "as": rb["no_active_skill"], "upd": rb["no_update"], "co": rb["candidate_only"]}),
        _wrap("case_c_dependency_protocol_mapping", rc, {"den": rc["denied_count"], "ins": rc["no_install"], "dl": rc["no_download"], "ex": rc["no_exec"]}),
        _wrap("case_d_output_contract_protocol_mapping", rd, {"b3": rd["b3_wrapper"], "c2": rd["c2_fact"], "raw": rd["raw_blocked"]}),
        _wrap("case_e_runtime_boundary_mapping", re, {"act": re["no_activation"], "ctrl": re["no_controlled"], "ex": re["no_exec"]}),
        _wrap("case_f_change_control_freeze", rf, {"dry": rf["dryrun_only"], "na": rf["no_active"], "fr": rf["freeze"], "next": rf["next_post_review"], "np": rf["no_preflight"]}),
        _wrap("case_g_evidence_chain_mapping", rg, {"refs": rg["refs"], "proto": rg["protocol"], "rate": rg["rate"]}),
        _wrap("case_h_metrics_protocol_compliance", rh, {"pr": rh["protocol_ref"], "co": rh["candidate_only"], "am": rh["no_active_model"], "reg": rh["no_registry"], "chain": rh["chain"], "br": rh["branch"]}),
    ]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    dryrun = run_processor()
    fd = FINAL_BLOCKED if failed else dryrun.get("final_decision", FINAL_BLOCKED)
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Model-Skill-Admission-Protocol-Alignment-DryRun-v1-001",
        "protocol_alignment_dryrun_only": True,
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "failed_checks": failed,
        "final_decision": fd,
        "dryrun_final_decision": dryrun.get("final_decision"),
        "recommended_next_phase": dryrun.get("recommended_next_phase"),
    }
