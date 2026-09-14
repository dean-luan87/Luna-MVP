# -*- coding: utf-8 -*-
"""Luna Document Surface Detector — planning smoke fixtures v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_real_runtime_planning_processor_v1 import (
    run_attention_blocked_skip,
    run_layout_detector_conflict,
    run_receipt_attached_to_package,
    run_runtime_unavailable,
    run_screen_document_confusion,
    run_stacked_menus_no_ocr,
    run_stacked_papers_occlusion,
    run_uncertain_boundary,
)
from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_real_runtime_planning_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    SMOKE_CASE_IDS,
)


def _wrap(case_id: str, result: Dict[str, Any], checks: Dict[str, bool]) -> Dict[str, Any]:
    return {"case_id": case_id, "passed": all(checks.values()), "result": result, "checks": checks}


def smoke_case_a() -> Dict[str, Any]:
    r = run_stacked_papers_occlusion()
    return _wrap("case_a_stacked_papers_occlusion", r, {
        "a": r.get("paper_a") is True,
        "b": r.get("paper_b") is True,
        "occ": r.get("occludes") is True,
        "no_ocr": r.get("no_ocr") is True,
    })


def smoke_case_b() -> Dict[str, Any]:
    r = run_stacked_menus_no_ocr()
    return _wrap("case_b_stacked_menus_no_ocr", r, {
        "two": r.get("two_surfaces") is True,
        "next": r.get("next_slot") is True,
        "no_ocr": r.get("no_ocr_text") is True,
    })


def smoke_case_c() -> Dict[str, Any]:
    r = run_receipt_attached_to_package()
    return _wrap("case_c_receipt_attached_to_package", r, {
        "receipt": r.get("receipt") is True,
        "pkg": r.get("package") is True,
        "attached": r.get("attached") is True,
    })


def smoke_case_d() -> Dict[str, Any]:
    r = run_attention_blocked_skip()
    return _wrap("case_d_attention_blocked_skip", r, {
        "skip": r.get("skipped") is True,
        "zero": r.get("zero_calls") is True,
    })


def smoke_case_e() -> Dict[str, Any]:
    r = run_uncertain_boundary()
    return _wrap("case_e_uncertain_boundary", r, {
        "unc": r.get("uncertain") is True,
        "evidence": r.get("more_evidence") is True,
    })


def smoke_case_f() -> Dict[str, Any]:
    r = run_runtime_unavailable()
    return _wrap("case_f_runtime_unavailable", r, {
        "err": r.get("error") is True,
        "handoff": r.get("handoff") is True,
        "no_fb": r.get("no_ocr_fallback") is True,
    })


def smoke_case_g() -> Dict[str, Any]:
    r = run_layout_detector_conflict()
    return _wrap("case_g_layout_detector_conflict", r, {
        "conflict": r.get("conflict") is True,
        "review": r.get("validation_review") is True,
    })


def smoke_case_h() -> Dict[str, Any]:
    r = run_screen_document_confusion()
    return _wrap("case_h_screen_document_confusion", r, {
        "screen": r.get("screen_hint") is True,
        "defer": r.get("defer_screen") is True,
    })


def run_smoke_cases() -> Dict[str, Any]:
    cases = [
        smoke_case_a(), smoke_case_b(), smoke_case_c(), smoke_case_d(),
        smoke_case_e(), smoke_case_f(), smoke_case_g(), smoke_case_h(),
    ]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Integration-Planning-v1-001",
        "runtime_id": "document_surface_detector_v1",
        "planning_only": True,
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "smoke_case_count": len(cases),
        "failed_checks": failed,
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
