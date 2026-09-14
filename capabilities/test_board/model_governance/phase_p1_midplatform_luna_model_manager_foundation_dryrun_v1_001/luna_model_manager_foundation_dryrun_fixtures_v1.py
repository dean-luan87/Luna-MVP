# -*- coding: utf-8 -*-
"""Luna Model Manager Foundation — dry-run fixtures & cases v1."""

from __future__ import annotations

from typing import Any, Dict, List

from capabilities.midplatform.model_manager.model_manager_dryrun.luna_model_manager_dryrun_adapter_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    run_model_manager_dryrun,
)
from capabilities.test_board.model_governance.phase_p1_midplatform_luna_agent_planning_layer_dryrun_v1_001.luna_agent_planning_layer_dryrun_fixtures_v1 import (
    fixture_job_564f1aa93983_shop_sign,
)
from capabilities.test_board.model_governance.phase_p1_midplatform_single_teacher_qwen_vl_integration_dryrun_v1_001.luna_qwen_vl_integration_dryrun_fixtures_v1 import (
    fixture_job_unknown_scene,
)

DRYRUN_CASE_IDS = (
    "case_a_shopfront_ocr_routing",
    "case_b_unknown_scene_qwen_handoff",
    "case_c_reliability_priority_routing",
    "case_d_ocr_unavailable_fallback",
    "case_e_gemini_admission_gate",
)


def _scores(result: Dict[str, Any]) -> Dict[str, float]:
    routing = result.get("routing_score_result") or {}
    return {s["model_id"]: s["routing_score"] for s in routing.get("provider_scores", [])}


def _selection(result: Dict[str, Any]) -> Dict[str, Any]:
    return result.get("provider_selection_candidate") or {}


def _capability(result: Dict[str, Any]) -> str:
    return (result.get("capability_match_candidate") or {}).get("required_capability", "")


def dryrun_case_a_shopfront_ocr() -> Dict[str, Any]:
    """Case A: shopfront → text_recognition → OCR 0.95 > Qwen 0.4, SLAM noop."""
    case_id = "case_a_shopfront_ocr_routing"
    result = run_model_manager_dryrun(
        fixture_job_564f1aa93983_shop_sign(),
        score_profile="shopfront_ocr",
    )
    sel = _selection(result)
    scores = _scores(result)
    noop_ids = {p.get("model_id") for p in (sel.get("noop_providers") or [])}
    passed = (
        _capability(result) == "text_recognition"
        and sel.get("selected_tool_id") == "ocr_v1"
        and scores.get("ocr_v1", 0) >= 0.9
        and scores.get("qwen_vl", 0) < scores.get("ocr_v1", 1)
        and scores.get("slam_v1", -1) == 0.0
        and sel.get("should_request_teacher") is False
        and "slam_v1" in noop_ids or scores.get("slam_v1") == 0.0
        and result.get("model_manager_no_decision_assertion", {}).get("passed") is True
        and result.get("no_model_execution_assertion") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_b_unknown_scene_qwen() -> Dict[str, Any]:
    """Case B: unknown_scene → Qwen 0.85, handoff Teacher Adapter."""
    case_id = "case_b_unknown_scene_qwen_handoff"
    result = run_model_manager_dryrun(
        fixture_job_unknown_scene(),
        score_profile="unknown_scene_multi",
    )
    sel = _selection(result)
    scores = _scores(result)
    teacher_handoff = result.get("teacher_adapter_handoff_candidate") or {}
    passed = (
        _capability(result) == "unknown_scene_reasoning"
        and sel.get("selected_model_id") == "qwen_vl"
        and scores.get("qwen_vl", 0) >= 0.8
        and scores.get("gemini_vision", 0) > 0.7
        and sel.get("should_request_teacher") is True
        and teacher_handoff.get("should_handoff") is True
        and teacher_handoff.get("target") == "teacher_adapter"
        and teacher_handoff.get("not_executed") is True
        and result.get("model_manager_not_tool_os_assertion", {}).get("passed") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_c_reliability_priority() -> Dict[str, Any]:
    """Case C: Gemini faster but Qwen more reliable → reliability_priority."""
    case_id = "case_c_reliability_priority_routing"
    result = run_model_manager_dryrun(
        fixture_job_unknown_scene(),
        score_profile="reliability_priority",
        scoring_mode="reliability_priority",
    )
    sel = _selection(result)
    routing = result.get("routing_score_result") or {}
    passed = (
        sel.get("selected_model_id") == "qwen_vl"
        and routing.get("routing_reason") == "reliability_priority"
        and sel.get("routing_reason") == "reliability_priority"
        and result.get("no_auto_policy_update_assertion") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_d_ocr_unavailable() -> Dict[str, Any]:
    """Case D: OCR unavailable → capability_missing + fallback to L2, no silent Qwen fallback."""
    case_id = "case_d_ocr_unavailable_fallback"
    result = run_model_manager_dryrun(
        fixture_job_564f1aa93983_shop_sign(),
        score_profile="shopfront_ocr",
        unavailable_providers=["ocr_v1"],
    )
    sel = _selection(result)
    missing = result.get("capability_missing_candidate") or {}
    fallback = result.get("fallback_plan_candidate") or {}
    passed = (
        missing.get("capability_missing_candidate") is True
        and missing.get("no_silent_model_fallback") is True
        and missing.get("return_to_l2_agent_planning") is True
        and fallback.get("fallback_plan_candidate") is True
        and fallback.get("owned_by") == "L2_Agent_Planning"
        and sel.get("selected_model_id") != "qwen_vl"
        and sel.get("should_request_teacher") is False
        and sel.get("routing_reason") == "provider_unavailable_no_silent_fallback"
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_e_gemini_admission() -> Dict[str, Any]:
    """Case E: Gemini candidate without admission → not in routing pool."""
    case_id = "case_e_gemini_admission_gate"
    not_admitted = run_model_manager_dryrun(
        fixture_job_unknown_scene(),
        score_profile="unknown_scene_multi",
        admitted_only=True,
        admission_model_id="gemini_vision",
        force_admitted=False,
    )
    admission = not_admitted.get("admission_pipeline") or {}
    adm = admission.get("admission") or {}
    scores_not_admitted = _scores(not_admitted)
    passed_not_admitted = (
        adm.get("admission_status") == "candidate"
        and adm.get("no_auto_admission") is True
        and admission.get("routing_eligible") is False
        and "gemini_vision" not in scores_not_admitted
    )

    admitted = run_model_manager_dryrun(
        fixture_job_unknown_scene(),
        score_profile="unknown_scene_multi",
        admitted_only=True,
        admission_model_id="gemini_vision",
        force_admitted=True,
    )
    admission_ok = admitted.get("admission_pipeline") or {}
    passed_admitted = admission_ok.get("routing_eligible") is True

    passed = passed_not_admitted and passed_admitted
    return {
        "case_id": case_id,
        "passed": passed,
        "result": {"not_admitted": not_admitted, "admitted": admitted},
    }


def run_all_dryrun_cases() -> Dict[str, Any]:
    runners = [
        dryrun_case_a_shopfront_ocr,
        dryrun_case_b_unknown_scene_qwen,
        dryrun_case_c_reliability_priority,
        dryrun_case_d_ocr_unavailable,
        dryrun_case_e_gemini_admission,
    ]
    cases = [fn() for fn in runners]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Foundation-DryRun-v1-001",
        "dryrun_only": True,
        "dryrun_case_ids": list(DRYRUN_CASE_IDS),
        "dryrun_cases": cases,
        "dryrun_passed": sum(1 for c in cases if c.get("passed")),
        "dryrun_case_count": len(cases),
        "failed_checks": failed,
        "unified_manager": True,
        "capability_scheduling_center": True,
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
