# -*- coding: utf-8 -*-
"""
Confirmation Input Bridge M0：用户确认输入桥。

将用户对引导的反馈（我看了没有/我打开了/我移开了/对就是这个/不是这个）接回系统，
形成：推理 → 引导 → 用户反馈 → 系统推进。
只做输入桥 + 最小状态推进；不做完整对话引擎、不做动作执行器。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Tuple


# 最小确认输入类型（离散集合）
CONFIRMATION_INPUT_TYPES = (
    "confirmed_yes",
    "confirmed_no",
    "opened_container",
    "occlusion_cleared",
    "checked_and_not_found",
    "target_found",
    "target_not_found",
    "cancelled",
    "unknown",
)

# 推进效果（写死第一版）
NEXT_EFFECTS = (
    "advance_to_recheck",
    "mark_container_rejected",
    "mark_occlusion_cleared",
    "mark_target_found",
    "mark_target_not_found",
    "cancel_search",
    "none",
)


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def map_raw_text_to_confirmation_type(raw_text: Optional[str]) -> Tuple[Optional[str], str]:
    """
    从原始文本做最小规则映射到确认输入类型。
    返回 (mapped_type, source)，source 为 "text_mapped" 或 "none"。
    """
    if not raw_text or not isinstance(raw_text, str):
        return None, "none"
    t = raw_text.strip().lower()
    if not t:
        return None, "none"
    # 看过了没有 / 检查了没有（先于通用「没有」）
    if any(k in t for k in ("我看过了没有", "看过了没有", "看过没有", "检查了没有")):
        return "checked_and_not_found", "text_mapped"
    # 没有/不是/没找到
    if any(k in t for k in ("没有", "不是", "不在", "没找到", "不是这个")):
        return "target_not_found", "text_mapped"
    # 有/是/对/找到了
    if any(k in t for k in ("有", "是", "对", "找到了", "就是这个", "在的")):
        return "target_found", "text_mapped"
    # 打开了
    if any(k in t for k in ("打开了", "我打开了", "开过了")):
        return "opened_container", "text_mapped"
    # 移开/清理
    if any(k in t for k in ("移开了", "清理了", "我挪开了", "挪开了", "挡的拿开了")):
        return "occlusion_cleared", "text_mapped"
    # 取消
    if any(k in t for k in ("取消", "不找了")):
        return "cancelled", "text_mapped"
    return None, "none"


@dataclass
class ConfirmationInputBridgeResult:
    """Confirmation Input Bridge M0：用户确认输入与最小推进建议。"""
    confirmation_input_type: Optional[str] = None
    confirmation_input_raw_text: Optional[str] = None
    confirmation_input_source: Optional[str] = None  # explicit_injection / text_mapped / none
    confirmation_bridge_reason: Optional[str] = None
    confirmation_bridge_applied: bool = False
    confirmation_bridge_target_flow: Optional[str] = None
    confirmation_bridge_next_effect: Optional[str] = None


def build_confirmation_input_bridge(
    object_search_interaction: Any,
    confirmation_input_type: Optional[str] = None,
    confirmation_input_raw_text: Optional[str] = None,
) -> ConfirmationInputBridgeResult:
    """
    根据当前 search 的 flow / subtask 与用户确认输入，生成桥接结果与 next_effect。
    只读 search，不反写；next_effect 供 builder 做最小推进（如 terminal_status）。
    """
    flow_type = _get(object_search_interaction, "interaction_flow_type")
    subtask_state = _get(object_search_interaction, "search_subtask_state") or "searching"

    # 输入来源与类型
    input_type = (confirmation_input_type or "").strip() or None
    raw_text = (confirmation_input_raw_text or "").strip() or None
    source = "none"
    if input_type and input_type in CONFIRMATION_INPUT_TYPES:
        source = "explicit_injection"
    elif raw_text:
        mapped, src = map_raw_text_to_confirmation_type(raw_text)
        if mapped:
            input_type = mapped
            source = src

    if not input_type or input_type == "unknown":
        return ConfirmationInputBridgeResult(
            confirmation_input_type=input_type or None,
            confirmation_input_raw_text=raw_text or None,
            confirmation_input_source=source,
            confirmation_bridge_target_flow=flow_type,
            confirmation_bridge_reason="no_valid_input",
            confirmation_bridge_applied=False,
            confirmation_bridge_next_effect="none",
        )

    target_flow = flow_type
    next_effect = "none"
    reason_parts = [f"flow={flow_type}", f"input={input_type}"]

    # D. 任意 flow：取消
    if input_type == "cancelled":
        next_effect = "cancel_search"
        reason_parts.append("cancel_search")
    # A. 容器流
    elif flow_type == "container_check_flow":
        if input_type in ("opened_container", "confirmed_yes"):
            next_effect = "advance_to_recheck"
            reason_parts.append("advance_to_recheck")
        elif input_type in ("confirmed_no", "target_not_found"):
            next_effect = "mark_container_rejected"
            reason_parts.append("mark_container_rejected")
        elif input_type == "target_found":
            next_effect = "mark_target_found"
            reason_parts.append("mark_target_found")
    # B. 遮挡流
    elif flow_type == "occlusion_clear_flow":
        if input_type == "occlusion_cleared":
            next_effect = "mark_occlusion_cleared"
            reason_parts.append("mark_occlusion_cleared")
        elif input_type in ("checked_and_not_found", "target_not_found"):
            next_effect = "mark_target_not_found"
            reason_parts.append("mark_target_not_found")
        elif input_type == "target_found":
            next_effect = "mark_target_found"
            reason_parts.append("mark_target_found")
    # C. 一般搜索 / 其他
    else:
        if input_type == "target_found":
            next_effect = "mark_target_found"
            reason_parts.append("mark_target_found")
        elif input_type == "target_not_found":
            next_effect = "mark_target_not_found"
            reason_parts.append("mark_target_not_found")

    applied = next_effect != "none"
    return ConfirmationInputBridgeResult(
        confirmation_input_type=input_type,
        confirmation_input_raw_text=raw_text,
        confirmation_input_source=source,
        confirmation_bridge_target_flow=target_flow,
        confirmation_bridge_reason="+".join(reason_parts),
        confirmation_bridge_applied=applied,
        confirmation_bridge_next_effect=next_effect,
    )
