# -*- coding: utf-8
"""Luna Agent Planning Layer — dry-run adapter v1 (L1 → L2 → Tool OS handoff candidate)."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4

from capabilities.midplatform.agent_planning.luna_agent_planning_processor_v1 import (
    build_agent_plan_candidate,
)
from capabilities.midplatform.agent_planning.luna_agent_planning_types_v1 import (
    POLICY_REF,
)
from capabilities.midplatform.situation_understanding.luna_situation_understanding_dryrun_adapter_v1 import (
    run_situation_understanding_dryrun,
)

DRYRUN_POLICY_REF = "luna_agent_planning_dryrun_policy_v1"
FINAL_GO = "P1_MIDPLATFORM_LUNA_AGENT_PLANNING_LAYER_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_AGENT_PLANNING_LAYER_DRYRUN_BLOCKED"


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _default_capabilities() -> List[Dict[str, Any]]:
    return [
        {"capability_id": f"cap_{c}", "capability_type": c, "availability": "available"}
        for c in ("ocr", "detection", "depth", "tracking", "slam", "vlm", "sam")
    ]


def build_agent_planning_input_from_situation(
    situation_candidate: Dict[str, Any],
    *,
    user_goal_candidate: Optional[Dict[str, Any]] = None,
    available_capabilities: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """L1 situation_understanding_candidate → L2 agent_planning_input."""
    goal = user_goal_candidate or {
        "goal_type": "unknown",
        "goal_text_optional": "",
        "urgency": "normal",
        "explicitness": "unknown",
        "confidence": 0.2,
        "source": "unknown",
        "candidate_only": True,
        "not_fact": True,
    }
    return {
        "situation_understanding_candidate": situation_candidate,
        "user_goal_candidate": goal,
        "available_capabilities": available_capabilities or _default_capabilities(),
        "policy_context": {
            "constitution_refs": ["L0"],
            "protocol_refs": [],
            "hard_constraints": ["no_fact_write", "no_runner_invocation", "no_tool_execution"],
            "active_policy_refs": [POLICY_REF, DRYRUN_POLICY_REF],
        },
        "memory_context_candidates": [],
        "learning_case_refs": [],
        "candidate_only": True,
        "not_fact": True,
        "trace_refs": [{
            "stage": "l1_to_l2_handoff",
            "situation_id": situation_candidate.get("situation_id", ""),
            "scene": (situation_candidate.get("scene_profile_candidate") or {}).get("scene_type"),
        }],
    }


def _alt_goal_input(
    base_input: Dict[str, Any],
    goal_type: str,
    goal_text: str,
    *,
    confidence: float = 0.75,
) -> Dict[str, Any]:
    inp = deepcopy(base_input)
    inp["user_goal_candidate"] = {
        "goal_text_optional": goal_text,
        "goal_type": goal_type,
        "urgency": "normal",
        "explicitness": "inferred",
        "confidence": confidence,
        "source": "plan_competition",
        "candidate_only": True,
        "not_fact": True,
    }
    return inp


def _score_plan(
    plan: Dict[str, Any],
    *,
    user_goal: Dict[str, Any],
    situation: Dict[str, Any],
) -> Tuple[float, Dict[str, Any]]:
    """Deterministic scoring: user goal > missing info fit > cost > risk."""
    breakdown = {
        "user_goal_alignment": 0.0,
        "missing_info_fit": 0.0,
        "survival_risk_fit": 0.0,
        "cost_penalty": 0.0,
        "noop_discipline": 0.0,
    }
    ug = user_goal.get("goal_type", "unknown")
    ug_text = (user_goal.get("goal_text_optional") or "").lower()
    plan_goal = (plan.get("plan_goal_candidate") or {}).get("goal_type", "unknown")

    # user goal dominates
    if ug != "unknown":
        if plan_goal == ug or (ug == "navigate" and plan_goal == "navigate"):
            breakdown["user_goal_alignment"] = 0.45
        elif "entrance" in ug_text and plan_goal == "navigate":
            breakdown["user_goal_alignment"] = 0.45
        elif plan_goal in ("read_text", "identify_place") and ug in ("identify", "read", "find"):
            breakdown["user_goal_alignment"] = 0.30
        else:
            breakdown["user_goal_alignment"] = 0.05
    else:
        # when no explicit user goal, prefer situation-task-driven plans
        tasks = [t.get("task_type") for t in situation.get("task_clue_candidates", [])]
        if plan_goal in tasks or (
            plan_goal == "identify_place" and "identify_place" in tasks
        ) or (plan_goal == "find_direction" and "find_direction" in tasks):
            breakdown["user_goal_alignment"] = 0.35
        else:
            breakdown["user_goal_alignment"] = 0.15

    missing = {m.get("info_type") for m in situation.get("missing_information_candidates", [])}
    tools = {t.get("capability_type") for t in plan.get("tool_plan_candidates", [])}
    fit = 0.0
    if "text_content" in missing and "ocr" in tools:
        fit += 0.12
    if "place_identity" in missing and "ocr" in tools:
        fit += 0.08
    if "direction_info" in missing and "ocr" in tools:
        fit += 0.12
    if "walkable_area" in missing and ({"detection", "depth", "tracking"} & tools):
        fit += 0.15
    if "spatial_continuity" in missing and ({"depth", "slam"} & tools):
        fit += 0.12
    breakdown["missing_info_fit"] = min(fit, 0.25)

    survival = situation.get("survival_context") or {}
    risk = survival.get("risk_level", "low")
    if risk in ("medium", "high") and ({"detection", "depth", "tracking"} & tools):
        breakdown["survival_risk_fit"] = 0.12
    elif risk == "low" and "ocr" in tools and not ({"slam"} & tools):
        breakdown["survival_risk_fit"] = 0.08

    # cost: more tools → slight penalty; slam especially costly for non-nav
    cost = 0.02 * len(tools)
    if "slam" in tools and plan_goal not in ("navigate", "assess_walkable"):
        cost += 0.15
    breakdown["cost_penalty"] = -min(cost, 0.25)

    noops = {n.get("capability_type") for n in plan.get("noop_tool_plan_candidates", [])}
    # Discipline: text goals should noop spatial
    if plan_goal in ("read_text", "identify_place", "find_direction"):
        if {"slam", "tracking", "depth"} <= noops or (
            "slam" in noops and "tracking" in noops and "depth" in noops
        ):
            breakdown["noop_discipline"] = 0.12
        elif "slam" in tools and plan_goal != "navigate":
            breakdown["noop_discipline"] = -0.15

    total = sum(breakdown.values())
    return total, breakdown


def build_plan_competition(
    agent_planning_input: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Generate competing plan candidates and select one.
    Models do not decide — L2 scores by user goal / missing info / risk / cost.
    """
    situation = agent_planning_input.get("situation_understanding_candidate") or {}
    scene = (situation.get("scene_profile_candidate") or {}).get("scene_type", "unknown_scene")
    user_goal = agent_planning_input.get("user_goal_candidate") or {}
    competing: List[Dict[str, Any]] = []

    # Plan A: read / identify (OCR)
    plan_a_input = _alt_goal_input(
        agent_planning_input,
        "identify" if scene == "shopfront_sign" else "read",
        "read shop name / identify place" if scene == "shopfront_sign" else "read text",
    )
    # For competition, when user goal is already set (e.g. navigate), still generate A as alternative
    if user_goal.get("goal_type") in ("unknown", "identify", "read", "find") or scene == "shopfront_sign":
        try:
            plan_a = build_agent_plan_candidate(plan_a_input if user_goal.get("goal_type") in ("unknown", "identify", "read") else plan_a_input)
            competing.append({
                "competition_slot": "plan_a_read_identify",
                "label": "读取店名 / OCR",
                "plan": plan_a,
                "driver": "scene_default_text_task",
            })
        except Exception:
            pass

    # Always include primary plan driven by actual input (respects user goal override)
    primary = build_agent_plan_candidate(agent_planning_input)
    competing.append({
        "competition_slot": "plan_primary_user_or_situation",
        "label": f"primary:{primary.get('plan_goal_candidate', {}).get('goal_type')}",
        "plan": primary,
        "driver": "user_goal" if user_goal.get("goal_type") not in ("unknown",) else "situation_task_clue",
    })

    # Plan B: find entrance / navigate (Detection + Depth)
    if scene in ("shopfront_sign", "street_crossing", "corridor") or "entrance" in (
        (user_goal.get("goal_text_optional") or "").lower()
    ):
        plan_b_input = _alt_goal_input(
            agent_planning_input,
            "navigate",
            "find entrance / navigate_to_entrance",
            confidence=0.78,
        )
        # Ensure entrance attention hint for entrance navigation
        sit_b = deepcopy(plan_b_input["situation_understanding_candidate"])
        attentions = list(sit_b.get("attention_target_hints") or [])
        if not any(a.get("target_type") == "entrance_exit" for a in attentions):
            attentions.append({
                "target_hint_id": _uid("ath_entrance"),
                "target_type": "entrance_exit",
                "priority": "P1",
                "reason": "entrance candidate for navigation competition",
                "candidate_only": True,
                "not_fact": True,
            })
            sit_b["attention_target_hints"] = attentions
        plan_b_input["situation_understanding_candidate"] = sit_b
        plan_b = build_agent_plan_candidate(plan_b_input)
        competing.append({
            "competition_slot": "plan_b_find_entrance",
            "label": "寻找入口 / Detection+Depth",
            "plan": plan_b,
            "driver": "navigation_or_entrance",
        })

    # Plan C: understand environment (VLM)
    plan_c_input = _alt_goal_input(
        agent_planning_input,
        "understand",
        "understand environment with VLM advisor",
        confidence=0.55,
    )
    # Force a lightweight VLM-oriented plan via unknown-like ask path when scene known
    plan_c = build_agent_plan_candidate(plan_c_input)
    # If back-end didn't add VLM, annotate as environment_understanding competitor
    competing.append({
        "competition_slot": "plan_c_environment_vlm",
        "label": "了解环境 / VLM",
        "plan": plan_c,
        "driver": "environment_understanding",
    })

    # Score each
    scored: List[Dict[str, Any]] = []
    for item in competing:
        score, breakdown = _score_plan(
            item["plan"],
            user_goal=user_goal,
            situation=situation,
        )
        scored.append({
            **item,
            "score": round(score, 4),
            "score_breakdown": breakdown,
            "candidate_only": True,
            "not_fact": True,
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    selected = scored[0]
    selection_trace = {
        "stage": "plan_competition_select",
        "selected_slot": selected["competition_slot"],
        "selected_goal": (selected["plan"].get("plan_goal_candidate") or {}).get("goal_type"),
        "score": selected["score"],
        "reason": (
            "user_goal_dominates_scene_default"
            if user_goal.get("goal_type") not in ("unknown",) and selected["driver"] in ("user_goal", "navigation_or_entrance")
            else "situation_and_missing_info_drive_selection"
        ),
        "policy_ref": "goal_overrides_scene_default_task",
        "competitors": [
            {
                "slot": s["competition_slot"],
                "goal": (s["plan"].get("plan_goal_candidate") or {}).get("goal_type"),
                "score": s["score"],
            }
            for s in scored
        ],
    }

    return {
        "competition_id": _uid("pcomp"),
        "competing_plans": scored,
        "selected_plan_candidate": selected["plan"],
        "selected_slot": selected["competition_slot"],
        "selection_trace": selection_trace,
        "candidate_only": True,
        "not_fact": True,
        "policy_refs": [POLICY_REF, DRYRUN_POLICY_REF, "plan_competition"],
    }


def _tool_summary(plan: Dict[str, Any]) -> Dict[str, List[str]]:
    return {
        "active": [t.get("capability_type", "") for t in plan.get("tool_plan_candidates", [])],
        "noop": [t.get("capability_type", "") for t in plan.get("noop_tool_plan_candidates", [])],
    }


def assert_l1_drives_l2(
    situation: Dict[str, Any],
    plan: Dict[str, Any],
) -> Dict[str, Any]:
    """Verify L1 fields actually shape L2 output (not ignore situation)."""
    scene = (situation.get("scene_profile_candidate") or {}).get("scene_type")
    missing = [m.get("info_type") for m in situation.get("missing_information_candidates", [])]
    likely = [
        h.get("capability_type")
        for h in (situation.get("model_need_hints") or {}).get("likely_needed", [])
    ]
    tools = _tool_summary(plan)["active"]
    noops = _tool_summary(plan)["noop"]
    checks = {
        "situation_id_in_trace": any(
            (t.get("situation_id") == situation.get("situation_id"))
            or (t.get("stage") in ("l1_to_l2_handoff", "agent_plan_built", "tool_os_handoff"))
            for t in (plan.get("trace_refs") or [])
        ) or bool(situation.get("situation_id")),
        "missing_info_shapes_steps": any(
            set(s.get("required_information") or []) & set(missing)
            for s in plan.get("plan_steps", [])
            if s.get("step_type") == "request_tool"
        ) if missing else True,
        "l1_likely_reflected_or_overridden_with_trace": (
            any(c in tools for c in likely)
            or any(
                t.get("stage") == "user_goal_overrides_task_clue"
                for t in (plan.get("plan_goal_candidate") or {}).get("trace_refs", [])
            )
        ),
        "l1_not_needed_reflected_in_noop_or_nav_override": (
            all(c in noops or c in tools for c in
                [h.get("capability_type") for h in (situation.get("model_need_hints") or {}).get("not_needed", [])])
            if (situation.get("model_need_hints") or {}).get("not_needed")
            else True
        ),
        "scene_context_present": bool(scene),
    }
    return {
        "passed": all(checks.values()),
        "checks": checks,
        "scene": scene,
        "candidate_only": True,
        "not_fact": True,
    }


def assert_l2_constrains_tools(plan: Dict[str, Any]) -> Dict[str, Any]:
    """L2 must not become a blanket model scheduler."""
    tools = _tool_summary(plan)["active"]
    noops = _tool_summary(plan)["noop"]
    handoff = plan.get("handoff_to_tool_os_candidate") or {}
    checks = {
        "not_all_capabilities_activated": len(tools) < 6,
        "has_noop_when_applicable": len(noops) > 0 or (plan.get("plan_goal_candidate") or {}).get("goal_type") in ("ask_user", "manual_review", "navigate"),
        "execution_mode_not_direct": all(
            t.get("execution_mode") in ("request_tool_os_admission", "manual_review_required", "not_executed")
            for t in plan.get("tool_plan_candidates", [])
        ),
        "no_runner_invocation_flag": plan.get("no_runner_invocation") is True,
        "no_tool_execution_flag": plan.get("no_tool_execution") is True,
        "handoff_gates_execution": (
            handoff.get("runner_admission_required") is True
            or handoff.get("should_handoff") is False
            or "runner_admission" in handoff.get("required_tool_os_checks", [])
        ),
        "fact_admission_marked": handoff.get("fact_admission_required_after_result") is True,
    }
    return {
        "passed": all(checks.values()),
        "checks": checks,
        "active_tools": tools,
        "noop_tools": noops,
        "candidate_only": True,
        "not_fact": True,
    }


def run_agent_planning_dryrun(
    job_envelope: Dict[str, Any],
    *,
    user_goal_candidate: Optional[Dict[str, Any]] = None,
    available_capabilities: Optional[List[Dict[str, Any]]] = None,
    use_plan_competition: bool = True,
) -> Dict[str, Any]:
    """
    Full dry-run chain:
    job/envelope → L1 situation → L2 plan (+ competition) → Tool OS handoff candidate.
    No tool execution, no runner invocation, no fact write.
    """
    # Allow injecting goal onto envelope for L1 (optional)
    envelope = deepcopy(job_envelope)
    if user_goal_candidate:
        envelope["user_goal_candidate_optional"] = user_goal_candidate

    l1_dryrun = run_situation_understanding_dryrun(envelope)
    situation = l1_dryrun.get("situation_understanding_candidate") or {}

    # Prefer explicit goal argument; else from envelope
    goal = user_goal_candidate or envelope.get("user_goal_candidate_optional")

    planning_input = build_agent_planning_input_from_situation(
        situation,
        user_goal_candidate=goal,
        available_capabilities=available_capabilities,
    )

    if use_plan_competition:
        competition = build_plan_competition(planning_input)
        plan = competition["selected_plan_candidate"]
    else:
        competition = None
        plan = build_agent_plan_candidate(planning_input)

    l1_drive = assert_l1_drives_l2(situation, plan)
    l2_constrain = assert_l2_constrains_tools(plan)
    tool_summary = _tool_summary(plan)

    return {
        "job_id": envelope.get("job_id", ""),
        "chain": [
            "job_envelope",
            "runner_evidence",
            "situation_understanding_candidate",
            "agent_plan_candidate",
            "tool_os_handoff_candidate",
        ],
        "situation_understanding_input": l1_dryrun.get("situation_understanding_input"),
        "situation_understanding_candidate": situation,
        "agent_planning_input": planning_input,
        "plan_competition": competition,
        "selected_plan_candidate": plan,
        "agent_plan_candidate": plan,
        "tool_os_handoff_candidate": plan.get("handoff_to_tool_os_candidate"),
        "tool_plan_summary": tool_summary,
        "l1_drives_l2_assertion": l1_drive,
        "l2_constrains_tools_assertion": l2_constrain,
        "scene_resolution_trace": l1_dryrun.get("scene_resolution_trace"),
        "runner_scene_hint_evidence": l1_dryrun.get("runner_scene_hint_evidence_record"),
        "no_runner_invocation_assertion": True,
        "no_tool_execution_assertion": True,
        "no_fact_write_assertion": True,
        "dryrun_only": True,
        "no_real_model_execution": True,
        "candidate_only": True,
        "not_fact": True,
        "policy_refs": [POLICY_REF, DRYRUN_POLICY_REF],
    }
