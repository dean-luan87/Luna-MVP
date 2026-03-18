# -*- coding: utf-8 -*-
"""
主线 1.3C：运行域守卫（Runtime Domain Guard）。

最小规则型：识别当前场景是否超出正常理解域（view_misaligned / vision_unusable / high_rotation_or_abnormal_motion），
并在必要时进入认知降级（normal / degraded / frozen），输出 degrade_action 与 recovery_condition。
不做复杂 IMU 融合、高阶运动模型。
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .schema import StateLayer, DecisionLayer

# 异常运动阈值：超过则视为 high_rotation_or_abnormal_motion（来自 ctx.motion_instability 等）
MOTION_ABNORMAL_HIGH = 0.9
MOTION_ABNORMAL_DEGRADED = 0.75


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def evaluate(
    ctx: Dict[str, Any],
    state: StateLayer,
    _decision: Optional[DecisionLayer] = None,
) -> Dict[str, Any]:
    """
    在 state_tracker -> view_guard -> predictive_hold 之后调用；
    基于 state 与 ctx 判断运行域是否失配，输出 8 个字段。
    """
    view_misaligned = _get(state, "view_misaligned")
    vision_quality = _get(state, "vision_quality_state")
    vision_degraded = _get(state, "vision_degraded")
    hold_active = _get(state, "predictive_hold_active")
    hold_allowed = _get(state, "predictive_hold_allowed")

    motion_instability = ctx.get("motion_instability")
    if motion_instability is None and ctx.get("pipeline_result"):
        motion_instability = _get(ctx["pipeline_result"], "motion_instability")
    motion_instability = float(motion_instability) if motion_instability is not None else 0.0

    mismatches: List[str] = []
    if view_misaligned is True:
        mismatches.append("view_misaligned")

    vision_unusable = False
    if vision_quality == "invalid":
        vision_unusable = True
    elif vision_degraded is True and not (hold_active or hold_allowed):
        vision_unusable = True
    if vision_unusable:
        mismatches.append("vision_unusable")

    high_rotation = False
    if motion_instability >= MOTION_ABNORMAL_DEGRADED:
        high_rotation = True
        mismatches.append("high_rotation_or_abnormal_motion")

    domain_mismatch_detected = len(mismatches) > 0
    domain_mismatch_reason = ";".join(mismatches) if mismatches else None

    if not domain_mismatch_detected:
        return {
            "runtime_domain_state": "normal",
            "runtime_domain_confidence": 1.0,
            "domain_mismatch_detected": False,
            "domain_mismatch_reason": None,
            "cognitive_degrade_level": "none",
            "cognitive_output_allowed": True,
            "degrade_action": None,
            "recovery_condition": None,
        }

    # 严重程度：frozen > degraded
    frozen = (
        vision_quality == "invalid"
        or motion_instability >= MOTION_ABNORMAL_HIGH
    )
    if frozen:
        runtime_domain_state = "frozen"
        cognitive_degrade_level = "high"
        cognitive_output_allowed = False
        if vision_quality == "invalid":
            degrade_action = "freeze_to_minimum_mode"
            recovery_condition = "vision_restored"
        else:
            degrade_action = "freeze_to_minimum_mode"
            recovery_condition = "motion_normalized"
        confidence = 0.2
    else:
        runtime_domain_state = "degraded"
        cognitive_degrade_level = "low"
        cognitive_output_allowed = True
        if "vision_unusable" in mismatches:
            degrade_action = "recheck_environment"
            recovery_condition = "vision_restored"
        elif "view_misaligned" in mismatches and "high_rotation_or_abnormal_motion" not in mismatches:
            degrade_action = "warn_user"
            recovery_condition = "view_aligned"
        elif "high_rotation_or_abnormal_motion" in mismatches:
            degrade_action = "warn_user"
            recovery_condition = "motion_normalized"
        else:
            degrade_action = "recheck_environment"
            recovery_condition = "vision_restored"
        confidence = 0.5

    return {
        "runtime_domain_state": runtime_domain_state,
        "runtime_domain_confidence": confidence,
        "domain_mismatch_detected": True,
        "domain_mismatch_reason": domain_mismatch_reason,
        "cognitive_degrade_level": cognitive_degrade_level,
        "cognitive_output_allowed": cognitive_output_allowed,
        "degrade_action": degrade_action,
        "recovery_condition": recovery_condition,
    }
