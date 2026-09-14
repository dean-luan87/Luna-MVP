# -*- coding: utf-8 -*-
"""Qwen-VL Teacher Admission — Luna controls when to ask Teacher."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.midplatform.teacher_adapter.providers.qwen_vl.qwen_vl_teacher_types_v1 import (
    PARENT_POLICY_REF,
    POLICY_REF,
    PROVIDER_ID,
    TEACHER_ROLE,
)

USAGE_POLICY_REF = "teacher_usage_policy_v1"
DRYRUN_POLICY_REF = "qwen_vl_integration_dryrun_policy_v1"


def _repo_root() -> Path:
    for base in (Path.cwd(), Path(__file__).resolve().parents[5]):
        if (base / "capabilities/test_board/test_board_protocol_v1.py").is_file():
            return base
    return Path(__file__).resolve().parents[5]


def _load_usage_policy() -> Dict[str, Any]:
    path = (
        _repo_root()
        / "capabilities/midplatform/teacher_adapter/providers/qwen_vl/governance/teacher_usage_policy_v1.json"
    )
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _scene(situation: Dict[str, Any]) -> str:
    return (situation.get("scene_profile_candidate") or {}).get("scene_type", "unknown_scene")


def _plan_goal(plan: Dict[str, Any]) -> str:
    return (plan.get("plan_goal_candidate") or {}).get("goal_type", "unknown")


def _active_tools(plan: Dict[str, Any]) -> List[str]:
    return [t.get("capability_type", "") for t in plan.get("tool_plan_candidates", [])]


def _uncertainty_high(situation: Dict[str, Any], validation: Dict[str, Any]) -> bool:
    unc = situation.get("uncertainty") or {}
    scene_conf = float((situation.get("scene_profile_candidate") or {}).get("confidence") or 1.0)
    val_status = validation.get("validation_status_candidate", "")
    return bool(
        unc.get("needs_manual_review")
        or unc.get("needs_user_goal")
        or scene_conf < 0.5
        or _scene(situation) == "unknown_scene"
        or val_status in ("needs_review", "insufficient_information")
    )


def _is_routine_case(
    situation: Dict[str, Any],
    plan: Dict[str, Any],
    validation: Dict[str, Any],
    policy: Dict[str, Any],
) -> bool:
    criteria = policy.get("routine_case_criteria") or {}
    scene = _scene(situation)
    goal = _plan_goal(plan)
    tools = _active_tools(plan)
    val_status = validation.get("validation_status_candidate", "")
    return (
        scene in criteria.get("scene_types", [])
        and goal in criteria.get("goal_types", [])
        and any(t in tools for t in criteria.get("required_tools", []))
        and val_status == criteria.get("validation_status", "validated_candidate")
    )


def evaluate_qwen_teacher_admission(
    *,
    decision_validation_result: Dict[str, Any],
    teacher_input: Optional[Dict[str, Any]] = None,
    admission_hints: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Luna decides whether to request Qwen-VL Teacher.
    Focus: when NOT to ask (noop) vs when to ask (admitted).
    """
    policy = _load_usage_policy()
    situation = decision_validation_result.get("situation_understanding_candidate") or {}
    plan = decision_validation_result.get("agent_plan_candidate") or {}
    validation = decision_validation_result.get("decision_validation_candidate") or {}
    hints = admission_hints or {}
    routine_criteria = policy.get("routine_case_criteria") or {}

    trace_refs = [{
        "stage": "qwen_teacher_admission",
        "scene": _scene(situation),
        "plan_id": plan.get("plan_id"),
        "validation_status": validation.get("validation_status_candidate"),
    }]

    base = {
        "teacher_role": TEACHER_ROLE,
        "preferred_provider": PROVIDER_ID,
        "provider_id": PROVIDER_ID,
        "candidate_only": True,
        "not_fact": True,
        "policy_refs": [POLICY_REF, USAGE_POLICY_REF, PARENT_POLICY_REF, DRYRUN_POLICY_REF],
        "trace_refs": trace_refs,
    }

    if hints.get("force_admission"):
        return {
            **base,
            "should_request_teacher": True,
            "admission_status": "admitted",
            "admission_reason": hints.get("admission_reason", "force_admission"),
            "noop_reason": "",
            "reject_reason": "",
        }

    if hints.get("policy_conflict"):
        return {
            **base,
            "should_request_teacher": True,
            "admission_status": "admitted",
            "admission_reason": "policy_conflict",
            "noop_reason": "",
            "reject_reason": "",
        }

    if hints.get("plan_challenge_requested"):
        return {
            **base,
            "should_request_teacher": True,
            "admission_status": "admitted",
            "admission_reason": "plan_challenge_requested",
            "noop_reason": "",
            "reject_reason": "",
        }

    if hints.get("high_risk_decision"):
        return {
            **base,
            "should_request_teacher": True,
            "admission_status": "admitted",
            "admission_reason": "high_risk_decision",
            "noop_reason": "",
            "reject_reason": "",
        }

    if _scene(situation) == "unknown_scene" and _uncertainty_high(situation, validation):
        return {
            **base,
            "should_request_teacher": True,
            "admission_status": "admitted",
            "admission_reason": "unknown_scene",
            "noop_reason": "",
            "reject_reason": "",
        }

    if _uncertainty_high(situation, validation) and not _is_routine_case(situation, plan, validation, policy):
        return {
            **base,
            "should_request_teacher": True,
            "admission_status": "admitted",
            "admission_reason": "uncertainty_high",
            "noop_reason": "",
            "reject_reason": "",
        }

    if _is_routine_case(situation, plan, validation, policy):
        noop_reason = routine_criteria.get("noop_reason", "current plan sufficient")
        return {
            **base,
            "should_request_teacher": False,
            "admission_status": "noop",
            "admission_reason": "routine_case",
            "noop_reason": noop_reason,
            "reject_reason": "",
        }

    if "ocr" in _active_tools(plan) and _plan_goal(plan) in ("read_text", "identify_place"):
        return {
            **base,
            "should_request_teacher": False,
            "admission_status": "noop",
            "admission_reason": "already_solved_by_tool",
            "noop_reason": "OCR plan covers text task; Teacher not required",
            "reject_reason": "",
        }

    return {
        **base,
        "should_request_teacher": False,
        "admission_status": "noop",
        "admission_reason": "no_admission_trigger",
        "noop_reason": "no_teacher_admission_trigger_matched",
        "reject_reason": "",
    }
