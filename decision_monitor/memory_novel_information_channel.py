# -*- coding: utf-8 -*-
"""
Memory vs Novel Information Channel M0（记忆信息 / 新增信息双通道）

定位（写死）：
- 信息来源通道层：区分记忆调用 vs 新信息获取 vs 排除推断 vs 用户提供 vs 混合
- 只做最小通道与标记层 + “新信息→记忆候选”占位；不做长期记忆系统重构/评分/写库
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def _s(x: Any) -> Optional[str]:
    if x is None:
        return None
    t = str(x)
    return t if t.strip() else None


def _get(d: Any, *keys: str) -> Any:
    cur = d
    for k in keys:
        if cur is None:
            return None
        if isinstance(cur, dict):
            cur = cur.get(k)
        else:
            cur = getattr(cur, k, None)
    return cur


CHANNEL_TYPES = ("memory_derived", "newly_observed", "inferred_from_exclusion", "user_provided", "hybrid")


@dataclass
class InformationChannelItem:
    channel_type: str
    channel_label: str
    channel_summary: str
    channel_source_module: Optional[str] = None
    channel_used_in_reasoning: bool = True
    channel_used_in_decision: bool = False
    channel_confidence: Optional[float] = None
    channel_note: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "channel_type": self.channel_type,
            "channel_label": self.channel_label,
            "channel_summary": self.channel_summary,
            "channel_source_module": self.channel_source_module,
            "channel_used_in_reasoning": bool(self.channel_used_in_reasoning),
            "channel_used_in_decision": bool(self.channel_used_in_decision),
            "channel_confidence": self.channel_confidence,
            "channel_note": self.channel_note,
        }


@dataclass
class NovelMemoryCandidate:
    candidate_label: str
    candidate_reason: str
    candidate_source: str  # newly_observed / inferred_from_exclusion / user_provided / hybrid
    candidate_ready_for_memory: bool = False
    candidate_summary: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "candidate_label": self.candidate_label,
            "candidate_reason": self.candidate_reason,
            "candidate_source": self.candidate_source,
            "candidate_ready_for_memory": bool(self.candidate_ready_for_memory),
            "candidate_summary": self.candidate_summary,
        }


@dataclass
class MemoryNovelInformationChannelResult:
    information_channels: List[InformationChannelItem] = field(default_factory=list)
    memory_channel_count: int = 0
    novel_channel_count: int = 0
    hybrid_channel_count: int = 0
    dominant_reasoning_channel: Optional[str] = None
    dominant_decision_channel: Optional[str] = None
    novel_memory_candidate: Optional[NovelMemoryCandidate] = None
    channel_summary: Optional[str] = None
    channel_applied: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "information_channels": [c.to_dict() for c in self.information_channels],
            "memory_channel_count": int(self.memory_channel_count),
            "novel_channel_count": int(self.novel_channel_count),
            "hybrid_channel_count": int(self.hybrid_channel_count),
            "dominant_reasoning_channel": self.dominant_reasoning_channel,
            "dominant_decision_channel": self.dominant_decision_channel,
            "novel_memory_candidate": self.novel_memory_candidate.to_dict() if self.novel_memory_candidate else None,
            "channel_summary": self.channel_summary,
            "channel_applied": bool(self.channel_applied),
        }


def build_memory_novel_information_channel(frame: Dict[str, Any]) -> MemoryNovelInformationChannelResult:
    """
    M0 最小规则（只读 frame）：
    - memory_derived：object_temporal_ledger 有 last_confirmed_location / last_confirmed_ts 或 experience_evolution 有 promotable/watchlist
    - newly_observed：visual_candidate_audit 有 mapped/detector labels 或 sidecar 有 candidates
    - inferred_from_exclusion：结构树存在 pruned/exclusion 节点，或 metrics.dead_branch_count>0 且 issue=high_dead_branch_ratio
    - user_provided：confirmation_input_bridge 有 raw_text/type
    - hybrid：同时存在 memory_derived + newly_observed
    - novel_memory_candidate：newly_observed 或 inferred_from_exclusion 且 used_in_decision（由 feedback/next_effect/active path 摘要近似）→ 生成占位候选
    """
    if not isinstance(frame, dict):
        return MemoryNovelInformationChannelResult(channel_applied=False, channel_summary="invalid frame")

    chans: List[InformationChannelItem] = []

    # user provided
    fb_raw = _s(_get(frame, "confirmation_input_bridge", "confirmation_input_raw_text"))
    fb_type = _s(_get(frame, "confirmation_input_bridge", "confirmation_input_type"))
    if fb_raw or fb_type:
        chans.append(
            InformationChannelItem(
                channel_type="user_provided",
                channel_label="User feedback",
                channel_summary=f"{fb_type or '—'} · {fb_raw or ''}".strip(),
                channel_source_module="confirmation_input_bridge",
                channel_used_in_reasoning=True,
                channel_used_in_decision=True,
            )
        )

    # memory derived (light heuristic)
    last_loc = _s(_get(frame, "object_temporal_ledger", "focus_object_entry", "last_confirmed_location"))
    last_ts = _get(frame, "object_temporal_ledger", "focus_object_entry", "last_confirmed_ts")
    exp = _get(frame, "experience_evolution", "candidates") or []
    exp_any = False
    if isinstance(exp, list):
        for c in exp[:3]:
            if isinstance(c, dict) and (c.get("evolution_status") in ("watchlist", "promotable")):
                exp_any = True
                break
    if last_loc or last_ts is not None or exp_any:
        chans.append(
            InformationChannelItem(
                channel_type="memory_derived",
                channel_label="Memory-derived",
                channel_summary=("last_confirmed=" + (last_loc or "—")) if last_loc else ("experience_governance=" + ("yes" if exp_any else "no")),
                channel_source_module="object_temporal_ledger" if last_loc or last_ts is not None else "experience_evolution",
                channel_used_in_reasoning=True,
                channel_used_in_decision=False,
            )
        )

    # newly observed
    vca = frame.get("visual_candidate_audit") if isinstance(frame.get("visual_candidate_audit"), dict) else None
    labels = None
    if isinstance(vca, dict):
        labels = vca.get("mapped_candidate_labels") or vca.get("detector_candidate_labels")
    sidecar = frame.get("spatial_expression_sidecar") if isinstance(frame.get("spatial_expression_sidecar"), dict) else None
    sc_count = 0
    if isinstance(sidecar, dict) and isinstance(sidecar.get("candidates"), list):
        sc_count = len(sidecar.get("candidates") or [])
    if (isinstance(labels, list) and len(labels) > 0) or sc_count > 0:
        lab = ",".join([str(x) for x in (labels or [])[:5]]) if isinstance(labels, list) and labels else f"sidecar_candidates={sc_count}"
        chans.append(
            InformationChannelItem(
                channel_type="newly_observed",
                channel_label="Newly observed",
                channel_summary=lab,
                channel_source_module="visual_candidate_audit" if isinstance(labels, list) else "spatial_expression_sidecar",
                channel_used_in_reasoning=True,
                channel_used_in_decision=False,
            )
        )

    # inferred from exclusion
    tree = frame.get("reasoning_structure_tree") if isinstance(frame.get("reasoning_structure_tree"), dict) else None
    pruned = set()
    if isinstance(tree, dict) and isinstance(tree.get("pruned_node_ids"), list):
        pruned = set(str(x) for x in tree.get("pruned_node_ids") if x is not None)
    nodes = tree.get("nodes") if isinstance(tree, dict) else None
    has_pruned = False
    if isinstance(nodes, list):
        for n in nodes:
            if isinstance(n, dict) and (str(n.get("node_id")) in pruned or (str(n.get("status") or "").lower() in ("pruned", "rejected"))):
                has_pruned = True
                break
    metrics = frame.get("reasoning_tree_metrics") if isinstance(frame.get("reasoning_tree_metrics"), dict) else None
    dead = int(metrics.get("dead_branch_count") or 0) if isinstance(metrics, dict) else 0
    issue = _s(metrics.get("possible_tree_issue_type")) if isinstance(metrics, dict) else None
    if has_pruned or (dead > 0 and issue == "high_dead_branch_ratio"):
        chans.append(
            InformationChannelItem(
                channel_type="inferred_from_exclusion",
                channel_label="Inferred from exclusion",
                channel_summary="pruned/excluded paths influenced candidate selection",
                channel_source_module="reasoning_structure_tree",
                channel_used_in_reasoning=True,
                channel_used_in_decision=False,
            )
        )

    # hybrid (if both memory and newly observed present)
    has_mem = any(c.channel_type == "memory_derived" for c in chans)
    has_novel = any(c.channel_type == "newly_observed" for c in chans)
    if has_mem and has_novel:
        chans.append(
            InformationChannelItem(
                channel_type="hybrid",
                channel_label="Hybrid",
                channel_summary="memory + newly observed combined",
                channel_source_module="memory_novel_information_channel",
                channel_used_in_reasoning=True,
                channel_used_in_decision=True,
            )
        )

    # counts & dominant channels
    mem_cnt = sum(1 for c in chans if c.channel_type == "memory_derived")
    novel_cnt = sum(1 for c in chans if c.channel_type in ("newly_observed", "inferred_from_exclusion", "user_provided"))
    hyb_cnt = sum(1 for c in chans if c.channel_type == "hybrid")

    # dominant reasoning: max count among memory vs novel vs hybrid
    if hyb_cnt > max(mem_cnt, novel_cnt):
        dom_r = "hybrid"
    elif novel_cnt >= mem_cnt:
        dom_r = "newly_observed" if has_novel else ("user_provided" if any(c.channel_type == "user_provided" for c in chans) else "inferred_from_exclusion")
    else:
        dom_r = "memory_derived"

    # dominant decision: if user_provided used_in_decision → user_provided; else hybrid; else memory/novel by presence
    if any(c.channel_type == "user_provided" and c.channel_used_in_decision for c in chans):
        dom_d = "user_provided"
    elif hyb_cnt > 0:
        dom_d = "hybrid"
    elif has_mem:
        dom_d = "memory_derived"
    else:
        dom_d = "newly_observed" if has_novel else None

    # novel_memory_candidate (reserve-only)
    next_effect = _s(_get(frame, "confirmation_input_bridge", "confirmation_bridge_next_effect"))
    used_in_decision = bool(next_effect and next_effect != "none") or bool(_get(metrics, "effective_feedback_count") or 0) > 0
    candidate = None
    if used_in_decision:
        if any(c.channel_type == "inferred_from_exclusion" for c in chans):
            candidate = NovelMemoryCandidate(
                candidate_label=_s(_get(frame, "object_search_interaction", "search_target_label")) or "novel_candidate",
                candidate_reason="derived from exclusion and impacted current decision",
                candidate_source="inferred_from_exclusion",
                candidate_ready_for_memory=False,
                candidate_summary="reserve-only (no memory write)",
            )
        elif any(c.channel_type == "newly_observed" for c in chans):
            candidate = NovelMemoryCandidate(
                candidate_label=_s(_get(frame, "object_search_interaction", "search_target_label")) or "novel_candidate",
                candidate_reason="new observation impacted current decision",
                candidate_source="newly_observed",
                candidate_ready_for_memory=False,
                candidate_summary="reserve-only (no memory write)",
            )

    summ = f"dominant_reasoning={dom_r} dominant_decision={dom_d} mem={mem_cnt} novel={novel_cnt} hybrid={hyb_cnt}"
    return MemoryNovelInformationChannelResult(
        information_channels=chans,
        memory_channel_count=mem_cnt,
        novel_channel_count=novel_cnt,
        hybrid_channel_count=hyb_cnt,
        dominant_reasoning_channel=dom_r,
        dominant_decision_channel=dom_d,
        novel_memory_candidate=candidate,
        channel_summary=summ,
        channel_applied=True,
    )

