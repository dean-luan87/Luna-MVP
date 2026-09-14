# -*- coding: utf-8 -*-
"""Luna Mixed Region Understanding — planning smoke fixtures v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.luna_model_manager_mixed_region_understanding_processor_v1 import (
    run_artistic_text_visual_gap,
    run_glass_reflection_ownership,
    run_logo_only_no_text_fact,
    run_metro_multi_channel,
    run_multi_object_multi_slots,
    run_occlusion_visual_supplement,
    run_ocr_wrong_visual_support,
    run_shelf_entity_separation,
    run_shopfront_information_slots,
    run_stacked_documents_ownership,
    run_text_visual_conflict,
)
from capabilities.midplatform.model_manager.luna_model_manager_mixed_region_understanding_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    SMOKE_CASE_IDS,
)


def _wrap(case_id: str, result: Dict[str, Any], checks: Dict[str, bool]) -> Dict[str, Any]:
    passed = all(checks.values())
    return {"case_id": case_id, "passed": passed, "result": result, "checks": checks}


def smoke_case_a() -> Dict[str, Any]:
    r = run_shopfront_information_slots()
    return _wrap("case_a_shopfront_information_slots", r, {
        "mixed_business_sign": r.get("mixed_business_sign") is True,
        "has_text_slot": r.get("has_text_slot") is True,
        "has_visual_slot": r.get("has_visual_slot") is True,
        "multi_slot": r.get("multi_slot_activation") is True,
        "not_recognizer": r.get("not_single_ocr_task") is True,
    })


def smoke_case_b() -> Dict[str, Any]:
    r = run_metro_multi_channel()
    return _wrap("case_b_metro_multi_channel", r, {
        "transit_sign": r.get("transit_sign") is True,
        "layout_slot": r.get("has_layout_slot") is True,
        "spatial": r.get("spatial_evidence") is True,
    })


def smoke_case_f() -> Dict[str, Any]:
    r = run_occlusion_visual_supplement()
    return _wrap("case_f_occlusion_visual_supplement", r, {
        "visual_supplements": r.get("visual_supplements") is True,
        "not_text_completion": r.get("not_text_completion") is True,
        "completeness": r.get("has_completeness") is True,
    })


def smoke_case_g() -> Dict[str, Any]:
    r = run_text_visual_conflict()
    return _wrap("case_g_text_visual_conflict", r, {
        "conflict": r.get("conflict") is True,
        "validation_review": r.get("validation_review") is True,
        "not_answer_merge": r.get("not_answer_merge") is True,
    })


def smoke_case_h() -> Dict[str, Any]:
    r = run_artistic_text_visual_gap()
    return _wrap("case_h_artistic_text_visual_gap", r, {
        "visual_supplements_gap": r.get("visual_supplements_gap") is True,
        "not_vlm_replaces_ocr": r.get("not_vlm_replaces_ocr") is True,
    })


def smoke_case_i() -> Dict[str, Any]:
    r = run_logo_only_no_text_fact()
    return _wrap("case_i_logo_only_no_text_fact", r, {
        "visual_exists": r.get("visual_exists") is True,
        "text_missing": r.get("text_missing") is True,
        "not_invented_text": r.get("not_invented_text") is True,
    })


def smoke_case_j() -> Dict[str, Any]:
    r = run_ocr_wrong_visual_support()
    return _wrap("case_j_ocr_wrong_visual_support", r, {
        "ocr_low": r.get("ocr_low_confidence") is True,
        "visual_support": r.get("visual_support") is True,
        "request_more": r.get("request_more_evidence") is True,
    })


def smoke_case_k() -> Dict[str, Any]:
    r = run_multi_object_multi_slots()
    return _wrap("case_k_multi_object_multi_slots", r, {
        "multi_object": r.get("multi_object") is True,
        "slot_count": r.get("slot_count_gte_4") is True,
        "not_one_ocr": r.get("not_one_ocr_task") is True,
    })


def smoke_case_l() -> Dict[str, Any]:
    r = run_stacked_documents_ownership()
    return _wrap("case_l_stacked_documents_ownership", r, {
        "multi_objects": r.get("multi_objects") is True,
        "occlusion": r.get("occlusion_graph") is True,
        "owners": r.get("each_text_has_owner") is True,
        "paper_a": r.get("paper_a_zhangsan") is True,
        "paper_b": r.get("paper_b_lisi") is True,
        "not_flat": r.get("not_flat_merge") is True,
    })


def smoke_case_m() -> Dict[str, Any]:
    r = run_glass_reflection_ownership()
    return _wrap("case_m_glass_reflection_ownership", r, {
        "real_reflection": r.get("has_real_and_reflection") is True,
        "reflection_marked": r.get("reflection_marked") is True,
        "separated": r.get("owners_separated") is True,
    })


def smoke_case_n() -> Dict[str, Any]:
    r = run_shelf_entity_separation()
    return _wrap("case_n_shelf_entity_separation", r, {
        "three_entities": r.get("three_entities") is True,
        "product": r.get("product_separated") is True,
        "price": r.get("price_separated") is True,
        "ad": r.get("ad_separated") is True,
    })


def run_smoke_cases() -> Dict[str, Any]:
    runners = [
        smoke_case_a, smoke_case_b, smoke_case_f, smoke_case_g,
        smoke_case_h, smoke_case_i, smoke_case_j, smoke_case_k,
        smoke_case_l, smoke_case_m, smoke_case_n,
    ]
    cases = [fn() for fn in runners]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Mixed-Region-Understanding-Planning-v1-001",
        "planning_only": True,
        "region_intelligence_layer": True,
        "ownership_understanding": True,
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "smoke_case_count": len(cases),
        "failed_checks": failed,
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
