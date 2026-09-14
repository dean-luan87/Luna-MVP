# -*- coding: utf-8 -*-
"""Luna Model Manager OCR Recognition Runtime — planning smoke fixtures v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.luna_model_manager_text_recognition_runtime_processor_v1 import (
    run_artistic_text_visual_gap,
    run_blurry_low_confidence_ocr,
    run_metro_direction_ocr,
    run_occlusion_visual_supplement,
    run_ocr_runtime_failure,
    run_shopfront_ocr,
    run_text_visual_conflict,
    run_unsupported_ocr_claim,
)
from capabilities.midplatform.model_manager.luna_model_manager_text_recognition_runtime_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    SMOKE_CASE_IDS,
)


def smoke_case_a_shopfront() -> Dict[str, Any]:
    case_id = "case_a_shopfront_ocr_text_candidate"
    result = run_shopfront_ocr()
    passed = (
        result.get("ocr_text_candidate") is True
        and result.get("candidate_text_correct") is True
        and result.get("source_region_bound") is True
        and result.get("not_location_fact") is True
        and result.get("fusion_identify_place") is True
        and result.get("not_fact_admission") is True
        and result.get("recognition_not_detection") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_b_metro() -> Dict[str, Any]:
    case_id = "case_b_metro_direction_ocr"
    result = run_metro_direction_ocr()
    passed = (
        result.get("ocr_text_candidate") is True
        and result.get("direction_text") is True
        and result.get("task_find_direction") is True
        and result.get("not_current_station") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_c_blurry() -> Dict[str, Any]:
    case_id = "case_c_blurry_low_confidence"
    result = run_blurry_low_confidence_ocr()
    passed = (
        result.get("low_confidence_candidate") is True
        and result.get("request_more_evidence") is True
        and result.get("not_qwen_auto_complete") is True
        and result.get("validation_request_more") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_d_unsupported() -> Dict[str, Any]:
    case_id = "case_d_unsupported_ocr_claim"
    result = run_unsupported_ocr_claim()
    passed = (
        result.get("unsupported_claim") is True
        and result.get("reject_reason") is True
        and result.get("validation_rejected") is True
        and result.get("no_location_fact") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_e_runtime_fail() -> Dict[str, Any]:
    case_id = "case_e_ocr_runtime_failure"
    result = run_ocr_runtime_failure()
    passed = (
        result.get("runtime_error") is True
        and result.get("l2_replan") is True
        and result.get("not_silent_qwen") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_f_occlusion() -> Dict[str, Any]:
    case_id = "case_f_occlusion_visual_supplement"
    result = run_occlusion_visual_supplement()
    passed = (
        result.get("dual_path_active") is True
        and result.get("text_damaged") is True
        and result.get("visual_supplements") is True
        and result.get("not_text_completion") is True
        and result.get("semantic_hint") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_g_conflict() -> Dict[str, Any]:
    case_id = "case_g_text_visual_conflict"
    result = run_text_visual_conflict()
    passed = (
        result.get("conflict_detected") is True
        and result.get("validation_review") is True
        and result.get("not_direct_confirm") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_h_artistic() -> Dict[str, Any]:
    case_id = "case_h_artistic_text_visual_gap"
    result = run_artistic_text_visual_gap()
    passed = (
        result.get("ocr_gap") is True
        and result.get("visual_supplements_gap") is True
        and result.get("not_vlm_replaces_ocr") is True
        and result.get("visual_has_flame") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def run_smoke_cases() -> Dict[str, Any]:
    runners = [
        smoke_case_a_shopfront,
        smoke_case_b_metro,
        smoke_case_c_blurry,
        smoke_case_d_unsupported,
        smoke_case_e_runtime_fail,
        smoke_case_f_occlusion,
        smoke_case_g_conflict,
        smoke_case_h_artistic,
    ]
    cases = [fn() for fn in runners]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Real-OCR-Recognition-Runtime-Integration-Planning-v1-001",
        "planning_only": True,
        "mixed_region_understanding_core": True,
        "text_visual_dual_processing": True,
        "ocr_is_text_branch_only": True,
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "smoke_case_count": len(cases),
        "failed_checks": failed,
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
