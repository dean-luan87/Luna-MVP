# -*- coding: utf-8 -*-
"""
空间遗忘 M0：Spatial Forgetting（最小版）。

在 Spatial Memory Pooling M0 基础上为 working / episode 增加最小出池规则：
- Working：TTL 过期
- Episode：Task-End Collapse（任务结束或上下文切换）+ 最小时间过期
Stable / Anchor 不做复杂遗忘，保持占位。
不做 Value Decay、Evidence Replacement、学习型策略。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional, Tuple

from .spatial_memory_pools import SpatialMemoryPools, SpatialMemoryItem

# 默认 TTL（毫秒）：可测、规则明确
WORKING_TTL_MS = 5000.0
EPISODE_TTL_MS = 30000.0


@dataclass
class SpatialForgettingSummary:
    """最小遗忘结果/摘要，供 frame / runtime_ctx / viewer 使用。"""
    working_expired_count: int = 0
    episode_collapsed_count: int = 0
    episode_expired_count: int = 0
    forgetting_reason_summary: Optional[str] = None
    forgetting_actions_applied: List[str] = field(default_factory=list)


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _task_ended_or_context_switched(
    goal: Any,
    goal_status: Optional[str],
    prev_goal_type: Optional[str],
    prev_goal_status: Optional[str],
    prev_dominant: Optional[str],
    current_dominant: Optional[str],
) -> bool:
    """
    最小任务结束或上下文切换条件（规则型）：
    - goal_status 变为 paused / completed
    - goal_type 与上一帧不同
    - dominant_skeleton 与上一帧不同
    """
    if goal_status in ("paused", "completed"):
        return True
    goal_type = _get(goal, "goal_type") if goal is not None else None
    if prev_goal_type is not None and goal_type is not None and goal_type != prev_goal_type:
        return True
    if prev_goal_status is not None and goal_status is not None and prev_goal_status != goal_status:
        if goal_status in ("paused", "completed"):
            return True
    if prev_dominant is not None and current_dominant is not None and prev_dominant != current_dominant:
        return True
    return False


def apply_spatial_forgetting(
    pools: SpatialMemoryPools,
    goal: Any,
    state: Any,
    current_ts: float,
    prev_goal_type: Optional[str] = None,
    prev_goal_status: Optional[str] = None,
    prev_dominant: Optional[str] = None,
    working_ttl_ms: float = WORKING_TTL_MS,
    episode_ttl_ms: float = EPISODE_TTL_MS,
) -> Tuple[SpatialMemoryPools, SpatialForgettingSummary]:
    """
    对当前帧的 pools 应用最小遗忘规则，返回更新后的池与遗忘摘要。
    - Working：超过 working_ttl_ms 的项移除
    - Episode：若任务结束/上下文切换则 collapse（清空）；否则按 episode_ttl_ms 过期
    - Stable / Anchor：不处理
    """
    now_ms = current_ts * 1000.0
    actions: List[str] = []
    reasons: List[str] = []

    # 1. Working TTL
    working = list(pools.working_memory_items)
    kept_working: List[SpatialMemoryItem] = []
    for it in working:
        ts_ms = (it.timestamp or 0.0) * 1000.0
        if now_ms - ts_ms <= working_ttl_ms:
            kept_working.append(it)
    working_expired_count = len(working) - len(kept_working)
    if working_expired_count > 0:
        actions.append("working_ttl")
        reasons.append(f"working_ttl_expired={working_expired_count}")

    # 2. Episode：Task-End Collapse 或 时间过期
    goal_status = _get(state, "goal_status") if state is not None else _get(goal, "goal_status")
    current_dominant = pools.dominant_skeleton
    task_ended = _task_ended_or_context_switched(
        goal, goal_status, prev_goal_type, prev_goal_status, prev_dominant, current_dominant
    )

    episode_collapsed_count = 0
    episode_expired_count = 0
    kept_episode: List[SpatialMemoryItem] = []
    episode = list(pools.episode_memory_items)

    if task_ended:
        episode_collapsed_count = len(episode)
        kept_episode = []
        actions.append("episode_collapse")
        reasons.append(f"task_end_or_switch collapse={episode_collapsed_count}")
    else:
        for it in episode:
            ts_ms = (it.timestamp or 0.0) * 1000.0
            if now_ms - ts_ms <= episode_ttl_ms:
                kept_episode.append(it)
        episode_expired_count = len(episode) - len(kept_episode)
        if episode_expired_count > 0:
            actions.append("episode_expiry")
            reasons.append(f"episode_ttl_expired={episode_expired_count}")

    summary = SpatialForgettingSummary(
        working_expired_count=working_expired_count,
        episode_collapsed_count=episode_collapsed_count,
        episode_expired_count=episode_expired_count,
        forgetting_reason_summary="; ".join(reasons) if reasons else None,
        forgetting_actions_applied=actions,
    )

    new_pools = SpatialMemoryPools(
        working_memory_items=kept_working,
        episode_memory_items=kept_episode,
        stable_memory_items=pools.stable_memory_items,
        anchor_memory_items=pools.anchor_memory_items,
        dominant_skeleton=pools.dominant_skeleton,
        pool_reason=pools.pool_reason,
    )
    return new_pools, summary
