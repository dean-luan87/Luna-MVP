# -*- coding: utf-8
"""Luna Decision Validation Layer — planning smoke v1."""

from __future__ import annotations

from typing import Any, Dict, List

from capabilities.midplatform.decision_validation.luna_decision_validation_processor_v1 import (
    validate_decision,
)
from capabilities.midplatform.decision_validation.luna_decision_validation_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    SMOKE_CASE_IDS,
)

FINAL_SMOKE_GO = FINAL_GO.replace("_GO", "_SMOKE_GO") if FINAL_GO.endswith("_GO") else FINAL_GO + "_SMOKE_GO"
FINAL_SMOKE_BLOCKED = FINAL_BLOCKED.replace("_BLOCKED", "_SMOKE_BLOCKED")


def _policy() -> Dict[str, Any]:
    return {
        "constitution_refs": ["L0"],
        "governance_refs": ["decision_validation_policy_v1"],
        "safety_constraints": ["no_fact_write", "no_runner_invocation"],
        "protocol_refs": [],
        "hard_constraints": ["no_fact_write", "no_runner_invocation"],
    }


def _situation(
    scene: str,
    *,
    tasks: List[Dict[str, Any]] | None = None,
    missing: List[Dict[str, Any]] | None = None,
    not_needed: List[str] | None = None,
) -> Dict[str, Any]:
    return {
        "situation_id": f"sit_{scene}",
        "scene_profile_candidate": {
            "scene_type": scene,
            "confidence": 0.35 if scene == "unknown_scene" else 0.85,
            "owned_by": "situation_understanding_layer",
            "candidate_only": True,
            "not_fact": True,
        },
        "task_clue_candidates": tasks or [],
        "missing_information_candidates": missing or [],
        "model_need_hints": {
            "likely_needed": [],
            "optional": [],
            "not_needed": [
                {"capability_type": c, "candidate_only": True} for c in (not_needed or [])
            ],
        },
        "uncertainty": {
            "needs_manual_review": scene == "unknown_scene",
            "needs_user_goal": scene == "unknown_scene",
        },
        "candidate_only": True,
        "not_fact": True,
    }


def _task(task_type: str, priority: str = "P0") -> Dict[str, Any]:
    return {"task_type": task_type, "priority": priority, "candidate_only": True, "not_fact": True}


def _missing(info_type: str, cap: str = "ocr") -> Dict[str, Any]:
    return {
        "info_type": info_type,
        "required_for": info_type,
        "suggested_capability": cap,
        "candidate_only": True,
        "not_fact": True,
    }


def _tool(cap: str, purpose: str = "") -> Dict[str, Any]:
    return {
        "capability_type": cap,
        "tool_purpose": purpose or cap,
        "execution_mode": "request_tool_os_admission",
        "candidate_only": True,
        "not_fact": True,
    }


def _noop(cap: str, reason: str = "") -> Dict[str, Any]:
    return {
        "capability_type": cap,
        "noop_reason": reason or f"{cap} not needed",
        "policy_ref": "decision_validation_policy_v1",
        "candidate_only": True,
        "not_fact": True,
    }


def _plan(
    goal: str,
    tools: List[str],
    *,
    noops: List[str] | None = None,
    strategy: str = "information_gathering",
    plan_id: str = "plan_smoke",
) -> Dict[str, Any]:
    return {
        "plan_id": plan_id,
        "plan_goal_candidate": {"goal_type": goal, "candidate_only": True, "not_fact": True},
        "plan_strategy": {"strategy_type": strategy, "candidate_only": True, "not_fact": True},
        "plan_steps": [{"step_type": "request_tool", "candidate_only": True}],
        "tool_plan_candidates": [_tool(t) for t in tools],
        "noop_tool_plan_candidates": [_noop(n) for n in (noops or [])],
        "selected_plan_candidate": True,
        "candidate_only": True,
        "not_fact": True,
        "no_runner_invocation": True,
    }


def _input(
    situation: Dict[str, Any],
    plan: Dict[str, Any],
    *,
    user_goal: Dict[str, Any] | None = None,
    case_library: List[Dict[str, Any]] | None = None,
) -> Dict[str, Any]:
    return {
        "agent_plan_candidate": plan,
        "situation_understanding_candidate": situation,
        "policy_context": _policy(),
        "case_library_candidates": case_library or [],
        "user_goal_candidate_optional": user_goal,
        "candidate_only": True,
        "not_fact": True,
    }


def _validation(result: Dict[str, Any]) -> Dict[str, Any]:
    return result.get("decision_validation_candidate") or {}


def smoke_case_a_shopfront_ocr_validated() -> Dict[str, Any]:
    case_id = "case_a_shopfront_ocr_validated"
    sit = _situation(
        "shopfront_sign",
        tasks=[_task("read_text"), _task("identify_place", "P1")],
        missing=[_missing("text_content"), _missing("place_identity")],
        not_needed=["slam", "tracking", "depth"],
    )
    plan = _plan("identify_place", ["ocr"], noops=["slam", "tracking", "depth"])
    result = validate_decision(_input(sit, plan))
    v = _validation(result)
    readiness = v.get("tool_execution_readiness_candidate") or {}
    reasons = [r.get("reason_code") for r in v.get("validation_reason_candidates", [])]
    passed = (
        v.get("validation_status_candidate") == "validated_candidate"
        and readiness.get("should_handoff_to_tool_os") is True
        and "text_objective_matches_ocr" in reasons
        and v.get("no_plan_override") is True
        and v.get("candidate_only") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_b_user_goal_needs_review() -> Dict[str, Any]:
    case_id = "case_b_user_goal_needs_review"
    sit = _situation(
        "shopfront_sign",
        tasks=[_task("read_text")],
        missing=[_missing("text_content")],
    )
    plan = _plan("read_text", ["ocr"], noops=["slam", "tracking", "depth"])
    user_goal = {
        "goal_type": "navigate",
        "goal_text_optional": "find entrance",
        "confidence": 0.9,
        "source": "user_command",
        "candidate_only": True,
        "not_fact": True,
    }
    result = validate_decision(_input(sit, plan, user_goal=user_goal))
    v = _validation(result)
    alts = v.get("alternative_plan_candidates") or []
    passed = (
        v.get("validation_status_candidate") == "needs_review"
        and len(alts) >= 1
        and alts[0].get("plan_goal_type") == "navigate"
        and alts[0].get("does_not_override_selected_plan") is True
        and plan["plan_goal_candidate"]["goal_type"] == "read_text"
        and v.get("no_plan_override") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_c_street_crossing_validated() -> Dict[str, Any]:
    case_id = "case_c_street_crossing_validated"
    sit = _situation(
        "street_crossing",
        tasks=[_task("assess_walkable")],
        missing=[_missing("walkable_area", "depth")],
        not_needed=["ocr"],
    )
    plan = _plan(
        "assess_walkable",
        ["detection", "depth"],
        noops=["ocr"],
        strategy="risk_assessment",
    )
    result = validate_decision(_input(sit, plan))
    v = _validation(result)
    passed = (
        v.get("validation_status_candidate") == "validated_candidate"
        and v.get("validation_result", {}).get("risk_level_candidate") == "medium"
        and v.get("no_tool_execution") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_d_unknown_blanket_blocked() -> Dict[str, Any]:
    case_id = "case_d_unknown_blanket_blocked"
    sit = _situation("unknown_scene", missing=[_missing("scene_identity", "vlm")])
    plan = _plan(
        "understand_environment",
        ["ocr", "slam", "detection", "depth", "tracking"],
        strategy="environment_understanding",
        plan_id="plan_blanket",
    )
    result = validate_decision(_input(sit, plan))
    v = _validation(result)
    conflicts = v.get("validation_result", {}).get("policy_conflict_detected") or []
    passed = (
        v.get("validation_status_candidate") == "blocked_candidate"
        and ("blanket_tool_activation" in conflicts or "unknown_scene_blanket_activation" in conflicts)
        and (v.get("tool_execution_readiness_candidate") or {}).get("should_handoff_to_tool_os") is False
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_e_slam_for_text_blocked() -> Dict[str, Any]:
    case_id = "case_e_slam_for_text_blocked"
    sit = _situation(
        "shopfront_sign",
        tasks=[_task("read_text")],
        missing=[_missing("text_content")],
    )
    plan = _plan("read_text", ["slam"], plan_id="plan_bad_slam")
    result = validate_decision(_input(sit, plan))
    v = _validation(result)
    conflicts = v.get("validation_result", {}).get("policy_conflict_detected") or []
    passed = (
        v.get("validation_status_candidate") == "blocked_candidate"
        and "text_goal_slam_tool_conflict" in conflicts
        and v.get("no_plan_override") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def run_smoke_cases() -> Dict[str, Any]:
    runners = [
        smoke_case_a_shopfront_ocr_validated,
        smoke_case_b_user_goal_needs_review,
        smoke_case_c_street_crossing_validated,
        smoke_case_d_unknown_blanket_blocked,
        smoke_case_e_slam_for_text_blocked,
    ]
    cases = [fn() for fn in runners]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Decision-Validation-Layer-Planning-v1-001",
        "planning_only": True,
        "deterministic_smoke_only": True,
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "smoke_case_count": len(cases),
        "failed_checks": failed,
        "final_decision": FINAL_SMOKE_GO if not failed else FINAL_SMOKE_BLOCKED,
    }
