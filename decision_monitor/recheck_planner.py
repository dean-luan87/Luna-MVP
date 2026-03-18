# -*- coding: utf-8 -*-
"""
补证规划 M0：Recheck Planner（最小补证执行入口）。

在 Hypothesis Layer M0 基础上，将 verification_hint / suggested_next_check 推进为最小可执行补证入口。
仅读取已有结构，不做多步规划、不做学习、不改 detector/OCR 主链。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

from .evidence_ledger import EvidenceLedger
from .hypothesis_layer import HypothesisLayer
from .local_goal_spatial_map import LocalGoalSpatialMap

RECHECK_ACTIONS = (
    "recheck_environment",
    "recheck_close_range",
    "hold_and_confirm",
    "look_forward",
    "shift_view_left",
    "shift_view_right",
    "ask_user_for_clarification",
)


@dataclass
class RecheckPlannerResult:
    """最小补证规划结果：动作、原因、目标、优先级、是否阻断、是否已执行。"""
    recheck_action: Optional[str] = None
    recheck_reason: Optional[str] = None
    recheck_target: Optional[str] = None
    recheck_priority: Optional[str] = None  # 规则型，如 high / normal / low
    recheck_blocked: bool = False
    recheck_block_reason: Optional[str] = None
    recheck_applied: bool = False


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _is_blocked(state: Any) -> tuple[bool, Optional[str]]:
    """
    风险与守底阻断：minimum_mode_active、runtime_domain_state==frozen、
    scene_gate_action==freeze_to_minimum_mode、high_level_output_suppressed、human_check_pending。
    """
    if state is None:
        return False, None
    if _get(state, "minimum_mode_active") is True:
        return True, "minimum_mode_active"
    if _get(state, "runtime_domain_state") == "frozen":
        return True, "runtime_domain_state=frozen"
    if _get(state, "scene_gate_action") == "freeze_to_minimum_mode":
        return True, "scene_gate_action=freeze_to_minimum_mode"
    if _get(state, "high_level_output_suppressed") is True:
        return True, "high_level_output_suppressed"
    if _get(state, "human_check_pending") is True:
        return True, "human_check_pending"
    return False, None


def _target_from_smap(smap: Optional[LocalGoalSpatialMap]) -> Optional[str]:
    """从 smap 取简短 target 摘要（focus/confirm/risk 区）。"""
    if not smap:
        return None
    parts = []
    focus = getattr(smap, "focus_region", None) or []
    confirm = getattr(smap, "confirm_region", None) or []
    risk = getattr(smap, "risk_region", None) or []
    if focus:
        parts.append("focus")
    if confirm:
        parts.append("confirm")
    if risk:
        parts.append("risk")
    return ",".join(parts) if parts else None


def build_recheck_planner(
    hypothesis_layer: Optional[HypothesisLayer],
    evidence_ledger: Optional[EvidenceLedger],
    state: Any,
    smap: Optional[LocalGoalSpatialMap],
) -> RecheckPlannerResult:
    """
    从 hypothesis_layer（首条 verification_hint）或 evidence_ledger（首条 suggested_next_check）生成最小补证计划。
    受阻断时 recheck_blocked=True，recheck_applied=False。
    """
    blocked, block_reason = _is_blocked(state)
    action: Optional[str] = None
    reason: Optional[str] = None
    target: Optional[str] = _target_from_smap(smap)
    priority = "normal"

    # A. 优先 hypothesis 首条
    if hypothesis_layer and getattr(hypothesis_layer, "hypotheses", None):
        first_h = hypothesis_layer.hypotheses[0]
        hint = _get(first_h, "verification_hint")
        if hint and hint in RECHECK_ACTIONS:
            action = hint
            reason = (_get(first_h, "hypothesis_summary") or "")[:60]
            miss = _get(first_h, "missing_evidence") or []
            if miss:
                reason += " [" + "; ".join((m or "")[:25] for m in miss[:2]) + "]"
            target = target or _get(first_h, "hypothesis_type")

    # B. 无 hypothesis 则用 evidence_ledger 首条 claim
    if not action and evidence_ledger and getattr(evidence_ledger, "entries", None):
        first_c = evidence_ledger.entries[0]
        sug = _get(first_c, "suggested_next_check")
        if sug and sug in RECHECK_ACTIONS:
            action = sug
            reason = (_get(first_c, "claim_summary") or "")[:60]
            miss = _get(first_c, "missing_evidence") or []
            if miss:
                reason += " [" + "; ".join((m or "")[:25] for m in miss[:2]) + "]"
            target = target or "claim"

    # C. 无 hypothesis / claim 则无动作
    if not action:
        return RecheckPlannerResult(
            recheck_action=None,
            recheck_reason=None,
            recheck_target=target,
            recheck_priority=priority,
            recheck_blocked=blocked,
            recheck_block_reason=block_reason,
            recheck_applied=False,
        )

    applied = not blocked
    return RecheckPlannerResult(
        recheck_action=action,
        recheck_reason=reason,
        recheck_target=target,
        recheck_priority=priority,
        recheck_blocked=blocked,
        recheck_block_reason=block_reason,
        recheck_applied=applied,
    )
