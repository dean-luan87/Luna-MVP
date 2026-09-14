# -*- coding: utf-8 -*-
"""
Action Hint Whitebox Trace M0（引导话术白盒轨迹）

沿用已冻结 Whitebox Trace Schema（五块骨架）+ 用户可见解释层：
- reasoning_steps
- weight_allocation
- exclusion_log
- interaction_trace
- user_visible_explanation（用户可见白盒层，短句映射，不直出内部 JSON）
- whitebox_summary / whitebox_applied

仅解释 action_hint_copy 结果，不改 Action Hint 主逻辑，不做对话引擎/NLG 重构/控制器升级。
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
class ActionHintReasoningStep:
    step_index: int
    step_name: str
    step_input_summary: Optional[str] = None
    step_output_summary: Optional[str] = None


@dataclass
class ActionHintWeightItem:
    hint_id: str
    hint_human_label: Optional[str] = None
    weight_total: float = 0.0
    weight_components: Dict[str, float] = field(default_factory=dict)
    weight_reason: Optional[str] = None


@dataclass
class ActionHintExclusionItem:
    excluded_hint_id: str
    excluded_hint_human_label: Optional[str] = None
    excluded_reason: Optional[str] = None
    excluded_at_stage: Optional[str] = None


@dataclass
class ActionHintInteractionItem:
    system_prompt_summary: Optional[str] = None
    user_feedback_raw: Optional[str] = None
    mapped_confirmation_type: Optional[str] = None
    next_effect: Optional[str] = None
    interaction_effect_on_hint: Optional[str] = None


@dataclass
class ActionHintUserVisibleExplanation:
    """用户可见白盒层：短句解释，不暴露内部 weight JSON。"""
    user_visible_reason_primary: Optional[str] = None
    user_visible_reason_followup: Optional[str] = None
    user_visible_reason_confirmation: Optional[str] = None
    user_visible_changed_by_feedback: Optional[str] = None
    user_visible_excluded_alternative: Optional[str] = None


@dataclass
class ActionHintWhiteboxTraceResult:
    reasoning_steps: List[ActionHintReasoningStep] = field(default_factory=list)
    weight_allocation: List[ActionHintWeightItem] = field(default_factory=list)
    exclusion_log: List[ActionHintExclusionItem] = field(default_factory=list)
    interaction_trace: List[ActionHintInteractionItem] = field(default_factory=list)
    user_visible_explanation: Optional[ActionHintUserVisibleExplanation] = None
    whitebox_summary: Optional[str] = None
    whitebox_applied: bool = False


# hint_id -> 人类可读标签
HINT_HUMAN_LABELS = {
    "primary_container": "容器检查主提示",
    "primary_occlusion": "遮挡移开主提示",
    "primary_general_search": "一般位置查看主提示",
    "bootstrap_description": "描述引导主提示",
    "followup_expand": "后续扩展提示",
    "confirm_target": "确认目标提示",
}


def _hint_human(hint_id: str) -> str:
    return HINT_HUMAN_LABELS.get(hint_id, hint_id or "—")


def build_action_hint_whitebox_trace(
    *,
    action_hint_copy: Any,
    object_search_interaction: Any,
    spatial_expression_sidecar: Any,
    grid_search_expansion: Any = None,
    confirmation_input_bridge: Any = None,
    local_task_space_grid: Any = None,
    evidence_ledger: Any = None,
    hypothesis_layer: Any = None,
) -> ActionHintWhiteboxTraceResult:
    """
    解释 action_hint_copy 的主提示/后续/确认话术选择，并产出用户可见解释层。
    """
    primary = _get(action_hint_copy, "action_hint_primary")
    followup = _get(action_hint_copy, "action_hint_followup")
    confirmation = _get(action_hint_copy, "action_hint_confirmation")
    stage = _get(action_hint_copy, "action_hint_stage")
    reason = _get(action_hint_copy, "action_hint_reason")
    applied = bool(_get(action_hint_copy, "action_hint_applied", False))

    flow_type = _get(object_search_interaction, "interaction_flow_type") or "general"
    loc = _get(spatial_expression_sidecar, "focus_target_expression")
    actionable = _get(spatial_expression_sidecar, "focus_target_actionable_expression")
    grid_hint = _get(grid_search_expansion, "grid_search_expansion_hint") if grid_search_expansion else None
    rec_label = _get(local_task_space_grid, "recommended_search_cell_human_label") if local_task_space_grid else None

    user_raw = _get(confirmation_input_bridge, "confirmation_input_raw_text") if confirmation_input_bridge else None
    mapped_type = _get(confirmation_input_bridge, "confirmation_input_type") if confirmation_input_bridge else None
    next_eff = _get(confirmation_input_bridge, "confirmation_bridge_next_effect") if confirmation_input_bridge else None

    # 当前主提示类型
    if flow_type == "description_bootstrap_flow" or stage == "reasoning":
        primary_hint_id = "bootstrap_description"
    elif flow_type == "container_check_flow":
        primary_hint_id = "primary_container"
    elif flow_type == "occlusion_clear_flow":
        primary_hint_id = "primary_occlusion"
    else:
        primary_hint_id = "primary_general_search"

    # ---------- Step 1: read_hint_context ----------
    ctx_parts = [f"flow={flow_type}", f"stage={stage}"]
    if loc:
        ctx_parts.append(f"focus_expr={loc}")
    if actionable:
        ctx_parts.append("actionable_expression=yes")
    if rec_label:
        ctx_parts.append(f"grid_rec={rec_label}")
    if mapped_type or next_eff:
        ctx_parts.append(f"confirmation={mapped_type} next={next_eff}")
    ctx_in = "; ".join(ctx_parts)
    ctx_out = f"primary_type={primary_hint_id} primary_len={len(primary or '')}"

    # ---------- Step 2: select_primary_hint ----------
    step2_in = f"candidates=container|occlusion|general|bootstrap; flow={flow_type}"
    step2_out = f"selected={primary_hint_id} ({_hint_human(primary_hint_id)}); primary_preview={(primary or '')[:40]}..."

    # ---------- Step 3: select_followup_and_confirmation ----------
    step3_in = f"grid_hint={bool(grid_hint)}; primary={primary_hint_id}"
    step3_out = f"followup={'grid_influenced' if grid_hint else 'default'}; confirmation=target_short_or_default"

    # ---------- Step 4: compose_hint_outcome ----------
    feedback_affected = bool(user_raw or (mapped_type and mapped_type != "none"))
    step4_in = f"feedback_present={feedback_affected}; grid_rec={bool(rec_label)}"
    step4_out = f"summary=primary={primary_hint_id}; applied={applied}; feedback_affected={feedback_affected}"

    steps = [
        ActionHintReasoningStep(1, "read_hint_context", ctx_in, ctx_out),
        ActionHintReasoningStep(2, "select_primary_hint", step2_in, step2_out),
        ActionHintReasoningStep(3, "select_followup_and_confirmation", step3_in, step3_out),
        ActionHintReasoningStep(4, "compose_hint_outcome", step4_in, step4_out),
    ]

    # ---------- Weight allocation（规则权重，第一版写死）----------
    def score_hint(hint_id: str) -> ActionHintWeightItem:
        comp: Dict[str, float] = {}
        total = 0.0
        rs: List[str] = []

        if hint_id == "primary_container":
            comp["container_hint_bonus"] = 0.70
            total += 0.70
            rs.append("container_flow")
            if actionable:
                comp["actionable_expression_bonus"] = 0.15
                total += 0.15
                rs.append("actionable")
            comp["container_name_bonus"] = 0.10
            total += 0.10
            rs.append("container_name")
        elif hint_id == "primary_occlusion":
            comp["occlusion_hint_bonus"] = 0.70
            total += 0.70
            rs.append("occlusion_flow")
            if loc:
                comp["near_field_bonus"] = 0.15
                total += 0.15
                rs.append("near_field")
            comp["focus_location_bonus"] = 0.10
            total += 0.10
            rs.append("focus_location")
        elif hint_id == "primary_general_search":
            comp["general_search_bonus"] = 0.50
            total += 0.50
            rs.append("general_search")
            if loc:
                comp["focus_present_bonus"] = 0.20
                total += 0.20
                rs.append("focus_present")
            if rec_label or grid_hint:
                comp["grid_support_bonus"] = 0.10
                total += 0.10
                rs.append("grid_support")
        elif hint_id == "bootstrap_description":
            comp["bootstrap_bonus"] = 0.60
            total += 0.60
            rs.append("bootstrap")
            comp["target_unclear_bonus"] = 0.20
            total += 0.20
            rs.append("target_unclear")
        elif hint_id == "followup_expand":
            comp["grid_followup_bonus"] = 0.20
            total += 0.20
            rs.append("grid_followup")
        elif hint_id == "confirm_target":
            comp["confirmation_phrase_bonus"] = 0.20
            total += 0.20
            rs.append("confirmation_phrase")

        if flow_type == "container_check_flow" and hint_id == "primary_occlusion":
            comp["wrong_flow_penalty"] = -0.30
            total += -0.30
            rs.append("wrong_flow")
        if flow_type == "occlusion_clear_flow" and hint_id == "primary_container":
            comp["wrong_flow_penalty"] = -0.30
            total += -0.30
            rs.append("wrong_flow")
        if mapped_type in ("confirmed_no", "target_not_found") and hint_id == "primary_container":
            comp["feedback_conflict_penalty"] = -0.30
            total += -0.30
            rs.append("feedback_conflict")

        return ActionHintWeightItem(
            hint_id=hint_id,
            hint_human_label=_hint_human(hint_id),
            weight_total=round(total, 3),
            weight_components=comp,
            weight_reason=";".join(rs) if rs else None,
        )

    weights: List[ActionHintWeightItem] = []
    weights.append(score_hint(primary_hint_id))
    others = [x for x in ("primary_container", "primary_occlusion", "primary_general_search", "bootstrap_description") if x != primary_hint_id]
    for o in others[:2]:
        weights.append(score_hint(o))
    if grid_hint or followup:
        weights.append(score_hint("followup_expand"))

    # ---------- Exclusion log ----------
    exclusions: List[ActionHintExclusionItem] = []
    for o in others[:3]:
        ex_reason = "lower_score_or_different_flow"
        if (flow_type == "container_check_flow" and o == "primary_occlusion") or (flow_type == "occlusion_clear_flow" and o == "primary_container"):
            ex_reason = "current_flow_prefers_other"
        elif o == "bootstrap_description" and primary_hint_id != "bootstrap_description":
            ex_reason = "target_not_unclear"
        exclusions.append(
            ActionHintExclusionItem(
                excluded_hint_id=o,
                excluded_hint_human_label=_hint_human(o),
                excluded_reason=ex_reason,
                excluded_at_stage="select_primary_hint",
            )
        )
    exclusions.append(
        ActionHintExclusionItem(
            excluded_hint_id="followup_other",
            excluded_hint_human_label="其他后续路径",
            excluded_reason="grid_expansion_or_default_followup_selected",
            excluded_at_stage="select_followup_and_confirmation",
        )
    )

    # ---------- Interaction trace ----------
    interaction_effect = "no_interaction_this_frame"
    if user_raw or mapped_type or (next_eff and next_eff != "none"):
        interaction_effect = "feedback_present"
        if mapped_type == "opened_container":
            interaction_effect = "opened_container;confirmation_leans_container"
        elif mapped_type == "occlusion_cleared":
            interaction_effect = "occlusion_cleared;hint_can_shift_to_confirm"
        elif mapped_type in ("confirmed_no", "target_not_found"):
            interaction_effect = "negative_signal;reduce_scope_confidence"
        elif mapped_type == "target_found":
            interaction_effect = "target_found;hint_converge"

    interaction_trace = [
        ActionHintInteractionItem(
            system_prompt_summary=primary,
            user_feedback_raw=user_raw,
            mapped_confirmation_type=mapped_type,
            next_effect=next_eff,
            interaction_effect_on_hint=interaction_effect,
        )
    ]

    # ---------- User visible explanation（用户可见白盒层）----------
    uv_primary = None
    uv_followup = None
    uv_confirmation = None
    uv_changed = None
    uv_excluded = None

    if primary_hint_id == "primary_container":
        uv_primary = "我之所以先让你看容器里，是因为当前目标更像在容器里。"
    elif primary_hint_id == "primary_occlusion":
        uv_primary = "我让你先移开遮挡，是因为目标位置已经比较明确，但那里可能被挡住了。"
    elif primary_hint_id == "primary_general_search":
        uv_primary = "我先让你看这个位置，是因为当前线索指向这里。"
    elif primary_hint_id == "bootstrap_description":
        uv_primary = "我先让你描述外观，是因为当前目标还不够明确。"

    if grid_hint or rec_label:
        uv_followup = "我让你再看附近区域，是因为相邻格还有相关候选。"
    else:
        uv_followup = "我建议的后续步骤是根据当前搜索状态来的。"

    uv_confirmation = "我让你确认一下，是因为当前证据已经接近目标，但还差最终确认。"

    if feedback_affected:
        if mapped_type == "opened_container":
            uv_changed = "你刚才说「打开了」，所以我继续保留容器方向的补证。"
        elif mapped_type in ("confirmed_no", "target_not_found"):
            uv_changed = "你刚才说「没有」，所以我降低了这个方向的优先级。"
        elif mapped_type == "occlusion_cleared":
            uv_changed = "你刚才说遮挡移开了，所以后续提示会偏确认那个位置。"
        else:
            uv_changed = "你刚才的反馈影响了当前话术的侧重点。"
    else:
        uv_changed = "本帧暂无用户反馈，话术未因反馈改变。"

    uv_excluded = f"我暂时没有先让你走另一条话术路径（如{_hint_human(others[0]) if others else '其他'}），因为当前 flow 与证据更符合已选提示。"

    user_visible = ActionHintUserVisibleExplanation(
        user_visible_reason_primary=uv_primary,
        user_visible_reason_followup=uv_followup,
        user_visible_reason_confirmation=uv_confirmation,
        user_visible_changed_by_feedback=uv_changed,
        user_visible_excluded_alternative=uv_excluded,
    )

    summary = f"primary={primary_hint_id} flow={flow_type} stage={stage} feedback={feedback_affected} applied={applied}"
    return ActionHintWhiteboxTraceResult(
        reasoning_steps=steps,
        weight_allocation=weights,
        exclusion_log=exclusions[:4],
        interaction_trace=interaction_trace,
        user_visible_explanation=user_visible,
        whitebox_summary=summary,
        whitebox_applied=applied,
    )
