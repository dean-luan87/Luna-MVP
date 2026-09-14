# -*- coding: utf-8 -*-
"""Luna Model Manager Qwen-VL — dryrun fixtures v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.providers.qwen_vl.dryrun.qwen_vl_lifecycle_integration_v1 import (
    run_qwen_version_switch_dryrun,
)
from capabilities.midplatform.model_manager.providers.qwen_vl.dryrun.qwen_vl_model_usage_metrics_v1 import (
    reset_qwen_model_usage_metrics,
)
from capabilities.midplatform.model_manager.providers.qwen_vl.dryrun.qwen_vl_provider_dryrun_adapter_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    run_qwen_vl_provider_dryrun,
)
from capabilities.midplatform.model_manager.luna_model_manager_qwen_vl_types_v1 import (
    DRYRUN_CASE_IDS,
)
from capabilities.test_board.model_governance.phase_p1_midplatform_luna_agent_planning_layer_dryrun_v1_001.luna_agent_planning_layer_dryrun_fixtures_v1 import (
    fixture_job_564f1aa93983_shop_sign,
)
from capabilities.test_board.model_governance.phase_p1_midplatform_single_teacher_qwen_vl_integration_dryrun_v1_001.luna_qwen_vl_integration_dryrun_fixtures_v1 import (
    fixture_job_unknown_scene,
)


def _plan_read_small_text() -> Dict[str, Any]:
    return {
        "plan_id": "plan_read_small_text",
        "plan_goal_candidate": {
            "goal_type": "read_small_text",
            "interpreted_goal": "read_precise_text",
            "candidate_only": True,
            "not_fact": True,
        },
        "tool_plan_candidates": [
            {"capability_type": "ocr", "execution_mode": "request_tool_os_admission", "candidate_only": True},
        ],
        "candidate_only": True,
        "not_fact": True,
    }


def dryrun_case_a_qwen_normal_closed_loop() -> Dict[str, Any]:
    """Case A: unknown_scene → Qwen → evidence → validation → evaluation."""
    reset_qwen_model_usage_metrics()
    case_id = "case_a_qwen_normal_closed_loop"
    result = run_qwen_vl_provider_dryrun(
        fixture_job_unknown_scene(),
        case_id=case_id,
        score_profile="unknown_scene_multi",
        mock_scenario="unknown_scene_hypothesis",
    )
    review = result.get("provider_validation_review") or {}
    eval_rec = result.get("model_evaluation_record") or {}
    passed = (
        result.get("provider_selected") is True
        and result.get("provider_selected_id") == "qwen_vl"
        and (result.get("capability_match") or {}).get("required_capability") == "unknown_scene_reasoning"
        and result.get("model_record", {}).get("lifecycle_state") == "active"
        and review.get("validation_status") == "accepted_as_evidence"
        and result.get("normalized_evidence") is not None
        and eval_rec.get("evaluation_engine") == "model_evaluation_engine_v1"
        and eval_rec.get("no_auto_policy_update") is True
        and (result.get("request_boundary_validation") or {}).get("passed") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_b_capability_mismatch() -> Dict[str, Any]:
    """Case B: read_small_text → OCR selected, Qwen noop."""
    reset_qwen_model_usage_metrics()
    case_id = "case_b_capability_mismatch_ocr_selected"
    result = run_qwen_vl_provider_dryrun(
        fixture_job_564f1aa93983_shop_sign(),
        case_id=case_id,
        score_profile="shopfront_ocr",
        plan_override=_plan_read_small_text(),
    )
    routing = result.get("routing_selection") or {}
    review = result.get("provider_validation_review") or {}
    metrics = result.get("model_usage_metrics") or {}
    passed = (
        routing.get("selected_tool_id") == "ocr_v1"
        and result.get("provider_selected") is False
        and review.get("qwen_noop") is True
        and metrics.get("noop_count", 0) >= 1
        and (result.get("goal_ownership_validation") or {}).get("passed") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_c_version_switch() -> Dict[str, Any]:
    """Case C: v1 active → v2 upgrade → v1 deprecated, L1/L2 unchanged."""
    case_id = "case_c_qwen_version_switch"
    outcome = run_qwen_version_switch_dryrun()
    passed = (
        outcome.get("v1_was_active") is True
        and outcome.get("v2_is_active") is True
        and outcome.get("v1_is_deprecated") is True
        and outcome.get("trace_preserved") is True
        and outcome.get("l1_l2_unchanged") is True
    )
    return {"case_id": case_id, "passed": passed, "outcome": outcome}


def dryrun_case_d_provider_timeout() -> Dict[str, Any]:
    """Case D: API timeout → provider_error → fallback L2, no silent switch."""
    reset_qwen_model_usage_metrics()
    case_id = "case_d_provider_timeout_no_silent_switch"
    result = run_qwen_vl_provider_dryrun(
        fixture_job_unknown_scene(),
        case_id=case_id,
        score_profile="unknown_scene_multi",
        simulate_timeout=True,
    )
    review = result.get("provider_validation_review") or {}
    fallback = result.get("fallback_plan_candidate") or {}
    passed = (
        result.get("provider_selected") is True
        and review.get("provider_error_candidate") is True
        and review.get("fallback_required") is True
        and fallback.get("owned_by") == "L2_Agent_Planning"
        and result.get("no_silent_model_switch") is True
        and (result.get("silent_switch_validation") or {}).get("passed") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_e_unsupported_claim() -> Dict[str, Any]:
    """Case E: Starbucks claim without OCR evidence → unsupported_claim → reject."""
    reset_qwen_model_usage_metrics()
    case_id = "case_e_unsupported_claim_governance"
    result = run_qwen_vl_provider_dryrun(
        fixture_job_unknown_scene(),
        case_id=case_id,
        score_profile="unknown_scene_multi",
        mock_scenario="unsupported_brand_claim",
    )
    review = result.get("provider_validation_review") or {}
    provider = result.get("provider_result") or {}
    metrics = result.get("model_usage_metrics") or {}
    passed = (
        provider.get("has_unsupported_claim") is True
        and review.get("validation_status") == "rejected_by_policy"
        and review.get("rejection_reason") == "unsupported_claim"
        and result.get("normalized_evidence") is not None
        and metrics.get("rejected_output_count", 0) >= 1
        and review.get("selected_plan_unchanged") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def run_all_dryrun_cases() -> Dict[str, Any]:
    runners = [
        dryrun_case_a_qwen_normal_closed_loop,
        dryrun_case_b_capability_mismatch,
        dryrun_case_c_version_switch,
        dryrun_case_d_provider_timeout,
        dryrun_case_e_unsupported_claim,
    ]
    cases = [fn() for fn in runners]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-QwenVL-Real-Provider-Integration-DryRun-v1-001",
        "dryrun_only": True,
        "dryrun_case_ids": list(DRYRUN_CASE_IDS),
        "dryrun_cases": cases,
        "dryrun_passed": sum(1 for c in cases if c.get("passed")),
        "dryrun_case_count": len(cases),
        "failed_checks": failed,
        "model_os_closed_loop": True,
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
