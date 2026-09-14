# -*- coding: utf-8
"""Third-Party Teacher Adapter — dry-run fixtures & cases v1."""

from __future__ import annotations

from typing import Any, Dict, List

from capabilities.midplatform.teacher_adapter.teacher_adapter_dryrun.luna_teacher_adapter_dryrun_adapter_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    run_teacher_adapter_dryrun,
)
from capabilities.test_board.model_governance.phase_p1_midplatform_luna_agent_planning_layer_dryrun_v1_001.luna_agent_planning_layer_dryrun_fixtures_v1 import (
    fixture_job_564f1aa93983_shop_sign,
)

DRYRUN_CASE_IDS = (
    "case_a_teacher_supports_ocr_plan",
    "case_b_teacher_slam_rejected",
    "case_c_teacher_alternative_keep_plan",
    "case_d_teacher_wrong_scene_rejected",
    "case_e_learning_case_no_training",
)

_FORCE_ADMIT = {
    "admission_status": "admitted",
    "should_request_teacher": True,
}


def _plan_goal(result: Dict[str, Any]) -> str:
    plan = result.get("agent_plan_candidate") or {}
    return (plan.get("plan_goal_candidate") or {}).get("goal_type", "")


def _tools(result: Dict[str, Any]) -> List[str]:
    return (result.get("tool_plan_summary") or {}).get("active", [])


def _plan_override_navigate_entrance() -> Dict[str, Any]:
    return {
        "plan_id": "plan_navigate_entrance",
        "plan_goal_candidate": {
            "goal_type": "navigate",
            "interpreted_goal": "navigate_to_entrance",
            "candidate_only": True,
            "not_fact": True,
        },
        "plan_strategy": {"strategy_type": "navigation_support", "candidate_only": True, "not_fact": True},
        "plan_steps": [{"step_type": "request_tool", "step_goal": "find entrance", "candidate_only": True}],
        "tool_plan_candidates": [
            {"capability_type": "detection", "execution_mode": "request_tool_os_admission", "candidate_only": True},
            {"capability_type": "depth", "execution_mode": "request_tool_os_admission", "candidate_only": True},
        ],
        "noop_tool_plan_candidates": [
            {"capability_type": "ocr", "noop_reason": "navigation first", "candidate_only": True},
        ],
        "handoff_to_tool_os_candidate": {
            "should_handoff": True,
            "runner_admission_required": True,
            "candidate_only": True,
        },
        "selected_plan_candidate": True,
        "candidate_only": True,
        "not_fact": True,
        "no_runner_invocation": True,
    }


def dryrun_case_a_teacher_supports_ocr() -> Dict[str, Any]:
    """Case A: Teacher supports OCR plan — accepted_as_evidence, plan unchanged."""
    case_id = "case_a_teacher_supports_ocr_plan"
    challenge = {
        "force_admission": {**_FORCE_ADMIT, "teacher_role": "planning_teacher"},
        "teacher_role": "planning_teacher",
        "provider_id": "gpt_vision",
        "suggestion_type": "supporting_hint",
        "suggestion_text": "可能需要确认店铺入口位置",
        "supports_plan": True,
        "confidence": 0.72,
        "supporting_evidence": [{"type": "entrance_hint", "candidate_only": True}],
    }
    result = run_teacher_adapter_dryrun(
        fixture_job_564f1aa93983_shop_sign(),
        teacher_challenge_fixture=challenge,
    )
    review = result.get("teacher_validation_review") or {}
    passed = (
        review.get("teacher_validation_status") == "accepted_as_evidence"
        and review.get("selected_plan_unchanged") is True
        and _plan_goal(result) in ("identify_place", "read_text")
        and "ocr" in _tools(result)
        and result.get("teacher_does_not_override_plan_assertion", {}).get("passed") is True
        and result.get("no_tool_execution_assertion") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_b_teacher_slam_rejected() -> Dict[str, Any]:
    """Case B: Teacher suggests SLAM for text — rejected_by_policy."""
    case_id = "case_b_teacher_slam_rejected"
    challenge = {
        "force_admission": {**_FORCE_ADMIT, "teacher_role": "planning_teacher"},
        "teacher_role": "planning_teacher",
        "teacher_suggests": "slam_for_text",
        "suggestion_type": "tool_plan",
        "suggestion_text": "启动 SLAM 建图读取文字",
        "tools_suggested": ["slam"],
        "policy_risk_candidates": ["tool_mismatch"],
    }
    result = run_teacher_adapter_dryrun(
        fixture_job_564f1aa93983_shop_sign(),
        teacher_challenge_fixture=challenge,
    )
    review = result.get("teacher_validation_review") or {}
    passed = (
        review.get("teacher_validation_status") == "rejected_by_policy"
        and review.get("selected_plan_unchanged") is True
        and any(
            c.get("conflict_type") == "tool_mismatch"
            for c in (review.get("conflict_candidates") or [])
        )
        and result.get("no_fact_write_assertion") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_c_teacher_alternative_keep_plan() -> Dict[str, Any]:
    """Case C: Luna navigate vs Teacher OCR alternative — keep_original_plan."""
    case_id = "case_c_teacher_alternative_keep_plan"
    challenge = {
        "force_admission": {**_FORCE_ADMIT, "teacher_role": "planning_teacher"},
        "teacher_role": "planning_teacher",
        "provider_id": "gpt_vision",
        "suggestion_type": "alternative_plan",
        "alternative_plan_goal": "read_text",
        "alternative_strategy": "information_gathering",
        "tools_suggested": ["ocr"],
        "suggestion_text": "先 OCR 店招",
    }
    result = run_teacher_adapter_dryrun(
        fixture_job_564f1aa93983_shop_sign(),
        plan_override=_plan_override_navigate_entrance(),
        teacher_challenge_fixture=challenge,
    )
    review = result.get("teacher_validation_review") or {}
    alt = review.get("alternative_plan_candidate_optional") or {}
    passed = (
        review.get("teacher_validation_status") == "accepted_as_alternative"
        and review.get("keep_original_plan") is True
        and review.get("selected_plan_unchanged") is True
        and _plan_goal(result) == "navigate"
        and alt.get("plan_goal_type") == "read_text"
        and alt.get("does_not_override_selected_plan") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_d_teacher_wrong_scene_rejected() -> Dict[str, Any]:
    """Case D: Teacher wrong scene — rejected, L1 unchanged."""
    case_id = "case_d_teacher_wrong_scene_rejected"
    challenge = {
        "force_admission": {**_FORCE_ADMIT, "teacher_role": "perception_teacher"},
        "teacher_role": "perception_teacher",
        "provider_id": "gemini",
        "suggestion_type": "scene_hypothesis",
        "proposed_scene_type": "indoor_store",
        "scene_hypothesis_candidates": [
            {"scene_type": "indoor_store", "confidence": 0.88, "candidate_only": True, "not_fact": True},
        ],
        "suggestion_text": "这看起来像室内商店",
        "asserts_as_fact": False,
    }
    result = run_teacher_adapter_dryrun(
        fixture_job_564f1aa93983_shop_sign(),
        teacher_challenge_fixture=challenge,
    )
    review = result.get("teacher_validation_review") or {}
    situation = result.get("situation_understanding_candidate") or {}
    l1_scene = (situation.get("scene_profile_candidate") or {}).get("scene_type")
    passed = (
        review.get("teacher_validation_status") == "rejected_by_policy"
        and l1_scene == "shopfront_sign"
        and result.get("teacher_does_not_override_l1_assertion", {}).get("passed") is True
        and any(
            c.get("conflict_type") == "l1_scene_override_attempt"
            for c in (review.get("conflict_candidates") or [])
        )
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def dryrun_case_e_learning_case_no_training() -> Dict[str, Any]:
    """Case E: Learning Teacher → case candidate, no direct training."""
    case_id = "case_e_learning_case_no_training"
    challenge = {
        "task_type": "learning_case",
        "required_output_type": "learning_candidate",
        "teacher_role": "learning_teacher",
        "provider_id": "internvl",
        "suggestion_type": "learning_case",
        "suggestion_text": "teacher case: shopfront_sign read_text pattern",
    }
    result = run_teacher_adapter_dryrun(
        fixture_job_564f1aa93983_shop_sign(),
        teacher_challenge_fixture=challenge,
    )
    review = result.get("teacher_validation_review") or {}
    learning = result.get("learning_case_candidate_optional") or review.get("learning_case_candidate_optional")
    passed = (
        review.get("teacher_validation_status") in ("requires_human_review", "accepted_as_evidence")
        and learning is not None
        and learning.get("review_status") == "pending_policy_review"
        and learning.get("no_direct_training") is True
        and result.get("no_direct_training_assertion") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def run_all_dryrun_cases() -> Dict[str, Any]:
    runners = [
        dryrun_case_a_teacher_supports_ocr,
        dryrun_case_b_teacher_slam_rejected,
        dryrun_case_c_teacher_alternative_keep_plan,
        dryrun_case_d_teacher_wrong_scene_rejected,
        dryrun_case_e_learning_case_no_training,
    ]
    cases = [fn() for fn in runners]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    case_a = next((c for c in cases if c["case_id"] == "case_a_teacher_supports_ocr_plan"), {})
    a_res = case_a.get("result") or {}
    return {
        "phase_id": "Phase-P1-Midplatform-Third-Party-Teacher-Adapter-DryRun-v1-001",
        "deterministic_dryrun_only": True,
        "no_real_api": True,
        "no_teacher_execution": True,
        "dryrun_case_ids": list(DRYRUN_CASE_IDS),
        "dryrun_cases": cases,
        "dryrun_cases_passed": sum(1 for c in cases if c.get("passed")),
        "dryrun_case_count": len(cases),
        "failed_checks": failed,
        "core_validations": {
            "teacher_after_validation": all(
                "teacher_validation_review" in (c.get("result") or {})
                for c in cases
            ),
            "no_plan_override_all": all(
                (c.get("result") or {}).get("teacher_does_not_override_plan_assertion", {}).get("passed")
                for c in cases
            ),
            "no_l1_override_all": all(
                (c.get("result") or {}).get("teacher_does_not_override_l1_assertion", {}).get("passed")
                for c in cases
            ),
        },
        "job_564f1aa93983_teacher_result": {
            "job_id": "job_564f1aa93983",
            "teacher_validation_status": (a_res.get("teacher_validation_review") or {}).get("teacher_validation_status"),
            "plan_goal": _plan_goal(a_res),
            "active_tools": _tools(a_res),
            "selected_plan_unchanged": (a_res.get("teacher_validation_review") or {}).get("selected_plan_unchanged"),
        },
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
