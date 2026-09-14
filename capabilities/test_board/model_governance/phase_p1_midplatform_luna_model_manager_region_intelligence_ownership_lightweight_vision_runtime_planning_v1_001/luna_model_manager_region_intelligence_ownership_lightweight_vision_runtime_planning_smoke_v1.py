# -*- coding: utf-8 -*-
"""Luna Lightweight Vision Runtime — planning smoke fixtures v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.luna_model_manager_region_intelligence_ownership_lightweight_vision_runtime_planning_processor_v1 import (
    run_attention_blocked_no_runtime,
    run_layout_multi_block,
    run_reflection_not_real_sign,
    run_runtime_conflict_validation,
    run_runtime_unavailable_replan,
    run_screen_surface_split,
    run_shelf_price_tag_separation,
    run_stacked_documents_occlusion,
)
from capabilities.midplatform.model_manager.luna_model_manager_region_intelligence_ownership_lightweight_vision_runtime_planning_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    SMOKE_CASE_IDS,
)


def _wrap(case_id: str, result: Dict[str, Any], checks: Dict[str, bool]) -> Dict[str, Any]:
    return {"case_id": case_id, "passed": all(checks.values()), "result": result, "checks": checks}


def smoke_case_a() -> Dict[str, Any]:
    r = run_stacked_documents_occlusion()
    return _wrap("case_a_stacked_documents_occlusion", r, {
        "doc": r.get("doc_runtime") is True,
        "paper_a": r.get("paper_a") is True,
        "paper_b": r.get("paper_b") is True,
        "occlusion": r.get("occlusion") is True,
    })


def smoke_case_b() -> Dict[str, Any]:
    r = run_shelf_price_tag_separation()
    return _wrap("case_b_shelf_price_tag_separation", r, {
        "price_rt": r.get("price_runtime") is True,
        "price": r.get("price_tag_entity") is True,
        "product": r.get("product_entity") is True,
        "separate": r.get("not_bound_to_package") is True,
    })


def smoke_case_c() -> Dict[str, Any]:
    r = run_screen_surface_split()
    return _wrap("case_c_screen_surface_split", r, {
        "screen_rt": r.get("screen_runtime") is True,
        "device": r.get("device") is True,
        "screen": r.get("screen") is True,
    })


def smoke_case_d() -> Dict[str, Any]:
    r = run_reflection_not_real_sign()
    return _wrap("case_d_reflection_not_real_sign", r, {
        "refl_rt": r.get("reflection_runtime") is True,
        "real": r.get("real_sign") is True,
        "not_real": r.get("not_real_sign") is True,
    })


def smoke_case_e() -> Dict[str, Any]:
    r = run_attention_blocked_no_runtime()
    return _wrap("case_e_attention_blocked_no_runtime", r, {
        "no_rt": r.get("no_runtimes") is True,
        "gate": r.get("attention_gate_required") is True,
    })


def smoke_case_f() -> Dict[str, Any]:
    r = run_runtime_unavailable_replan()
    return _wrap("case_f_runtime_unavailable_replan", r, {
        "error": r.get("runtime_error") is True,
        "replan": r.get("replan") is True,
        "no_fallback": r.get("no_fallback") is True,
    })


def smoke_case_g() -> Dict[str, Any]:
    r = run_layout_multi_block()
    return _wrap("case_g_layout_multi_block", r, {
        "layout": r.get("layout_runtime") is True,
        "title": r.get("has_title") is True,
        "table": r.get("has_table") is True,
        "no_merge": r.get("not_flat_merge") is True,
    })


def smoke_case_h() -> Dict[str, Any]:
    r = run_runtime_conflict_validation()
    return _wrap("case_h_runtime_conflict_validation", r, {
        "conflict": r.get("conflict_detected") is True,
        "review": r.get("validation_review") is True,
    })


def run_smoke_cases() -> Dict[str, Any]:
    cases = [
        smoke_case_a(), smoke_case_b(), smoke_case_c(), smoke_case_d(),
        smoke_case_e(), smoke_case_f(), smoke_case_g(), smoke_case_h(),
    ]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Lightweight-Vision-Runtime-Planning-v1-001",
        "planning_only": True,
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "smoke_case_count": len(cases),
        "failed_checks": failed,
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
