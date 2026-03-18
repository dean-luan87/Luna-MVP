# -*- coding: utf-8 -*-
"""
人工沟通校准器（Interaction Calibrator）：在关键边界动作前插入短确认，避免系统单方面误判。

Scene Gate 先判，本模块再决定是否需要人来复核一次。
第一版仅在三类场景触发：Scene Gate 即将 pause/freeze 且非绝对硬证据；
view_guard 长期偏航未恢复；runtime_domain degraded 未 frozen。
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from .schema import StateLayer

# blocking_level
BLOCKING_SOFT = "soft"
BLOCKING_CONFIRM_BEFORE_DEGRADE = "confirm_before_degrade"
BLOCKING_CONFIRM_BEFORE_FREEZE = "confirm_before_freeze"

# 默认超时（毫秒）
DEFAULT_TIMEOUT_MS = 15_000


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def evaluate(
    ctx: Dict[str, Any],
    state: StateLayer,
) -> Dict[str, Any]:
    """
    在 Scene Gate 轻量控制之后调用；根据当前 state 判断是否需要人工确认。
    仅当「需要确认且尚未收到回复」时，主循环应暂缓高代价动作。

    返回：human_check_needed, human_check_reason, human_check_question,
          human_check_blocking_level, human_check_timeout_ms, human_check_default_action。
    human_check_response / human_check_resolved 由 ctx 注入或主循环在收到回复后写入。
    """
    out = {
        "human_check_needed": False,
        "human_check_reason": None,
        "human_check_question": None,
        "human_check_blocking_level": None,
        "human_check_timeout_ms": None,
        "human_check_default_action": None,
    }
    # 若上一轮已收到回复或已解析，本次不再重复询问（由 builder 结合 ctx 处理）
    response = ctx.get("human_check_response")
    resolved = ctx.get("human_check_resolved")
    if response is not None or resolved is True:
        return out

    scene_gate_action = _get(state, "scene_gate_action")
    scene_gate_state = _get(state, "scene_gate_state")
    scene_supported = _get(state, "scene_supported")
    scene_type = _get(state, "scene_type")
    scene_gate_reason = _get(state, "scene_gate_reason") or ""
    view_misaligned = _get(state, "view_misaligned") is True
    view_correction_needed = _get(state, "view_correction_needed") is True
    runtime_domain_state = _get(state, "runtime_domain_state")
    frame_quality = _get(state, "frame_quality")
    vision_quality = _get(state, "vision_quality_state")

    # A. Scene Gate 准备执行 pause_goal_progress 或 freeze_to_minimum_mode，且非绝对硬证据
    if scene_gate_state == "suspended" and scene_gate_action in (
        "pause_goal_progress",
        "freeze_to_minimum_mode",
    ):
        # 硬证据：视觉完全不可用、长期不可用 → 不询问，直接执行
        if runtime_domain_state == "frozen" and (
            "vision_invalid" in scene_gate_reason
            or "long_unusable" in scene_gate_reason
            or (frame_quality == "INVALID" or vision_quality == "invalid")
        ):
            return out
        # 否则先询问
        if scene_gate_action == "freeze_to_minimum_mode":
            out["human_check_needed"] = True
            out["human_check_reason"] = "scene_gate_freeze_candidate"
            out["human_check_question"] = "当前环境变化异常，可能超出正常理解范围。是否先暂停高层判断？"
            out["human_check_blocking_level"] = BLOCKING_CONFIRM_BEFORE_FREEZE
            out["human_check_timeout_ms"] = DEFAULT_TIMEOUT_MS
            out["human_check_default_action"] = "freeze_to_minimum_mode"
            return out
        if scene_gate_action == "pause_goal_progress":
            out["human_check_needed"] = True
            out["human_check_reason"] = "scene_gate_pause_candidate"
            out["human_check_question"] = "当前环境不适合继续推进目标，是否先暂停观察？"
            out["human_check_blocking_level"] = BLOCKING_CONFIRM_BEFORE_DEGRADE
            out["human_check_timeout_ms"] = DEFAULT_TIMEOUT_MS
            out["human_check_default_action"] = "pause_goal_progress"
            return out

    # B. view_guard 长期偏航未恢复：suspended + view_misaligned
    if (
        scene_gate_state == "suspended"
        and view_misaligned
        and view_correction_needed
        and scene_type == "unsupported_view_context"
    ):
        out["human_check_needed"] = True
        out["human_check_reason"] = "view_guard_long_misaligned"
        out["human_check_question"] = "当前镜头可能没有对准前方，是否请调整到前方环境？"
        out["human_check_blocking_level"] = BLOCKING_CONFIRM_BEFORE_DEGRADE
        out["human_check_timeout_ms"] = DEFAULT_TIMEOUT_MS
        out["human_check_default_action"] = "pause_goal_progress"
        return out

    # C. runtime_domain degraded 但未 frozen：让用户帮忙确认
    if runtime_domain_state == "degraded":
        out["human_check_needed"] = True
        out["human_check_reason"] = "runtime_domain_degraded"
        out["human_check_question"] = "当前环境判断存在不确定性，是否继续当前任务？"
        out["human_check_blocking_level"] = BLOCKING_SOFT
        out["human_check_timeout_ms"] = DEFAULT_TIMEOUT_MS
        out["human_check_default_action"] = "continue_cautious"
        return out

    return out
