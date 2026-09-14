# -*- coding: utf-8 -*-
"""Luna Model Manager Text Detection Runtime — planning smoke fixtures v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.luna_model_manager_text_detection_runtime_processor_v1 import (
    run_low_confidence_detection,
    run_metro_direction_detection,
    run_no_text_detection,
    run_shopfront_text_detection,
)
from capabilities.midplatform.model_manager.luna_model_manager_text_detection_runtime_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    SMOKE_CASE_IDS,
)


def smoke_case_a_shopfront() -> Dict[str, Any]:
    case_id = "case_a_shopfront_text_region"
    result = run_shopfront_text_detection()
    passed = (
        result.get("has_regions") is True
        and result.get("evidence_type_correct") is True
        and result.get("next_slot_is_ocr") is True
        and result.get("not_shopfront_fact") is True
        and result.get("l2_plan_unchanged") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_b_metro() -> Dict[str, Any]:
    case_id = "case_b_metro_direction_region"
    result = run_metro_direction_detection()
    passed = (
        result.get("direction_region_detected") is True
        and result.get("not_station_name_fact") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_c_no_text() -> Dict[str, Any]:
    case_id = "case_c_no_text_image"
    result = run_no_text_detection()
    passed = (
        result.get("no_text") is True
        and result.get("no_forced_ocr") is True
        and result.get("next_slot_none") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_d_low_confidence() -> Dict[str, Any]:
    case_id = "case_d_low_confidence_detection"
    result = run_low_confidence_detection()
    passed = (
        result.get("low_confidence") is True
        and result.get("not_direct_ocr") is True
        and result.get("requires_validation") is True
        and result.get("validation_before_ocr") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def run_smoke_cases() -> Dict[str, Any]:
    runners = [smoke_case_a_shopfront, smoke_case_b_metro, smoke_case_c_no_text, smoke_case_d_low_confidence]
    cases = [fn() for fn in runners]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Real-Text-Detection-Runtime-Integration-Planning-v1-001",
        "planning_only": True,
        "single_runtime_text_detection": True,
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "smoke_case_count": len(cases),
        "failed_checks": failed,
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
