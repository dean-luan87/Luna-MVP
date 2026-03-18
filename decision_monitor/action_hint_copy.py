# -*- coding: utf-8 -*-
"""
Action Hint Copy M0：从推理到引导，再到确认。

仅文案级动作提示：先看哪里、先检查什么、先移开什么、再确认什么。
不做动作控制、不改主状态机、不反写 evidence/hypothesis/recheck/arbitration/bundle。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _container_display(name: Optional[str]) -> str:
    if not (name or "").strip():
        return "容器"
    c = (name or "").strip().lower()
    return {"cup": "杯子", "bottle": "瓶子", "bowl": "碗"}.get(c, c)


@dataclass
class ActionHintCopyResult:
    """Action Hint Copy M0：推理→引导→确认 文案链（单条主提示+后续+确认）。"""
    action_hint_stage: Optional[str] = None  # reasoning / guidance / confirmation
    action_hint_summary: Optional[str] = None
    action_hint_primary: Optional[str] = None
    action_hint_followup: Optional[str] = None
    action_hint_confirmation: Optional[str] = None
    action_hint_reason: Optional[str] = None
    action_hint_applied: bool = False


def build_action_hint_copy(
    object_search_interaction: Any,
    spatial_expression_sidecar: Any,
    object_temporal_ledger: Any,
    evidence_ledger: Any = None,
    hypothesis_layer: Any = None,
    recheck_planner: Any = None,
) -> ActionHintCopyResult:
    """
    基于 object_search、sidecar、ledger 等生成「推理→引导→确认」文案链。
    只读上述模块，不反写。当前只做单条主提示+后续+确认。
    """
    flow_type = _get(object_search_interaction, "interaction_flow_type")
    action = _get(object_search_interaction, "interaction_action")
    subtask_state = _get(object_search_interaction, "search_subtask_state") or "searching"

    # 主提示用 Level 1 短位词（中间偏左/中间偏右），避免「在…那个杯子里」整句再塞进「先看…里」造成重复
    loc = (_get(spatial_expression_sidecar, "focus_target_expression") or "").strip() or None

    entry = _get(object_temporal_ledger, "focus_object_entry")
    container_candidate = _get(entry, "current_container_candidate") if entry else None
    container_name = _container_display(container_candidate) if container_candidate else None
    target_label = _get(entry, "object_label") if entry else None
    target_short = (target_label or "目标")[:10] if target_label else "目标"

    stage = "guidance"
    primary: Optional[str] = None
    followup: Optional[str] = None
    confirmation: Optional[str] = None
    reason_parts: list = []

    # D. 目标不清 / description_bootstrap
    if subtask_state in ("target_unclear", "gathering_description") or flow_type == "description_bootstrap_flow":
        stage = "reasoning"
        primary = "请先描述一下目标的大概外观"
        followup = "比如颜色、大小或放在什么附近"
        confirmation = "描述后我再帮你缩小范围"
        reason_parts.append("target_unclear_or_description_bootstrap")
    # A. 容器流
    elif flow_type == "container_check_flow" or action in ("ask_user_to_open_container", "ask_if_in_container"):
        if loc and container_name:
            primary = f"先看{loc}那个{container_name}里"
        else:
            primary = f"先检查右边那个{container_name}里面" if container_name else "先检查目标容器里面"
        followup = "如果没看到，再回到最后可信位置继续找"
        confirmation = f"确认一下{container_name}里是不是{target_short}" if container_name else "看看里面有没有目标"
        reason_parts.append("container_check_flow")
        if _get(spatial_expression_sidecar, "focus_target_actionable_expression"):
            reason_parts.append("actionable_expression")
        if container_candidate:
            reason_parts.append("container_candidate")
    # B. 遮挡流
    elif flow_type == "occlusion_clear_flow" or action == "ask_user_to_clear_occlusion":
        if loc:
            primary = f"先把{loc}的遮挡移开看看"
        else:
            primary = "先把中间偏左位置前面的遮挡物移开看看"
        followup = "移开后再看看那个位置"
        confirmation = "看看遮挡后面有没有目标"
        reason_parts.append("occlusion_clear_flow")
        if loc:
            reason_parts.append("near_field")
    # C. 一般搜索流
    elif loc:
        primary = f"先看{loc}的位置"
        followup = "如果没看到，再往附近找一找"
        confirmation = "看看那个位置是不是目标"
        reason_parts.append("general_search")
        reason_parts.append("focus_location")
    else:
        primary = "先查看目标区域"
        followup = "如果还不确定，请告诉我你现在看到什么"
        confirmation = "确认一下那里有没有目标"
        reason_parts.append("general_fallback")

    reason_str = "+".join(reason_parts) if reason_parts else None
    summary_parts = [p for p in (primary, followup, confirmation) if p]
    summary = "；".join(summary_parts) if summary_parts else None
    applied = bool(primary)

    return ActionHintCopyResult(
        action_hint_stage=stage,
        action_hint_summary=summary,
        action_hint_primary=primary,
        action_hint_followup=followup,
        action_hint_confirmation=confirmation,
        action_hint_reason=reason_str,
        action_hint_applied=applied,
    )
