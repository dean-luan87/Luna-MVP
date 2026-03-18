# -*- coding: utf-8 -*-
"""
主线 2 第二阶段 M2：Local Goal Spatial Map 区域关系（最小版）。

在 M1.5 标尺层基础上增加最小区域关系表达，使局部空间图从“区域集合”推进为“区域关系图”。
不做 3D、occupancy 网格、语义拓扑、对象级关系、长时记忆。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from .local_goal_spatial_map import LocalGoalSpatialMap, SpatialRegion

RELATION_TYPES = ("adjacent_to", "overlaps_with", "supports", "conflicts_with")

# 扇区邻接（用于 adjacent_to）：方向维度上相邻
SECTOR_NEIGHBORS = {
    "front": ("front_left", "front_right"),
    "front_left": ("front", "left"),
    "front_right": ("front", "right"),
    "left": ("front_left", "rear"),
    "right": ("front_right", "rear"),
    "rear": ("left", "right"),
}

DISTANCE_BAND_ORDER = ("immediate", "near", "mid", "far")


@dataclass
class SpatialRelation:
    """最小区域关系：source -> target，relation_type，confidence，reason。"""
    source_region_type: str  # focus_region / traversable_region / risk_region / confirm_region
    source_priority_rank: int  # 1/2/3
    target_region_type: str
    target_priority_rank: int
    relation_type: str  # one of RELATION_TYPES
    confidence: float  # 0~1
    reason: Optional[str] = None


def _band_index(band: Optional[str]) -> int:
    if not band:
        return 1
    try:
        return DISTANCE_BAND_ORDER.index(band)
    except ValueError:
        return 1


def _bands_close(band_a: Optional[str], band_b: Optional[str]) -> bool:
    """距离带接近：同带或相邻带（immediate/near, near/mid, mid/far）。"""
    i, j = _band_index(band_a), _band_index(band_b)
    return abs(i - j) <= 1


def _sectors_adjacent(sector_a: str, sector_b: str) -> bool:
    return sector_b in SECTOR_NEIGHBORS.get(sector_a, ())


def _same_sector(sector_a: str, sector_b: str) -> bool:
    return sector_a == sector_b


def _sectors_overlap(sector_a: str, sector_b: str) -> bool:
    """同扇区或邻接扇区视为可重叠。"""
    return _same_sector(sector_a, sector_b) or _sectors_adjacent(sector_a, sector_b)


def _regions(
    smap: Optional[LocalGoalSpatialMap],
) -> List[tuple[str, int, SpatialRegion]]:
    """(region_type, priority_rank, region) 列表，用于关系生成。"""
    out: List[tuple[str, int, SpatialRegion]] = []
    if not smap:
        return out
    for r in (smap.focus_region or []):
        out.append(("focus_region", r.priority_rank, r))
    for r in (smap.traversable_region or []):
        out.append(("traversable_region", r.priority_rank, r))
    for r in (smap.risk_region or []):
        out.append(("risk_region", r.priority_rank, r))
    for r in (smap.confirm_region or []):
        out.append(("confirm_region", r.priority_rank, r))
    return out


def build_relations(smap: Optional[LocalGoalSpatialMap]) -> List[SpatialRelation]:
    """
    从 LocalGoalSpatialMap 生成最小区域关系（规则型）。
    - adjacent_to: sector 邻接 + distance_band 接近
    - overlaps_with: 同 sector 或扇区接近且距离带一致
    - supports: confirm -> focus；traversable -> goal（用 focus 主区代理）
    - conflicts_with: risk 与 traversable 在相近 sector/band 冲突；高 urgency risk 与 focus/confirm 冲突
    """
    relations: List[SpatialRelation] = []
    if not smap:
        return relations

    regions = _regions(smap)
    focus_main = next((r for rt, rank, r in regions if rt == "focus_region" and rank == 1), None)
    focus_sector = focus_main.sector if focus_main else "front"
    focus_band = focus_main.distance_band if focus_main else "mid"

    # --- supports / conflicts_with 先生成，保证验收至少出现（再截断时优先保留）
    # --- supports: confirm_region -> focus_region；traversable_region -> focus（goal 代理）
    for src_type, src_rank, src in regions:
        if src_type == "confirm_region" and focus_main and _sectors_overlap(src.sector, focus_sector):
            relations.append(
                SpatialRelation(
                    source_region_type="confirm_region",
                    source_priority_rank=src_rank,
                    target_region_type="focus_region",
                    target_priority_rank=1,
                    relation_type="supports",
                    confidence=0.65 + 0.2 * src.confidence,
                    reason="confirm_supports_focus",
                )
            )
        if src_type == "traversable_region" and focus_main and _sectors_overlap(src.sector, focus_sector):
            relations.append(
                SpatialRelation(
                    source_region_type="traversable_region",
                    source_priority_rank=src_rank,
                    target_region_type="focus_region",
                    target_priority_rank=1,
                    relation_type="supports",
                    confidence=0.6 + 0.2 * src.confidence,
                    reason="traversable_supports_goal",
                )
            )

    # --- conflicts_with: risk vs traversable；risk vs focus/confirm
    for src_type, src_rank, src in regions:
        if src_type != "risk_region":
            continue
        for tgt_type, tgt_rank, tgt in regions:
            if tgt_type == "traversable_region" and _sectors_overlap(src.sector, tgt.sector) and _bands_close(src.distance_band, tgt.distance_band):
                relations.append(
                    SpatialRelation(
                        source_region_type="risk_region",
                        source_priority_rank=src_rank,
                        target_region_type="traversable_region",
                        target_priority_rank=tgt_rank,
                        relation_type="conflicts_with",
                        confidence=0.65 + 0.2 * src.confidence,
                        reason="risk_vs_traversable_same_zone",
                    )
                )
            if tgt_type in ("focus_region", "confirm_region") and _sectors_overlap(src.sector, tgt.sector):
                conf = 0.5 + 0.3 * src.confidence
                relations.append(
                    SpatialRelation(
                        source_region_type="risk_region",
                        source_priority_rank=src_rank,
                        target_region_type=tgt_type,
                        target_priority_rank=tgt_rank,
                        relation_type="conflicts_with",
                        confidence=conf,
                        reason="risk_vs_focus_confirm",
                    )
                )

    # --- adjacent_to: 不同 region_type 间 sector 邻接且 band 接近
    for i, (src_type, src_rank, src) in enumerate(regions):
        for j, (tgt_type, tgt_rank, tgt) in enumerate(regions):
            if i >= j or src_type == tgt_type:
                continue
            if _sectors_adjacent(src.sector, tgt.sector) and _bands_close(src.distance_band, tgt.distance_band):
                relations.append(
                    SpatialRelation(
                        source_region_type=src_type,
                        source_priority_rank=src_rank,
                        target_region_type=tgt_type,
                        target_priority_rank=tgt_rank,
                        relation_type="adjacent_to",
                        confidence=0.6 + 0.2 * min(src.confidence, tgt.confidence),
                        reason="sector_adjacent_band_close",
                    )
                )

    # --- overlaps_with: 同 sector 且同/近 distance_band
    for i, (src_type, src_rank, src) in enumerate(regions):
        for j, (tgt_type, tgt_rank, tgt) in enumerate(regions):
            if i >= j:
                continue
            if _same_sector(src.sector, tgt.sector) and _bands_close(src.distance_band, tgt.distance_band):
                relations.append(
                    SpatialRelation(
                        source_region_type=src_type,
                        source_priority_rank=src_rank,
                        target_region_type=tgt_type,
                        target_priority_rank=tgt_rank,
                        relation_type="overlaps_with",
                        confidence=0.55 + 0.25 * min(src.confidence, tgt.confidence),
                        reason="same_sector_same_band",
                    )
                )

    return relations[:20]  # 上限避免爆炸
