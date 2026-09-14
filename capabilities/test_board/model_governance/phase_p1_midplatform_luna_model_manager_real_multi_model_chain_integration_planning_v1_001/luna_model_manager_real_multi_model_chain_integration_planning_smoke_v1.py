# -*- coding: utf-8 -*-
"""Luna Model Manager Real Multi-Model Chain — planning smoke fixtures v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.collaboration.real_chain.real_chain_orchestrator_v1 import (
    run_detector_unavailable_degradation,
    run_normal_shopfront_chain,
    run_ocr_failure_chain,
    run_qwen_unsupported_claim_chain,
)
from capabilities.midplatform.model_manager.luna_model_manager_real_chain_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    SMOKE_CASE_IDS,
)


def smoke_case_a_normal_shopfront() -> Dict[str, Any]:
    """Case A: Detector + OCR + Qwen context — full chain."""
    case_id = "case_a_normal_shopfront_chain"
    result = run_normal_shopfront_chain()
    binding = result.get("binding_check") or {}
    fusion = result.get("fusion_candidate") or {}
    passed = (
        binding.get("all_slots_filled") is True
        and binding.get("qwen_not_in_ocr_slot") is True
        and result.get("all_slots_completed") is True
        and fusion.get("fusion_candidate") is True
        and fusion.get("not_answer_fusion") is True
        and result.get("qwen_not_ocr") is True
        and len(result.get("evidence_packages") or []) == 3
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_b_ocr_failure() -> Dict[str, Any]:
    """Case B: OCR failure → challenge → request_more_evidence."""
    case_id = "case_b_ocr_failure_challenge"
    result = run_ocr_failure_chain()
    ocr_fail = result.get("ocr_failure_candidate") or {}
    validation = result.get("validation_review") or {}
    passed = (
        ocr_fail.get("evidence_type") == "ocr_failure_candidate"
        and ocr_fail.get("status") == "failed"
        and result.get("not_auto_model_replacement") is True
        and result.get("no_qwen_text_guess") is True
        and validation.get("validation_status") == "request_more_evidence"
        and validation.get("l2_replan_candidate") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_c_qwen_unsupported() -> Dict[str, Any]:
    """Case C: Qwen Starbucks without OCR support → reject."""
    case_id = "case_c_qwen_unsupported_claim_reject"
    result = run_qwen_unsupported_claim_chain()
    unsupported = result.get("unsupported_claim_check") or {}
    validation = result.get("validation_review") or {}
    passed = (
        unsupported.get("has_unsupported_claim") is True
        and unsupported.get("ocr_contains_claim") is False
        and validation.get("validation_status") == "rejected_by_policy"
        and validation.get("rejection_reason") == "unsupported_claim"
        and result.get("teacher_not_fact_owner") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_d_detector_unavailable() -> Dict[str, Any]:
    """Case D: Detector unavailable → degradation → replan."""
    case_id = "case_d_detector_unavailable_degradation"
    result = run_detector_unavailable_degradation()
    degradation = result.get("collaboration_degradation") or {}
    passed = (
        degradation.get("collaboration_degradation_candidate") is True
        and result.get("lost_capability_recorded") is True
        and result.get("not_silent") is True
        and (result.get("l2_replan_candidate") or {}).get("owned_by") == "L2_Agent_Planning"
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def run_smoke_cases() -> Dict[str, Any]:
    runners = [
        smoke_case_a_normal_shopfront,
        smoke_case_b_ocr_failure,
        smoke_case_c_qwen_unsupported,
        smoke_case_d_detector_unavailable,
    ]
    cases = [fn() for fn in runners]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Real-Multi-Model-Chain-Integration-Planning-v1-001",
        "planning_only": True,
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "smoke_case_count": len(cases),
        "failed_checks": failed,
        "model_os_frozen": True,
        "single_real_chain": True,
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
