# -*- coding: utf-8 -*-
"""
Scene Gate v1：日常场景分类 + 非支持场景挂起。

先不负责复杂裁决，只做两件事：
1）判断当前属于哪类日常场景
2）判断当前场景是否在 Luna 支持域内

若当前场景属于已知非支持域，系统不再接受该场景的高层输入进入正常理解链。
保守优先：判断不稳时进 unknown_context；高旋转/长期偏航时进 unsupported_*。
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from .schema import StateLayer

# 场景类型（7 类）
SCENE_NORMAL_WALK = "normal_walk_navigation"
SCENE_STATIONARY = "stationary_observation"
SCENE_CLOSE_RANGE = "close_range_check"
SCENE_CAUTIOUS = "cautious_navigation"
SCENE_UNSUPPORTED_MOTION = "unsupported_motion_context"
SCENE_UNSUPPORTED_VIEW = "unsupported_view_context"
SCENE_UNKNOWN = "unknown_context"

# 门状态 / 动作
GATE_OPEN = "open"
GATE_CAUTIOUS = "cautious"
GATE_SUSPENDED = "suspended"
ACTION_CONTINUE_NORMAL = "continue_normal"
ACTION_CONTINUE_CAUTIOUS = "continue_cautious"
ACTION_PAUSE_GOAL = "pause_goal_progress"
ACTION_IGNORE_HIGH_LEVEL = "ignore_high_level_input"
ACTION_FREEZE = "freeze_to_minimum_mode"


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def evaluate(
    ctx: Dict[str, Any],
    state: StateLayer,
    goal: Any = None,
) -> Dict[str, Any]:
    """
    在 runtime_domain_guard 之后调用；
    基于 state（含运行域、视线、视觉）、goal（目标类型）与 ctx 做场景分类与门控。
    输出：scene_type, scene_supported, scene_gate_state, scene_gate_reason, scene_gate_action
    """
    domain_state = _get(state, "runtime_domain_state")
    domain_reason = _get(state, "domain_mismatch_reason") or ""
    view_misaligned = _get(state, "view_misaligned")
    vision_quality = _get(state, "vision_quality_state")
    state_trend = _get(state, "state_trend")
    goal_type = _get(goal, "goal_type") if goal is not None else ctx.get("goal_type")
    domain_confidence = _get(state, "runtime_domain_confidence")
    b2_applied = ctx.get("policy_intent") and _get(ctx.get("policy_intent"), "b2_impact_applied")

    # 非支持域：优先判 unsupported_motion / unsupported_view
    if domain_state == "frozen":
        if "high_rotation_or_abnormal_motion" in domain_reason or "high_rotation" in domain_reason:
            return {
                "scene_type": SCENE_UNSUPPORTED_MOTION,
                "scene_supported": False,
                "scene_gate_state": GATE_SUSPENDED,
                "scene_gate_reason": "high_rotation_or_abnormal_motion_frozen",
                "scene_gate_action": ACTION_FREEZE,
            }
        return {
            "scene_type": SCENE_UNSUPPORTED_VIEW,
            "scene_supported": False,
            "scene_gate_state": GATE_SUSPENDED,
            "scene_gate_reason": "vision_invalid_or_long_unusable",
            "scene_gate_action": ACTION_FREEZE,
        }

    if domain_state == "degraded":
        if view_misaligned is True or "view_misaligned" in domain_reason:
            return {
                "scene_type": SCENE_UNSUPPORTED_VIEW,
                "scene_supported": False,
                "scene_gate_state": GATE_SUSPENDED,
                "scene_gate_reason": "view_misaligned_long_term",
                "scene_gate_action": ACTION_PAUSE_GOAL,
            }
        if "high_rotation_or_abnormal_motion" in domain_reason:
            return {
                "scene_type": SCENE_UNSUPPORTED_MOTION,
                "scene_supported": False,
                "scene_gate_state": GATE_SUSPENDED,
                "scene_gate_reason": "high_rotation_or_abnormal_motion",
                "scene_gate_action": ACTION_FREEZE,
            }
        return {
            "scene_type": SCENE_CAUTIOUS,
            "scene_supported": True,
            "scene_gate_state": GATE_CAUTIOUS,
            "scene_gate_reason": "vision_degraded_in_support_domain",
            "scene_gate_action": ACTION_CONTINUE_CAUTIOUS,
        }

    # 支持域内：normal
    if domain_state != "normal":
        return {
            "scene_type": SCENE_UNKNOWN,
            "scene_supported": False,
            "scene_gate_state": GATE_CAUTIOUS,
            "scene_gate_reason": "domain_state_uncertain",
            "scene_gate_action": ACTION_IGNORE_HIGH_LEVEL,
        }

    if domain_confidence is not None and float(domain_confidence) < 0.5:
        return {
            "scene_type": SCENE_UNKNOWN,
            "scene_supported": False,
            "scene_gate_state": GATE_CAUTIOUS,
            "scene_gate_reason": "low_domain_confidence",
            "scene_gate_action": ACTION_IGNORE_HIGH_LEVEL,
        }

    if b2_applied or state_trend not in ("stable", None):
        return {
            "scene_type": SCENE_CAUTIOUS,
            "scene_supported": True,
            "scene_gate_state": GATE_CAUTIOUS,
            "scene_gate_reason": "weak_evidence_or_uncertain_env",
            "scene_gate_action": ACTION_CONTINUE_CAUTIOUS,
        }

    if goal_type in ("hold_for_floor", "recheck_environment"):
        return {
            "scene_type": SCENE_CLOSE_RANGE,
            "scene_supported": True,
            "scene_gate_state": GATE_OPEN,
            "scene_gate_reason": "close_range_or_floor_check",
            "scene_gate_action": ACTION_CONTINUE_NORMAL,
        }

    return {
        "scene_type": SCENE_NORMAL_WALK,
        "scene_supported": True,
        "scene_gate_state": GATE_OPEN,
        "scene_gate_reason": "normal_walk_navigation",
        "scene_gate_action": ACTION_CONTINUE_NORMAL,
    }
