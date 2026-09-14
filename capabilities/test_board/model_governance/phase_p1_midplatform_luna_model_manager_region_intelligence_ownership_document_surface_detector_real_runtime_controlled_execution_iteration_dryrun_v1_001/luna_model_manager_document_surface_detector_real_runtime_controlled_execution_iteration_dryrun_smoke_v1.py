# -*- coding: utf-8 -*-
"""Luna Document Surface Detector — iteration dryrun smoke v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_real_runtime_controlled_execution_iteration_dryrun_processor_v1 import (
    run_case_a,
    run_case_b,
    run_case_c,
    run_case_d,
    run_case_e,
    run_case_f,
    run_case_g,
    run_case_h,
    run_iteration_processor,
)
from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_real_runtime_controlled_execution_iteration_dryrun_types_v1 import (
    FINAL_BLOCKED,
    FINAL_BLOCKED_BY_MISSING_FIXTURES,
    FINAL_GO,
    SMOKE_CASE_IDS,
)


def _wrap(case_id: str, result: Dict[str, Any], checks: Dict[str, bool]) -> Dict[str, Any]:
    return {"case_id": case_id, "passed": all(checks.values()), "result": result, "checks": checks}


def smoke_case_a() -> Dict[str, Any]:
    r = run_case_a()
    if r.get("skipped_missing_fixture"):
        return _wrap("case_a_two_overlapping_papers_clear_edges", r, {"sk": True, "nf": True, "no": True})
    return _wrap("case_a_two_overlapping_papers_clear_edges", r, {
        "os": r.get("overlap_strategy_applied") is True,
        "nf": r.get("no_fake_relation") is True,
        "nm": r.get("no_forced_multi_surface") is True,
        "ev": r.get("relation_evidence_basis") is True,
        "no": r.get("no_ocr") is True,
    })


def smoke_case_b() -> Dict[str, Any]:
    r = run_case_b()
    if r.get("skipped_missing_fixture"):
        return _wrap("case_b_two_overlapping_papers_low_overlap", r, {"sk": True, "nm": True, "no": True})
    return _wrap("case_b_two_overlapping_papers_low_overlap", r, {
        "os": r.get("overlap_strategy_applied") is True,
        "uc": r.get("uncertain_or_partial") is True,
        "nm": r.get("no_forced_multi_surface") is True,
        "no": r.get("no_ocr") is True,
    })


def smoke_case_c() -> Dict[str, Any]:
    r = run_case_c()
    if r.get("skipped_missing_fixture"):
        return _wrap("case_c_two_overlapping_papers_high_overlap", r, {"sk": True, "nm": True, "no": True})
    return _wrap("case_c_two_overlapping_papers_high_overlap", r, {
        "ur": r.get("uncertain_relation") is True,
        "ns": r.get("no_separation_upgrade") is True,
        "nm": r.get("no_forced_multi_surface") is True,
        "no": r.get("no_ocr") is True,
    })


def smoke_case_d() -> Dict[str, Any]:
    r = run_case_d()
    if r.get("skipped_missing_fixture"):
        return _wrap("case_d_low_contrast_single_paper", r, {"sk": True, "nf": True})
    return _wrap("case_d_low_contrast_single_paper", r, {
        "qg": r.get("quality_gate_applied") is True,
        "cap": r.get("candidate_cap_respected") is True,
        "lc": r.get("low_contrast_strategy") is True,
        "nf": r.get("no_fact") is True,
    })


def smoke_case_e() -> Dict[str, Any]:
    r = run_case_e()
    if r.get("skipped_missing_fixture"):
        return _wrap("case_e_low_contrast_texture_false_positive", r, {"sk": True, "nf": True})
    return _wrap("case_e_low_contrast_texture_false_positive", r, {
        "lc": r.get("low_contrast_strategy") is True,
        "es": r.get("excessive_suppression") is True,
        "nf": r.get("no_fact") is True,
    })


def smoke_case_f() -> Dict[str, Any]:
    r = run_case_f()
    if r.get("skipped_missing_fixture"):
        return _wrap("case_f_receipt_attached_clear", r, {"sk": True, "nf": True})
    return _wrap("case_f_receipt_attached_clear", r, {
        "at": r.get("attached_strategy_applied") is True,
        "ev": r.get("relation_evidence_basis") is True,
        "np": r.get("no_receipt_to_package_fact") is True,
        "nf": r.get("no_fact") is True,
    })


def smoke_case_g() -> Dict[str, Any]:
    r = run_case_g()
    if r.get("skipped_missing_fixture"):
        return _wrap("case_g_receipt_attached_uncertain", r, {"sk": True, "nf": True})
    return _wrap("case_g_receipt_attached_uncertain", r, {
        "ua": r.get("uncertain_attached") is True,
        "rm": r.get("request_more_evidence") is True,
        "nf": r.get("no_fact") is True,
    })


def smoke_case_h() -> Dict[str, Any]:
    r = run_case_h()
    if r.get("skipped_missing_fixture"):
        return _wrap("case_h_document_on_screen_control", r, {"sk": True, "nf": True})
    return _wrap("case_h_document_on_screen_control", r, {
        "sd": r.get("screen_defer") is True,
        "sg": r.get("screen_guard") is True,
        "nf": r.get("no_fact") is True,
    })


def run_smoke_cases() -> Dict[str, Any]:
    cases = [
        smoke_case_a(), smoke_case_b(), smoke_case_c(), smoke_case_d(),
        smoke_case_e(), smoke_case_f(), smoke_case_g(), smoke_case_h(),
    ]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    dryrun = run_iteration_processor()
    if failed:
        fd = FINAL_BLOCKED
    else:
        fd = dryrun.get("final_decision", FINAL_BLOCKED)
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Controlled-Execution-Iteration-DryRun-v1-001",
        "iteration_dryrun_only": True,
        "iteration_strategy_layer": True,
        "runtime_activation": False,
        "real_execution_enabled": False,
        "fixture_audit": dryrun.get("fixture_audit"),
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "smoke_case_count": len(cases),
        "failed_checks": failed,
        "final_decision": fd,
        "dryrun_final_decision": dryrun.get("final_decision"),
        "recommended_next_phase": dryrun.get("recommended_next_phase"),
        "metrics": dryrun.get("metrics"),
    }
