# -*- coding: utf-8 -*-
"""
任务仲裁 M0：Task Arbitration（最小版）。

“意图池化 → 空间聚合 → 任务仲裁 → 骨架融合 → 分层执行”中的任务仲裁层最小落成。
仅读取已有运行事实（goal、state、skeleton_mix、object_search_interaction、recheck、object_temporal_ledger、ctx 候选任务提示）；不做完整任务中心、不做多任务执行器、不正式改 Task Chain。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional

ARBITRATION_ACTIONS = (
    "preempt",
    "interrupt_then_resume",
    "merge_into_bundle",
    "run_in_background",
    "defer",
    "continue_current",
)

FOREGROUND_TASK_TYPES = (
    "object_search",
    "navigation",
    "safety_guard",
    "recheck",
    "observation",
    "interaction_confirm",
)

LEVELS = ("low", "medium", "high")


@dataclass
class TaskArbitrationResult:
    """任务仲裁 M0：最小仲裁结果（仅判断，不实现调度迁移）。"""
    foreground_task_type: Optional[str] = None
    candidate_task_types: List[str] = field(default_factory=list)
    arbitration_action: str = "continue_current"  # one of ARBITRATION_ACTIONS
    arbitration_reason: Optional[str] = None
    risk_priority_level: str = "low"  # one of LEVELS, or "safety" when preempt
    environment_overlap_level: str = "low"  # one of LEVELS
    resource_conflict_level: str = "low"  # one of LEVELS
    user_interruption_cost: str = "low"  # one of LEVELS
    arbitration_applied: bool = True


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _foreground_from_context(
    goal: Any,
    state: Any,
    object_search_interaction: Any,
    recheck_planner: Any,
) -> str:
    """从当前模块状态映射出轻量 foreground_task_type。"""
    minimum_mode = _get(state, "minimum_mode_active") is True
    runtime_domain = (_get(state, "runtime_domain_state") or "").strip()
    scene_gate_action = (_get(state, "scene_gate_action") or "").strip()
    if minimum_mode or runtime_domain == "frozen" or scene_gate_action == "freeze_to_minimum_mode":
        return "safety_guard"
    if object_search_interaction:
        subtask = _get(object_search_interaction, "search_subtask_state") or ""
        terminal = _get(object_search_interaction, "search_terminal_status") or "none"
        if terminal == "none" and subtask not in ("", "search_done"):
            return "object_search"
    if recheck_planner and _get(recheck_planner, "recheck_action"):
        if _get(recheck_planner, "recheck_blocked") is True:
            return "safety_guard"
        return "recheck"
    goal_type = (_get(goal, "goal_type") or "observe_navigate").strip()
    if goal_type in ("hold_for_floor",):
        return "safety_guard"
    if goal_type in ("observe_navigate", "confirm_path", "slow_down_observe"):
        return "navigation"
    if goal_type in ("close_range_check",):
        return "interaction_confirm"
    if goal_type in ("run_detector_check", "run_ocr_check", "recheck_environment"):
        return "observation"
    return "navigation"


def _candidates_from_context(
    goal: Any,
    state: Any,
    object_search_interaction: Any,
    recheck_planner: Any,
    skeleton_mix: Any,
    incoming_task_type: Optional[str],
) -> List[str]:
    """收集候选任务类型（轻量字符串列表）。"""
    cand = []
    if recheck_planner and _get(recheck_planner, "recheck_action"):
        cand.append("recheck")
    if object_search_interaction and (_get(object_search_interaction, "search_terminal_status") or "none") == "none":
        cand.append("object_search")
    if _get(state, "minimum_mode_active") is True or (_get(state, "runtime_domain_state") or "") == "frozen":
        cand.append("safety_guard")
    dominant = _get(skeleton_mix, "dominant_skeleton")
    if dominant == "observation":
        cand.append("observation")
    if dominant == "navigation":
        cand.append("navigation")
    if incoming_task_type and (incoming_task_type.strip().lower() not in [c.lower() for c in cand]):
        cand.append(incoming_task_type.strip())
    return list(dict.fromkeys(cand))[:8]


def build_task_arbitration(
    goal: Any,
    state: Any,
    skeleton_mix: Any,
    object_search_interaction: Any,
    recheck_planner: Any,
    object_temporal_ledger: Any,
    # 可选：ctx 注入的候选任务提示
    incoming_task_type: Optional[str] = None,
    incoming_task_zone: Optional[str] = None,
    incoming_task_risk: Optional[str] = None,
    incoming_task_requires_user_attention: Optional[bool] = None,
) -> TaskArbitrationResult:
    """
    M0：从已有运行事实做最小五维仲裁，产出仲裁动作与等级。
    不做真正多任务执行器，不正式改 Task Chain。
    """
    minimum_mode = _get(state, "minimum_mode_active") is True
    runtime_domain = (_get(state, "runtime_domain_state") or "").strip()
    scene_gate_action = (_get(state, "scene_gate_action") or "").strip()
    high_level_suppressed = _get(state, "high_level_output_suppressed") is True
    recheck_blocked = bool(recheck_planner and _get(recheck_planner, "recheck_blocked") is True)
    human_check_pending = _get(state, "human_check_pending") is True

    # 当前主任务与候选
    foreground = _foreground_from_context(goal, state, object_search_interaction, recheck_planner)
    candidate_types = _candidates_from_context(
        goal, state, object_search_interaction, recheck_planner, skeleton_mix, incoming_task_type
    )

    # --------- 五维判断 ---------
    # A/B. 风险与目标优先级
    risk_priority_level = "low"
    if minimum_mode or runtime_domain == "frozen" or scene_gate_action == "freeze_to_minimum_mode":
        risk_priority_level = "high"
    elif runtime_domain == "degraded" or high_level_suppressed or recheck_blocked:
        risk_priority_level = "medium"

    # C. 资源冲突（当前与 incoming 争抢视角/注意力/recheck/对象账本/骨架）
    resource_conflict_level = "low"
    incoming_attention = incoming_task_requires_user_attention is True
    current_search_waiting = bool(object_search_interaction and _get(object_search_interaction, "search_waiting_user_input") is True)
    if incoming_attention and (current_search_waiting or human_check_pending):
        resource_conflict_level = "high"
    elif incoming_task_type and foreground and (incoming_task_type.strip().lower() == foreground.lower() or (incoming_task_type.strip().lower() in ("object_search", "recheck") and foreground in ("object_search", "recheck"))):
        resource_conflict_level = "medium"
    elif incoming_task_type and foreground:
        resource_conflict_level = "medium"

    # D. 环境重合度（当前任务与 incoming 是否同区域/同容器/同路径）
    environment_overlap_level = "low"
    current_zone = None
    if object_search_interaction:
        current_zone = _get(object_search_interaction, "suggested_search_zone")
    if incoming_task_zone and current_zone and (incoming_task_zone.strip() in (current_zone or "") or (current_zone or "").strip() in incoming_task_zone.strip()):
        environment_overlap_level = "high"
    elif incoming_task_zone or current_zone:
        environment_overlap_level = "medium"

    # E. 用户打扰成本（是否新增追问、额外动作、打断当前操作）
    user_interruption_cost = "low"
    if human_check_pending or current_search_waiting:
        user_interruption_cost = "high"
    elif foreground in ("object_search", "interaction_confirm"):
        user_interruption_cost = "medium"

    # --------- 仲裁规则 ---------
    action = "continue_current"
    reason = "无强切换理由，继续当前任务"

    # A. 安全/守底抢占
    if minimum_mode or runtime_domain == "frozen" or scene_gate_action == "freeze_to_minimum_mode":
        action = "preempt"
        foreground = "safety_guard"
        reason = "安全/守底优先，抢占为 safety_guard"
        risk_priority_level = "high"
    # B. 同环境可组合
    elif incoming_task_type and environment_overlap_level == "high" and resource_conflict_level != "high":
        action = "merge_into_bundle"
        reason = "环境重合度高且资源冲突不高，可空间聚合/同环境合并"
    # C. 资源冲突高但非抢占
    elif resource_conflict_level == "high" and risk_priority_level != "high":
        action = "defer"
        reason = "资源冲突高，暂缓接入新任务"
    # D. 可后台运行（观察型/低频守护/账本维护，打扰成本低）
    elif incoming_task_type and (incoming_task_type.strip().lower() in ("observation", "recheck")) and user_interruption_cost == "low" and not incoming_attention:
        action = "run_in_background"
        reason = "新任务为观察/补证型且用户打扰成本低，可后台"
    # E. 可插入恢复（简化为：incoming 风险高于当前且当前可恢复）
    elif incoming_task_risk and (incoming_task_risk.strip().lower() in ("high", "medium")) and foreground in ("navigation", "observation") and user_interruption_cost != "high":
        action = "interrupt_then_resume"
        reason = "新任务风险较高且当前可恢复，建议短暂插入后恢复"
    # F. 默认
    else:
        action = "continue_current"
        if not reason:
            reason = "继续当前任务"

    applied = not (minimum_mode or runtime_domain == "frozen" or recheck_blocked)

    return TaskArbitrationResult(
        foreground_task_type=foreground,
        candidate_task_types=candidate_types,
        arbitration_action=action,
        arbitration_reason=reason,
        risk_priority_level=risk_priority_level,
        environment_overlap_level=environment_overlap_level,
        resource_conflict_level=resource_conflict_level,
        user_interruption_cost=user_interruption_cost,
        arbitration_applied=applied,
    )
