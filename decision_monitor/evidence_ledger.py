# -*- coding: utf-8 -*-
"""
证据账本 M0：Evidence Ledger（最小版）。

在 Skeleton Mix / Filter / Spatial Memory Pooling / Spatial Forgetting 基础上，
增加最小证据账本：claim + supporting / conflicting / missing 证据 + confidence + risk_if_wrong + suggested_next_check。
不做完整推理引擎、不做 Hypothesis Layer、不做学习。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional

from .local_goal_spatial_map import LocalGoalSpatialMap
from .local_goal_spatial_relations import SpatialRelation
from .skeleton_filter import SkeletonFilterResult
from .skeleton_mix import SkeletonMix
from .spatial_forgetting import SpatialForgettingSummary
from .spatial_memory_pools import SpatialMemoryPools

SUGGESTED_CHECKS = ("recheck_environment", "recheck_close_range", "shift_view_left", "shift_view_right", "look_forward", "hold_and_confirm")


@dataclass
class EvidenceLedgerEntry:
    """单条证据账本条目：结论 + 支持/冲突/缺失证据 + 置信度与建议。"""
    claim_summary: str
    supporting_evidence: List[str] = field(default_factory=list)
    conflicting_evidence: List[str] = field(default_factory=list)
    missing_evidence: List[str] = field(default_factory=list)
    evidence_confidence: float = 0.0
    risk_if_wrong: Optional[str] = None
    suggested_next_check: Optional[str] = None


@dataclass
class EvidenceLedger:
    """最小证据账本：多条 claim 条目。"""
    entries: List[EvidenceLedgerEntry] = field(default_factory=list)


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _region_summary(r: Any) -> str:
    sector = getattr(r, "sector", "") or "—"
    band = getattr(r, "distance_band", None) or "—"
    rt = getattr(r, "region_type", "") or "region"
    return f"{rt} sector={sector} band={band}"


def build_evidence_ledger(
    smap: Optional[LocalGoalSpatialMap],
    relations: Optional[List[SpatialRelation]],
    mix: Optional[SkeletonMix],
    filt: Optional[SkeletonFilterResult],
    pools: Optional[SpatialMemoryPools],
    forgetting: Optional[SpatialForgettingSummary],
    goal: Any,
    state: Any,
) -> EvidenceLedger:
    """
    从 smap、relations、mix、filt、pools、forgetting、goal、state 生成最小证据账本（1~3 条 claim）。
    """
    entries: List[EvidenceLedgerEntry] = []

    dominant = _get(mix, "dominant_skeleton") or "navigation"
    keep = list(_get(filt, "keep_region_types") or [])
    suppress = list(_get(filt, "suppress_region_types") or [])

    # ----- Claim 1: 当前主导空间关注 -----
    support_1: List[str] = []
    support_1.append(f"dominant={dominant}")
    if _get(mix, "mix_reason"):
        support_1.append(f"mix_reason={_get(mix, 'mix_reason')}")
    if keep:
        support_1.append(f"keep={','.join(keep[:3])}")
    conflict_1: List[str] = []
    if suppress and dominant != "safety":
        conflict_1.append(f"suppress={','.join(suppress[:2])}")
    missing_1: List[str] = []
    if dominant == "safety":
        has_risk = smap and (getattr(smap, "risk_region", None) or [])
        if not has_risk:
            missing_1.append("需要风险区域信息")
    conf_1 = 0.6 + 0.1 * (1 if keep else 0)
    risk_1 = "误判可能导致空间关注偏差，影响后续过滤与分池"
    sug_1 = "hold_and_confirm" if missing_1 else ("recheck_environment" if dominant == "safety" else None)
    entries.append(EvidenceLedgerEntry(
        claim_summary=f"当前主导空间关注：{dominant.replace('_', ' ')}",
        supporting_evidence=support_1,
        conflicting_evidence=conflict_1,
        missing_evidence=missing_1,
        evidence_confidence=min(1.0, conf_1),
        risk_if_wrong=risk_1,
        suggested_next_check=sug_1,
    ))

    # ----- Claim 2: 当前主要空间结构 -----
    support_2: List[str] = []
    conflict_2: List[str] = []
    missing_2: List[str] = []
    claim_2 = "当前主要空间结构："
    if smap:
        focus = getattr(smap, "focus_region", None) or []
        trav = getattr(smap, "traversable_region", None) or []
        risk = getattr(smap, "risk_region", None) or []
        confirm = getattr(smap, "confirm_region", None) or []
        for r in focus[:1]:
            support_2.append("focus " + _region_summary(r))
        for r in trav[:2]:
            support_2.append("traversable " + _region_summary(r))
        for r in risk[:2]:
            conflict_2.append("risk " + _region_summary(r))
        if trav:
            claim_2 += "前方可通行主区成立"
        if risk and trav:
            claim_2 += "；存在风险与可通行冲突"
        elif risk:
            claim_2 += "存在主要风险区"
        if not trav and not risk:
            claim_2 += "待补充"
        if confirm and focus:
            support_2.append("confirm 支撑 focus")
        elif focus and not confirm:
            missing_2.append("需要 confirm 区支撑 focus")
    else:
        claim_2 += "无空间图"
        missing_2.append("需要局部空间图")
    if relations:
        for rel in relations[:5]:
            if rel.relation_type == "supports":
                support_2.append(f"relation supports: {rel.source_region_type}->{rel.target_region_type}")
            elif rel.relation_type == "conflicts_with":
                conflict_2.append(f"relation conflict: {rel.source_region_type} vs {rel.target_region_type}")
    conf_2 = 0.5 + 0.2 * min(1, len(support_2)) - 0.1 * min(1, len(conflict_2))
    risk_2 = "结构误判可能导致路径或交互决策错误"
    sug_2 = "recheck_close_range" if missing_2 else ("hold_and_confirm" if conflict_2 else "look_forward")
    entries.append(EvidenceLedgerEntry(
        claim_summary=claim_2,
        supporting_evidence=support_2[:5],
        conflicting_evidence=conflict_2[:3],
        missing_evidence=missing_2,
        evidence_confidence=max(0.0, min(1.0, conf_2)),
        risk_if_wrong=risk_2,
        suggested_next_check=sug_2,
    ))

    # ----- Claim 3: 当前记忆状态 -----
    working_n = len(getattr(pools, "working_memory_items", None) or [])
    episode_n = len(getattr(pools, "episode_memory_items", None) or [])
    collapse_n = _get(forgetting, "episode_collapsed_count") or 0
    support_3: List[str] = [f"working={working_n} episode={episode_n}"]
    if forgetting and getattr(forgetting, "forgetting_reason_summary", None):
        support_3.append("forgetting=" + (getattr(forgetting, "forgetting_reason_summary", "") or "")[:40])
    missing_3: List[str] = []
    if working_n == 0:
        missing_3.append("需要当前帧空间证据")
    if collapse_n > 0:
        claim_3 = "当前记忆状态：episode 已塌缩，证据依赖短时池"
    else:
        claim_3 = "当前记忆状态：working 证据充足" if working_n >= 1 else "当前记忆状态：证据依赖短时池，working 为空"
    conf_3 = 0.4 + 0.3 * min(1, working_n) + 0.2 * min(1, episode_n)
    risk_3 = "记忆状态误判可能影响跨帧一致性"
    sug_3 = "recheck_environment" if missing_3 else None
    entries.append(EvidenceLedgerEntry(
        claim_summary=claim_3,
        supporting_evidence=support_3,
        conflicting_evidence=[],
        missing_evidence=missing_3,
        evidence_confidence=min(1.0, conf_3),
        risk_if_wrong=risk_3,
        suggested_next_check=sug_3,
    ))

    return EvidenceLedger(entries=entries)
