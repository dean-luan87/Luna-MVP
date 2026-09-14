# -*- coding: utf-8
"""Luna Agent Planning — UI payload builder v1 (explainable L1→L2→L3 chain)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

FORBIDDEN_UI_COPY = (
    "Luna decided",
    "Model chose",
    "OCR required",
    "This is a shop",
    "这是店",
    "已确认为店",
    "模型已决定",
    "必须执行 OCR",
    "confirmed shop",
)


def build_goal_candidates(dryrun: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Multi-goal interpretation candidates (not a single ground-truth goal)."""
    competition = dryrun.get("plan_competition") or {}
    plans = competition.get("competing_plans") or []
    goals: List[Dict[str, Any]] = []
    seen = set()
    for item in plans:
        plan = item.get("plan") or {}
        g = plan.get("plan_goal_candidate") or {}
        gt = g.get("goal_type", "unknown")
        if gt in seen:
            continue
        seen.add(gt)
        goals.append({
            "goal_type": gt,
            "interpreted_goal": g.get("interpreted_goal", gt),
            "confidence": round(float(g.get("confidence") or item.get("score") or 0.5), 2),
            "source": g.get("source", item.get("driver", "inferred")),
            "competition_slot": item.get("competition_slot"),
            "candidate_only": True,
            "not_fact": True,
        })
    # Sort by confidence desc
    goals.sort(key=lambda x: x.get("confidence", 0), reverse=True)
    return goals


def build_selection_reason(dryrun: Dict[str, Any]) -> Dict[str, Any]:
    competition = dryrun.get("plan_competition") or {}
    selection = competition.get("selection_trace") or {}
    selected = dryrun.get("selected_plan_candidate") or {}
    goal = (selected.get("plan_goal_candidate") or {}).get("goal_type", "unknown")
    tools = [t.get("capability_type") for t in selected.get("tool_plan_candidates", [])]
    noops = [n.get("capability_type") for n in selected.get("noop_tool_plan_candidates", [])]
    situation = dryrun.get("situation_understanding_candidate") or {}
    missing = [m.get("info_type") for m in situation.get("missing_information_candidates", [])]
    user_goal = (dryrun.get("agent_planning_input") or {}).get("user_goal_candidate") or {}

    positives: List[str] = []
    negatives: List[str] = []

    ug = user_goal.get("goal_type", "unknown")
    if ug in ("unknown",) and goal in ("identify_place", "read_text"):
        positives.append("用户当前未提出导航需求")
    if ug == "navigate" and goal == "navigate":
        positives.append("用户目标明确为导航 / 寻找入口")
    if missing and any(m in ("text_content", "place_identity", "direction_info") for m in missing):
        if "ocr" in tools:
            positives.append("当前缺失信息是文字/地点内容")
            positives.append("OCR 成本低，适合 information gathering")
    if "detection" in tools or "depth" in tools:
        positives.append("目标与通行/入口相关，需要空间风险感知候选")
    if "slam" in noops:
        negatives.append("无需空间建模（SLAM noop）")
    if "tracking" in noops:
        negatives.append("无需动态目标分析（Tracking noop）")
    if "depth" in noops and "detection" not in tools:
        negatives.append("无需深度测距（Depth noop）")
    if goal == "ask_user":
        positives.append("场景不确定，优先向用户澄清")
        negatives.append("不 blanket 激活全部模型")

    final_label = {
        "identify_place": "OCR-first information gathering",
        "read_text": "OCR-first information gathering",
        "find_direction": "OCR-first direction finding",
        "navigate": "navigation-support plan candidate",
        "assess_walkable": "risk-assessment plan candidate",
        "ask_user": "ask-user-first (no blanket activation)",
        "understand_environment": "environment-understanding / VLM advisor candidate",
    }.get(goal, "selected plan candidate")

    return {
        "positives": positives,
        "negatives": negatives,
        "final_label": final_label,
        "selection_reason_code": selection.get("reason", "situation_and_missing_info_drive_selection"),
        "selected_slot": competition.get("selected_slot") or selection.get("selected_slot"),
        "selected_goal": goal,
        "candidate_only": True,
        "not_fact": True,
    }


def build_competition_cards(dryrun: Dict[str, Any]) -> List[Dict[str, Any]]:
    competition = dryrun.get("plan_competition") or {}
    selected_slot = competition.get("selected_slot")
    cards = []
    for item in competition.get("competing_plans") or []:
        plan = item.get("plan") or {}
        goal = plan.get("plan_goal_candidate") or {}
        strategy = plan.get("plan_strategy") or {}
        tools = [t.get("capability_type") for t in plan.get("tool_plan_candidates", [])]
        noops = [n.get("capability_type") for n in plan.get("noop_tool_plan_candidates", [])]
        cards.append({
            "slot": item.get("competition_slot"),
            "label": item.get("label"),
            "goal_type": goal.get("goal_type"),
            "strategy_type": strategy.get("strategy_type"),
            "tools": tools,
            "noops": noops,
            "score": item.get("score"),
            "score_breakdown": item.get("score_breakdown"),
            "status": "selected" if item.get("competition_slot") == selected_slot else "candidate",
            "driver": item.get("driver"),
            "candidate_only": True,
            "not_fact": True,
        })
    cards.sort(key=lambda c: c.get("score") or 0, reverse=True)
    return cards


def build_tool_plan_ui(plan: Dict[str, Any]) -> Dict[str, Any]:
    active = []
    for t in plan.get("tool_plan_candidates") or []:
        active.append({
            "capability_type": t.get("capability_type"),
            "purpose": t.get("tool_purpose"),
            "execution_mode": t.get("execution_mode"),
            "priority": t.get("priority"),
            "reason": t.get("reason"),
            "candidate_only": True,
            "not_fact": True,
        })
    noop = []
    for n in plan.get("noop_tool_plan_candidates") or []:
        noop.append({
            "capability_type": n.get("capability_type"),
            "noop_reason": n.get("noop_reason"),
            "policy_ref": n.get("policy_ref"),
            "candidate_only": True,
            "not_fact": True,
        })
    return {
        "active": active,
        "noop": noop,
        "candidate_only": True,
        "not_fact": True,
        "not_executed": True,
    }


def build_handoff_ui(plan: Dict[str, Any]) -> Dict[str, Any]:
    handoff = plan.get("handoff_to_tool_os_candidate") or {}
    tools = [t.get("capability_type") for t in plan.get("tool_plan_candidates", [])]
    return {
        "should_handoff": handoff.get("should_handoff"),
        "request_capabilities": tools,
        "required_checks": handoff.get("required_tool_os_checks") or [
            "permission check", "resource check", "runner admission",
        ],
        "runner_admission_required": handoff.get("runner_admission_required"),
        "fact_admission_required_after_result": handoff.get("fact_admission_required_after_result"),
        "handoff_reason": handoff.get("handoff_reason"),
        "status": "candidate_only",
        "not_executed": True,
        "candidate_only": True,
        "not_fact": True,
    }


def build_chain_trace(dryrun: Dict[str, Any]) -> List[Dict[str, Any]]:
    situation = dryrun.get("situation_understanding_candidate") or {}
    scene = (situation.get("scene_profile_candidate") or {}).get("scene_type", "unknown_scene")
    plan = dryrun.get("selected_plan_candidate") or {}
    goal = (plan.get("plan_goal_candidate") or {}).get("goal_type", "unknown")
    tools = [t.get("capability_type") for t in plan.get("tool_plan_candidates", [])]
    return [
        {"stage": "L1_Situation", "summary": f"scene={scene} candidate", "candidate_only": True, "not_fact": True},
        {"stage": "L2_Goal", "summary": f"goal={goal} candidate", "candidate_only": True, "not_fact": True},
        {"stage": "L2_PlanCompetition", "summary": "competing plans scored", "candidate_only": True, "not_fact": True},
        {"stage": "L2_SelectedPlan", "summary": f"selected_goal={goal}", "candidate_only": True, "not_fact": True},
        {"stage": "L2_ToolPlan", "summary": f"active={tools}", "candidate_only": True, "not_fact": True},
        {"stage": "L3_ToolOSHandoff", "summary": "handoff candidate_only · not executed", "candidate_only": True, "not_fact": True},
    ]


def build_ui_payload_from_agent_planning_dryrun(dryrun: Dict[str, Any]) -> Dict[str, Any]:
    plan = dryrun.get("selected_plan_candidate") or dryrun.get("agent_plan_candidate") or {}
    situation = dryrun.get("situation_understanding_candidate") or {}
    return {
        "job_id": dryrun.get("job_id", ""),
        "situation_summary": {
            "scene_type": (situation.get("scene_profile_candidate") or {}).get("scene_type"),
            "confidence": (situation.get("scene_profile_candidate") or {}).get("confidence"),
            "task_clues": [
                {"task_type": t.get("task_type"), "priority": t.get("priority")}
                for t in situation.get("task_clue_candidates", [])
            ],
            "missing_information": [
                m.get("info_type") for m in situation.get("missing_information_candidates", [])
            ],
            "owned_by": (situation.get("scene_profile_candidate") or {}).get("owned_by", "situation_understanding_layer"),
            "candidate_only": True,
            "not_fact": True,
            "wording": "当前证据支持这是一个场景候选，不是已确认事实",
        },
        "goal_candidates": build_goal_candidates(dryrun),
        "plan_competition_cards": build_competition_cards(dryrun),
        "selected_plan": {
            "plan_id": plan.get("plan_id"),
            "goal_type": (plan.get("plan_goal_candidate") or {}).get("goal_type"),
            "strategy_type": (plan.get("plan_strategy") or {}).get("strategy_type"),
            "steps": [
                {"step_order": s.get("step_order"), "step_type": s.get("step_type"), "step_goal": s.get("step_goal")}
                for s in plan.get("plan_steps", [])
            ],
            "candidate_only": True,
            "not_fact": True,
        },
        "selection_reason": build_selection_reason(dryrun),
        "tool_plan": build_tool_plan_ui(plan),
        "tool_os_handoff": build_handoff_ui(plan),
        "chain_trace": build_chain_trace(dryrun),
        "badges": [
            "candidate_only", "not_fact", "selected_plan_candidate",
            "no_tool_execution", "no_runner_invocation",
        ],
        "candidate_only": True,
        "not_fact": True,
        "ui_execution_only": True,
        "explainable_decision_chain": True,
    }


def audit_ui_copy(text: str) -> List[str]:
    return [f for f in FORBIDDEN_UI_COPY if f in text]
