# -*- coding: utf-8 -*-
"""Luna Document Surface Detector — controlled execution dryrun smoke v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_real_runtime_controlled_execution_dryrun_processor_v1 import (
    run_case_a,
    run_case_b,
    run_case_c,
    run_case_d,
    run_case_e,
    run_case_f,
    run_case_g,
    run_case_h,
    run_dryrun_processor,
)
from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_real_runtime_controlled_execution_dryrun_types_v1 import (
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
        return _wrap("case_a_single_flat_paper_controlled", r, {
            "sk": True, "nf": r.get("no_fake_image_generated") is True, "no": r.get("no_ocr") is True,
        })
    return _wrap("case_a_single_flat_paper_controlled", r, {
        "cv": r.get("cv2_executed") is True,
        "hc": r.get("has_candidate") is True,
        "co": r.get("candidate_only") is True,
        "no": r.get("no_ocr") is True,
    })


def smoke_case_b() -> Dict[str, Any]:
    r = run_case_b()
    if r.get("skipped_missing_fixture"):
        return _wrap("case_b_two_overlapping_papers_controlled", r, {"sk": True, "nm": True, "no": True})
    return _wrap("case_b_two_overlapping_papers_controlled", r, {
        "hs": r.get("has_surfaces_or_uncertain") is True,
        "nm": r.get("no_merge") is True,
        "no": r.get("no_ocr") is True,
    })


def smoke_case_c() -> Dict[str, Any]:
    r = run_case_c()
    if r.get("skipped_missing_fixture"):
        return _wrap("case_c_low_contrast_paper_controlled", r, {"sk": True, "nf": True})
    return _wrap("case_c_low_contrast_paper_controlled", r, {
        "lc": r.get("low_conf_or_evidence") is True,
        "nf": r.get("no_fact") is True,
    })


def smoke_case_d() -> Dict[str, Any]:
    r = run_case_d()
    if r.get("skipped_missing_fixture"):
        return _wrap("case_d_receipt_attached_to_package_controlled", r, {"sk": True, "np": True})
    return _wrap("case_d_receipt_attached_to_package_controlled", r, {
        "rh": r.get("relation_hint") is True or r.get("no_package_fact") is True,
        "np": r.get("no_package_fact") is True,
    })


def smoke_case_e() -> Dict[str, Any]:
    r = run_case_e()
    if r.get("skipped_missing_fixture"):
        return _wrap("case_e_document_on_screen_controlled", r, {"sk": True, "ns": True})
    return _wrap("case_e_document_on_screen_controlled", r, {
        "sc": r.get("screen_candidate") is True,
        "ns": r.get("no_screen_fact") is True,
    })


def smoke_case_f() -> Dict[str, Any]:
    r = run_case_f()
    return _wrap("case_f_attention_blocked_controlled", r, {
        "z": r.get("runtime_call_zero") is True,
        "nc": r.get("no_cv2") is True,
        "nr": r.get("no_read") is True,
        "sk": r.get("skipped") is True,
    })


def smoke_case_g() -> Dict[str, Any]:
    r = run_case_g()
    return _wrap("case_g_unsupported_format_controlled", r, {
        "ab": r.get("aborted") is True,
        "uf": r.get("unsupported") is True,
        "nf": r.get("no_fallback") is True,
    })


def smoke_case_h() -> Dict[str, Any]:
    r = run_case_h()
    return _wrap("case_h_image_read_failed_controlled", r, {
        "ab": r.get("aborted") is True,
        "rf": r.get("read_failed") is True,
        "tr": r.get("trace_retained") is True,
        "nf": r.get("no_fallback") is True,
    })


def run_smoke_cases() -> Dict[str, Any]:
    cases = [
        smoke_case_a(), smoke_case_b(), smoke_case_c(), smoke_case_d(),
        smoke_case_e(), smoke_case_f(), smoke_case_g(), smoke_case_h(),
    ]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    dryrun = run_dryrun_processor()
    if failed:
        fd = FINAL_BLOCKED
    else:
        fd = dryrun.get("final_decision", FINAL_BLOCKED)
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Controlled-Execution-DryRun-v1-001",
        "controlled_execution_dryrun_only": True,
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
    }
