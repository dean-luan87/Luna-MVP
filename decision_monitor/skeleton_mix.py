# -*- coding: utf-8 -*-
"""
Skeleton Mix M0：最小运行时骨架配比。

依据 SPATIAL_SKELETON_SYSTEM_CONSTITUTION.md v1.0；
将四类骨架权重与保底落到运行时，规则型推导，不做学习。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

SKELETON_NAMES = ("navigation", "fine_interaction", "observation", "safety")
SAFETY_FLOOR_MIN = 0.15  # 宪法：safety_floor 不得为 0


@dataclass
class SkeletonMix:
    """当前帧骨架配比：4 权重 + 4 保底 + 主导骨架 + 原因。"""
    navigation_weight: float = 0.0
    fine_interaction_weight: float = 0.0
    observation_weight: float = 0.0
    safety_weight: float = 0.0
    navigation_floor: float = 0.0
    fine_interaction_floor: float = 0.0
    observation_floor: float = 0.0
    safety_floor: float = SAFETY_FLOOR_MIN
    dominant_skeleton: Optional[str] = None  # one of SKELETON_NAMES
    mix_reason: Optional[str] = None


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def build_skeleton_mix(
    goal: Any,
    state: Any,
    local_goal_spatial_map: Any,
) -> SkeletonMix:
    """
    最小规则型 Skeleton Mix：基于 goal_type、scene_profile、scene_type、
    minimum_mode、goal_progress_paused、high_level_output_suppressed 推导。
    """
    goal_type = _get(goal, "goal_type") or "observe_navigate"
    scene_type = _get(state, "scene_type") or ""
    scene_profile = _get(local_goal_spatial_map, "scene_profile") or "outdoor"
    minimum_mode = _get(state, "minimum_mode_active") is True
    goal_paused = _get(state, "goal_progress_paused") is True
    high_level_suppressed = _get(state, "high_level_output_suppressed") is True
    runtime_domain = _get(state, "runtime_domain_state") or "normal"

    # 保底：safety 不得为 0
    nav_floor = 0.05
    fine_floor = 0.05
    obs_floor = 0.05
    safe_floor = max(SAFETY_FLOOR_MIN, 0.15)

    # 默认：室外导航倾向
    nav_w = 0.6
    fine_w = 0.15
    obs_w = 0.15
    safe_w = 0.2
    reason = "default_outdoor_nav"

    # 高风险/冻结：safety 提升
    if minimum_mode or runtime_domain == "frozen" or high_level_suppressed:
        safe_w = 0.5
        nav_w = 0.2
        fine_w = 0.15
        obs_w = 0.15
        reason = "minimum_mode_or_frozen_safety_up"
    elif goal_paused:
        safe_w = 0.35
        nav_w = 0.25
        reason = "goal_paused_safety_up"

    # 近场/桌面交互：fine_interaction 高
    if "close_range" in scene_type or goal_type in ("hold_for_floor", "recheck_environment"):
        fine_w = max(fine_w, 0.55)
        nav_w = min(nav_w, 0.2)
        obs_w = 0.15
        safe_w = max(safe_w, 0.2)
        reason = "close_range_fine_interaction"
    # 观察/停留
    elif "stationary" in scene_type or (goal_type == "observe_navigate" and "observation" in (scene_type or "").lower()):
        obs_w = max(obs_w, 0.5)
        nav_w = min(nav_w, 0.25)
        fine_w = 0.15
        reason = "stationary_observation"

    # 室外导航类：navigation 高
    if scene_profile == "outdoor" and goal_type == "observe_navigate" and not minimum_mode:
        if "close_range" not in scene_type and "stationary" not in scene_type:
            nav_w = 0.55
            fine_w = 0.1
            obs_w = 0.2
            safe_w = 0.2
            reason = "outdoor_navigation"

    # 路径确认 / slow_down：nav + 一定 observation/safety
    if goal_type in ("confirm_path", "slow_down_observe"):
        nav_w = 0.4
        obs_w = 0.25
        safe_w = 0.25
        fine_w = 0.1
        reason = "confirm_path_or_slow_down"

    # 归一化到近似 1（可选，当前保持相对比例即可）
    total = nav_w + fine_w + obs_w + safe_w
    if total > 0:
        nav_w /= total
        fine_w /= total
        obs_w /= total
        safe_w /= total

    weights = [nav_w, fine_w, obs_w, safe_w]
    dominant = SKELETON_NAMES[weights.index(max(weights))]

    return SkeletonMix(
        navigation_weight=round(nav_w, 3),
        fine_interaction_weight=round(fine_w, 3),
        observation_weight=round(obs_w, 3),
        safety_weight=round(safe_w, 3),
        navigation_floor=nav_floor,
        fine_interaction_floor=fine_floor,
        observation_floor=obs_floor,
        safety_floor=safe_floor,
        dominant_skeleton=dominant,
        mix_reason=reason,
    )
