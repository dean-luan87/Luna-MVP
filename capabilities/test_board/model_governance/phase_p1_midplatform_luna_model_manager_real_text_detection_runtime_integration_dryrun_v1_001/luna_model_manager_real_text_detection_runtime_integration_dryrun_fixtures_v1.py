# -*- coding: utf-8 -*-
"""Luna Text Detection Runtime — dryrun fixtures v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.luna_model_manager_text_detection_runtime_types_v1 import (
    DRYRUN_CASE_IDS,
    DRYRUN_FINAL_BLOCKED,
    DRYRUN_FINAL_GO,
)
from capabilities.midplatform.model_manager.runtime.text_detection.dryrun.text_detection_runtime_dryrun_adapter_v1 import (
    run_case_a_shopfront_dryrun,
    run_case_b_subway_dryrun,
    run_case_c_no_text_dryrun,
    run_case_d_low_confidence_dryrun,
    run_case_e_runtime_failure_dryrun,
)


def dryrun_case_a() -> Dict[str, Any]:
    case_id = "case_a_shopfront_text_region_dryrun"
    result = run_case_a_shopfront_dryrun()
    passed = (
        result.get("evidence_type_correct") is True
        and result.get("no_recognized_text") is True
        and result.get("next_slot_ocr") is True
        and result.get("governance_loop_complete") is True
        and result.get("detector_did_not_decide_next") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_b() -> Dict[str, Any]:
    case_id = "case_b_subway_direction_dryrun"
    result = run_case_b_subway_dryrun()
    passed = (
        result.get("direction_region") is True
        and result.get("not_station_fact") is True
        and result.get("ocr_worthwhile") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_c() -> Dict[str, Any]:
    case_id = "case_c_no_text_environment_dryrun"
    result = run_case_c_no_text_dryrun()
    passed = (
        result.get("no_text_candidate") is True
        and result.get("no_forced_ocr") is True
        and result.get("next_slot_none") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_d() -> Dict[str, Any]:
    case_id = "case_d_false_detection_dryrun"
    result = run_case_d_low_confidence_dryrun()
    passed = (
        result.get("low_confidence") is True
        and result.get("needs_review") is True
        and result.get("not_direct_ocr") is True
        and result.get("next_slot_none") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_e() -> Dict[str, Any]:
    case_id = "case_e_runtime_failure_dryrun"
    result = run_case_e_runtime_failure_dryrun()
    passed = (
        result.get("runtime_error") is True
        and result.get("l2_replan") is True
        and result.get("not_silent_qwen") is True
        and result.get("not_silent_sam") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def run_all_dryrun_cases() -> Dict[str, Any]:
    cases = [dryrun_case_a(), dryrun_case_b(), dryrun_case_c(), dryrun_case_d(), dryrun_case_e()]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Real-Text-Detection-Runtime-Integration-DryRun-v1-001",
        "dryrun_only": True,
        "governance_loop_not_ocr_pipeline": True,
        "deterministic_fixture_only": True,
        "dryrun_case_ids": list(DRYRUN_CASE_IDS),
        "dryrun_cases": cases,
        "dryrun_passed": sum(1 for c in cases if c.get("passed")),
        "dryrun_case_count": len(cases),
        "failed_checks": failed,
        "final_decision": DRYRUN_FINAL_GO if not failed else DRYRUN_FINAL_BLOCKED,
    }
