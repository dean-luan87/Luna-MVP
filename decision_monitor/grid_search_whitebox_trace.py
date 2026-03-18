# -*- coding: utf-8 -*-
"""
Grid Search Whitebox Trace M0（局部任务空间格搜索扩展白盒轨迹）

为 Grid-driven Search Expansion（建议层）提供白盒化结果结构：
- 推理过程（Reasoning Trace）
- 权重分配（Weight Allocation Trace）
- 排除逻辑（Exclusion Trace）
- 互动过程（Interaction Trace）

注意：本模块只做解释与审计，不改变 expansion 结果、不改主状态机、不做执行控制。
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
class GridSearchReasoningStep:
    step_index: int
    step_name: str
    step_input_summary: Optional[str] = None
    step_output_summary: Optional[str] = None


@dataclass
class GridSearchWeightItem:
    cell_id: str
    cell_human_label: Optional[str] = None
    weight_total: float = 0.0
    weight_components: Dict[str, float] = field(default_factory=dict)
    weight_reason: Optional[str] = None


@dataclass
class GridSearchExclusionItem:
    excluded_cell_id: str
    excluded_cell_human_label: Optional[str] = None
    excluded_reason: Optional[str] = None
    excluded_at_stage: Optional[str] = None  # primary_selection / secondary_selection


@dataclass
class GridSearchInteractionItem:
    system_prompt_summary: Optional[str] = None
    system_followup_summary: Optional[str] = None
    user_feedback_raw: Optional[str] = None
    mapped_confirmation_type: Optional[str] = None
    next_effect: Optional[str] = None
    interaction_effect_on_search: Optional[str] = None


@dataclass
class GridSearchWhiteboxTraceResult:
    reasoning_steps: List[GridSearchReasoningStep] = field(default_factory=list)
    weight_allocation: List[GridSearchWeightItem] = field(default_factory=list)
    exclusion_log: List[GridSearchExclusionItem] = field(default_factory=list)
    interaction_trace: List[GridSearchInteractionItem] = field(default_factory=list)
    whitebox_summary: Optional[str] = None
    whitebox_applied: bool = False


def _human_for(cell_id: Optional[str], grid: Any) -> Optional[str]:
    if not cell_id:
        return None
    for c in (_get(grid, "cells", None) or []):
        if _get(c, "cell_id") == cell_id:
            return _get(c, "cell_human_label")
    return None


def _same_row(a: str, b: str) -> bool:
    # cell_id: h_d
    try:
        return a.split("_", 1)[1] == b.split("_", 1)[1]
    except Exception:
        return False


def _same_col(a: str, b: str) -> bool:
    try:
        return a.split("_", 1)[0] == b.split("_", 1)[0]
    except Exception:
        return False


def build_grid_search_whitebox_trace(
    *,
    local_task_space_grid: Any,
    grid_search_expansion: Any,
    object_search_interaction: Any,
    action_hint_copy: Any,
    confirmation_input_bridge: Any,
) -> GridSearchWhiteboxTraceResult:
    grid = local_task_space_grid
    exp = grid_search_expansion
    flow = _get(object_search_interaction, "interaction_flow_type") or _get(exp, "expansion_flow_type")

    focus_cell = _get(grid, "focus_target_cell_id")
    container_cell = _get(grid, "container_candidate_cell_id")
    occlusion_cells = _get(grid, "occlusion_cell_ids", []) or []
    recommended = _get(grid, "recommended_search_cell_id")

    primary = _get(exp, "primary_search_cell_id")
    secondary: List[str] = list(_get(exp, "secondary_search_cell_ids", []) or [])
    strategy = _get(exp, "expansion_strategy_type") or "none"
    hint = _get(exp, "grid_search_expansion_hint")

    # ---- Interaction trace ----
    interaction: List[GridSearchInteractionItem] = []
    ah_primary = _get(action_hint_copy, "action_hint_primary")
    ah_follow = _get(action_hint_copy, "action_hint_followup")
    user_raw = _get(confirmation_input_bridge, "confirmation_input_raw_text")
    mapped_type = _get(confirmation_input_bridge, "confirmation_input_type")
    next_eff = _get(confirmation_input_bridge, "confirmation_bridge_next_effect")
    if user_raw or mapped_type or (next_eff and next_eff != "none"):
        effect = "feedback_present"
        # 仅描述影响（不反写 expansion）
        if mapped_type in ("confirmed_no", "target_not_found") and flow == "container_check_flow":
            effect = "container_rejected_signal;apply_rejection_penalty_in_trace"
        elif mapped_type == "occlusion_cleared" and flow == "occlusion_clear_flow":
            effect = "occlusion_cleared_signal;keep_primary_expand_secondary"
        elif mapped_type == "target_found":
            effect = "target_found;expansion_should_end"
        elif mapped_type == "cancelled":
            effect = "cancelled;expansion_should_end"
        interaction.append(
            GridSearchInteractionItem(
                system_prompt_summary=ah_primary,
                system_followup_summary=ah_follow,
                user_feedback_raw=user_raw,
                mapped_confirmation_type=mapped_type,
                next_effect=next_eff,
                interaction_effect_on_search=effect,
            )
        )
    else:
        interaction.append(GridSearchInteractionItem(interaction_effect_on_search="no_interaction_this_frame"))

    # ---- Reasoning steps ----
    steps: List[GridSearchReasoningStep] = []
    steps.append(
        GridSearchReasoningStep(
            step_index=1,
            step_name="read_context",
            step_input_summary=f"flow={flow}; focus={focus_cell}; container={container_cell}; occlusion={occlusion_cells}; recommended={recommended}",
            step_output_summary=f"strategy={strategy}",
        )
    )
    steps.append(
        GridSearchReasoningStep(
            step_index=2,
            step_name="select_primary",
            step_input_summary=f"focus={focus_cell}; container={container_cell}; occlusion={occlusion_cells}; recommended={recommended}",
            step_output_summary=f"primary={primary}",
        )
    )
    steps.append(
        GridSearchReasoningStep(
            step_index=3,
            step_name="select_secondary",
            step_input_summary=f"primary={primary}; secondary_limit=3; adjacent_from_grid=yes",
            step_output_summary=f"secondary={secondary}",
        )
    )
    steps.append(
        GridSearchReasoningStep(
            step_index=4,
            step_name="compose_hint",
            step_input_summary=f"primary={primary}; secondary={secondary}",
            step_output_summary=f"hint={hint}",
        )
    )

    # ---- Weight allocation ----
    weights: List[GridSearchWeightItem] = []
    exclusions: List[GridSearchExclusionItem] = []

    # 固定规则权重（写死第一版）
    if flow == "container_check_flow":
        base_primary_key = "container_priority_score"
        base_primary = 0.70
        focus_bonus = 0.20
        adjacency_bonus = 0.15
        same_line_bonus = 0.05  # same row
    elif flow == "occlusion_clear_flow":
        base_primary_key = "occlusion_priority_score"
        base_primary = 0.70
        focus_bonus = 0.20
        adjacency_bonus = 0.15
        same_line_bonus = 0.05  # same column
    else:
        base_primary_key = "focus_priority_score"
        base_primary = 0.60
        focus_bonus = 0.00
        adjacency_bonus = 0.20
        same_line_bonus = 0.10  # same band/row as proxy

    rejection_penalty = -0.40
    non_adjacent_penalty = -0.20
    weak_penalty = -0.10

    # 选择需要打分的 cell：primary、secondary（最多 3）、以及 1-2 个排除 cell
    scored_cells: List[str] = []
    if primary:
        scored_cells.append(primary)
    scored_cells.extend(secondary[:3])

    # 排除候选：优先 focus/container（若未被选中），再加一个“非邻接且未入选”的 cell
    if focus_cell and focus_cell not in scored_cells:
        scored_cells.append(focus_cell)
        exclusions.append(
            GridSearchExclusionItem(
                excluded_cell_id=focus_cell,
                excluded_cell_human_label=_human_for(focus_cell, grid),
                excluded_reason="not_primary_due_to_flow_priority_or_limit",
                excluded_at_stage="primary_selection",
            )
        )
    if container_cell and container_cell not in scored_cells:
        scored_cells.append(container_cell)
        exclusions.append(
            GridSearchExclusionItem(
                excluded_cell_id=container_cell,
                excluded_cell_human_label=_human_for(container_cell, grid),
                excluded_reason="not_selected_in_secondary_or_not_primary",
                excluded_at_stage="secondary_selection",
            )
        )
    # 再补一个排除格：第一个与 primary 不邻接且未入选的格（如果能找到）
    primary_adj = set()
    if primary:
        for c in (_get(grid, "cells", None) or []):
            if _get(c, "cell_id") == primary:
                primary_adj = set(_get(c, "adjacent_cell_ids", []) or [])
                break
    for c in (_get(grid, "cells", None) or []):
        cid = _get(c, "cell_id")
        if not cid or cid in scored_cells:
            continue
        if primary and cid not in primary_adj and cid != primary:
            scored_cells.append(cid)
            exclusions.append(
                GridSearchExclusionItem(
                    excluded_cell_id=cid,
                    excluded_cell_human_label=_human_for(cid, grid),
                    excluded_reason="non_adjacent_or_weak_relevance",
                    excluded_at_stage="secondary_selection",
                )
            )
            break

    # 去重保持顺序，最多 6 个
    _seen = set()
    scored_cells = [x for x in scored_cells if x and (x not in _seen and not _seen.add(x))]  # type: ignore
    scored_cells = scored_cells[:6]

    for cid in scored_cells:
        comp: Dict[str, float] = {}
        total = 0.0
        reasons: List[str] = []

        # base score
        if cid == primary:
            comp[base_primary_key] = base_primary
            total += base_primary
            reasons.append("is_primary")
        elif cid in secondary:
            comp["adjacency_bonus"] = adjacency_bonus
            total += adjacency_bonus
            reasons.append("is_secondary_or_adjacent")
        else:
            comp["weak_relevance_penalty"] = weak_penalty
            total += weak_penalty
            reasons.append("not_selected_candidate")

        # focus bonus
        if focus_cell and cid == focus_cell:
            comp["focus_bonus"] = focus_bonus if focus_bonus else 0.20
            total += comp["focus_bonus"]
            reasons.append("focus_cell")

        # container/occlusion special
        if flow == "container_check_flow" and container_cell and cid == container_cell and cid != primary:
            if "container_priority_score" not in comp:
                comp["container_priority_score"] = 0.70
                total += 0.70
            reasons.append("container_cell")
        if flow == "occlusion_clear_flow" and occlusion_cells and cid == occlusion_cells[0] and cid != primary:
            if "occlusion_priority_score" not in comp:
                comp["occlusion_priority_score"] = 0.70
                total += 0.70
            reasons.append("occlusion_cell")

        # same row/col bonus
        if primary and cid != primary:
            if flow == "container_check_flow" and _same_row(cid, primary):
                comp["same_row_bonus"] = same_line_bonus
                total += same_line_bonus
                reasons.append("same_row")
            if flow == "occlusion_clear_flow" and _same_col(cid, primary):
                comp["same_column_bonus"] = same_line_bonus
                total += same_line_bonus
                reasons.append("same_column")
            if flow not in ("container_check_flow", "occlusion_clear_flow") and _same_row(cid, primary):
                comp["same_band_bonus"] = same_line_bonus
                total += same_line_bonus
                reasons.append("same_band")

        # penalties based on interaction signal
        if mapped_type in ("confirmed_no", "target_not_found") and flow == "container_check_flow" and cid == container_cell:
            comp["confirmation_rejection_penalty"] = rejection_penalty
            total += rejection_penalty
            reasons.append("rejected_by_user_signal")
        if primary and cid != primary and (cid not in primary_adj) and (cid not in secondary):
            comp["non_adjacent_penalty"] = non_adjacent_penalty
            total += non_adjacent_penalty
            reasons.append("non_adjacent")

        weights.append(
            GridSearchWeightItem(
                cell_id=cid,
                cell_human_label=_human_for(cid, grid),
                weight_total=round(total, 3),
                weight_components=comp,
                weight_reason=";".join(reasons) if reasons else None,
            )
        )

    # ---- Summary ----
    excl_summary = ", ".join([e.excluded_cell_id for e in exclusions[:3]]) if exclusions else "—"
    summary = f"primary={primary}; secondary={','.join(secondary[:3]) if secondary else '—'}; strategy={strategy}; excluded={excl_summary}"

    return GridSearchWhiteboxTraceResult(
        reasoning_steps=steps,
        weight_allocation=weights,
        exclusion_log=exclusions[:3],
        interaction_trace=interaction,
        whitebox_summary=summary,
        whitebox_applied=bool(primary),
    )

