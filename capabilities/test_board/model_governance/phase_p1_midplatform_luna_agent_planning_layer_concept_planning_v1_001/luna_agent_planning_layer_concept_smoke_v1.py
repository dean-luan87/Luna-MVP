# -*- coding: utf-8
"""Luna Agent Planning Layer — concept planning smoke v1."""

from __future__ import annotations

from typing import Any, Dict, List

from capabilities.midplatform.agent_planning.luna_agent_planning_processor_v1 import (
    build_agent_plan_candidate,
)
from capabilities.midplatform.agent_planning.luna_agent_planning_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    SMOKE_CASE_IDS,
)

FINAL_SMOKE_GO = FINAL_GO.replace("_GO", "_SMOKE_GO") if FINAL_GO.endswith("_GO") else FINAL_GO + "_SMOKE_GO"
FINAL_SMOKE_BLOCKED = FINAL_BLOCKED.replace("_BLOCKED", "_SMOKE_BLOCKED")


def _need(cap: str, reason: str, policy: str) -> Dict[str, Any]:
    return {
        "capability_type": cap,
        "reason": reason,
        "policy_ref": policy,
        "candidate_only": True,
        "not_fact": True,
    }


def _situation(
    scene: str,
    tasks: List[Dict[str, Any]],
    missing: List[Dict[str, Any]],
    likely: List[str],
    not_needed: List[str],
    optional: List[str] | None = None,
    *,
    uncertainty: Dict[str, Any] | None = None,
    attention: List[Dict[str, Any]] | None = None,
) -> Dict[str, Any]:
    return {
        "situation_id": f"sit_{scene}",
        "scene_profile_candidate": {
            "scene_type": scene,
            "confidence": 0.85 if scene != "unknown_scene" else 0.35,
            "owned_by": "situation_understanding_layer",
            "candidate_only": True,
            "not_fact": True,
            "evidence_refs": [],
            "case_refs": [],
        },
        "survival_context": {"environment_type": "unknown", "risk_level": "low"},
        "task_clue_candidates": tasks,
        "missing_information_candidates": missing,
        "attention_target_hints": attention or [],
        "model_need_hints": {
            "likely_needed": [_need(c, f"{c} likely", "l1") for c in likely],
            "optional": [_need(c, f"{c} optional", "l1") for c in (optional or [])],
            "not_needed": [_need(c, f"{c} not needed", "l1") for c in not_needed],
        },
        "uncertainty": uncertainty or {
            "needs_user_goal": False,
            "needs_manual_review": False,
            "fallback_suggestion": "",
        },
        "candidate_only": True,
        "not_fact": True,
        "trace_refs": [],
    }


def _task(task_type: str, priority: str = "P0") -> Dict[str, Any]:
    return {
        "task_type": task_type,
        "priority": priority,
        "reason": f"fixture {task_type}",
        "evidence_refs": [],
        "candidate_only": True,
        "not_fact": True,
    }


def _missing(info_type: str, required_for: str, cap: str) -> Dict[str, Any]:
    return {
        "info_type": info_type,
        "required_for": required_for,
        "suggested_capability": cap,
        "reason": f"need {info_type}",
        "candidate_only": True,
        "not_fact": True,
    }


def _input(
    situation: Dict[str, Any],
    *,
    goal_type: str = "unknown",
    goal_text: str = "",
    capabilities: List[Dict[str, Any]] | None = None,
) -> Dict[str, Any]:
    default_caps = [
        {"capability_id": f"cap_{c}", "capability_type": c, "availability": "available"}
        for c in ("ocr", "detection", "depth", "tracking", "slam", "vlm", "sam")
    ]
    return {
        "situation_understanding_candidate": situation,
        "user_goal_candidate": {
            "goal_text_optional": goal_text,
            "goal_type": goal_type,
            "urgency": "normal",
            "explicitness": "explicit" if goal_type != "unknown" else "unknown",
            "confidence": 0.8 if goal_type != "unknown" else 0.2,
            "source": "user_command" if goal_type != "unknown" else "unknown",
            "candidate_only": True,
            "not_fact": True,
        },
        "available_capabilities": capabilities if capabilities is not None else default_caps,
        "policy_context": {
            "constitution_refs": ["L0"],
            "protocol_refs": [],
            "hard_constraints": ["no_fact_write", "no_runner_invocation"],
            "active_policy_refs": ["luna_agent_planning_policy_v1"],
        },
        "memory_context_candidates": [],
        "learning_case_refs": [],
        "candidate_only": True,
        "not_fact": True,
    }


def _tool_caps(plan: Dict[str, Any]) -> List[str]:
    return [t["capability_type"] for t in plan.get("tool_plan_candidates", [])]


def _noop_caps(plan: Dict[str, Any]) -> List[str]:
    return [t["capability_type"] for t in plan.get("noop_tool_plan_candidates", [])]


def _step_types(plan: Dict[str, Any]) -> List[str]:
    return [s["step_type"] for s in plan.get("plan_steps", [])]


def smoke_case_a_shopfront() -> Dict[str, Any]:
    case_id = "case_a_shopfront_sign"
    sit = _situation(
        "shopfront_sign",
        [_task("read_text", "P0"), _task("identify_place", "P1")],
        [_missing("text_content", "read_text", "ocr"), _missing("place_identity", "identify_place", "ocr")],
        ["ocr"],
        ["slam", "tracking", "depth"],
    )
    plan = build_agent_plan_candidate(_input(sit, goal_type="identify"))
    goal = plan["plan_goal_candidate"]["goal_type"]
    handoff = plan["handoff_to_tool_os_candidate"]
    passed = (
        goal in ("identify_place", "read_text")
        and plan["plan_strategy"]["strategy_type"] in ("information_gathering", "place_identification")
        and "request_tool" in _step_types(plan)
        and "ocr" in _tool_caps(plan)
        and "slam" in _noop_caps(plan)
        and "tracking" in _noop_caps(plan)
        and "depth" in _noop_caps(plan)
        and handoff.get("should_handoff") is True
        and (handoff.get("runner_admission_required") is True or "runner_admission" in handoff.get("required_tool_os_checks", []))
        and plan["candidate_only"] is True
        and plan["not_fact"] is True
        and plan.get("no_runner_invocation") is True
    )
    return {"case_id": case_id, "passed": passed, "plan": plan}


def smoke_case_b_subway() -> Dict[str, Any]:
    case_id = "case_b_subway_platform"
    sit = _situation(
        "subway_platform",
        [_task("find_direction"), _task("read_text")],
        [_missing("direction_info", "find_direction", "ocr"), _missing("text_content", "read_text", "ocr")],
        ["ocr"],
        ["slam"],
        optional=["detection"],
    )
    plan = build_agent_plan_candidate(_input(sit, goal_type="find"))
    passed = (
        plan["plan_goal_candidate"]["goal_type"] == "find_direction"
        and plan["plan_strategy"]["strategy_type"] == "information_gathering"
        and "ocr" in _tool_caps(plan)
        and "slam" in _noop_caps(plan)
        and plan["not_fact"] is True
    )
    return {"case_id": case_id, "passed": passed, "plan": plan}


def smoke_case_c_street() -> Dict[str, Any]:
    case_id = "case_c_street_crossing"
    sit = _situation(
        "street_crossing",
        [_task("assess_walkable"), _task("avoid_obstacle", "P1")],
        [_missing("walkable_area", "assess_walkable", "depth"), _missing("dynamic_motion", "avoid_obstacle", "tracking")],
        ["detection", "depth", "tracking"],
        ["ocr"],
    )
    plan = build_agent_plan_candidate(_input(sit, goal_type="navigate"))
    tools = _tool_caps(plan)
    stops = [s["condition_type"] for s in plan.get("stop_conditions", [])]
    passed = (
        plan["plan_strategy"]["strategy_type"] in ("risk_assessment", "navigation_support")
        and "detection" in tools
        and "depth" in tools
        and "tracking" in tools
        and "ocr" not in tools
        and ("risk_high" in stops or "confidence_sufficient" in stops)
        and plan["not_fact"] is True
    )
    return {"case_id": case_id, "passed": passed, "plan": plan}


def smoke_case_d_corridor() -> Dict[str, Any]:
    case_id = "case_d_corridor"
    sit = _situation(
        "corridor",
        [_task("assess_walkable")],
        [_missing("walkable_area", "assess_walkable", "depth"), _missing("spatial_continuity", "assess_walkable", "slam")],
        ["depth", "slam"],
        ["ocr"],
    )
    plan = build_agent_plan_candidate(_input(sit, goal_type="navigate", goal_text="navigate corridor"))
    tools = _tool_caps(plan)
    passed = (
        plan["plan_goal_candidate"]["goal_type"] == "navigate"
        and plan["plan_strategy"]["strategy_type"] == "navigation_support"
        and "depth" in tools
        and "slam" in tools
        and "ocr" in _noop_caps(plan)
        and plan["not_fact"] is True
    )
    return {"case_id": case_id, "passed": passed, "plan": plan}


def smoke_case_e_unknown() -> Dict[str, Any]:
    case_id = "case_e_unknown_scene"
    sit = _situation(
        "unknown_scene",
        [],
        [],
        [],
        ["slam", "detection", "ocr", "tracking", "depth"],
        optional=["vlm"],
        uncertainty={"needs_user_goal": True, "needs_manual_review": True, "fallback_suggestion": "ask_user / vlm_advisor"},
    )
    plan = build_agent_plan_candidate(_input(sit, goal_type="unknown"))
    tools = _tool_caps(plan)
    passed = (
        plan["plan_goal_candidate"]["goal_type"] in ("ask_user", "understand_environment", "manual_review")
        and plan["plan_strategy"]["strategy_type"] in ("ask_user_first", "manual_review")
        and len(tools) <= 1
        and plan["fallback_strategy"]["fallback_type"] in ("ask_user", "use_vlm_advisor", "manual_review")
        and plan.get("no_runner_invocation") is True
    )
    return {"case_id": case_id, "passed": passed, "plan": plan}


def smoke_case_f_tool_unavailable() -> Dict[str, Any]:
    case_id = "case_f_tool_unavailable"
    sit = _situation(
        "shopfront_sign",
        [_task("read_text")],
        [_missing("text_content", "read_text", "ocr")],
        ["ocr"],
        ["slam", "tracking", "depth"],
    )
    caps = [
        {"capability_id": "cap_ocr", "capability_type": "ocr", "availability": "unavailable"},
        {"capability_id": "cap_vlm", "capability_type": "vlm", "availability": "available"},
    ]
    plan = build_agent_plan_candidate(_input(sit, goal_type="read", capabilities=caps))
    handoff = plan["handoff_to_tool_os_candidate"]
    passed = (
        "ocr" not in _tool_caps(plan)
        and plan["fallback_strategy"]["fallback_type"] in ("use_vlm_advisor", "ask_user", "manual_review")
        and (
            handoff.get("should_handoff") is False
            or "tool_unavailable" in handoff.get("required_tool_os_checks", [])
            or "unavailable" in handoff.get("handoff_reason", "")
        )
        and plan.get("no_runner_invocation") is True
    )
    return {"case_id": case_id, "passed": passed, "plan": plan}


def smoke_case_g_user_goal_override() -> Dict[str, Any]:
    case_id = "case_g_user_goal_override"
    sit = _situation(
        "shopfront_sign",
        [_task("read_text")],
        [_missing("text_content", "read_text", "ocr")],
        ["ocr"],
        ["slam", "tracking", "depth"],
        attention=[{
            "target_hint_id": "ath_entrance",
            "target_type": "entrance_exit",
            "priority": "P1",
            "reason": "entrance for navigate",
            "candidate_only": True,
            "not_fact": True,
        }],
    )
    plan = build_agent_plan_candidate(_input(
        sit,
        goal_type="navigate",
        goal_text="navigate_to_entrance",
    ))
    tools = _tool_caps(plan)
    goal_traces = plan["plan_goal_candidate"].get("trace_refs", [])
    override_traced = any(t.get("stage") == "user_goal_overrides_task_clue" for t in goal_traces)
    passed = (
        plan["plan_goal_candidate"]["goal_type"] == "navigate"
        and plan["plan_strategy"]["strategy_type"] == "navigation_support"
        and ("detection" in tools or "depth" in tools)
        and override_traced
        and plan["not_fact"] is True
    )
    return {"case_id": case_id, "passed": passed, "plan": plan}


def run_smoke_cases() -> Dict[str, Any]:
    runners = [
        smoke_case_a_shopfront,
        smoke_case_b_subway,
        smoke_case_c_street,
        smoke_case_d_corridor,
        smoke_case_e_unknown,
        smoke_case_f_tool_unavailable,
        smoke_case_g_user_goal_override,
    ]
    cases = [fn() for fn in runners]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Agent-Planning-Layer-Concept-Planning-v1-001",
        "deterministic_smoke_only": True,
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "smoke_case_count": len(cases),
        "failed_checks": failed,
        "final_decision": FINAL_SMOKE_GO if not failed else FINAL_SMOKE_BLOCKED,
    }
