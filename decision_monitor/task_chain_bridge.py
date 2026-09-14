# -*- coding: utf-8 -*-
"""
任务链摘要桥接层 M0：Task Chain Bridge。

将 task_arbitration / task_bundle / object_search_interaction 等运行事实映射为
任务链可读的摘要状态（task_chain_state / foreground_summary / can_resume 等）。
仅做接口对接与摘要映射，不正式改 Task Chain 主体、不做执行器。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional

# 任务链视角状态（映射自下层，非原始状态）
TASK_CHAIN_STATES = (
    "active",
    "paused",
    "waiting_user",
    "blocked",
    "bundled",
    "done",
    "cancelled",
)
# bundle 语境状态
TASK_CHAIN_BUNDLE_STATES = ("none", "proposed", "active", "blocked", "closed")


@dataclass
class TaskChainBridgeResult:
    """任务链桥接 M0：最小摘要结构，供 Task Chain / 日志 / UI 读取。"""
    task_chain_foreground_summary: Optional[str] = None
    task_chain_state: str = "active"  # one of TASK_CHAIN_STATES
    task_chain_substate: Optional[str] = None
    task_chain_blocked: bool = False
    task_chain_block_reason: Optional[str] = None
    task_chain_can_resume: bool = False
    task_chain_bundle_state: str = "none"  # one of TASK_CHAIN_BUNDLE_STATES
    task_chain_source_modules: List[str] = field(default_factory=list)
    task_chain_summary_text: Optional[str] = None
    task_chain_bridge_applied: bool = True


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def build_task_chain_bridge(
    task_arbitration: Any,
    task_bundle: Any,
    object_search_interaction: Any,
    state: Any,
    current_foreground_task_type: Optional[str] = None,
) -> TaskChainBridgeResult:
    """
    从 arbitration / bundle / object_search 及 state 生成任务链可读摘要。
    仅读取已有运行结果，不引入新主感知源。
    """
    sources: List[str] = []
    foreground = current_foreground_task_type or _get(task_arbitration, "foreground_task_type") or ""
    arb_action = _get(task_arbitration, "arbitration_action") or "continue_current"
    if task_arbitration:
        sources.append("task_arbitration")
    if task_bundle:
        sources.append("task_bundle")
    if object_search_interaction:
        sources.append("object_search_interaction")

    # ----- 守底阻断 -----
    minimum_mode = _get(state, "minimum_mode_active") is True
    runtime_domain = (_get(state, "runtime_domain_state") or "").strip()
    scene_gate = (_get(state, "scene_gate_action") or "").strip()
    high_level_suppressed = _get(state, "high_level_output_suppressed") is True
    human_check_pending = _get(state, "human_check_pending") is True
    goal_progress_paused = _get(state, "goal_progress_paused") is True

    is_blocked = (
        minimum_mode
        or runtime_domain == "frozen"
        or scene_gate == "freeze_to_minimum_mode"
        or high_level_suppressed
        or human_check_pending
    )
    block_reason: Optional[str] = None
    if minimum_mode:
        block_reason = "minimum_mode_active"
    elif runtime_domain == "frozen":
        block_reason = "runtime_domain_state=frozen"
    elif scene_gate == "freeze_to_minimum_mode":
        block_reason = "scene_gate_action=freeze"
    elif high_level_suppressed:
        block_reason = "high_level_output_suppressed"
    elif human_check_pending:
        block_reason = "human_check_pending"

    # preempt -> safety_guard 视为 blocked 语义
    if arb_action == "preempt" and (_get(task_arbitration, "foreground_task_type") or "").strip() == "safety_guard":
        if not is_blocked:
            is_blocked = True
            block_reason = block_reason or "arbitration_preempt_safety_guard"

    # ----- search 终端状态 -----
    search_terminal = _get(object_search_interaction, "search_terminal_status") or "none"
    search_waiting_user = _get(object_search_interaction, "search_waiting_user_input") is True
    search_can_resume = _get(object_search_interaction, "search_can_resume_main_task") is True
    search_subtask = _get(object_search_interaction, "search_subtask_state") or ""

    # ----- bundle 状态 -----
    bundle_status = _get(task_bundle, "bundle_status") or "closed"
    bundle_created = _get(task_bundle, "bundle_created") is True
    if not task_bundle or not bundle_created:
        task_chain_bundle_state = "none"
    elif bundle_status in ("proposed", "active"):
        task_chain_bundle_state = bundle_status
    elif bundle_status == "blocked":
        task_chain_bundle_state = "blocked"
    else:
        task_chain_bundle_state = "closed"

    # ----- 任务链状态映射（优先级从高到低）-----
    if is_blocked:
        task_chain_state = "blocked"
    elif human_check_pending or search_waiting_user:
        task_chain_state = "waiting_user"
    elif search_terminal == "found":
        task_chain_state = "done"
    elif search_terminal == "cancelled":
        task_chain_state = "cancelled"
    elif bundle_created and task_chain_bundle_state in ("proposed", "active"):
        task_chain_state = "bundled"
    elif goal_progress_paused or arb_action in ("interrupt_then_resume", "defer"):
        task_chain_state = "paused"
    else:
        task_chain_state = "active"

    # ----- task_chain_foreground_summary -----
    if is_blocked and (foreground == "safety_guard" or arb_action == "preempt"):
        task_chain_foreground_summary = "blocked(safety_guard)"
    elif bundle_created and task_chain_bundle_state in ("proposed", "active"):
        types = _get(task_bundle, "bundle_task_types") or []
        if isinstance(types, list) and len(types) >= 2:
            task_chain_foreground_summary = "bundled(" + "+".join(types[:3]) + ")"
        elif isinstance(types, list) and types:
            task_chain_foreground_summary = "bundled(" + types[0] + ")"
        else:
            task_chain_foreground_summary = foreground or "bundled"
    else:
        task_chain_foreground_summary = foreground or "unknown"

    # ----- task_chain_substate -----
    if is_blocked and block_reason:
        task_chain_substate = "safety_preempt" if "safety" in (block_reason or "") or arb_action == "preempt" else "blocked"
    elif search_waiting_user or human_check_pending:
        task_chain_substate = "waiting_human_check"
    elif task_chain_bundle_state in ("proposed", "active"):
        task_chain_substate = "bundle_active"
    elif arb_action == "defer":
        task_chain_substate = "deferred_by_conflict"
    elif arb_action == "interrupt_then_resume":
        task_chain_substate = "interrupt_then_resume"
    elif search_subtask:
        # 直接沿用 search 子状态摘要
        task_chain_substate = search_subtask
    else:
        task_chain_substate = None

    # ----- task_chain_can_resume -----
    if is_blocked:
        task_chain_can_resume = False
    elif search_can_resume or search_terminal in ("found", "cancelled"):
        task_chain_can_resume = True
    elif arb_action == "interrupt_then_resume" and task_chain_state in ("done", "cancelled"):
        task_chain_can_resume = True
    else:
        task_chain_can_resume = False

    # ----- task_chain_summary_text -----
    parts = [
        f"前台任务={task_chain_foreground_summary or '—'}",
        f"状态={task_chain_state}",
    ]
    if task_chain_substate:
        parts.append(f"子状态={task_chain_substate}")
    parts.append(f"可恢复={task_chain_can_resume}")
    parts.append(f"bundle={task_chain_bundle_state}")
    if is_blocked and block_reason:
        parts.append(f"原因={block_reason}")
    task_chain_summary_text = "；".join(parts)

    return TaskChainBridgeResult(
        task_chain_foreground_summary=task_chain_foreground_summary,
        task_chain_state=task_chain_state,
        task_chain_substate=task_chain_substate,
        task_chain_blocked=is_blocked,
        task_chain_block_reason=block_reason,
        task_chain_can_resume=task_chain_can_resume,
        task_chain_bundle_state=task_chain_bundle_state,
        task_chain_source_modules=sources,
        task_chain_summary_text=task_chain_summary_text,
        task_chain_bridge_applied=True,
    )
