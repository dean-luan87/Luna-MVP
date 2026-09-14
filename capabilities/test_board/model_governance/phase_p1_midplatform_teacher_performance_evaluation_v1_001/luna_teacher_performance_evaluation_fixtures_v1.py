# -*- coding: utf-8 -*-
"""Teacher Performance Evaluation — fixtures v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.teacher_evaluation.luna_teacher_performance_evaluation_adapter_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    run_teacher_performance_evaluation_chain,
)
from capabilities.midplatform.teacher_evaluation.teacher_performance_metrics_v1 import (
    get_performance_metrics,
    reset_performance_metrics,
)
from capabilities.test_board.model_governance.phase_p1_midplatform_luna_agent_planning_layer_dryrun_v1_001.luna_agent_planning_layer_dryrun_fixtures_v1 import (
    fixture_job_564f1aa93983_shop_sign,
)
from capabilities.test_board.model_governance.phase_p1_midplatform_single_teacher_qwen_vl_integration_dryrun_v1_001.luna_qwen_vl_integration_dryrun_fixtures_v1 import (
    fixture_job_unknown_scene,
)

EVALUATION_CASE_IDS = (
    "case_a_high_value_unknown_scene",
    "case_b_low_value_shopfront_noop",
    "case_c_policy_rejection_slam",
    "case_d_unsupported_claim_hallucination",
)


def eval_case_a_high_value_unknown_scene() -> Dict[str, Any]:
    """Case A: unknown_scene + accepted evidence → value_score ↑."""
    case_id = "case_a_high_value_unknown_scene"
    result = run_teacher_performance_evaluation_chain(
        fixture_job_unknown_scene(),
        recorded_fixture_id="unknown_scene_hypothesis",
        case_id=case_id,
    )
    eval_out = result.get("teacher_performance_evaluation") or {}
    profile = result.get("teacher_usage_profile_candidate") or {}
    passed = (
        eval_out.get("evaluation_outcome") == "high_value_evidence"
        and eval_out.get("value_score", 0) > 0
        and profile.get("recommended_usage") == "high"
        and result.get("does_not_affect_current_decision") is True
        and result.get("decision_unchanged_assertion", {}).get("passed") is True
        and (result.get("usage_policy_update_candidate") or {}).get("no_auto_apply") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def eval_case_b_low_value_shopfront_noop() -> Dict[str, Any]:
    """Case B: shopfront + OCR — teacher noop correct."""
    case_id = "case_b_low_value_shopfront_noop"
    result = run_teacher_performance_evaluation_chain(
        fixture_job_564f1aa93983_shop_sign(),
        case_id=case_id,
    )
    eval_out = result.get("teacher_performance_evaluation") or {}
    record = result.get("teacher_performance_record") or {}
    profile = result.get("teacher_usage_profile_candidate") or {}
    passed = (
        eval_out.get("evaluation_outcome") == "noop_correct"
        and record.get("teacher_noop_correct") is True
        and profile.get("recommended_usage") == "low"
        and result.get("raw_teacher_response") is None
        and result.get("does_not_affect_current_decision") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def eval_case_c_policy_rejection_slam() -> Dict[str, Any]:
    """Case C: SLAM suggestion → policy_rejection recorded."""
    case_id = "case_c_policy_rejection_slam"
    result = run_teacher_performance_evaluation_chain(
        fixture_job_564f1aa93983_shop_sign(),
        recorded_fixture_id="slam_for_text",
        admission_hints={"force_admission": True},
        case_id=case_id,
    )
    eval_out = result.get("teacher_performance_evaluation") or {}
    record = result.get("teacher_performance_record") or {}
    passed = (
        eval_out.get("evaluation_outcome") == "policy_rejection"
        and record.get("validation_status") == "rejected_by_policy"
        and eval_out.get("value_score", 0) < 0
        and result.get("does_not_affect_current_decision") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def eval_case_d_unsupported_claim() -> Dict[str, Any]:
    """Case D: brand claim without OCR → unsupported_claim."""
    case_id = "case_d_unsupported_claim_hallucination"
    result = run_teacher_performance_evaluation_chain(
        fixture_job_564f1aa93983_shop_sign(),
        recorded_fixture_id="unsupported_brand_claim",
        admission_hints={"force_admission": True},
        case_id=case_id,
    )
    eval_out = result.get("teacher_performance_evaluation") or {}
    reliability = result.get("teacher_reliability_metrics") or {}
    passed = (
        eval_out.get("evaluation_outcome") == "unsupported_claim"
        and "unsupported_claim" in (result.get("teacher_performance_record") or {}).get("conflict_types", [])
        and reliability.get("unsupported_claim_rate", 0) >= 0
        and result.get("does_not_affect_current_decision") is True
        and (result.get("usage_policy_update_candidate") or {}).get("review_status") == "pending_policy_review"
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def run_all_evaluation_cases() -> Dict[str, Any]:
    reset_performance_metrics()
    runners = [
        eval_case_a_high_value_unknown_scene,
        eval_case_b_low_value_shopfront_noop,
        eval_case_c_policy_rejection_slam,
        eval_case_d_unsupported_claim,
    ]
    cases = [fn() for fn in runners]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    metrics = get_performance_metrics()
    return {
        "phase_id": "Phase-P1-Midplatform-Teacher-Performance-Evaluation-v1-001",
        "provider": "qwen_vl",
        "evaluation_case_ids": list(EVALUATION_CASE_IDS),
        "evaluation_cases": cases,
        "evaluation_cases_passed": sum(1 for c in cases if c.get("passed")),
        "evaluation_case_count": len(cases),
        "failed_checks": failed,
        "teacher_reliability_metrics": metrics.to_reliability_metrics(
            provider_id="qwen_vl",
            metrics_id="trm_aggregate",
        ),
        "teacher_performance_metrics": metrics.to_dict(),
        "does_not_affect_current_decision": all(
            (c.get("result") or {}).get("does_not_affect_current_decision") is True for c in cases
        ),
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
