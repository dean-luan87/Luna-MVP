# -*- coding: utf-8 -*-
"""
Confirmation Whitebox Trace M0（确认输入白盒轨迹）

目标：
- 不改 Confirmation Input Bridge 主逻辑
- 只解释「映射」与「推进」（type / next_effect）的原因
- 复用统一五块骨架 + 用户可见解释层
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


@dataclass
class ConfirmationReasoningStep:
    step_index: int
    step_name: str
    step_input_summary: Optional[str] = None
    step_output_summary: Optional[str] = None


@dataclass
class ConfirmationWeightItem:
    candidate_type_id: str
    candidate_human_label: Optional[str] = None
    weight_total: float = 0.0
    weight_components: Dict[str, float] = field(default_factory=dict)
    weight_reason: Optional[str] = None


@dataclass
class ConfirmationExclusionItem:
    excluded_type_id: str
    excluded_type_human_label: Optional[str] = None
    excluded_reason: Optional[str] = None
    excluded_at_stage: Optional[str] = None


@dataclass
class ConfirmationInteractionItem:
    system_prompt_summary: Optional[str] = None
    user_feedback_raw: Optional[str] = None
    mapped_confirmation_type: Optional[str] = None
    next_effect: Optional[str] = None
    interaction_effect_on_confirmation: Optional[str] = None


@dataclass
class ConfirmationUserVisibleExplanation:
    user_visible_reason_mapping: Optional[str] = None
    user_visible_reason_next_effect: Optional[str] = None
    user_visible_changed_search_direction: Optional[str] = None
    user_visible_excluded_alternative: Optional[str] = None


@dataclass
class ConfirmationWhiteboxTraceResult:
    reasoning_steps: List[ConfirmationReasoningStep] = field(default_factory=list)
    weight_allocation: List[ConfirmationWeightItem] = field(default_factory=list)
    exclusion_log: List[ConfirmationExclusionItem] = field(default_factory=list)
    interaction_trace: List[ConfirmationInteractionItem] = field(default_factory=list)
    user_visible_explanation: Optional[ConfirmationUserVisibleExplanation] = None
    whitebox_summary: Optional[str] = None
    whitebox_applied: bool = False


TYPE_HUMAN_LABELS = {
    "confirmed_yes": "肯定（是/有/对）",
    "confirmed_no": "否定（不是/没有）",
    "opened_container": "已打开容器",
    "occlusion_cleared": "遮挡已移开",
    "checked_and_not_found": "已检查但未找到",
    "target_found": "已找到目标",
    "target_not_found": "未找到目标",
    "cancelled": "取消本次查找",
    "unknown": "无法判断/未知",
}


EFFECT_HUMAN_LABELS = {
    "advance_to_recheck": "推进到补证",
    "mark_container_rejected": "否定容器方向",
    "mark_occlusion_cleared": "记录遮挡已清理",
    "mark_target_found": "标记已找到",
    "mark_target_not_found": "标记未找到",
    "cancel_search": "取消搜索",
    "none": "不推进",
}


def _type_human(type_id: Optional[str]) -> str:
    if not type_id:
        return "—"
    return TYPE_HUMAN_LABELS.get(type_id, type_id)


def _effect_human(effect: Optional[str]) -> str:
    if not effect:
        return "—"
    return EFFECT_HUMAN_LABELS.get(effect, effect)


def build_confirmation_whitebox_trace(
    *,
    confirmation_input_bridge: Any,
    object_search_interaction: Any = None,
    action_hint_copy: Any = None,
    grid_search_expansion: Any = None,
    recheck_planner: Any = None,
) -> ConfirmationWhiteboxTraceResult:
    """
    解释 confirmation_input_bridge 的 mapping 与 next_effect，并产出用户可见解释层。
    """
    raw_text = _get(confirmation_input_bridge, "confirmation_input_raw_text")
    mapped_type = _get(confirmation_input_bridge, "confirmation_input_type")
    source = _get(confirmation_input_bridge, "confirmation_input_source") or "none"
    target_flow = _get(confirmation_input_bridge, "confirmation_bridge_target_flow")
    next_effect = _get(confirmation_input_bridge, "confirmation_bridge_next_effect") or "none"
    applied = bool(_get(confirmation_input_bridge, "confirmation_bridge_applied", False))
    bridge_reason = _get(confirmation_input_bridge, "confirmation_bridge_reason")

    osi_flow = _get(object_search_interaction, "interaction_flow_type") if object_search_interaction else None
    osi_state = _get(object_search_interaction, "search_subtask_state") if object_search_interaction else None
    ah_primary = _get(action_hint_copy, "action_hint_primary") if action_hint_copy else None
    ah_confirm = _get(action_hint_copy, "action_hint_confirmation") if action_hint_copy else None
    exp_hint = _get(grid_search_expansion, "grid_search_expansion_hint") if grid_search_expansion else None
    recheck_action = _get(recheck_planner, "recheck_action") if recheck_planner else None

    # Step 1: read_confirmation_context
    in1_parts = [
        f"raw={raw_text or '—'}",
        f"explicit_type={(mapped_type or '—')}",
        f"source={source}",
        f"target_flow={(target_flow or osi_flow or '—')}",
        f"search_state={(osi_state or '—')}",
    ]
    if ah_primary:
        in1_parts.append("has_action_hint=yes")
    if exp_hint:
        in1_parts.append("has_grid_hint=yes")
    if recheck_action:
        in1_parts.append(f"recheck_action={recheck_action}")
    step1_in = "; ".join(in1_parts)
    step1_out = f"context_ready flow={(target_flow or osi_flow or '—')}"

    # Step 2: map_confirmation_type
    mapping_basis: List[str] = []
    if source == "explicit_injection":
        mapping_basis.append("explicit_injection_priority")
    if raw_text:
        t = str(raw_text).strip().lower()
        if any(k in t for k in ("打开",)):
            mapping_basis.append("keyword:打开")
        if any(k in t for k in ("取消", "不找了")):
            mapping_basis.append("keyword:取消")
        if any(k in t for k in ("移开", "清理", "挪开", "拿开")):
            mapping_basis.append("keyword:遮挡清理")
        if any(k in t for k in ("没有", "不是", "没找到", "不在")):
            mapping_basis.append("keyword:否定/未找到")
        if any(k in t for k in ("有", "对", "是", "找到了", "就是这个")):
            mapping_basis.append("keyword:肯定/找到")
        if any(k in t for k in ("看过", "检查了")):
            mapping_basis.append("keyword:检查过")
    if target_flow:
        mapping_basis.append(f"flow_ctx={target_flow}")
    step2_in = f"raw={raw_text or '—'}; source={source}; flow={target_flow or osi_flow or '—'}"
    step2_out = f"mapped_type={mapped_type or '—'} basis={','.join(mapping_basis) or 'none'}"

    # Step 3: select_next_effect
    eff_basis = []
    if target_flow:
        eff_basis.append(f"flow={target_flow}")
    if mapped_type:
        eff_basis.append(f"type={mapped_type}")
    if bridge_reason:
        eff_basis.append("bridge_reason_present")
    step3_in = f"mapped_type={mapped_type or '—'}; flow={target_flow or '—'}"
    step3_out = f"next_effect={next_effect} ({_effect_human(next_effect)}) basis={','.join(eff_basis) or 'none'}"

    # Step 4: compose_confirmation_outcome
    step4_in = f"applied={applied}; next_effect={next_effect}"
    step4_out = f"summary_ready"

    steps = [
        ConfirmationReasoningStep(1, "read_confirmation_context", step1_in, step1_out),
        ConfirmationReasoningStep(2, "map_confirmation_type", step2_in, step2_out),
        ConfirmationReasoningStep(3, "select_next_effect", step3_in, step3_out),
        ConfirmationReasoningStep(4, "compose_confirmation_outcome", step4_in, step4_out),
    ]

    # Weight allocation（规则权重，第一版写死；只用于解释）
    def score_type(type_id: str) -> ConfirmationWeightItem:
        comp: Dict[str, float] = {}
        total = 0.0
        rs: List[str] = []

        # A. 显式注入优先
        if source == "explicit_injection" and type_id == (mapped_type or ""):
            comp["explicit_input_priority"] = 0.90
            total += 0.90
            rs.append("explicit")

        # B. 文本映射基础分
        if raw_text:
            comp["text_keyword_match_bonus"] = 0.60
            total += 0.60
            rs.append("text_match")
            # flow alignment
            if (target_flow or "") and (
                (target_flow == "container_check_flow" and type_id in ("opened_container", "target_not_found", "target_found"))
                or (target_flow == "occlusion_clear_flow" and type_id in ("occlusion_cleared", "target_not_found", "target_found"))
            ):
                comp["flow_alignment_bonus"] = 0.20
                total += 0.20
                rs.append("flow_align")
            # action context
            if ah_primary or ah_confirm:
                comp["action_context_bonus"] = 0.10
                total += 0.10
                rs.append("has_hint_ctx")

        # C. 明确强信号（按 type）
        if type_id == "target_found":
            comp["target_found_bonus"] = 0.70
            total += 0.70
            rs.append("target_found")
        if type_id == "cancelled":
            comp["cancel_signal_bonus"] = 0.70
            total += 0.70
            rs.append("cancel_signal")
        if type_id == "opened_container":
            comp["opened_container_bonus"] = 0.60
            total += 0.60
            rs.append("opened_container")
        if type_id == "occlusion_cleared":
            comp["occlusion_cleared_bonus"] = 0.60
            total += 0.60
            rs.append("occlusion_cleared")
        if type_id == "checked_and_not_found":
            comp["checked_and_not_found_bonus"] = 0.55
            total += 0.55
            rs.append("checked_and_not_found")
        if type_id in ("confirmed_no", "target_not_found"):
            comp["negative_confirmation_bonus"] = 0.50
            total += 0.50
            rs.append("negative")

        # penalties（最低限支持）
        if not raw_text and source != "explicit_injection":
            comp["weak_match_penalty"] = -0.10
            total += -0.10
            rs.append("weak_match")
        if raw_text and mapped_type and type_id != mapped_type and type_id in ("target_found", "cancelled"):
            comp["conflicting_signal_penalty"] = -0.30
            total += -0.30
            rs.append("conflict")
        if target_flow == "container_check_flow" and type_id == "occlusion_cleared":
            comp["wrong_flow_penalty"] = -0.20
            total += -0.20
            rs.append("wrong_flow")
        if target_flow == "occlusion_clear_flow" and type_id == "opened_container":
            comp["wrong_flow_penalty"] = -0.20
            total += -0.20
            rs.append("wrong_flow")

        return ConfirmationWeightItem(
            candidate_type_id=type_id,
            candidate_human_label=_type_human(type_id),
            weight_total=round(total, 3),
            weight_components=comp,
            weight_reason=";".join(rs) if rs else None,
        )

    # 输出：selected + 1~2 个排除
    selected_id = mapped_type or "unknown"
    candidates = [
        selected_id,
        "cancelled" if selected_id != "cancelled" else "target_found",
        "target_found" if selected_id != "target_found" else "target_not_found",
    ]
    seen = set()
    weights: List[ConfirmationWeightItem] = []
    for cid in candidates:
        if cid in seen:
            continue
        seen.add(cid)
        weights.append(score_type(cid))

    # Exclusion log：映射排除 + next_effect 排除（最小 2 条）
    exclusions: List[ConfirmationExclusionItem] = []
    for ex_id in [c for c in ("cancelled", "target_found", "target_not_found") if c != selected_id][:2]:
        exclusions.append(
            ConfirmationExclusionItem(
                excluded_type_id=ex_id,
                excluded_type_human_label=_type_human(ex_id),
                excluded_reason="lower_score_or_context_mismatch",
                excluded_at_stage="map_confirmation_type",
            )
        )
    exclusions.append(
        ConfirmationExclusionItem(
            excluded_type_id=f"next_effect_not_{next_effect}",
            excluded_type_human_label="其他推进效果",
            excluded_reason="next_effect_selected_by_flow_and_type",
            excluded_at_stage="select_next_effect",
        )
    )

    # Interaction trace：必须能表达有输入/无输入
    if not raw_text and source == "none" and not mapped_type:
        interaction_effect = "no_confirmation_input_this_frame"
    else:
        # 最小语义：按 mapped_type/next_effect 输出影响
        interaction_effect = f"mapped={mapped_type or '—'};next={next_effect}"
        if next_effect == "cancel_search":
            interaction_effect = "cancelled;terminate_search"
        elif next_effect == "mark_target_found":
            interaction_effect = "target_found;end_search"
        elif next_effect == "mark_container_rejected":
            interaction_effect = "negative_signal;reject_container_path"
        elif next_effect == "mark_occlusion_cleared":
            interaction_effect = "occlusion_cleared;shift_to_recheck"
        elif next_effect == "advance_to_recheck":
            interaction_effect = "opened_or_yes;advance_to_recheck"

    interaction_trace = [
        ConfirmationInteractionItem(
            system_prompt_summary=(ah_confirm or ah_primary),
            user_feedback_raw=raw_text,
            mapped_confirmation_type=mapped_type,
            next_effect=next_effect,
            interaction_effect_on_confirmation=interaction_effect,
        )
    ]

    # User visible explanation（短句映射，不直出内部 JSON）
    uv_map = None
    uv_eff = None
    uv_changed = None
    uv_excl = None

    if source == "explicit_injection":
        uv_map = f"我按你给定的确认类型来理解：{_type_human(mapped_type)}。"
    else:
        uv_map = f"我把你这句理解为「{_type_human(mapped_type)}」。"

    uv_eff = f"因此我会执行推进：{_effect_human(next_effect)}。"

    if next_effect == "advance_to_recheck":
        uv_changed = "你的反馈让我继续沿当前方向做下一步复核。"
    elif next_effect in ("mark_container_rejected", "mark_target_not_found"):
        uv_changed = "你的反馈让我降低这一方向/位置的优先级，并尝试其它路径。"
    elif next_effect == "mark_target_found":
        uv_changed = "你的反馈让我结束当前搜索并恢复主任务。"
    elif next_effect == "cancel_search":
        uv_changed = "你选择取消，所以我终止本次搜索。"
    else:
        uv_changed = "当前反馈不触发推进，本帧只记录输入。"

    uv_excl = f"我没有把它理解成「{_type_human('target_found' if selected_id != 'target_found' else 'cancelled')}」，因为当前语句与上下文更符合已选类型。"

    user_visible = ConfirmationUserVisibleExplanation(
        user_visible_reason_mapping=uv_map,
        user_visible_reason_next_effect=uv_eff,
        user_visible_changed_search_direction=uv_changed,
        user_visible_excluded_alternative=uv_excl,
    )

    summary = (
        f"type={mapped_type or '—'} source={source} flow={(target_flow or osi_flow or '—')} "
        f"next={next_effect} applied={applied}"
    )
    return ConfirmationWhiteboxTraceResult(
        reasoning_steps=steps,
        weight_allocation=weights,
        exclusion_log=exclusions[:3],
        interaction_trace=interaction_trace,
        user_visible_explanation=user_visible,
        whitebox_summary=summary,
        whitebox_applied=applied,
    )

