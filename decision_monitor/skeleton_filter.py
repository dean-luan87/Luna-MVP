# -*- coding: utf-8 -*-
"""
骨架过滤 M0：Skeleton-aware Visual Relevance Filter（最小版）。

依据 SPATIAL_SKELETON_SYSTEM_CONSTITUTION.md v1.0 与 Skeleton Mix M0；
当前骨架配比影响“哪些空间信息保留、哪些降权”，仅作用于空间结构保留策略，
不直接控制 detector/OCR，不做记忆/假设层联动。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .skeleton_mix import SkeletonMix, SKELETON_NAMES

GRANULARITY_BIAS = ("coarse", "mid", "fine", "safety_first")
DETAIL_LEVEL = ("coarse", "mid", "fine", "object")


@dataclass
class SkeletonFilterResult:
    """最小骨架感知过滤结果：保留/压低、粒度偏向、原因。"""
    keep_region_types: List[str] = field(default_factory=list)   # 建议保留的区域类型
    suppress_region_types: List[str] = field(default_factory=list)  # 建议压低的区域类型
    keep_anchor_priority: Optional[str] = None   # 锚点保留优先级：path_anchor / interaction_anchor / overview_anchor / safety_anchor
    suppress_detail_level: Optional[str] = None  # 压低的信息粒度：coarse / mid / fine / object
    granularity_bias: Optional[str] = None       # 当前粒度偏向：coarse / mid / fine / safety_first
    filter_reason: Optional[str] = None


def _get(mix: Optional[SkeletonMix], key: str, default=None):
    if mix is None:
        return default
    return getattr(mix, key, default)


def build_skeleton_filter(mix: Optional[SkeletonMix]) -> SkeletonFilterResult:
    """
    基于 Skeleton Mix 生成最小过滤策略；不执行真实过滤，仅产出“当前保留/压低策略”供展示与后续引用。
    """
    if mix is None:
        return SkeletonFilterResult(
            keep_region_types=["focus_region", "traversable_region", "risk_region", "confirm_region"],
            suppress_region_types=[],
            keep_anchor_priority="path_anchor",
            suppress_detail_level="object",
            granularity_bias="mid",
            filter_reason="no_mix_default_keep_all",
        )

    dominant = _get(mix, "dominant_skeleton") or "navigation"
    nav_w = _get(mix, "navigation_weight") or 0.0
    fine_w = _get(mix, "fine_interaction_weight") or 0.0
    obs_w = _get(mix, "observation_weight") or 0.0
    safe_w = _get(mix, "safety_weight") or 0.0

    if dominant == "navigation":
        keep = ["traversable_region", "risk_region", "confirm_region", "focus_region", "anchor", "portal", "segment"]
        suppress = ["fine_interaction_detail", "far_decoration", "low_value_local_object"]
        anchor_pri = "path_anchor"
        detail_suppress = "object"
        granularity = "coarse"
        reason = "navigation_dominant_keep_path_risk_confirm_suppress_detail"
    elif dominant == "fine_interaction":
        keep = ["focus_region", "confirm_region", "interaction_region", "object_cluster", "occlusion", "reachability", "height_depth"]
        suppress = ["long_path_detail", "far_navigation_anchor"]
        anchor_pri = "interaction_anchor"
        detail_suppress = "coarse"
        granularity = "fine"
        reason = "fine_interaction_dominant_keep_nearfield_suppress_path"
    elif dominant == "observation":
        keep = ["focus_region", "container", "major_region", "anchor", "state_summary"]
        suppress = ["object_level_detail"]
        anchor_pri = "overview_anchor"
        detail_suppress = "object"
        granularity = "mid"
        reason = "observation_dominant_keep_overview_suppress_object_detail"
    elif dominant == "safety":
        keep = ["risk_region", "blocking", "clearance", "anomaly", "confirm_region", "traversable_region"]
        suppress = []  # 其他降级不抹掉
        anchor_pri = "safety_anchor"
        detail_suppress = "mid"
        granularity = "safety_first"
        reason = "safety_dominant_keep_risk_clearance_others_downgrade"
    else:
        keep = ["focus_region", "traversable_region", "risk_region", "confirm_region"]
        suppress = []
        anchor_pri = "path_anchor"
        detail_suppress = "object"
        granularity = "mid"
        reason = "unknown_dominant_default"

    # Safety 权重高时无论主导是谁，都确保 risk/clearance 在保留列表
    if safe_w >= 0.3 and "risk_region" not in keep:
        keep = list(keep) + ["risk_region"]
    if safe_w >= 0.35 and "clearance" not in keep:
        keep = list(keep) + ["clearance"]

    return SkeletonFilterResult(
        keep_region_types=keep,
        suppress_region_types=suppress,
        keep_anchor_priority=anchor_pri,
        suppress_detail_level=detail_suppress,
        granularity_bias=granularity,
        filter_reason=reason,
    )
