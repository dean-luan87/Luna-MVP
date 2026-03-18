# -*- coding: utf-8 -*-
"""
骨架记忆分池 M0：Skeleton-aware Spatial Memory Pooling（最小版）。

依据 SPATIAL_MEMORY_POLICY_CONSTITUTION.md v1.0 与 Skeleton Mix M0、Skeleton Filter M0；
将当前空间信息分流到四层记忆池，working / episode 为主，stable / anchor 占位。
不做持久化、不做复杂遗忘、不做长期证据门槛。
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, List, Optional

from .local_goal_spatial_map import LocalGoalSpatialMap, SpatialRegion
from .local_goal_spatial_relations import SpatialRelation
from .skeleton_filter import SkeletonFilterResult
from .skeleton_mix import SkeletonMix

MEMORY_LAYERS = ("working", "episode", "stable", "anchor")
RETENTION_POLICIES = ("ttl", "task_end", "value_decay", "evidence_replace")


@dataclass
class SpatialMemoryItem:
    """最小空间记忆项。"""
    memory_layer: str  # working / episode / stable / anchor
    source_type: str   # focus_region / traversable_region / risk_region / confirm_region / relation
    payload_summary: str
    skeleton_context: Optional[str] = None  # 当前 dominant_skeleton
    retention_policy: Optional[str] = None
    timestamp: Optional[float] = None
    confidence: Optional[float] = None
    use_count: Optional[int] = None
    conflict_count: Optional[int] = None
    last_used_ts: Optional[float] = None


@dataclass
class SpatialMemoryPools:
    """四层空间记忆池（运行时分池，无持久化）。"""
    working_memory_items: List[SpatialMemoryItem] = field(default_factory=list)
    episode_memory_items: List[SpatialMemoryItem] = field(default_factory=list)
    stable_memory_items: List[SpatialMemoryItem] = field(default_factory=list)
    anchor_memory_items: List[SpatialMemoryItem] = field(default_factory=list)
    dominant_skeleton: Optional[str] = None
    pool_reason: Optional[str] = None


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _region_summary(region: SpatialRegion) -> str:
    band = getattr(region, "distance_band", None) or "—"
    return f"{region.region_type}#{region.priority_rank} sector={region.sector} band={band}"


def _relation_summary(rel: SpatialRelation) -> str:
    return f"{rel.source_region_type}#{rel.source_priority_rank}->{rel.target_region_type}#{rel.target_priority_rank} [{rel.relation_type}]"


def build_spatial_memory_pools(
    mix: Optional[SkeletonMix],
    filt: Optional[SkeletonFilterResult],
    smap: Optional[LocalGoalSpatialMap],
    relations: Optional[List[SpatialRelation]],
    goal: Any,
) -> SpatialMemoryPools:
    """
    基于 skeleton_mix、skeleton_filter、local_goal_spatial_map、relations、goal 做最小分池。
    working / episode 从 keep 区域与关系中写入；stable / anchor 仅占位或空。
    suppress 内容不进入 stable / anchor。
    """
    now = time.time()
    dominant = _get(mix, "dominant_skeleton") or "navigation"
    keep = set(_get(filt, "keep_region_types") or [])
    suppress = set(_get(filt, "suppress_region_types") or [])
    goal_type = _get(goal, "goal_type") or "observe_navigate"

    working: List[SpatialMemoryItem] = []
    episode: List[SpatialMemoryItem] = []
    stable: List[SpatialMemoryItem] = []
    anchor: List[SpatialMemoryItem] = []

    # 区域 -> working（在 keep 中且非 suppress 的进入 working）
    region_type_to_list = [
        ("focus_region", smap.focus_region if smap else None),
        ("traversable_region", smap.traversable_region if smap else None),
        ("risk_region", smap.risk_region if smap else None),
        ("confirm_region", smap.confirm_region if smap else None),
    ]
    for region_type, regions in region_type_to_list:
        if region_type in suppress:
            continue
        if not regions:
            continue
        for r in regions[:3]:  # 每类最多 3 条
            if region_type not in keep and dominant != "safety":
                continue
            if dominant == "safety" and region_type in ("risk_region", "confirm_region", "traversable_region"):
                pass  # safety 时风险相关必进
            elif region_type not in keep:
                continue
            item = SpatialMemoryItem(
                memory_layer="working",
                source_type=region_type,
                payload_summary=_region_summary(r),
                skeleton_context=dominant,
                retention_policy="ttl",
                timestamp=now,
                confidence=r.confidence if hasattr(r, "confidence") else 0.7,
            )
            working.append(item)
            # 部分进入 episode：与当前任务强相关、可跨帧复用
            if dominant == "navigation" and region_type in ("traversable_region", "confirm_region", "focus_region"):
                ep_item = SpatialMemoryItem(
                    memory_layer="episode",
                    source_type=region_type,
                    payload_summary=_region_summary(r),
                    skeleton_context=dominant,
                    retention_policy="task_end",
                    timestamp=now,
                    confidence=r.confidence if hasattr(r, "confidence") else 0.6,
                )
                episode.append(ep_item)
            elif dominant == "fine_interaction" and region_type in ("focus_region", "confirm_region"):
                ep_item = SpatialMemoryItem(
                    memory_layer="episode",
                    source_type=region_type,
                    payload_summary=_region_summary(r),
                    skeleton_context=dominant,
                    retention_policy="task_end",
                    timestamp=now,
                    confidence=r.confidence if hasattr(r, "confidence") else 0.6,
                )
                episode.append(ep_item)
            elif dominant == "observation" and region_type == "focus_region":
                ep_item = SpatialMemoryItem(
                    memory_layer="episode",
                    source_type=region_type,
                    payload_summary=_region_summary(r),
                    skeleton_context=dominant,
                    retention_policy="task_end",
                    timestamp=now,
                    confidence=r.confidence if hasattr(r, "confidence") else 0.5,
                )
                episode.append(ep_item)

    # 关系 -> working（supports/conflicts 等与 keep 一致的可进 working）
    if relations:
        for rel in relations[:5]:
            if rel.relation_type in ("supports", "conflicts_with") or rel.source_region_type in keep:
                item = SpatialMemoryItem(
                    memory_layer="working",
                    source_type="relation",
                    payload_summary=_relation_summary(rel),
                    skeleton_context=dominant,
                    retention_policy="ttl",
                    timestamp=now,
                    confidence=rel.confidence,
                )
                working.append(item)
            if dominant == "navigation" and rel.relation_type == "supports":
                ep_item = SpatialMemoryItem(
                    memory_layer="episode",
                    source_type="relation",
                    payload_summary=_relation_summary(rel),
                    skeleton_context=dominant,
                    retention_policy="task_end",
                    timestamp=now,
                    confidence=rel.confidence,
                )
                episode.append(ep_item)

    # stable / anchor：占位，不把 suppress 或当前瞬时内容写入
    stable.append(
        SpatialMemoryItem(
            memory_layer="stable",
            source_type="placeholder",
            payload_summary="(stable placeholder M0)",
            skeleton_context=dominant,
            retention_policy="evidence_replace",
            timestamp=now,
            confidence=0.0,
        )
    )
    anchor.append(
        SpatialMemoryItem(
            memory_layer="anchor",
            source_type="placeholder",
            payload_summary="(anchor placeholder M0)",
            skeleton_context=dominant,
            retention_policy="evidence_replace",
            timestamp=now,
            confidence=0.0,
        )
    )

    reason = f"dominant={dominant} keep={len(keep)} working={len(working)} episode={len(episode)}"
    return SpatialMemoryPools(
        working_memory_items=working[:15],
        episode_memory_items=episode[:10],
        stable_memory_items=stable,
        anchor_memory_items=anchor,
        dominant_skeleton=dominant,
        pool_reason=reason,
    )
