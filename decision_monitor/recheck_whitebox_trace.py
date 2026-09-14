# -*- coding: utf-8 -*-
"""
Recheck Whitebox Trace M0（补证链路白盒轨迹）

沿用已冻结 Whitebox Trace Schema（五块骨架）：
- reasoning_steps
- weight_allocation
- exclusion_log
- interaction_trace
- whitebox_summary / whitebox_applied

仅解释 recheck_planner 结果，不改 recheck_planner 主逻辑，不改主状态机，不做控制层升级。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .recheck_planner import RECHECK_ACTIONS


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


@dataclass
class RecheckReasoningStep:
    step_index: int
    step_name: str
    step_input_summary: Optional[str] = None
    step_output_summary: Optional[str] = None


@dataclass
class RecheckWeightItem:
    action_id: str
    action_human_label: Optional[str] = None
    weight_total: float = 0.0
    weight_components: Dict[str, float] = field(default_factory=dict)
    weight_reason: Optional[str] = None


@dataclass
class RecheckExclusionItem:
    excluded_action_id: str
    excluded_action_human_label: Optional[str] = None
    excluded_reason: Optional[str] = None
    excluded_at_stage: Optional[str] = None


@dataclass
class RecheckInteractionItem:
    system_prompt_summary: Optional[str] = None
    user_feedback_raw: Optional[str] = None
    mapped_confirmation_type: Optional[str] = None
    next_effect: Optional[str] = None
    interaction_effect_on_recheck: Optional[str] = None


@dataclass
class RecheckWhiteboxTraceResult:
    reasoning_steps: List[RecheckReasoningStep] = field(default_factory=list)
    weight_allocation: List[RecheckWeightItem] = field(default_factory=list)
    exclusion_log: List[RecheckExclusionItem] = field(default_factory=list)
    interaction_trace: List[RecheckInteractionItem] = field(default_factory=list)
    whitebox_summary: Optional[str] = None
    whitebox_applied: bool = False


def _action_human(action: Optional[str]) -> str:
    m = {
        "recheck_close_range": "近场补证",
        "recheck_environment": "环境补证",
        "look_forward": "看前方",
        "shift_view_left": "看左侧",
        "shift_view_right": "看右侧",
        "hold_and_confirm": "暂停并确认",
        "ask_user_for_clarification": "询问澄清",
    }
    return m.get(action or "", action or "—")


def build_recheck_whitebox_trace(
    *,
    recheck_planner: Any,
    object_search_interaction: Any,
    evidence_ledger: Any,
    hypothesis_layer: Any,
    confirmation_input_bridge: Any,
    action_hint_copy: Any,
    local_task_space_grid: Any = None,
    state: Any = None,
) -> RecheckWhiteboxTraceResult:
    """
    解释 recheck_planner 的补证结果与阻断，并给出显式权重、排除与互动摘要。
    """
    action = _get(recheck_planner, "recheck_action")
    blocked = bool(_get(recheck_planner, "recheck_blocked", False))
    block_reason = _get(recheck_planner, "recheck_block_reason")
    reason = _get(recheck_planner, "recheck_reason")
    target = _get(recheck_planner, "recheck_target")

    flow = _get(object_search_interaction, "interaction_flow_type") or "general"
    hyp_type = None
    if hypothesis_layer and _get(hypothesis_layer, "hypotheses"):
        hyp_type = _get(hypothesis_layer.hypotheses[0], "hypothesis_type")

    # evidence missing/conflict 摘要（最小）
    miss = None
    if evidence_ledger and _get(evidence_ledger, "entries"):
        miss_list = _get(evidence_ledger.entries[0], "missing_evidence") or []
        miss = ";".join((m or "")[:24] for m in miss_list[:2]) if miss_list else None

    # interaction
    ah_primary = _get(action_hint_copy, "action_hint_primary")
    user_raw = _get(confirmation_input_bridge, "confirmation_input_raw_text")
    mapped_type = _get(confirmation_input_bridge, "confirmation_input_type")
    next_eff = _get(confirmation_input_bridge, "confirmation_bridge_next_effect")
    interaction_effect = "no_interaction_this_frame"
    if user_raw or mapped_type or (next_eff and next_eff != "none"):
        interaction_effect = "feedback_present"
        if mapped_type in ("opened_container",):
            interaction_effect = "opened_container_signal;close_range_still_valid"
        elif mapped_type in ("occlusion_cleared",):
            interaction_effect = "occlusion_cleared_signal;reduce_environment_need"
        elif mapped_type in ("confirmed_no", "target_not_found"):
            interaction_effect = "negative_signal;reduce_current_scope_confidence"
        elif mapped_type == "target_found":
            interaction_effect = "target_found;recheck_should_end"
        elif mapped_type == "cancelled":
            interaction_effect = "cancelled;recheck_should_end"

    interaction_trace = [
        RecheckInteractionItem(
            system_prompt_summary=ah_primary,
            user_feedback_raw=user_raw,
            mapped_confirmation_type=mapped_type,
            next_effect=next_eff,
            interaction_effect_on_recheck=interaction_effect,
        )
    ]

    # reasoning steps（固定 4 步）
    steps: List[RecheckReasoningStep] = []
    steps.append(
        RecheckReasoningStep(
            step_index=1,
            step_name="read_recheck_context",
            step_input_summary=f"flow={flow}; hyp={hyp_type}; missing={miss}; action={action}; blocked={blocked}({block_reason}); confirmation={mapped_type}",
            step_output_summary=f"context=local_task_recheck; target={target}",
        )
    )
    steps.append(
        RecheckReasoningStep(
            step_index=2,
            step_name="select_recheck_action",
            step_input_summary=f"action_candidates={len(RECHECK_ACTIONS)}; flow={flow}",
            step_output_summary=f"selected={action} ({_action_human(action)}); reason={reason}",
        )
    )
    steps.append(
        RecheckReasoningStep(
            step_index=3,
            step_name="exclude_other_actions",
            step_input_summary=f"selected={action}; blocked={blocked}",
            step_output_summary="see exclusion_log",
        )
    )
    steps.append(
        RecheckReasoningStep(
            step_index=4,
            step_name="compose_recheck_outcome",
            step_input_summary=f"blocked={blocked}; block_reason={block_reason}",
            step_output_summary=f"summary={action or 'none'}; applied={bool(action) and (not blocked)}",
        )
    )

    # weights：显式规则权重（第一版写死）
    # context signals（最小）：
    focus_present = bool(local_task_space_grid and _get(local_task_space_grid, "focus_target_cell_id"))
    container_or_occ = flow in ("container_check_flow", "occlusion_clear_flow")
    wide_uncertainty = (not focus_present) and bool(miss)
    alignment_good = _get(state, "view_misaligned") is False if state is not None else None
    human_pending = _get(state, "human_check_pending") is True if state is not None else None

    def score(action_id: str) -> RecheckWeightItem:
        comp: Dict[str, float] = {}
        total = 0.0
        rs: List[str] = []

        # A. close_range
        if action_id == "recheck_close_range":
            comp["close_range_bonus"] = 0.60
            total += 0.60
            rs.append("close_range")
            if focus_present:
                comp["focus_present_bonus"] = 0.20
                total += 0.20
                rs.append("focus_present")
            if container_or_occ:
                comp["container_or_occlusion_bonus"] = 0.15
                total += 0.15
                rs.append("container_or_occlusion")

        # B. environment
        if action_id == "recheck_environment":
            comp["environment_bonus"] = 0.60
            total += 0.60
            rs.append("environment")
            if wide_uncertainty:
                comp["wide_uncertainty_bonus"] = 0.20
                total += 0.20
                rs.append("wide_uncertainty")
            if not focus_present:
                comp["no_clear_focus_bonus"] = 0.10
                total += 0.10
                rs.append("no_clear_focus")

        # C. look_forward
        if action_id == "look_forward":
            comp["look_forward_bonus"] = 0.40
            total += 0.40
            rs.append("look_forward")
            if alignment_good is True:
                comp["directional_alignment_bonus"] = 0.20
                total += 0.20
                rs.append("aligned")

        # D. hold_and_confirm
        if action_id == "hold_and_confirm":
            comp["hold_and_confirm_bonus"] = 0.50
            total += 0.50
            rs.append("hold_and_confirm")
            if human_pending:
                comp["human_input_needed_bonus"] = 0.20
                total += 0.20
                rs.append("human_pending")

        # penalties（支持）
        if blocked:
            comp["blocked_penalty"] = -0.80
            total += -0.80
            rs.append("blocked")
        if human_pending:
            comp["human_check_pending_penalty"] = -0.60
            total += -0.60
            rs.append("human_check_pending")
        if container_or_occ and action_id == "recheck_environment":
            comp["wrong_scope_penalty"] = -0.30
            total += -0.30
            rs.append("wrong_scope_for_local_flow")
        if miss:
            comp["weak_evidence_penalty"] = -0.10
            total += -0.10
            rs.append("missing_evidence")

        return RecheckWeightItem(
            action_id=action_id,
            action_human_label=_action_human(action_id),
            weight_total=round(total, 3),
            weight_components=comp,
            weight_reason=";".join(rs) if rs else None,
        )

    selected_id = action or "none"
    # weight_allocation：selected + 1~2 excluded
    candidates = ["recheck_close_range", "recheck_environment", "look_forward", "hold_and_confirm"]
    weights: List[RecheckWeightItem] = []
    if action:
        weights.append(score(action))
    # pick excluded candidates different from selected
    for a in candidates:
        if a == action:
            continue
        weights.append(score(a))
        if len(weights) >= (1 if action else 0) + 3:
            break

    # exclusion_log：至少 1 条
    exclusions: List[RecheckExclusionItem] = []
    for a in candidates:
        if a == action:
            continue
        ex_reason = None
        if blocked:
            ex_reason = f"blocked:{block_reason or 'blocked'}"
        elif flow in ("container_check_flow", "occlusion_clear_flow") and a == "recheck_environment":
            ex_reason = "local_flow;close_range_preferred"
        elif focus_present and a == "recheck_environment":
            ex_reason = "focus_present;environment_not_first"
        else:
            ex_reason = "lower_score_or_less_relevant"
        exclusions.append(
            RecheckExclusionItem(
                excluded_action_id=a,
                excluded_action_human_label=_action_human(a),
                excluded_reason=ex_reason,
                excluded_at_stage="exclude_other_actions",
            )
        )
        if len(exclusions) >= 3:
            break

    summary = f"action={action or 'none'} blocked={blocked}({block_reason or '—'}) flow={flow} hyp={hyp_type or '—'}"
    return RecheckWhiteboxTraceResult(
        reasoning_steps=steps,
        weight_allocation=weights,
        exclusion_log=exclusions[:3],
        interaction_trace=interaction_trace,
        whitebox_summary=summary,
        whitebox_applied=bool(action),
    )

