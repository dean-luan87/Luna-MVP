# -*- coding: utf-8
"""Luna Decision Validation Layer — deterministic processor v1 (planning only)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set, Tuple
from uuid import uuid4

from capabilities.midplatform.decision_validation.luna_decision_validation_types_v1 import (
    POLICY_REF,
    VALIDATION_SOURCE_TYPES,
)

BLANKET_TOOL_THRESHOLD = 4
TEXT_GOALS = frozenset({"read_text", "identify_place", "find_direction"})
SPATIAL_TOOLS = frozenset({"slam", "depth", "tracking", "detection"})
TEXT_TOOLS = frozenset({"ocr"})


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _plan(input_data: Dict[str, Any]) -> Dict[str, Any]:
    return input_data.get("agent_plan_candidate") or {}


def _situation(input_data: Dict[str, Any]) -> Dict[str, Any]:
    return input_data.get("situation_understanding_candidate") or {}


def _scene(situation: Dict[str, Any]) -> str:
    return (situation.get("scene_profile_candidate") or {}).get("scene_type", "unknown_scene")


def _goal_type(plan: Dict[str, Any]) -> str:
    return (plan.get("plan_goal_candidate") or {}).get("goal_type", "unknown")


def _strategy_type(plan: Dict[str, Any]) -> str:
    return (plan.get("plan_strategy") or {}).get("strategy_type", "unknown")


def _active_tools(plan: Dict[str, Any]) -> List[str]:
    return [t.get("capability_type", "") for t in plan.get("tool_plan_candidates", [])]


def _noop_tools(plan: Dict[str, Any]) -> List[str]:
    return [t.get("capability_type", "") for t in plan.get("noop_tool_plan_candidates", [])]


def _missing_types(situation: Dict[str, Any]) -> List[str]:
    return [m.get("info_type", "") for m in situation.get("missing_information_candidates", [])]


def _task_types(situation: Dict[str, Any]) -> List[str]:
    return [t.get("task_type", "") for t in situation.get("task_clue_candidates", [])]


def _user_goal(input_data: Dict[str, Any]) -> Dict[str, Any]:
    ug = input_data.get("user_goal_candidate_optional")
    if ug:
        return ug
    return (input_data.get("agent_plan_candidate") or {}).get("user_goal_candidate") or {}


def _reason(code: str, text: str, polarity: str = "positive") -> Dict[str, Any]:
    return {
        "reason_code": code,
        "reason_text": text,
        "polarity": polarity,
        "candidate_only": True,
        "not_fact": True,
    }


def validate_plan_alignment(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Check plan alignment with L1 Situation."""
    plan = _plan(input_data)
    situation = _situation(input_data)
    scene = _scene(situation)
    goal = _goal_type(plan)
    tools = set(_active_tools(plan))
    missing = set(_missing_types(situation))
    tasks = set(_task_types(situation))
    reasons: List[Dict[str, Any]] = []
    score = 0.5
    aligned = True

    if scene == "shopfront_sign" and goal in TEXT_GOALS:
        if "ocr" in tools:
            score += 0.25
            reasons.append(_reason("text_objective_matches_ocr", "Situation indicates text objective; OCR matches missing information"))
        if "slam" in _noop_tools(plan) and "tracking" in _noop_tools(plan):
            reasons.append(_reason("spatial_noop_correct", "SLAM/Tracking unnecessary for text gathering"))
            score += 0.1

    if scene == "street_crossing" and goal in ("assess_walkable", "navigate"):
        if tools & SPATIAL_TOOLS:
            score += 0.3
            reasons.append(_reason("risk_plan_matches_scene", "Street crossing plan aligns with spatial risk assessment"))
        if "ocr" in _noop_tools(plan) or "ocr" not in tools:
            reasons.append(_reason("no_full_image_ocr", "No inappropriate full-image OCR for street crossing"))

    if scene == "unknown_scene":
        aligned = len(tools) <= 1
        if not aligned:
            reasons.append(_reason("unknown_scene_misaligned", "Plan does not align with unknown_scene uncertainty", "negative"))
            score -= 0.4

    if missing and goal in TEXT_GOALS and "text_content" in missing and "ocr" in tools:
        score += 0.15
        reasons.append(_reason("addresses_text_gap", "Plan addresses text_content missing information"))

    if tasks and goal == "unknown":
        aligned = False
        reasons.append(_reason("goal_unknown_with_tasks", "Plan goal unclear despite task clues", "warning"))

    score = max(0.0, min(1.0, score))
    return {
        "aligned": aligned and score >= 0.55,
        "plan_alignment_score_candidate": round(score, 2),
        "reasons": reasons,
        "candidate_only": True,
        "not_fact": True,
    }


def validate_policy_conflict(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Check Constitution / policy conflicts."""
    plan = _plan(input_data)
    situation = _situation(input_data)
    scene = _scene(situation)
    goal = _goal_type(plan)
    tools = set(_active_tools(plan))
    policy = input_data.get("policy_context") or {}
    conflicts: List[str] = []
    reasons: List[Dict[str, Any]] = []

    hard = set(policy.get("hard_constraints") or [])
    if "no_fact_write" not in hard and policy.get("constitution_refs"):
        conflicts.append("missing_no_fact_write_constraint")

    # Case E: OCR/text goal but SLAM active
    if goal in TEXT_GOALS and "slam" in tools and scene == "shopfront_sign":
        conflicts.append("text_goal_slam_tool_conflict")
        reasons.append(_reason("policy_conflict_slam_for_text", "OCR/text task with SLAM tool violates text_goal_no_slam_tool", "negative"))

    # Case B dryrun: shopfront text objective with SLAM mapping plan
    tasks = set(_task_types(situation))
    missing = set(_missing_types(situation))
    if scene == "shopfront_sign" and "slam" in tools and "ocr" not in tools:
        if tasks & {"read_text", "identify_place"} or missing & {"text_content", "place_identity"}:
            conflicts.append("text_objective_slam_mapping_conflict")
            reasons.append(_reason(
                "policy_conflict_slam_mapping",
                "Text objective does not require spatial mapping (SLAM)",
                "negative",
            ))

    # Case D: blanket activation
    if len(tools) >= BLANKET_TOOL_THRESHOLD:
        conflicts.append("blanket_tool_activation")
        reasons.append(_reason("blanket_activation_blocked", "Blanket activation of all models violates no_blanket_activation", "negative"))

    if scene == "unknown_scene" and len(tools) >= 3:
        conflicts.append("unknown_scene_blanket_activation")
        reasons.append(_reason("unknown_blanket_blocked", "unknown_scene must not blanket activate perception tools", "negative"))

    constitution_refs = policy.get("constitution_refs") or []
    if "L0" in constitution_refs and "no_runner_invocation" in hard:
        if plan.get("runner_invoked"):
            conflicts.append("constitution_runner_violation")
            reasons.append(_reason("constitution_blocked", "Constitution violation: runner invocation detected", "negative"))

    return {
        "has_conflict": bool(conflicts),
        "policy_conflict_detected": conflicts,
        "reasons": reasons,
        "candidate_only": True,
        "not_fact": True,
    }


def validate_missing_information(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Check whether plan addresses current information gaps."""
    plan = _plan(input_data)
    situation = _situation(input_data)
    goal = _goal_type(plan)
    tools = set(_active_tools(plan))
    missing = _missing_types(situation)
    detected: List[str] = []
    reasons: List[Dict[str, Any]] = []
    sufficient = True

    mapping = {
        "text_content": "ocr",
        "place_identity": "ocr",
        "direction_info": "ocr",
        "walkable_area": "depth",
        "dynamic_motion": "tracking",
        "spatial_continuity": "slam",
    }
    for info in missing:
        suggested = mapping.get(info)
        if suggested and suggested not in tools and goal not in ("ask_user", "manual_review"):
            detected.append(info)
            sufficient = False
        elif suggested and suggested in tools:
            reasons.append(_reason(f"addresses_{info}", f"Plan tool addresses missing {info}"))

    if not missing:
        reasons.append(_reason("no_missing_info", "No critical missing information detected", "neutral"))

    return {
        "sufficient": sufficient,
        "missing_information_detected": detected,
        "reasons": reasons,
        "candidate_only": True,
        "not_fact": True,
    }


def validate_tool_selection(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate active tools and noop discipline."""
    plan = _plan(input_data)
    situation = _situation(input_data)
    scene = _scene(situation)
    goal = _goal_type(plan)
    tools = set(_active_tools(plan))
    noops = set(_noop_tools(plan))
    hints = situation.get("model_need_hints") or {}
    not_needed = {h.get("capability_type") for h in hints.get("not_needed", [])}
    reasons: List[Dict[str, Any]] = []
    valid = True

    wrongly_active = tools & not_needed
    if wrongly_active:
        valid = False
        reasons.append(_reason("noop_violation", f"Active tools conflict with L1 not_needed: {sorted(wrongly_active)}", "negative"))

    if scene == "shopfront_sign" and goal in TEXT_GOALS:
        if "slam" in noops and "tracking" in noops and "depth" in noops:
            reasons.append(_reason("noop_discipline_ok", "SLAM/Tracking/Depth correctly noop for text plan"))

    if scene == "street_crossing":
        if "detection" in tools and "depth" in tools:
            reasons.append(_reason("risk_tools_selected", "Detection + Depth appropriate for crossing safety"))

    return {
        "valid": valid,
        "reasons": reasons,
        "candidate_only": True,
        "not_fact": True,
    }


def _user_goal_conflict(input_data: Dict[str, Any]) -> Tuple[bool, List[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """Case B: user navigate goal vs OCR-default plan."""
    plan = _plan(input_data)
    user_goal = _user_goal(input_data)
    ug_type = user_goal.get("goal_type", "unknown")
    ug_text = (user_goal.get("goal_text_optional") or "").lower()
    plan_goal = _goal_type(plan)
    alternatives: List[Dict[str, Any]] = []
    reasons: List[Dict[str, Any]] = []

    navigate_like = (
        ug_type == "navigate"
        or "entrance" in ug_text
        or "navigate" in ug_text
        or "入口" in ug_text
    )
    ocr_plan = plan_goal in TEXT_GOALS and set(_active_tools(plan)) <= {"ocr", "vlm"}

    if navigate_like and ocr_plan and _scene(_situation(input_data)) == "shopfront_sign":
        reasons.append(_reason("user_goal_plan_mismatch", "User goal find entrance conflicts with OCR-first plan", "warning"))
        alt = {
            "plan_goal_type": "navigate",
            "strategy_type": "navigation_support",
            "tools_suggested": ["detection", "depth"],
            "suggested_summary": "navigation candidate — confirm entrance before reading sign",
            "does_not_override_selected_plan": True,
            "source": "validation_layer",
            "candidate_only": True,
            "not_fact": True,
        }
        alternatives.append(alt)
        return True, reasons, alt
    return False, reasons, None


def _risk_level(input_data: Dict[str, Any], alignment: Dict[str, Any]) -> str:
    scene = _scene(_situation(input_data))
    goal = _goal_type(_plan(input_data))
    tools = set(_active_tools(_plan(input_data)))
    if scene == "street_crossing" and goal == "navigate":
        return "high"
    if scene == "street_crossing" or goal == "assess_walkable":
        return "medium"
    if scene == "unknown_scene":
        return "high"
    if alignment.get("plan_alignment_score_candidate", 0) < 0.5:
        return "high"
    return "low"


def _high_risk_crossing_needs_review(input_data: Dict[str, Any]) -> bool:
    """Case E: street_crossing + cross road plan requires review."""
    scene = _scene(_situation(input_data))
    goal = _goal_type(_plan(input_data))
    strategy = _strategy_type(_plan(input_data))
    if scene != "street_crossing":
        return False
    if goal == "navigate" or strategy == "navigation_support":
        return True
    plan_steps = _plan(input_data).get("plan_steps") or []
    for s in plan_steps:
        sg = (s.get("step_goal") or "").lower()
        if "cross" in sg or "road" in sg:
            return True
    return False


def build_validation_candidate(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Build unified decision_validation_candidate."""
    plan = _plan(input_data)
    situation = _situation(input_data)
    plan_id = plan.get("plan_id", "unknown_plan")

    alignment = validate_plan_alignment(input_data)
    policy = validate_policy_conflict(input_data)
    missing = validate_missing_information(input_data)
    tools = validate_tool_selection(input_data)
    user_conflict, user_reasons, user_alt = _user_goal_conflict(input_data)

    all_reasons: List[Dict[str, Any]] = (
        alignment.get("reasons", [])
        + policy.get("reasons", [])
        + missing.get("reasons", [])
        + tools.get("reasons", [])
        + user_reasons
    )

    contradictions: List[Dict[str, Any]] = []
    if user_conflict:
        contradictions.append({
            "type": "user_goal_vs_plan_goal",
            "plan_goal": _goal_type(plan),
            "user_goal": _user_goal(input_data).get("goal_type"),
            "candidate_only": True,
            "not_fact": True,
        })

    risk = _risk_level(input_data, alignment)
    status = "validated_candidate"
    alternative_plans: List[Dict[str, Any]] = []
    high_risk_crossing = _high_risk_crossing_needs_review(input_data)

    if policy.get("has_conflict"):
        status = "blocked_candidate"
    elif user_conflict:
        status = "needs_review"
        if user_alt:
            alternative_plans.append(user_alt)
    elif high_risk_crossing:
        status = "needs_review"
        risk = "high"
        all_reasons.append(_reason(
            "high_risk_crossing_review",
            "Street crossing plan requires additional evidence before Tool OS handoff",
            "warning",
        ))
    elif not alignment.get("aligned") or not tools.get("valid"):
        status = "needs_review"
    elif missing.get("missing_information_detected") and _scene(situation) != "unknown_scene":
        status = "insufficient_information"
    elif risk == "high" and _scene(situation) == "unknown_scene":
        status = "blocked_candidate"

    should_handoff = status == "validated_candidate"
    required_checks = ["permission check", "resource check", "runner admission"]
    if status == "needs_review":
        required_checks.append("human_review_optional")
        if high_risk_crossing:
            required_checks.append("additional_evidence_required")
    if status in ("blocked_candidate", "insufficient_information"):
        required_checks.append("resolve_validation_before_handoff")

    vid = _uid("dvc")
    trace_refs = [
        {"stage": "situation", "ref": situation.get("situation_id", _scene(situation))},
        {"stage": "agent_plan", "ref": plan_id},
        {"stage": "policy", "ref": POLICY_REF},
        {"stage": "validation", "ref": vid},
    ]
    case_refs = input_data.get("case_library_candidates") or []
    if case_refs:
        trace_refs.append({"stage": "case_library", "ref": str(case_refs[0].get("case_ref", "none"))})

    return {
        "validation_id": vid,
        "validation_status_candidate": status,
        "validation_result": {
            "plan_alignment_score_candidate": alignment.get("plan_alignment_score_candidate", 0.5),
            "risk_level_candidate": risk,
            "missing_information_detected": missing.get("missing_information_detected", []),
            "policy_conflict_detected": policy.get("policy_conflict_detected", []),
            "contradiction_candidates": contradictions,
            "candidate_only": True,
            "not_fact": True,
        },
        "validation_reason_candidates": all_reasons,
        "tool_execution_readiness_candidate": {
            "should_handoff_to_tool_os": should_handoff,
            "required_checks": required_checks,
            "admission_required": True,
            "candidate_only": True,
            "not_fact": True,
            "not_execution_permission": True,
        },
        "alternative_plan_candidates": alternative_plans,
        "validation_sources_used": list(VALIDATION_SOURCE_TYPES[:3]),
        "validation_sources_future_ready": list(VALIDATION_SOURCE_TYPES[3:]),
        "single_teacher_validator_future_ready": True,
        "multi_teacher_validator_future_ready": True,
        "tool_os_before_execution": True,
        "no_plan_override": True,
        "no_plan_ownership": True,
        "no_tool_execution": True,
        "no_runner_invocation": True,
        "no_fact_write": True,
        "candidate_only": True,
        "not_fact": True,
        "planning_only": True,
        "trace_refs": trace_refs,
        "policy_refs": [POLICY_REF],
    }


def validate_decision(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Public entry — wraps input envelope + validation candidate."""
    return {
        "input_candidate_id": _uid("dvi"),
        "decision_validation_input_candidate": {
            "agent_plan_candidate": _plan(input_data),
            "situation_understanding_candidate": _situation(input_data),
            "policy_context": input_data.get("policy_context", {}),
            "case_library_candidates": input_data.get("case_library_candidates", []),
            "user_goal_candidate_optional": input_data.get("user_goal_candidate_optional"),
            "candidate_only": True,
            "not_fact": True,
        },
        "decision_validation_candidate": build_validation_candidate(input_data),
        "candidate_only": True,
        "not_fact": True,
        "planning_only": True,
        "no_network": True,
        "no_tool_execution": True,
    }
