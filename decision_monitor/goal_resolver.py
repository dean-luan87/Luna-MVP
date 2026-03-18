# -*- coding: utf-8 -*-
"""
目标层真实化：根据当前运行态解析 goal_type / goal_description / subgoal / status。

规则驱动，不碰复杂意图系统。支持：observe_navigate, confirm_path, recheck_environment,
slow_down_observe, hold_for_floor, run_detector_check, run_ocr_check。
"""

from __future__ import annotations

from typing import Any, Dict

from .schema import GoalLayer


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def resolve(ctx: Dict[str, Any]) -> GoalLayer:
    """
    根据运行态解析当前目标。优先级：守底 > B2 介入 > 子目标( detector/ocr check ) > 默认观测导航。
    """
    floor_forced = ctx.get("detector_floor_due") or ctx.get("ocr_floor_due") or ctx.get("floor_forced")
    escape_fired = ctx.get("detector_escape_hatch_fired") or ctx.get("ocr_escape_hatch_fired")
    policy_intent = ctx.get("policy_intent")
    b2_applied = bool(_get(policy_intent, "b2_impact_applied", False))
    policy_should_sample = ctx.get("policy_should_sample")
    policy_run_detector = ctx.get("policy_run_detector", True)
    policy_run_ocr = ctx.get("policy_run_ocr", True)
    sampled = ctx.get("sampled")
    if sampled is None and ctx.get("obs") is not None:
        sampled = _get(ctx["obs"], "sampled")
    risk_score = ctx.get("risk_score")
    safety_level = ctx.get("decision")
    if safety_level is not None:
        sl = getattr(safety_level, "safety_level", None) or getattr(safety_level, "mode", None)
        safety_level = getattr(sl, "value", None) if sl is not None else str(sl) if sl else None

    goal_id = "default"
    goal_type = "observe_navigate"
    goal_description = "持续观测与导航"
    goal_source = "system_generated"
    goal_priority = None
    goal_confidence = 0.9
    goal_status = "active"
    subgoal_description = None
    goal_switch_reason = None

    # 1) 守底触发 → 当前目标：满足底线 / 重新确认环境
    if floor_forced or escape_fired:
        goal_type = "hold_for_floor"
        goal_description = "满足最小观察底线，重新采样确认环境"
        subgoal_description = "recheck_environment"
        goal_switch_reason = "floor_forced_or_escape_hatch"
        goal_confidence = 0.95
        return GoalLayer(
            goal_id=goal_id,
            goal_type=goal_type,
            goal_description=goal_description,
            goal_source=goal_source,
            goal_priority=goal_priority,
            goal_confidence=goal_confidence,
            goal_status=goal_status,
            subgoal_description=subgoal_description,
            goal_switch_reason=goal_switch_reason,
        )

    # 2) B2 介入 → 提高观察强度、放慢节奏
    if b2_applied:
        goal_type = "slow_down_observe"
        goal_description = "在弱证据下提高观察强度，放慢节奏"
        subgoal_description = "confirm_path"
        goal_switch_reason = "b2_impact_applied"
        goal_confidence = 0.85
        return GoalLayer(
            goal_id=goal_id,
            goal_type=goal_type,
            goal_description=goal_description,
            goal_source=goal_source,
            goal_priority=goal_priority,
            goal_confidence=goal_confidence,
            goal_status=goal_status,
            subgoal_description=subgoal_description,
            goal_switch_reason=goal_switch_reason,
        )

    # 3) 子目标：本轮是否在执行 detector / OCR 检查
    sub_parts = []
    if sampled and policy_run_detector:
        sub_parts.append("run_detector_check")
    if sampled and policy_run_ocr:
        sub_parts.append("run_ocr_check")
    if sub_parts:
        subgoal_description = " / ".join(sub_parts)

    # 4) 若被采样门跳过，目标仍是观测导航，但状态可标为“节流中”
    if policy_should_sample is False:
        goal_status = "advancing"
        goal_description = "持续观测与导航（本轮节流跳过）"
        goal_switch_reason = "sampling_gate_skip"

    # 5) 风险态时保持观察
    if safety_level == "DANGER":
        goal_status = "active"
        goal_description = "持续观测与导航（当前风险态，保持观察）"

    return GoalLayer(
        goal_id=goal_id,
        goal_type=goal_type,
        goal_description=goal_description,
        goal_source=goal_source,
        goal_priority=goal_priority,
        goal_confidence=goal_confidence,
        goal_status=goal_status,
        subgoal_description=subgoal_description,
        goal_switch_reason=goal_switch_reason,
    )
