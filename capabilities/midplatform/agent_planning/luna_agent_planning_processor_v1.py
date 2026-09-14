# -*- coding: utf-8
"""Luna Agent Planning Layer — deterministic processor stub v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set
from uuid import uuid4

from capabilities.midplatform.agent_planning.luna_agent_planning_types_v1 import (
    POLICY_REF,
)


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _situation(input_data: Dict[str, Any]) -> Dict[str, Any]:
    return input_data.get("situation_understanding_candidate") or {}


def _scene_type(situation: Dict[str, Any]) -> str:
    return (situation.get("scene_profile_candidate") or {}).get("scene_type", "unknown_scene")


def _task_types(situation: Dict[str, Any]) -> List[str]:
    return [c.get("task_type", "") for c in situation.get("task_clue_candidates", [])]


def _missing_types(situation: Dict[str, Any]) -> List[str]:
    return [m.get("info_type", "") for m in situation.get("missing_information_candidates", [])]


def _need_caps(situation: Dict[str, Any], bucket: str) -> List[str]:
    hints = situation.get("model_need_hints") or {}
    return [h.get("capability_type", "") for h in hints.get(bucket, [])]


def _goal(input_data: Dict[str, Any]) -> Dict[str, Any]:
    return input_data.get("user_goal_candidate") or {}


def _cap_available(input_data: Dict[str, Any], cap: str) -> bool:
    for c in input_data.get("available_capabilities") or []:
        if c.get("capability_type") == cap:
            return c.get("availability", "available") != "unavailable"
    return True


def _has_attention(situation: Dict[str, Any], *types: str) -> bool:
    hints = situation.get("attention_target_hints") or []
    values = {h.get("target_type", "") for h in hints}
    return any(t in values for t in types)


def infer_plan_goal(input_data: Dict[str, Any]) -> Dict[str, Any]:
    situation = _situation(input_data)
    scene = _scene_type(situation)
    user_goal = _goal(input_data)
    goal_type_raw = user_goal.get("goal_type", "unknown")
    goal_text = (user_goal.get("goal_text_optional") or "").lower()
    tasks = _task_types(situation)
    traces: List[Dict[str, Any]] = []

    # User navigate goal can override text task clues
    navigate_like = (
        goal_type_raw in ("navigate",)
        or "navigate" in goal_text
        or "navigation" in goal_text
        or "entrance" in goal_text
    )
    if navigate_like and scene != "unknown_scene":
        traces.append({
            "stage": "user_goal_overrides_task_clue",
            "user_goal": goal_type_raw or goal_text,
            "prior_task_clues": tasks,
            "resolution": "plan_goal_navigate",
            "policy_ref": POLICY_REF,
        })
        return {
            "interpreted_goal": user_goal.get("goal_text_optional") or "navigate based on user goal",
            "goal_type": "navigate",
            "source": "user_goal",
            "confidence": float(user_goal.get("confidence") or 0.8),
            "candidate_only": True,
            "not_fact": True,
            "trace_refs": traces,
            "policy_refs": [POLICY_REF],
        }

    if scene == "unknown_scene" or not tasks:
        uncertainty = situation.get("uncertainty") or {}
        goal_type = "ask_user" if uncertainty.get("needs_manual_review") or goal_type_raw == "unknown" else "understand_environment"
        return {
            "interpreted_goal": f"clarify goal in {scene}",
            "goal_type": goal_type,
            "source": "inferred",
            "confidence": 0.4,
            "candidate_only": True,
            "not_fact": True,
            "trace_refs": [{"stage": "infer_plan_goal", "scene": scene}],
            "policy_refs": [POLICY_REF, "unknown_scene_asks_user_or_vlm"],
        }

    priority_map = {
        "read_text": "read_text",
        "identify_place": "identify_place",
        "find_direction": "find_direction",
        "assess_walkable": "assess_walkable",
        "avoid_obstacle": "assess_walkable",
        "ask_user": "ask_user",
        "manual_review": "manual_review",
    }
    chosen = "unknown"
    for t in tasks:
        if t in priority_map:
            chosen = priority_map[t]
            if t in ("read_text", "find_direction", "assess_walkable"):
                break
    if scene == "shopfront_sign" and "identify_place" in tasks:
        chosen = "identify_place" if "identify_place" in tasks else chosen
        if "read_text" in tasks and chosen == "identify_place":
            # Prefer identify_place as goal when both present; read_text still drives OCR step
            pass
    if scene == "subway_platform" and "find_direction" in tasks:
        chosen = "find_direction"

    return {
        "interpreted_goal": f"{chosen} for {scene}",
        "goal_type": chosen,
        "source": "situation_task_clue",
        "confidence": 0.82,
        "candidate_only": True,
        "not_fact": True,
        "trace_refs": [{"stage": "infer_plan_goal", "task_clues": tasks, "chosen": chosen}],
        "policy_refs": [POLICY_REF, "missing_information_drives_plan"],
    }


def build_plan_strategy(input_data: Dict[str, Any], goal: Dict[str, Any]) -> Dict[str, Any]:
    situation = _situation(input_data)
    scene = _scene_type(situation)
    gt = goal.get("goal_type", "unknown")
    strategy = "information_gathering"
    reason = "default information gathering"
    policy = POLICY_REF

    if gt in ("ask_user", "manual_review") or scene == "unknown_scene":
        strategy = "ask_user_first" if gt == "ask_user" else "manual_review"
        reason = "unknown scene or unclear goal requires user / review first"
        policy = "unknown_scene_asks_user_or_vlm"
    elif gt in ("read_text",) or (gt == "identify_place" and scene == "shopfront_sign"):
        strategy = "place_identification" if gt == "identify_place" else "information_gathering"
        reason = "text/place identification driven by L1 task clues"
        policy = "text_goal_prefers_ocr_plan"
    elif gt == "find_direction":
        strategy = "information_gathering"
        reason = "direction finding via signage/text"
        policy = "text_goal_prefers_ocr_plan"
    elif gt in ("assess_walkable",) or scene == "street_crossing":
        strategy = "risk_assessment"
        reason = "street crossing requires risk/walkability assessment"
        policy = "street_crossing_prefers_risk_assessment_plan"
    elif gt == "navigate" and scene == "corridor":
        strategy = "navigation_support"
        reason = "corridor navigate prefers spatial tools"
        policy = "corridor_navigation_prefers_spatial_plan"
    elif gt == "navigate":
        strategy = "navigation_support"
        reason = "user navigate goal"
        policy = POLICY_REF

    return {
        "strategy_type": strategy,
        "reason": reason,
        "candidate_only": True,
        "not_fact": True,
        "trace_refs": [{"stage": "build_plan_strategy", "goal_type": gt, "scene": scene}],
        "policy_refs": [POLICY_REF, policy],
    }


def build_plan_steps(
    input_data: Dict[str, Any],
    goal: Dict[str, Any],
    strategy: Dict[str, Any],
) -> List[Dict[str, Any]]:
    situation = _situation(input_data)
    missing = _missing_types(situation)
    gt = goal.get("goal_type", "unknown")
    scene = _scene_type(situation)
    steps: List[Dict[str, Any]] = []
    order = 1

    def step(step_type: str, step_goal: str, required: List[str], expected: str, deps: Optional[List[str]] = None) -> Dict[str, Any]:
        nonlocal order
        sid = _uid("step")
        s = {
            "step_id": sid,
            "step_order": order,
            "step_type": step_type,
            "step_goal": step_goal,
            "required_information": required,
            "expected_output": expected,
            "depends_on_step_ids": deps or [],
            "candidate_only": True,
            "not_fact": True,
            "trace_refs": [{
                "stage": "build_plan_steps",
                "missing": required,
                "task_clues": _task_types(situation),
                "policy_ref": "missing_information_drives_plan",
            }],
            "policy_refs": [POLICY_REF, "all_steps_traceable"],
        }
        order += 1
        return s

    if strategy.get("strategy_type") in ("ask_user_first", "manual_review") or gt in ("ask_user", "manual_review"):
        steps.append(step("ask_user", "clarify user goal", ["user_goal"], "user_goal_candidate"))
        steps.append(step("stop", "await clarification", ["user_goal"], "stop_until_goal_clear"))
        return steps

    steps.append(step("observe", f"observe {scene} context", missing or ["unknown"], "observation_candidate"))

    if gt in ("read_text", "identify_place", "find_direction"):
        req = [m for m in missing if m in ("text_content", "place_identity", "direction_info")] or ["text_content"]
        steps.append(step("request_tool", "request OCR via Tool OS", req, "ocr_result_candidate", [steps[0]["step_id"]]))
        steps.append(step("evaluate_result", "evaluate OCR sufficiency", req, "confidence_assessment", [steps[-1]["step_id"]]))
    elif scene == "street_crossing" or gt == "assess_walkable":
        req = [m for m in missing if m in ("walkable_area", "dynamic_motion")] or ["walkable_area"]
        steps.append(step("request_tool", "request Detection/Depth/Tracking", req, "risk_assessment_result", [steps[0]["step_id"]]))
        steps.append(step("evaluate_result", "evaluate walkability confidence", req, "confidence_assessment", [steps[-1]["step_id"]]))
    elif gt == "navigate" and scene == "corridor":
        req = [m for m in missing if m in ("walkable_area", "spatial_continuity")] or ["spatial_continuity"]
        steps.append(step("request_tool", "request Depth/SLAM", req, "spatial_plan_result", [steps[0]["step_id"]]))
        steps.append(step("evaluate_result", "evaluate spatial continuity", req, "confidence_assessment", [steps[-1]["step_id"]]))
    elif gt == "navigate":
        req = missing or ["walkable_area"]
        steps.append(step("request_tool", "request navigation-support tools", req, "nav_support_result", [steps[0]["step_id"]]))
        steps.append(step("evaluate_result", "evaluate navigation support", req, "confidence_assessment", [steps[-1]["step_id"]]))
    else:
        steps.append(step("fallback", "fallback without blanket tools", missing, "fallback_candidate"))

    steps.append(step("fallback", "low confidence fallback", missing, "fallback_or_ask_user", [steps[-1]["step_id"]]))
    steps.append(step("stop", "apply stop conditions", [], "stop_decision"))
    return steps


def build_tool_plan_candidates(
    input_data: Dict[str, Any],
    plan_steps: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    situation = _situation(input_data)
    scene = _scene_type(situation)
    goal = infer_plan_goal(input_data)  # stay consistent for override cases when called alone
    # Prefer goal already inferred upstream if present in input cache
    cached_goal = input_data.get("_plan_goal") or goal
    gt = cached_goal.get("goal_type", "unknown")
    likely = set(_need_caps(situation, "likely_needed"))
    optional = set(_need_caps(situation, "optional"))
    missing = _missing_types(situation)
    plans: List[Dict[str, Any]] = []

    def tool(cap: str, purpose: str, priority: str, reason: str, policy: str) -> None:
        if not _cap_available(input_data, cap):
            return
        target_refs = [
            h.get("target_hint_id", "")
            for h in situation.get("attention_target_hints", [])
        ]
        plans.append({
            "tool_plan_id": _uid("tp"),
            "capability_type": cap,
            "tool_purpose": purpose,
            "input_target_hint_refs": target_refs,
            "required_information_refs": missing,
            "execution_mode": "request_tool_os_admission",
            "priority": priority,
            "reason": reason,
            "candidate_only": True,
            "not_fact": True,
            "trace_refs": [{"stage": "build_tool_plan", "capability": cap, "plan_steps": [s["step_id"] for s in plan_steps]}],
            "policy_refs": [POLICY_REF, policy],
        })

    if gt in ("ask_user", "manual_review") or scene == "unknown_scene":
        if "vlm" in optional or scene == "unknown_scene":
            if _cap_available(input_data, "vlm"):
                tool("vlm", "advisor for unknown scene", "P2", "optional VLM advisor only", "unknown_scene_asks_user_or_vlm")
        return plans

    if gt in ("read_text", "identify_place", "find_direction") or "ocr" in likely:
        tool("ocr", "read text / place / direction", "P0", "text goal prefers OCR plan", "text_goal_prefers_ocr_plan")

    if scene == "subway_platform" and (
        "detection" in optional or _has_attention(situation, "person_candidate", "entrance_exit")
    ):
        tool("detection", "optional safety/door/people target", "P2", "optional Detection when safety target exists", "text_goal_prefers_ocr_plan")

    if scene == "street_crossing" or gt == "assess_walkable":
        for cap in ("detection", "depth", "tracking"):
            if cap in likely or scene == "street_crossing":
                tool(cap, f"{cap} for walkability/risk", "P0", "street crossing risk assessment", "street_crossing_prefers_risk_assessment_plan")
        # OCR not full-image for street: only optional if text attention exists
        if _has_attention(situation, "direction_sign", "primary_text_block") and "ocr" in optional:
            tool("ocr", "optional sign text only", "P3", "OCR only for sign/text target, not full-image", "street_crossing_prefers_risk_assessment_plan")

    if gt == "navigate" and scene == "corridor":
        for cap in ("depth", "slam"):
            if cap in likely or True:
                tool(cap, f"{cap} for corridor navigation", "P0", "corridor navigation spatial plan", "corridor_navigation_prefers_spatial_plan")

    if gt == "navigate" and scene == "shopfront_sign":
        for cap in ("detection", "depth"):
            tool(cap, f"{cap} for entrance navigation support", "P1", "user navigate overrides text-only focus", POLICY_REF)
        tool("slam", "optional SLAM due to navigation context not text task", "P2", "navigation context may optionally include SLAM", POLICY_REF)
        if "ocr" in likely or True:
            tool("ocr", "optional OCR for sign/context", "P2", "OCR optional under navigate override", "text_goal_prefers_ocr_plan")

    # De-dupe capability types keeping first (higher priority insertion order)
    seen: Set[str] = set()
    deduped: List[Dict[str, Any]] = []
    for p in plans:
        cap = p["capability_type"]
        if cap in seen:
            continue
        seen.add(cap)
        deduped.append(p)
    return deduped


def build_noop_tool_plan_candidates(input_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    situation = _situation(input_data)
    scene = _scene_type(situation)
    goal = input_data.get("_plan_goal") or infer_plan_goal(input_data)
    gt = goal.get("goal_type", "unknown")
    not_needed = list(_need_caps(situation, "not_needed"))
    noops: List[Dict[str, Any]] = []

    def noop(cap: str, reason: str, policy: str) -> None:
        noops.append({
            "capability_type": cap,
            "noop_reason": reason,
            "policy_ref": policy,
            "candidate_only": True,
            "not_fact": True,
            "trace_refs": [{"stage": "build_noop_tool_plan", "capability": cap}],
        })

    for cap in not_needed:
        policy = "text_goal_no_default_slam_plan" if cap == "slam" else "noop_plan_required"
        noop(cap, f"L1 not_needed inherits noop for {cap}", policy)

    # Ensure shopfront text goals noop Spatial trio even if L1 omitted
    if scene == "shopfront_sign" and gt in ("read_text", "identify_place"):
        for cap in ("slam", "tracking", "depth"):
            if not any(n["capability_type"] == cap for n in noops):
                noop(cap, "text goal no default spatial tools", "text_goal_no_default_slam_plan")

    if scene == "subway_platform" and gt != "navigate":
        if not any(n["capability_type"] == "slam" for n in noops):
            noop("slam", "SLAM noop unless navigate", "text_goal_no_default_slam_plan")

    if scene == "corridor" and not any(n["capability_type"] == "ocr" for n in noops):
        if not _has_attention(situation, "primary_text_block", "direction_sign") and "ocr" not in _need_caps(situation, "likely_needed"):
            noop("ocr", "OCR noop unless text evidence", "corridor_navigation_prefers_spatial_plan")

    if scene == "street_crossing":
        # OCR full-image not planned: record noop if OCR not in tool plans path
        if not _has_attention(situation, "direction_sign", "primary_text_block"):
            if not any(n["capability_type"] == "ocr" for n in noops):
                noop("ocr", "no full-image OCR plan for street crossing", "street_crossing_prefers_risk_assessment_plan")

    return noops


def build_fallback_strategy(input_data: Dict[str, Any]) -> Dict[str, Any]:
    situation = _situation(input_data)
    scene = _scene_type(situation)
    ocr_available = _cap_available(input_data, "ocr")
    goal = input_data.get("_plan_goal") or infer_plan_goal(input_data)
    gt = goal.get("goal_type", "unknown")

    if scene == "unknown_scene":
        return {
            "fallback_type": "ask_user",
            "trigger_condition": "scene_unknown_or_goal_unclear",
            "reason": "unknown_scene requires ask_user / vlm advisor",
            "candidate_only": True,
            "not_fact": True,
            "trace_refs": [{"stage": "fallback", "scene": scene}],
            "policy_refs": [POLICY_REF, "unknown_scene_asks_user_or_vlm"],
        }

    if gt in ("read_text", "identify_place", "find_direction") and not ocr_available:
        return {
            "fallback_type": "use_vlm_advisor",
            "trigger_condition": "tool_unavailable:ocr",
            "reason": "OCR unavailable → VLM advisor or ask_user",
            "candidate_only": True,
            "not_fact": True,
            "trace_refs": [{"stage": "fallback", "tool_unavailable": "ocr"}],
            "policy_refs": [POLICY_REF],
        }

    return {
        "fallback_type": "ask_user" if scene == "unknown_scene" else "lower_confidence_output",
        "trigger_condition": "low_confidence_after_evaluate",
        "reason": "evaluate_result low confidence triggers fallback",
        "candidate_only": True,
        "not_fact": True,
        "trace_refs": [{"stage": "fallback", "default": True}],
        "policy_refs": [POLICY_REF],
    }


def build_ask_user_strategy(input_data: Dict[str, Any]) -> Dict[str, Any]:
    situation = _situation(input_data)
    scene = _scene_type(situation)
    user_goal = _goal(input_data)
    uncertainty = situation.get("uncertainty") or {}
    should = (
        scene == "unknown_scene"
        or user_goal.get("goal_type", "unknown") == "unknown"
        or uncertainty.get("needs_user_goal") is True
        or uncertainty.get("needs_manual_review") is True
    )
    return {
        "should_ask_user": should,
        "question_candidate": "请确认当前目标：读文字、找方向、评估通行，还是导航？" if should else "",
        "ask_reason": "goal unclear or unknown_scene" if should else "goal sufficiently clear",
        "trigger_condition": "user_goal_unclear" if should else "not_required",
        "candidate_only": True,
        "not_fact": True,
        "trace_refs": [{"stage": "ask_user_strategy", "should_ask_user": should}],
        "policy_refs": [POLICY_REF, "unknown_scene_asks_user_or_vlm"],
    }


def build_stop_conditions(input_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    situation = _situation(input_data)
    scene = _scene_type(situation)
    conditions = [
        {
            "condition_type": "required_info_obtained",
            "reason": "stop when missing information filled",
            "candidate_only": True,
            "not_fact": True,
            "trace_refs": [{"stage": "stop_conditions"}],
        },
        {
            "condition_type": "confidence_sufficient",
            "reason": "stop when evaluate_result confidence sufficient",
            "candidate_only": True,
            "not_fact": True,
            "trace_refs": [{"stage": "stop_conditions"}],
        },
        {
            "condition_type": "manual_review_required",
            "reason": "stop for manual review when flagged",
            "candidate_only": True,
            "not_fact": True,
            "trace_refs": [{"stage": "stop_conditions"}],
        },
    ]
    if scene == "street_crossing":
        conditions.append({
            "condition_type": "risk_high",
            "reason": "street crossing may stop on high risk",
            "candidate_only": True,
            "not_fact": True,
            "trace_refs": [{"stage": "stop_conditions", "scene": scene}],
        })
    if scene == "unknown_scene":
        conditions.append({
            "condition_type": "user_goal_unclear",
            "reason": "unknown scene stops until goal clarified",
            "candidate_only": True,
            "not_fact": True,
            "trace_refs": [{"stage": "stop_conditions", "scene": scene}],
        })
    if not _cap_available(input_data, "ocr") and _scene_type(_situation(input_data)) == "shopfront_sign":
        conditions.append({
            "condition_type": "tool_unavailable",
            "reason": "OCR unavailable for text goal",
            "candidate_only": True,
            "not_fact": True,
            "trace_refs": [{"stage": "stop_conditions", "tool": "ocr"}],
        })
    return conditions


def build_tool_os_handoff_candidate(
    input_data: Dict[str, Any],
    tool_plan_candidates: List[Dict[str, Any]],
) -> Dict[str, Any]:
    situation = _situation(input_data)
    ocr_needed = any(t.get("capability_type") == "ocr" for t in tool_plan_candidates)
    ocr_unavailable = ocr_needed and not _cap_available(input_data, "ocr")
    should = bool(tool_plan_candidates) and not ocr_unavailable
    checks = ["capability_availability", "permission_check", "sandbox_policy", "runner_admission"]
    if ocr_unavailable:
        checks.append("tool_unavailable")
        should = False
    return {
        "should_handoff": should,
        "handoff_reason": (
            "tool_unavailable:ocr"
            if ocr_unavailable
            else ("handoff tool plans to Tool OS" if should else "no executable tool plan")
        ),
        "required_tool_os_checks": checks,
        "runner_admission_required": True if tool_plan_candidates else False,
        "fact_admission_required_after_result": True,
        "candidate_only": True,
        "not_fact": True,
        "trace_refs": [{
            "stage": "tool_os_handoff",
            "situation_id": situation.get("situation_id", ""),
            "tool_plan_count": len(tool_plan_candidates),
        }],
        "policy_refs": [
            POLICY_REF,
            "tool_os_handoff_required",
            "runner_admission_required",
            "fact_admission_required_after_result",
        ],
    }


def build_agent_plan_candidate(input_data: Dict[str, Any]) -> Dict[str, Any]:
    if not input_data.get("situation_understanding_candidate"):
        raise ValueError("situation_input_required")

    goal = infer_plan_goal(input_data)
    input_data = {**input_data, "_plan_goal": goal}
    strategy = build_plan_strategy(input_data, goal)
    steps = build_plan_steps(input_data, goal, strategy)
    tools = build_tool_plan_candidates(input_data, steps)
    noops = build_noop_tool_plan_candidates(input_data)
    # Remove overlap: if a cap is in tools, drop from noops (navigate override)
    tool_caps = {t["capability_type"] for t in tools}
    noops = [n for n in noops if n["capability_type"] not in tool_caps]
    fallback = build_fallback_strategy(input_data)
    ask_user = build_ask_user_strategy(input_data)
    stops = build_stop_conditions(input_data)
    handoff = build_tool_os_handoff_candidate(input_data, tools)

    # Guard: no blanket tool plan
    if len(tools) >= 7:
        tools = tools[:3]

    situation = _situation(input_data)
    traces = list(goal.get("trace_refs") or [])
    traces.append({"stage": "agent_plan_built", "situation_id": situation.get("situation_id", "")})

    return {
        "plan_id": _uid("plan"),
        "plan_goal_candidate": goal,
        "plan_strategy": strategy,
        "plan_steps": steps,
        "tool_plan_candidates": tools,
        "noop_tool_plan_candidates": noops,
        "fallback_strategy": fallback,
        "ask_user_strategy": ask_user,
        "stop_conditions": stops,
        "handoff_to_tool_os_candidate": handoff,
        "trace_refs": traces,
        "candidate_only": True,
        "not_fact": True,
        "policy_refs": [POLICY_REF],
        "no_runner_invocation": True,
        "no_tool_execution": True,
        "no_fact_write": True,
    }
