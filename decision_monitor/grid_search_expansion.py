# -*- coding: utf-8 -*-
"""
Grid-driven Search Expansion M0（基于任务空间格的搜索扩展建议）

只产出建议层结果：
- primary_search_cell
- secondary_search_cells（最多 2~3）
- expansion_reason / summary

不做动作执行、不改 object_search_interaction 主状态机、不做路径规划/环境模型/持久化。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional, Sequence


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


@dataclass
class GridSearchExpansionResult:
    primary_search_cell_id: Optional[str] = None
    primary_search_cell_human_label: Optional[str] = None
    secondary_search_cell_ids: List[str] = field(default_factory=list)
    secondary_search_cell_human_labels: List[str] = field(default_factory=list)
    expansion_flow_type: Optional[str] = None
    expansion_strategy_type: Optional[str] = None
    expansion_reason: Optional[str] = None
    expansion_summary: Optional[str] = None
    expansion_applied: bool = False
    # 用于文案轻接入的短 hint（不替代原语义）
    grid_search_expansion_hint: Optional[str] = None


def _human_for(cell_id: Optional[str], grid: Any) -> Optional[str]:
    if not cell_id:
        return None
    # 结果级字段优先
    if cell_id == _get(grid, "focus_target_cell_id"):
        return _get(grid, "focus_target_cell_human_label")
    if cell_id == _get(grid, "container_candidate_cell_id"):
        return _get(grid, "container_candidate_cell_human_label")
    if cell_id == _get(grid, "recommended_search_cell_id"):
        return _get(grid, "recommended_search_cell_human_label")
    # cells 列表兜底
    for c in (_get(grid, "cells", None) or []):
        if _get(c, "cell_id") == cell_id:
            return _get(c, "cell_human_label")
    return None


def _dedup_keep_order(items: Sequence[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for x in items:
        if not x or x in seen:
            continue
        seen.add(x)
        out.append(x)
    return out


def build_grid_search_expansion(
    *,
    local_task_space_grid: Any,
    object_search_interaction: Any,
) -> GridSearchExpansionResult:
    grid = local_task_space_grid
    flow = _get(object_search_interaction, "interaction_flow_type")

    focus_cell = _get(grid, "focus_target_cell_id")
    container_cell = _get(grid, "container_candidate_cell_id")
    occlusion_cells = _get(grid, "occlusion_cell_ids", []) or []
    recommended = _get(grid, "recommended_search_cell_id")
    rec_adj = _get(grid, "recommended_search_adjacent_cells", []) or []

    primary: Optional[str] = None
    secondary: List[str] = []
    strategy: str = "none"
    reason_parts: List[str] = []

    if flow == "container_check_flow":
        strategy = "container_priority"
        primary = container_cell or recommended
        reason_parts.append("container_flow")
        if container_cell:
            reason_parts.append("primary=container_cell")
        else:
            reason_parts.append("primary=recommended")
        secondary = list(rec_adj)
        # 若 focus 与 container 不同，补 focus
        if focus_cell and primary and focus_cell != primary:
            secondary.append(focus_cell)
            reason_parts.append("add_focus_cell")
        # 最多 3 个 secondary
        secondary = _dedup_keep_order(secondary)[:3]
    elif flow == "occlusion_clear_flow":
        strategy = "occlusion_priority"
        primary = (occlusion_cells[0] if occlusion_cells else None) or focus_cell or recommended
        reason_parts.append("occlusion_flow")
        reason_parts.append("primary=occlusion_or_focus")
        # secondary：primary 的 adjacent（优先用 recommended_search_adjacent_cells；若 primary!=recommended，尝试用 cell 内邻接）
        if primary == recommended:
            secondary = list(rec_adj)
        else:
            # 从 grid.cells 找 primary 的 adjacent_cell_ids
            for c in (_get(grid, "cells", None) or []):
                if _get(c, "cell_id") == primary:
                    secondary = list(_get(c, "adjacent_cell_ids", []) or [])
                    break
        if focus_cell and primary and focus_cell != primary:
            secondary.append(focus_cell)
            reason_parts.append("add_focus_cell")
        secondary = _dedup_keep_order(secondary)[:3]
    else:
        # 一般搜索
        strategy = "focus_then_adjacent"
        primary = focus_cell or recommended
        if primary:
            reason_parts.append("general_flow")
            reason_parts.append("primary=focus_or_recommended")
            secondary = list(rec_adj) if primary == recommended else []
            if not secondary and primary:
                for c in (_get(grid, "cells", None) or []):
                    if _get(c, "cell_id") == primary:
                        secondary = list(_get(c, "adjacent_cell_ids", []) or [])
                        break
            secondary = _dedup_keep_order(secondary)[:3]

    if not primary:
        return GridSearchExpansionResult(
            expansion_flow_type=flow,
            expansion_strategy_type="none",
            expansion_reason="no_focus_or_recommended",
            expansion_applied=False,
        )

    primary_h = _human_for(primary, grid)
    secondary_h = [(_human_for(x, grid) or x) for x in secondary]
    applied = True

    hint = None
    if primary_h and secondary_h:
        hint = f"如果{primary_h}没有，再看" + "或".join(secondary_h[:2])
    elif primary_h:
        hint = f"如果{primary_h}没有，再看看附近区域"

    summary = f"primary={primary} secondary={','.join(secondary) if secondary else '—'} strategy={strategy}"
    return GridSearchExpansionResult(
        primary_search_cell_id=primary,
        primary_search_cell_human_label=primary_h or primary,
        secondary_search_cell_ids=secondary,
        secondary_search_cell_human_labels=secondary_h,
        expansion_flow_type=flow,
        expansion_strategy_type=strategy,
        expansion_reason="+".join(reason_parts) if reason_parts else None,
        expansion_summary=summary,
        expansion_applied=applied,
        grid_search_expansion_hint=hint,
    )

