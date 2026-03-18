# -*- coding: utf-8 -*-
"""
假设层 M0：Hypothesis Layer（最小候选解释层）。

在 Evidence Ledger M0 基础上增加最小 Hypothesis Layer：
仅基于已有证据结构生成少量、受约束、可回溯、可验证的候选解释。
不做完整场景推理、不做学习、不做经验沉淀、不做开放世界无限候选。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional

from .evidence_ledger import EvidenceLedger
from .local_goal_spatial_map import LocalGoalSpatialMap
from .local_goal_spatial_relations import SpatialRelation
from .skeleton_filter import SkeletonFilterResult
from .skeleton_mix import SkeletonMix
from .spatial_memory_pools import SpatialMemoryPools

HYPOTHESIS_TYPES = (
    "container_candidate",
    "path_continuation_candidate",
    "occluded_object_candidate",
    "interaction_target_candidate",
)
HYPOTHESIS_STATUSES = ("candidate", "needs_check", "rejected", "promoted")
VERIFICATION_HINTS = (
    "recheck_environment",
    "recheck_close_range",
    "shift_view_left",
    "shift_view_right",
    "look_forward",
    "hold_and_confirm",
    "ask_user_for_clarification",
)


@dataclass
class Hypothesis:
    """单条候选假设：摘要、类型、证据引用、缺失、置信度、风险、验证建议、状态。"""
    hypothesis_summary: str
    hypothesis_type: str  # one of HYPOTHESIS_TYPES
    supporting_evidence_refs: List[str] = field(default_factory=list)
    missing_evidence: List[str] = field(default_factory=list)
    hypothesis_confidence: float = 0.0
    risk_if_wrong: Optional[str] = None
    verification_hint: Optional[str] = None
    hypothesis_status: str = "candidate"  # candidate / needs_check / rejected / promoted


@dataclass
class HypothesisLayer:
    """假设层容器：多条假设 + 可选主导类型与原因摘要。"""
    hypotheses: List[Hypothesis] = field(default_factory=list)
    dominant_hypothesis_type: Optional[str] = None
    hypothesis_reason_summary: Optional[str] = None


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _ledger_has_missing(ledger: Optional[EvidenceLedger], *keywords: str) -> bool:
    if not ledger or not getattr(ledger, "entries", None):
        return False
    for e in ledger.entries:
        for m in getattr(e, "missing_evidence", None) or []:
            for kw in keywords:
                if kw in (m or ""):
                    return True
    return False


def _ledger_claim_texts(ledger: Optional[EvidenceLedger]) -> List[str]:
    if not ledger or not getattr(ledger, "entries", None):
        return []
    return [getattr(e, "claim_summary", "") or "" for e in ledger.entries]


def _apply_risk_gate(
    status: str,
    verification_hint: Optional[str],
    dominant: str,
    runtime_domain_state: Optional[str],
    risk_if_wrong: Optional[str],
) -> tuple[str, Optional[str]]:
    """
    风险闸门：当 dominant==safety 或 runtime_domain 为 degraded/frozen 或风险高时，
    status 不得为 promoted，至少 candidate/needs_check，verification_hint 必须存在。
    """
    high_risk = (
        dominant == "safety"
        or (runtime_domain_state or "") in ("degraded", "frozen")
        or (risk_if_wrong and ("高" in risk_if_wrong or "严重" in risk_if_wrong))
    )
    if high_risk and status == "promoted":
        status = "needs_check"
    if high_risk and not verification_hint:
        verification_hint = "hold_and_confirm"
    return status, verification_hint


def build_hypothesis_layer(
    ledger: Optional[EvidenceLedger],
    smap: Optional[LocalGoalSpatialMap],
    relations: Optional[List[Any]],
    mix: Optional[SkeletonMix],
    filt: Optional[SkeletonFilterResult],
    pools: Optional[SpatialMemoryPools],
    state: Any,
) -> HypothesisLayer:
    """
    仅从 evidence_ledger、smap、relations、mix、filt、pools 生成 1～3 条受约束候选假设。
    高风险场景下不设 promoted，verification_hint 必填。
    """
    hypotheses: List[Hypothesis] = []
    dominant = _get(mix, "dominant_skeleton") or "navigation"
    runtime_domain_state = _get(state, "runtime_domain_state")
    claim_texts = _ledger_claim_texts(ledger)
    working_n = len(getattr(pools, "working_memory_items", None) or [])

    # ----- object_search hints (M0): promote container/occlusion when explicit hint exists -----
    container_hint: Optional[str] = None
    occlusion_hint: Optional[str] = None
    for text in claim_texts[:3]:
        t = (text or "").strip()
        if t.startswith("容器候选："):
            # e.g. "容器候选：cup | ..."
            v = t[len("容器候选：") :].strip()
            container_hint = (v.split("|", 1)[0].strip() or None)
        if t.startswith("遮挡候选："):
            v = t[len("遮挡候选：") :].strip()
            occlusion_hint = (v.split("|", 1)[0].strip() or None)

    if container_hint:
        refs = ["evidence_ledger", f"claim:{claim_texts[0][:40]}"]
        missing = ["需确认对象是否进入容器或离开视野", "需要打开容器确认"]
        status = "needs_check"
        hint = "recheck_close_range"
        status, hint = _apply_risk_gate(status, hint, dominant, runtime_domain_state, "容器误判可能导致搜索动作错误")
        hypotheses.append(Hypothesis(
            hypothesis_summary=container_hint,
            hypothesis_type="container_candidate",
            supporting_evidence_refs=refs[:3],
            missing_evidence=missing,
            hypothesis_confidence=0.65,
            risk_if_wrong="容器误判可能导致搜索动作错误",
            verification_hint=hint,
            hypothesis_status=status,
        ))

    if occlusion_hint and not container_hint:
        refs = ["evidence_ledger", f"claim:{claim_texts[0][:40]}"]
        missing = ["当前目标/交互对象可能被遮挡或未进入视野", "需要清理遮挡或调整视角复核"]
        status = "needs_check"
        hint = "recheck_environment"
        status, hint = _apply_risk_gate(status, hint, dominant, runtime_domain_state, "遮挡误判可能漏检目标")
        hypotheses.append(Hypothesis(
            hypothesis_summary="目标或交互对象可能被遮挡，需复核环境",
            hypothesis_type="occluded_object_candidate",
            supporting_evidence_refs=refs[:3],
            missing_evidence=missing,
            hypothesis_confidence=0.5,
            risk_if_wrong="遮挡误判可能漏检目标",
            verification_hint=hint,
            hypothesis_status=status,
        ))

    # ----- path_continuation_candidate -----
    focus = getattr(smap, "focus_region", None) or []
    trav = getattr(smap, "traversable_region", None) or []
    confirm = getattr(smap, "confirm_region", None) or []
    has_path_evidence = (len(focus) > 0 or len(trav) > 0) and (len(confirm) == 0 or working_n == 0)
    has_supports = False
    if relations:
        for r in relations:
            if getattr(r, "relation_type", "") in ("supports", "adjacent_to"):
                has_supports = True
                break
    if has_path_evidence or has_supports:
        refs = ["claim:空间结构"]
        if claim_texts:
            refs.append(claim_texts[0][:30] if len(claim_texts[0]) > 30 else claim_texts[0])
        missing = ["需 confirm 或 anchor 支撑路径延续"] if not confirm else []
        status = "candidate"
        hint = "recheck_close_range" if missing else "look_forward"
        status, hint = _apply_risk_gate(status, hint, dominant, runtime_domain_state, "路径误判可能导致错误前进")
        hypotheses.append(Hypothesis(
            hypothesis_summary="路径可能延续，需 confirm 或锚点支撑",
            hypothesis_type="path_continuation_candidate",
            supporting_evidence_refs=refs,
            missing_evidence=missing,
            hypothesis_confidence=0.5,
            risk_if_wrong="路径误判可能导致错误前进",
            verification_hint=hint,
            hypothesis_status=status,
        ))

    # ----- interaction_target_candidate -----
    if dominant == "fine_interaction" and (confirm or focus):
        refs = ["dominant=fine_interaction", "claim:主导空间关注"]
        missing = ["目标未完全确认"]
        status = "candidate"
        hint = "recheck_close_range"
        status, hint = _apply_risk_gate(status, hint, dominant, runtime_domain_state, "交互目标误判可能导致误操作")
        hypotheses.append(Hypothesis(
            hypothesis_summary="近场存在可交互目标候选，需进一步确认",
            hypothesis_type="interaction_target_candidate",
            supporting_evidence_refs=refs,
            missing_evidence=missing,
            hypothesis_confidence=0.45,
            risk_if_wrong="交互目标误判可能导致误操作",
            verification_hint=hint,
            hypothesis_status=status,
        ))

    # ----- occluded_object_candidate -----
    if not occlusion_hint and (_ledger_has_missing(ledger, "需要", "遮挡", "近场", "覆盖", "证据") or not focus):
        refs = ["evidence_ledger"]
        for e in (getattr(ledger, "entries", None) or [])[:2]:
            refs.append(f"claim:{(getattr(e, 'claim_summary', '') or '')[:25]}")
        missing = ["当前目标/交互对象可能被遮挡或未进入视野"]
        status = "needs_check"
        hint = "recheck_environment"
        status, hint = _apply_risk_gate(status, hint, dominant, runtime_domain_state, "遮挡误判可能漏检目标")
        hypotheses.append(Hypothesis(
            hypothesis_summary="目标或交互对象可能被遮挡，需复核环境",
            hypothesis_type="occluded_object_candidate",
            supporting_evidence_refs=refs[:3],
            missing_evidence=missing,
            hypothesis_confidence=0.35,
            risk_if_wrong="遮挡误判可能漏检目标",
            verification_hint=hint,
            hypothesis_status=status,
        ))

    # ----- container_candidate（仅当证据暗示容器/可见性丢失时）-----
    if not container_hint:
        for text in claim_texts:
            if "容器" in text or "portal" in text.lower() or "可见性" in text or "消失" in text:
                refs = ["evidence_ledger"]
                missing = ["需确认对象是否进入容器或离开视野"]
                status = "candidate"
                hint = "recheck_environment"
                status, hint = _apply_risk_gate(status, hint, dominant, runtime_domain_state, "容器/可见性误判可能丢失目标")
                hypotheses.append(Hypothesis(
                    hypothesis_summary="对象可能进入容器或离开当前视野",
                    hypothesis_type="container_candidate",
                    supporting_evidence_refs=refs,
                    missing_evidence=missing,
                    hypothesis_confidence=0.3,
                    risk_if_wrong="容器/可见性误判可能丢失目标",
                    verification_hint=hint,
                    hypothesis_status=status,
                ))
                break

    # 若尚未生成 container，且已有假设不足 3 条，可补一条弱 container（仅当有 missing 证据提及“区域”等）
    has_container = any(getattr(h, "hypothesis_type", "") == "container_candidate" for h in hypotheses)
    if not has_container and len(hypotheses) < 3 and _ledger_has_missing(ledger, "区域", "空间图"):
        refs = ["claim:空间结构"]
        missing = ["需确认是否进入某区域或容器"]
        status = "candidate"
        hint = "hold_and_confirm"
        status, hint = _apply_risk_gate(status, hint, dominant, runtime_domain_state, "区域误判可能丢失目标")
        hypotheses.append(Hypothesis(
            hypothesis_summary="可能进入某区域或容器，需确认",
            hypothesis_type="container_candidate",
            supporting_evidence_refs=refs,
            missing_evidence=missing,
            hypothesis_confidence=0.25,
            risk_if_wrong="区域误判可能丢失目标",
            verification_hint=hint,
            hypothesis_status=status,
        ))

    # 去重类型并限制 3 条
    seen_types: set = set()
    deduped: List[Hypothesis] = []
    for h in hypotheses:
        if h.hypothesis_type not in seen_types and len(deduped) < 3:
            seen_types.add(h.hypothesis_type)
            deduped.append(h)
    hypotheses = deduped

    dominant_type = hypotheses[0].hypothesis_type if hypotheses else None
    reason = f"dominant={dominant} n={len(hypotheses)}"
    return HypothesisLayer(
        hypotheses=hypotheses,
        dominant_hypothesis_type=dominant_type,
        hypothesis_reason_summary=reason,
    )
