# -*- coding: utf-8 -*-
"""
主线 A：任务态 × 复杂度的「介入资格门禁」（v0）

目标：把两件事彻底分离
  - 世界是否复杂（A3 已算）
  - 系统是否有资格介入（本模块定义）

v0 只做资格判断，不触发建议、不改策略、不抬安全。
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, Union


class TaskState(Enum):
    """v0 最小任务态模型"""

    NONE = "NONE"  # 无任务（默认）
    PASSIVE = "PASSIVE"  # 被动任务（陪走/观察/无明确目标）
    ACTIVE = "ACTIVE"  # 主动任务（导航/找路/明确目标）


# v0 阈值（写死）
COMPLEXITY_THRESHOLD = 0.5


def infer_task_state(has_goal: bool, explore_mode: bool = False) -> TaskState:
    """
    v0 从现有标志推断 TaskState（只读）。

    - 若有明确目标/导航中：ACTIVE
    - 否则（陪走、未指定目标）：PASSIVE
    - 无任务：NONE
    """
    if has_goal:
        return TaskState.ACTIVE
    if explore_mode:
        return TaskState.PASSIVE
    return TaskState.NONE


def compute_intervention_eligibility(
    task_state: Union[TaskState, str],
    complexity_effective: float,
) -> Dict[str, Any]:
    """
    计算介入资格（v0 规则，写死）。

    条件：
      - task_state == NONE → ❌
      - task_state == PASSIVE → ❌
      - task_state == ACTIVE 且 complexity_effective < 0.5 → ❌
      - task_state == ACTIVE 且 complexity_effective >= 0.5 → ✅

    Returns:
        {"allowed": bool, "reason": str}
    """
    if isinstance(task_state, str):
        try:
            task_state = TaskState(task_state)
        except ValueError:
            task_state = TaskState.NONE

    if task_state != TaskState.ACTIVE:
        return {
            "allowed": False,
            "reason": "NO_ACTIVE_TASK",
        }

    if complexity_effective < COMPLEXITY_THRESHOLD:
        return {
            "allowed": False,
            "reason": "LOW_COMPLEXITY",
        }

    return {
        "allowed": True,
        "reason": "ACTIVE_TASK_AND_HIGH_COMPLEXITY",
    }
