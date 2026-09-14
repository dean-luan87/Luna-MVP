# -*- coding: utf-8 -*-
"""Luna Document Surface Detector — implementation dryrun smoke v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_real_runtime_implementation_dryrun_processor_v1 import (
    run_attention_blocked,
    run_document_on_screen,
    run_folded_or_curved_paper,
    run_low_contrast_paper_on_desk,
    run_receipt_attached_to_package,
    run_runtime_error,
    run_single_flat_paper,
    run_two_overlapping_papers,
)
from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_real_runtime_implementation_dryrun_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    SMOKE_CASE_IDS,
)


def _wrap(case_id: str, result: Dict[str, Any], checks: Dict[str, bool]) -> Dict[str, Any]:
    return {"case_id": case_id, "passed": all(checks.values()), "result": result, "checks": checks}


def smoke_case_a() -> Dict[str, Any]:
    r = run_single_flat_paper()
    return _wrap("case_a_single_flat_paper", r, {
        "quad": r.get("quadrilateral") is True,
        "surf": r.get("surface") is True,
        "vis": r.get("visible") is True,
        "own": r.get("ownership_ok") is True,
        "no_ocr": r.get("no_ocr") is True,
    })


def smoke_case_b() -> Dict[str, Any]:
    r = run_two_overlapping_papers()
    return _wrap("case_b_two_overlapping_papers", r, {
        "a": r.get("paper_a") is True,
        "b": r.get("paper_b") is True,
        "rel": r.get("overlap_or_occludes") is True,
        "nm": r.get("not_merged") is True,
        "ready": r.get("text_ready") is True,
    })


def smoke_case_c() -> Dict[str, Any]:
    r = run_folded_or_curved_paper()
    return _wrap("case_c_folded_or_curved_paper", r, {
        "poly": r.get("polygon") is True,
        "ev": r.get("needs_evidence") is True,
        "nf": r.get("no_fact") is True,
    })


def smoke_case_d() -> Dict[str, Any]:
    r = run_receipt_attached_to_package()
    return _wrap("case_d_receipt_attached_to_package", r, {
        "rec": r.get("receipt") is True,
        "pkg": r.get("package") is True,
        "att": r.get("attached") is True,
        "own": r.get("receipt_owner") is True,
    })


def smoke_case_e() -> Dict[str, Any]:
    r = run_document_on_screen()
    return _wrap("case_e_document_on_screen", r, {
        "scr": r.get("screen_hint") is True,
        "def": r.get("defer") is True,
        "npf": r.get("not_paper_fact") is True,
    })


def smoke_case_f() -> Dict[str, Any]:
    r = run_low_contrast_paper_on_desk()
    return _wrap("case_f_low_contrast_paper_on_desk", r, {
        "lc": r.get("low_contrast") is True,
        "ev": r.get("needs_evidence") is True,
        "act": r.get("next_action") is True,
    })


def smoke_case_g() -> Dict[str, Any]:
    r = run_attention_blocked()
    return _wrap("case_g_attention_blocked", r, {
        "zero": r.get("zero_calls") is True,
        "skip": r.get("skipped") is True,
        "ns": r.get("no_surfaces") is True,
    })


def smoke_case_h() -> Dict[str, Any]:
    r = run_runtime_error()
    return _wrap("case_h_runtime_error", r, {
        "err": r.get("error") is True,
        "hand": r.get("handled") is True,
        "ho": r.get("handoff") is True,
        "ns": r.get("no_silent") is True,
    })


def run_smoke_cases() -> Dict[str, Any]:
    cases = [
        smoke_case_a(), smoke_case_b(), smoke_case_c(), smoke_case_d(),
        smoke_case_e(), smoke_case_f(), smoke_case_g(), smoke_case_h(),
    ]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Implementation-DryRun-v1-001",
        "runtime_id": "document_surface_detector_v1",
        "implementation_dryrun_only": True,
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "smoke_case_count": len(cases),
        "failed_checks": failed,
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
