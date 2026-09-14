# -*- coding: utf-8 -*-
"""Qwen-VL Real Provider Integration — integration fixtures v1."""

from __future__ import annotations

from typing import Any, Dict, List

from capabilities.midplatform.teacher_adapter.providers.qwen_vl.qwen_vl_real_integration.luna_qwen_vl_real_integration_adapter_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    run_qwen_vl_real_provider_integration,
)
from capabilities.midplatform.teacher_adapter.providers.qwen_vl.teacher_usage_metrics_v1 import (
    reset_teacher_usage_metrics,
)
from capabilities.test_board.model_governance.phase_p1_midplatform_luna_agent_planning_layer_dryrun_v1_001.luna_agent_planning_layer_dryrun_fixtures_v1 import (
    fixture_job_564f1aa93983_shop_sign,
)
from capabilities.test_board.model_governance.phase_p1_midplatform_single_teacher_qwen_vl_integration_dryrun_v1_001.luna_qwen_vl_integration_dryrun_fixtures_v1 import (
    fixture_job_unknown_scene,
)

INTEGRATION_CASE_IDS = (
    "case_a_unknown_scene_real_evidence",
    "case_b_shopfront_teacher_noop",
    "case_c_slam_suggestion_rejected",
    "case_d_unsupported_claim_rejected",
)


def _scene(result: Dict[str, Any]) -> str:
    sit = result.get("situation_understanding_candidate") or {}
    return (sit.get("scene_profile_candidate") or {}).get("scene_type", "")


def _tools(result: Dict[str, Any]) -> List[str]:
    plan = result.get("agent_plan_candidate") or {}
    return [t.get("capability_type", "") for t in plan.get("tool_plan_candidates", [])]


def integration_case_a_unknown_scene() -> Dict[str, Any]:
    """Case A: unknown_scene — real pipeline, accepted_as_evidence, L1 unchanged."""
    case_id = "case_a_unknown_scene_real_evidence"
    result = run_qwen_vl_real_provider_integration(
        fixture_job_unknown_scene(),
        recorded_fixture_id="unknown_scene_hypothesis",
        case_id=case_id,
    )
    review = result.get("teacher_validation_review") or {}
    raw = result.get("raw_teacher_response") or {}
    evidence = result.get("teacher_evidence_candidate") or {}
    passed = (
        result.get("raw_separated_from_evidence") is True
        and raw is not None
        and evidence is not None
        and raw is not evidence
        and review.get("teacher_validation_status") == "accepted_as_evidence"
        and _scene(result) == "unknown_scene"
        and review.get("l1_scene_unchanged") is True
        and result.get("teacher_admission", {}).get("should_request_teacher") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def integration_case_b_shopfront_noop() -> Dict[str, Any]:
    """Case B: shopfront + OCR — teacher_usage_policy noop, no Qwen call."""
    case_id = "case_b_shopfront_teacher_noop"
    result = run_qwen_vl_real_provider_integration(
        fixture_job_564f1aa93983_shop_sign(),
        case_id=case_id,
    )
    admission = result.get("teacher_admission") or {}
    passed = (
        admission.get("admission_status") == "noop"
        and admission.get("should_request_teacher") is False
        and "sufficient" in (admission.get("noop_reason") or "").lower()
        and result.get("raw_teacher_response") is None
        and result.get("teacher_evidence_candidate") is None
        and "ocr" in _tools(result)
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def integration_case_c_slam_rejected() -> Dict[str, Any]:
    """Case C: Qwen SLAM for text — rejected_by_policy."""
    case_id = "case_c_slam_suggestion_rejected"
    result = run_qwen_vl_real_provider_integration(
        fixture_job_564f1aa93983_shop_sign(),
        recorded_fixture_id="slam_for_text",
        admission_hints={"force_admission": True},
        case_id=case_id,
    )
    review = result.get("teacher_validation_review") or {}
    passed = (
        result.get("raw_separated_from_evidence") is True
        and review.get("teacher_validation_status") == "rejected_by_policy"
        and any(c.get("conflict_type") == "tool_mismatch" for c in (review.get("conflict_candidates") or []))
        and review.get("selected_plan_unchanged") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def integration_case_d_unsupported_claim() -> Dict[str, Any]:
    """Case D: Starbucks claim without OCR — unsupported_claim reject."""
    case_id = "case_d_unsupported_claim_rejected"
    result = run_qwen_vl_real_provider_integration(
        fixture_job_564f1aa93983_shop_sign(),
        recorded_fixture_id="unsupported_brand_claim",
        admission_hints={"force_admission": True},
        case_id=case_id,
    )
    review = result.get("teacher_validation_review") or {}
    passed = (
        result.get("raw_separated_from_evidence") is True
        and review.get("teacher_validation_status") == "rejected_by_policy"
        and any(c.get("conflict_type") == "unsupported_claim" for c in (review.get("conflict_candidates") or []))
        and review.get("no_fact_write") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def run_all_integration_cases() -> Dict[str, Any]:
    reset_teacher_usage_metrics()
    runners = [
        integration_case_a_unknown_scene,
        integration_case_b_shopfront_noop,
        integration_case_c_slam_rejected,
        integration_case_d_unsupported_claim,
    ]
    cases = [fn() for fn in runners]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    metrics = cases[-1].get("result", {}).get("teacher_usage_metrics") if cases else {}
    return {
        "phase_id": "Phase-P1-Midplatform-Single-Teacher-QwenVL-Real-Provider-Integration-v1-001",
        "provider": "qwen_vl",
        "integration_case_ids": list(INTEGRATION_CASE_IDS),
        "integration_cases": cases,
        "integration_cases_passed": sum(1 for c in cases if c.get("passed")),
        "integration_case_count": len(cases),
        "failed_checks": failed,
        "teacher_usage_metrics": metrics,
        "raw_response_separated": all(
            (c.get("result") or {}).get("raw_separated_from_evidence") is not False
            or (c.get("result") or {}).get("teacher_admission", {}).get("admission_status") == "noop"
            for c in cases
        ),
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
