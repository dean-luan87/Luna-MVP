# -*- coding: utf-8 -*-
"""Luna Document Surface — Option B candidate route dryrun smoke v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_option_b_candidate_route_dryrun_processor_v1 import (
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
from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_option_b_candidate_route_dryrun_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    SMOKE_CASE_IDS,
)


def _wrap(case_id: str, result: Dict[str, Any], checks: Dict[str, bool]) -> Dict[str, Any]:
    return {"case_id": case_id, "passed": all(checks.values()), "result": result, "checks": checks}


def run_smoke_cases() -> Dict[str, Any]:
    cases = [
        _wrap("case_a_option_b_admission_gate", run_case_a(), {
            "cr": run_case_a().get("candidate_route_only") is True,
            "ex": run_case_a().get("execution_forbidden") is True,
            "ad": run_case_a().get("admission_required") is True,
            "nm": run_case_a().get("no_active_model") is True,
        }),
        _wrap("case_b_output_contract", run_case_b(), {
            "ao": run_case_b().get("allowed_ok") is True,
            "fb": run_case_b().get("forbidden_blocked") is True,
        }),
        _wrap("case_c_route_selection", run_case_c(), {
            "rc": run_case_c().get("route_candidate_only") is True,
            "ne": run_case_c().get("no_execution_decision") is True,
            "vr": run_case_c().get("validation_required") is True,
        }),
        _wrap("case_d_ab_conflict_policy", run_case_d(), {
            "vr": run_case_d().get("validation_review") is True,
            "nc": run_case_d().get("no_confidence_override") is True,
            "sf": run_case_d().get("no_silent_fallback") is True,
        }),
        _wrap("case_e_case_mapping_acf", run_case_e(), {
            "a": run_case_e().get("a_b_recommended") is True,
            "c": run_case_e().get("c_b_recommended") is True,
            "f": run_case_e().get("f_b_recommended") is True,
            "ne": run_case_e().get("no_execution") is True,
        }),
        _wrap("case_f_case_mapping_beh", run_case_f(), {
            "b": run_case_f().get("b_conflict_review") is True,
            "e": run_case_f().get("e_not_default_b") is True,
            "h": run_case_f().get("h_defer") is True,
            "fc": run_case_f().get("h_fixture_correction") is True,
        }),
        _wrap("case_g_metrics", run_case_g(), {
            "eb": run_case_g().get("exec_block") is True,
            "db": run_case_g().get("download_block") is True,
            "rb": run_case_g().get("registry_block") is True,
            "nl": run_case_g().get("no_leak") is True,
        }),
        _wrap("case_h_protocol_compliance", run_case_h(), {
            "pr": run_case_h().get("protocol") is True,
            "ce": run_case_h().get("chain_extension") is True,
            "nb": run_case_h().get("not_new_branch") is True,
            "co": run_case_h().get("candidate_only") is True,
            "nf": run_case_h().get("not_fact") is True,
        }),
    ]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    dryrun = run_processor()
    fd = FINAL_BLOCKED if failed else dryrun.get("final_decision", FINAL_BLOCKED)
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Candidate-Route-DryRun-v1-001",
        "option_b_candidate_route_dryrun_only": True,
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "failed_checks": failed,
        "final_decision": fd,
        "dryrun_final_decision": dryrun.get("final_decision"),
        "recommended_next_phase": dryrun.get("recommended_next_phase"),
    }
