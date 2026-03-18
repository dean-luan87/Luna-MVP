# -*- coding: utf-8 -*-
"""
主线 2.0：局部时空状态图（Local Goal State）构建器。

从现有 goal / state / view_guard / predictive_hold / scene_gate / consequence 等汇聚，
产出围绕当前目标的短时局部状态，供 Decision Monitor 与后续导航/确认/视角控制使用。
第一版仅支持 observe_navigate / confirm_path / close_range_check 三类目标。
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .schema import (
    ConsequenceLayer,
    GoalLayer,
    InputsLayer,
    LocalGoalState,
    OutputsLayer,
    StateLayer,
)


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


# 第一版支持的 goal 类型（与 goal_resolver / scene 对齐）
GOAL_OBSERVE_NAVIGATE = "observe_navigate"
GOAL_CONFIRM_PATH = "confirm_path"
GOAL_CLOSE_RANGE_CHECK = "close_range_check"

# next_best_action 枚举
ACTION_CONTINUE_FORWARD = "continue_forward_observation"
ACTION_RECHECK_CLOSE = "recheck_close_range"
ACTION_RECHECK_ENV = "recheck_environment"
ACTION_HOLD_CONFIRM = "hold_and_confirm"
ACTION_SHIFT_VIEW_LEFT = "shift_view_left"
ACTION_SHIFT_VIEW_RIGHT = "shift_view_right"


def build(
    ctx: Dict[str, Any],
    goal: GoalLayer,
    state: StateLayer,
    inputs: InputsLayer,
    outputs: OutputsLayer,
    consequence: ConsequenceLayer,
) -> LocalGoalState:
    """
    从已有各层汇聚出 LocalGoalState。
    第一版只支持 observe_navigate / confirm_path / close_range_check；
    其他 goal_type 仍产出结构，但 focus_region / next_best_action 用通用占位。
    """
    goal_type = _get(goal, "goal_type") or GOAL_OBSERVE_NAVIGATE
    subgoal = _get(goal, "subgoal_description") or ""
    goal_status = _get(goal, "goal_status")
    scene_type = _get(state, "scene_type")
    scene_gate_action = _get(state, "scene_gate_action")
    view_misaligned = _get(state, "view_misaligned") is True
    view_correction_needed = _get(state, "view_correction_needed") is True
    goal_progress_paused = _get(state, "goal_progress_paused") is True
    predictive_hold_active = _get(state, "predictive_hold_active") is True
    predictive_hold_expired = _get(state, "predictive_hold_expired") is True
    runtime_domain_state = _get(state, "runtime_domain_state")
    traversability_state = _get(state, "traversability_state")
    local_risk_summary = _get(state, "local_risk_summary")
    risk_score = _get(state, "risk_score")
    state_confidence = _get(state, "state_confidence")
    state_trend = _get(state, "state_trend")
    action_summary = _get(outputs, "action_summary")
    delta_t_ms = _get(inputs, "delta_t_ms")
    post_action_check = _get(consequence, "post_action_check_needed") is True

    # 归一化“当前等效目标类型”用于 focus_region（第一版 3 类）
    effective_goal = _effective_goal_type(goal_type, subgoal, scene_type)
    goal_focus_region = _goal_focus_region(effective_goal)
    goal_progress_state = _goal_progress_state(
        goal_status, goal_progress_paused, scene_gate_action, predictive_hold_active, predictive_hold_expired
    )
    primary_view_direction = _primary_view_direction(view_misaligned, view_correction_needed, state)
    traversable_region_summary = _traversable_summary(traversability_state, local_risk_summary, runtime_domain_state)
    critical_objects: List[str] = []  # 第一版不接复杂对象，留空
    state_staleness_ms = float(delta_t_ms) if delta_t_ms is not None else 0.0
    recheck_required = post_action_check or predictive_hold_expired or view_correction_needed
    local_risk_str = local_risk_summary if isinstance(local_risk_summary, str) else None
    if not local_risk_str and risk_score is not None:
        local_risk_str = f"risk_score={risk_score:.2f}"
    next_best_action = _next_best_action(
        goal_progress_paused,
        scene_gate_action,
        view_correction_needed,
        predictive_hold_expired,
        effective_goal,
        action_summary,
    )

    return LocalGoalState(
        goal_id=_get(goal, "goal_id"),
        goal_type=goal_type,
        goal_focus_region=goal_focus_region,
        goal_progress_state=goal_progress_state,
        primary_view_direction=primary_view_direction,
        traversable_region_summary=traversable_region_summary,
        critical_objects=critical_objects if critical_objects else None,
        state_confidence=state_confidence,
        state_staleness_ms=state_staleness_ms if state_staleness_ms >= 0 else None,
        recheck_required=recheck_required,
        local_risk_summary=local_risk_str,
        next_best_action=next_best_action,
    )


def _effective_goal_type(goal_type: str, subgoal: str, scene_type: Optional[str]) -> str:
    """第一版 3 类：observe_navigate, confirm_path, close_range_check。"""
    if "confirm" in (subgoal or "").lower() or goal_type == "slow_down_observe":
        return GOAL_CONFIRM_PATH
    if goal_type in ("hold_for_floor", "recheck_environment") or (scene_type or "").startswith("close_range"):
        return GOAL_CLOSE_RANGE_CHECK
    return GOAL_OBSERVE_NAVIGATE


def _goal_focus_region(effective_goal: str) -> str:
    if effective_goal == GOAL_OBSERVE_NAVIGATE:
        return "前向观测区"
    if effective_goal == GOAL_CONFIRM_PATH:
        return "路径确认区"
    if effective_goal == GOAL_CLOSE_RANGE_CHECK:
        return "近场检查区"
    return "当前目标区"


def _goal_progress_state(
    goal_status: Optional[str],
    goal_progress_paused: bool,
    scene_gate_action: Optional[str],
    predictive_hold_active: bool,
    predictive_hold_expired: bool,
) -> str:
    if goal_progress_paused or (scene_gate_action in ("pause_goal_progress", "freeze_to_minimum_mode")):
        return "需等待"
    if goal_status == "paused":
        return "已暂停"
    if predictive_hold_expired:
        return "需确认"
    if predictive_hold_active:
        return "短时稳住"
    if goal_status == "active" or goal_status == "advancing":
        return "推进中"
    return "推进中"


def _primary_view_direction(
    view_misaligned: bool,
    view_correction_needed: bool,
    state: StateLayer,
) -> str:
    if view_correction_needed or view_misaligned:
        hint = _get(state, "view_correction_hint")
        if hint and "左" in str(hint):
            return "左前"
        if hint and "右" in str(hint):
            return "右前"
        return "需纠正"
    return "前方"


def _traversable_summary(
    traversability_state: Optional[str],
    local_risk_summary: Any,
    runtime_domain_state: Optional[str],
) -> str:
    if runtime_domain_state == "frozen":
        return "不可通行（域冻结）"
    if runtime_domain_state == "degraded":
        return "通行存疑（域降级）"
    if traversability_state:
        return str(traversability_state)
    if local_risk_summary:
        return f"局部：{local_risk_summary}"
    return "可观测"


def _next_best_action(
    goal_progress_paused: bool,
    scene_gate_action: Optional[str],
    view_correction_needed: bool,
    predictive_hold_expired: bool,
    effective_goal: str,
    action_summary: Optional[str],
) -> str:
    if goal_progress_paused or scene_gate_action in ("pause_goal_progress", "freeze_to_minimum_mode"):
        return ACTION_HOLD_CONFIRM
    if view_correction_needed:
        return ACTION_SHIFT_VIEW_LEFT  # 第一版不区分左右，统一建议纠正
    if predictive_hold_expired:
        return ACTION_HOLD_CONFIRM
    if effective_goal == GOAL_CLOSE_RANGE_CHECK:
        return ACTION_RECHECK_CLOSE
    if effective_goal == GOAL_CONFIRM_PATH:
        return ACTION_RECHECK_ENV
    if action_summary and "skip" in (action_summary or "").lower():
        return ACTION_HOLD_CONFIRM
    return ACTION_CONTINUE_FORWARD
