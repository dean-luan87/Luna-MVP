# -*- coding: utf-8 -*-
"""
Local Task Space Grid M0（局部任务空间格）

仅做“当前帧/当前任务附近”的 2D 3x3 网格组织层：
- horizontal: left / center / right
- depth: back / mid / front

用于把 focus/容器候选/遮挡与候选标签挂到统一空间骨架上，便于审计与后续扩展。
不做全局地图、不做 3D、不做持久化、不替代底层 bbox/sidecar 事实。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence


H_BANDS = ("left", "center", "right")
D_BANDS = ("back", "mid", "front")


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _normalize_hband(hb: Optional[str]) -> Optional[str]:
    """兼容 sidecar 的 mid_left/mid/mid_right -> left/center/right。"""
    if not hb:
        return None
    hb = str(hb).strip()
    if hb in ("left",):
        return "left"
    if hb in ("right",):
        return "right"
    if hb in ("mid_left",):
        return "left"
    if hb in ("mid_right",):
        return "right"
    if hb in ("mid", "center"):
        return "center"
    return None


def _normalize_dband(vb: Optional[str]) -> Optional[str]:
    if not vb:
        return None
    vb = str(vb).strip()
    if vb in D_BANDS:
        return vb
    return None


def _cell_id(h: str, d: str) -> str:
    return f"{h}_{d}"


def _cell_human_label(h: str, d: str) -> str:
    hmap = {"left": "左", "center": "中", "right": "右"}
    dmap = {"front": "前", "mid": "中", "back": "后"}
    # 标准化标签：center_mid 用「中间区」
    if h == "center" and d == "mid":
        return "中间区"
    return f"{hmap.get(h, h)}{dmap.get(d, d)}区"


@dataclass
class TaskGridCell:
    cell_id: str
    horizontal_band: str
    depth_band: str
    cell_human_label: str
    candidate_labels: List[str] = field(default_factory=list)
    candidate_count: int = 0
    focus_target_present: bool = False
    container_candidate_present: bool = False
    occlusion_present: bool = False
    dominant_semantic: str = "empty"  # focus/container/occlusion/mixed/empty
    cell_reason: Optional[str] = None
    adjacent_cell_ids: List[str] = field(default_factory=list)


@dataclass
class LocalTaskSpaceGridResult:
    grid_rows: int = 3
    grid_cols: int = 3
    cells: List[TaskGridCell] = field(default_factory=list)
    focus_target_cell_id: Optional[str] = None
    container_candidate_cell_id: Optional[str] = None
    occlusion_cell_ids: List[str] = field(default_factory=list)
    recommended_search_cell_id: Optional[str] = None
    # 轻消费辅助字段（供文案/提示组合，不替代 cell_id）
    focus_target_cell_human_label: Optional[str] = None
    container_candidate_cell_human_label: Optional[str] = None
    recommended_search_cell_human_label: Optional[str] = None
    recommended_search_adjacent_cells: List[str] = field(default_factory=list)
    grid_followup_hint: Optional[str] = None
    grid_summary: Optional[str] = None
    grid_applied: bool = False


def _init_cells() -> Dict[str, TaskGridCell]:
    out: Dict[str, TaskGridCell] = {}
    for d in D_BANDS:
        for h in H_BANDS:
            cid = _cell_id(h, d)
            out[cid] = TaskGridCell(
                cell_id=cid,
                horizontal_band=h,
                depth_band=d,
                cell_human_label=_cell_human_label(h, d),
            )
    return out


def _adjacent_map() -> Dict[str, List[str]]:
    """
    3x3 固定邻接表（8 邻域，去掉自身）。
    允许写死，不做动态计算。
    """
    coords = {
        "left": 0,
        "center": 1,
        "right": 2,
        "back": 0,
        "mid": 1,
        "front": 2,
    }
    rev_h = {0: "left", 1: "center", 2: "right"}
    rev_d = {0: "back", 1: "mid", 2: "front"}

    out: Dict[str, List[str]] = {}
    for d in D_BANDS:
        for h in H_BANDS:
            x = coords[h]
            y = coords[d]
            cid = _cell_id(h, d)
            adj: List[str] = []
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    nx = x + dx
                    ny = y + dy
                    if nx < 0 or nx > 2 or ny < 0 or ny > 2:
                        continue
                    adj.append(_cell_id(rev_h[nx], rev_d[ny]))
            out[cid] = adj
    return out


def _dominant_semantic(cell: TaskGridCell) -> str:
    if cell.focus_target_present:
        return "focus"
    if cell.container_candidate_present:
        return "container"
    if cell.occlusion_present:
        return "occlusion"
    if cell.candidate_count > 0:
        return "mixed"
    return "empty"


def build_local_task_space_grid(
    *,
    spatial_expression_sidecar: Any,
    object_search_interaction: Any,
    object_temporal_ledger: Any,
) -> LocalTaskSpaceGridResult:
    """
    将 sidecar candidates 挂载到 3x3 网格，并标注 focus/container/occlusion 语义。
    只做组织与摘要，不反写任何输入模块。
    """
    cells = _init_cells()
    adj_map = _adjacent_map()
    for cid, cell in cells.items():
        cell.adjacent_cell_ids = list(adj_map.get(cid, []))
    cands: Sequence[Any] = _get(spatial_expression_sidecar, "candidates", None) or []

    # 1) 挂载候选
    focus_cell_id: Optional[str] = None
    focus_candidate = None
    for c in cands:
        hb = _normalize_hband(_get(c, "candidate_horizontal_band"))
        vb = _normalize_dband(_get(c, "candidate_vertical_band"))
        if not hb or not vb:
            continue
        cid = _cell_id(hb, vb)
        cell = cells.get(cid)
        if not cell:
            continue
        lab = (_get(c, "candidate_label") or "").strip() or "unknown"
        cell.candidate_labels.append(lab)
        cell.candidate_count += 1
        if _get(c, "candidate_is_focus_target") is True:
            cell.focus_target_present = True
            if focus_cell_id is None:
                focus_cell_id = cid
                focus_candidate = c

    # 2) 容器候选挂载
    container_cell_id: Optional[str] = None
    entry = _get(object_temporal_ledger, "focus_object_entry")
    container_candidate = (_get(entry, "current_container_candidate") or "").strip() if entry else ""
    if container_candidate:
        # 找到第一个 label 匹配的候选 cell
        for c in cands:
            lab = (_get(c, "candidate_label") or "").strip()
            if lab != container_candidate:
                continue
            hb = _normalize_hband(_get(c, "candidate_horizontal_band"))
            vb = _normalize_dband(_get(c, "candidate_vertical_band"))
            if not hb or not vb:
                continue
            cid = _cell_id(hb, vb)
            if cid in cells:
                cells[cid].container_candidate_present = True
                container_cell_id = cid
                break

    # 3) 遮挡挂载：遮挡流则把 focus cell 标记为 occlusion_present（M0：只做最小挂载）
    flow_type = _get(object_search_interaction, "interaction_flow_type")
    occlusion_cell_ids: List[str] = []
    if flow_type == "occlusion_clear_flow" and focus_cell_id and focus_cell_id in cells:
        cells[focus_cell_id].occlusion_present = True
        occlusion_cell_ids.append(focus_cell_id)

    # 4) recommended search cell：按 flow
    recommended: Optional[str] = None
    if flow_type == "container_check_flow" and container_cell_id:
        recommended = container_cell_id
    elif flow_type == "occlusion_clear_flow" and (occlusion_cell_ids or focus_cell_id):
        recommended = occlusion_cell_ids[0] if occlusion_cell_ids else focus_cell_id
    elif focus_cell_id:
        recommended = focus_cell_id

    # 5) dominant semantic + reason
    for cell in cells.values():
        cell.dominant_semantic = _dominant_semantic(cell)
        if cell.dominant_semantic != "empty":
            parts = []
            if cell.focus_target_present:
                parts.append("focus")
            if cell.container_candidate_present:
                parts.append("container")
            if cell.occlusion_present:
                parts.append("occlusion")
            if cell.candidate_count:
                parts.append(f"cands={cell.candidate_count}")
            cell.cell_reason = ",".join(parts) if parts else None

    # 6) summary
    summary_parts: List[str] = []
    if focus_cell_id:
        summary_parts.append(f"focus in {focus_cell_id}")
    if container_cell_id:
        summary_parts.append(f"container in {container_cell_id}")
    if occlusion_cell_ids:
        summary_parts.append(f"occlusion in {','.join(occlusion_cell_ids[:3])}")
    if not summary_parts:
        # 粗略：是否有候选
        total = sum(c.candidate_count for c in cells.values())
        summary_parts.append("no strong focus" if total else "empty grid")
    grid_summary = "; ".join(summary_parts)

    focus_human = cells[focus_cell_id].cell_human_label if focus_cell_id and focus_cell_id in cells else None
    container_human = (
        cells[container_cell_id].cell_human_label if container_cell_id and container_cell_id in cells else None
    )
    rec_human = cells[recommended].cell_human_label if recommended and recommended in cells else None
    rec_adj = list(adj_map.get(recommended, [])) if recommended else []
    # followup hint：保守短句；可选稍具体（列 1-2 个相邻格）
    followup_hint = None
    if rec_human and rec_adj:
        # 取前两个相邻格的人类标签
        h1 = cells[rec_adj[0]].cell_human_label if rec_adj[0] in cells else None
        h2 = cells[rec_adj[1]].cell_human_label if len(rec_adj) > 1 and rec_adj[1] in cells else None
        if h1 and h2:
            followup_hint = f"如果{rec_human}没有，再看{h1}或{h2}"
        elif h1:
            followup_hint = f"如果{rec_human}没有，再看看附近区域"
        else:
            followup_hint = "如果这里没有，再看看附近的格子"

    return LocalTaskSpaceGridResult(
        grid_rows=3,
        grid_cols=3,
        cells=list(cells.values()),
        focus_target_cell_id=focus_cell_id,
        container_candidate_cell_id=container_cell_id,
        occlusion_cell_ids=occlusion_cell_ids,
        recommended_search_cell_id=recommended,
        focus_target_cell_human_label=focus_human,
        container_candidate_cell_human_label=container_human,
        recommended_search_cell_human_label=rec_human,
        recommended_search_adjacent_cells=rec_adj,
        grid_followup_hint=followup_hint,
        grid_summary=grid_summary,
        grid_applied=True,
    )

