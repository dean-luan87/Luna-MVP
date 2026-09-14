# -*- coding: utf-8 -*-
"""Luna Model Manager Qwen-VL — planning smoke fixtures v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.luna_model_manager_qwen_vl_processor_v1 import (
    run_model_manager_qwen_vl_planning,
    run_qwen_lifecycle_version_switch_planning,
)
from capabilities.midplatform.model_manager.luna_model_manager_qwen_vl_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    SMOKE_CASE_IDS,
)
from capabilities.test_board.model_governance.phase_p1_midplatform_luna_agent_planning_layer_dryrun_v1_001.luna_agent_planning_layer_dryrun_fixtures_v1 import (
    fixture_job_564f1aa93983_shop_sign,
)
from capabilities.test_board.model_governance.phase_p1_midplatform_single_teacher_qwen_vl_integration_dryrun_v1_001.luna_qwen_vl_integration_dryrun_fixtures_v1 import (
    fixture_job_unknown_scene,
)


def smoke_case_a_unknown_scene_qwen_evidence() -> Dict[str, Any]:
    """Case A: unknown_scene → MM selects Qwen → Evidence Candidate → Validation."""
    case_id = "case_a_unknown_scene_qwen_evidence"
    result = run_model_manager_qwen_vl_planning(
        fixture_job_unknown_scene(),
        score_profile="unknown_scene_multi",
        mock_scenario="unknown_scene_hypothesis",
    )
    review = result.get("provider_validation_review") or {}
    routing = result.get("routing_selection") or {}
    passed = (
        result.get("registry_owned") is True
        and result.get("qwen_selected") is True
        and routing.get("selected_model_id") == "qwen_vl"
        and (result.get("capability_match") or {}).get("required_capability") == "unknown_scene_reasoning"
        and review.get("validation_status") == "accepted_as_evidence"
        and (result.get("provider_result") or {}).get("evidence_candidate") is not None
        and result.get("no_fact_write") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_b_shopfront_ocr_qwen_noop() -> Dict[str, Any]:
    """Case B: shopfront_sign → OCR selected, Qwen noop."""
    case_id = "case_b_shopfront_ocr_qwen_noop"
    result = run_model_manager_qwen_vl_planning(
        fixture_job_564f1aa93983_shop_sign(),
        score_profile="shopfront_ocr",
    )
    routing = result.get("routing_selection") or {}
    review = result.get("provider_validation_review") or {}
    passed = (
        routing.get("selected_tool_id") == "ocr_v1"
        and result.get("qwen_selected") is False
        and review.get("qwen_noop") is True
        and (result.get("provider_result") is None or not result.get("provider_result", {}).get("invoked"))
        and result.get("no_hardcoded_provider_call") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_c_qwen_timeout_fallback() -> Dict[str, Any]:
    """Case C: API timeout → provider_error → fallback_plan_candidate → L2."""
    case_id = "case_c_qwen_provider_timeout_fallback"
    result = run_model_manager_qwen_vl_planning(
        fixture_job_unknown_scene(),
        score_profile="unknown_scene_multi",
        simulate_timeout=True,
    )
    review = result.get("provider_validation_review") or {}
    fallback = result.get("fallback_plan_candidate") or {}
    passed = (
        result.get("qwen_selected") is True
        and review.get("provider_error_candidate") is True
        and review.get("fallback_required") is True
        and fallback.get("fallback_plan_candidate") is True
        and fallback.get("owned_by") == "L2_Agent_Planning"
        and (result.get("provider_result") or {}).get("error_type") == "api_timeout"
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_d_unsupported_claim_reject() -> Dict[str, Any]:
    """Case D: 'This is Starbucks' without evidence → unsupported_claim → reject."""
    case_id = "case_d_qwen_unsupported_claim_reject"
    result = run_model_manager_qwen_vl_planning(
        fixture_job_unknown_scene(),
        score_profile="unknown_scene_multi",
        mock_scenario="unsupported_brand_claim",
    )
    review = result.get("provider_validation_review") or {}
    provider = result.get("provider_result") or {}
    passed = (
        provider.get("has_unsupported_claim") is True
        and review.get("validation_status") == "rejected_by_policy"
        and review.get("rejection_reason") == "unsupported_claim"
        and review.get("selected_plan_unchanged") is True
        and (provider.get("evidence_candidate") is None)
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_e_lifecycle_version_switch() -> Dict[str, Any]:
    """Case E: qwen_vl v1 active → v2 upgrade → v1 deprecated."""
    case_id = "case_e_qwen_lifecycle_version_switch"
    outcome = run_qwen_lifecycle_version_switch_planning()
    passed = (
        outcome.get("v2_active") is True
        and outcome.get("v1_deprecated") is True
        and outcome.get("upper_layer_unchanged") is True
        and (outcome.get("v1_deprecation") or {}).get("trace_preserved") is True
    )
    return {"case_id": case_id, "passed": passed, "outcome": outcome}


def run_smoke_cases() -> Dict[str, Any]:
    runners = [
        smoke_case_a_unknown_scene_qwen_evidence,
        smoke_case_b_shopfront_ocr_qwen_noop,
        smoke_case_c_qwen_timeout_fallback,
        smoke_case_d_unsupported_claim_reject,
        smoke_case_e_lifecycle_version_switch,
    ]
    cases = [fn() for fn in runners]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-QwenVL-Real-Provider-Integration-Planning-v1-001",
        "planning_only": True,
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "smoke_case_count": len(cases),
        "failed_checks": failed,
        "qwen_under_model_manager": True,
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
