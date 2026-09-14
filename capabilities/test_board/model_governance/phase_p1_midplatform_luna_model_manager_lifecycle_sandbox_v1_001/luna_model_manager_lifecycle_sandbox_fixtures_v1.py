# -*- coding: utf-8 -*-
"""Luna Model Manager Lifecycle Sandbox — fixtures & cases v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.lifecycle.luna_model_manager_lifecycle_sandbox_adapter_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    run_lifecycle_sandbox_case,
)

SANDBOX_CASE_IDS = (
    "case_a_new_ocr_model_lifecycle",
    "case_b_insufficient_capability_rejected",
    "case_c_ocr_v1_deprecation",
    "case_d_malicious_model_blocked",
)


def sandbox_case_a_new_ocr_model() -> Dict[str, Any]:
    """Case A: new OCR model → candidate → evaluation → active."""
    case_id = "case_a_new_ocr_model_lifecycle"
    outcome = run_lifecycle_sandbox_case(case_type="new_ocr_model")
    return {"case_id": case_id, "passed": outcome.get("passed") is True, "outcome": outcome}


def sandbox_case_b_insufficient_capability() -> Dict[str, Any]:
    """Case B: Qwen precise OCR → evaluation_failed → not_routing_eligible."""
    case_id = "case_b_insufficient_capability_rejected"
    outcome = run_lifecycle_sandbox_case(case_type="insufficient_capability")
    return {"case_id": case_id, "passed": outcome.get("passed") is True, "outcome": outcome}


def sandbox_case_c_ocr_deprecation() -> Dict[str, Any]:
    """Case C: OCR-v1 deprecated by OCR-v2, trace preserved."""
    case_id = "case_c_ocr_v1_deprecation"
    outcome = run_lifecycle_sandbox_case(case_type="model_deprecation")
    return {"case_id": case_id, "passed": outcome.get("passed") is True, "outcome": outcome}


def sandbox_case_d_malicious_blocked() -> Dict[str, Any]:
    """Case D: unsupported claim abuse → blocked."""
    case_id = "case_d_malicious_model_blocked"
    outcome = run_lifecycle_sandbox_case(case_type="malicious_model_block")
    return {"case_id": case_id, "passed": outcome.get("passed") is True, "outcome": outcome}


def run_all_sandbox_cases() -> Dict[str, Any]:
    runners = [
        sandbox_case_a_new_ocr_model,
        sandbox_case_b_insufficient_capability,
        sandbox_case_c_ocr_deprecation,
        sandbox_case_d_malicious_blocked,
    ]
    cases = [fn() for fn in runners]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Lifecycle-Sandbox-v1-001",
        "sandbox_only": True,
        "sandbox_case_ids": list(SANDBOX_CASE_IDS),
        "sandbox_cases": cases,
        "sandbox_passed": sum(1 for c in cases if c.get("passed")),
        "sandbox_case_count": len(cases),
        "failed_checks": failed,
        "luna_owns_model_lifecycle": True,
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
