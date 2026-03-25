# -*- coding: utf-8 -*-
"""
Evidence / Hypothesis Whitebox Trace M0（证据×假设白盒轨迹）

沿用已冻结 Whitebox Trace Schema（五块骨架）+ 用户可见解释层：
- reasoning_steps
- weight_allocation
- exclusion_log
- interaction_trace
- user_visible_explanation
- whitebox_summary / whitebox_applied

定位：
- 只解释，不改写 evidence_ledger / hypothesis_layer 主逻辑
- 明确：evidence 如何形成、hypothesis 为什么是这个、为何排除其它、反馈如何影响
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


def _s(x: Any) -> Optional[str]:
    if x is None:
        return None
    t = str(x)
    return t if t.strip() else None


@dataclass
class EvidenceHypothesisReasoningStep:
    step_index: int
    step_name: str
    step_input_summary: Optional[str] = None
    step_output_summary: Optional[str] = None


@dataclass
class EvidenceHypothesisWeightItem:
    candidate_id: str
    candidate_human_label: Optional[str] = None
    weight_total: float = 0.0
    weight_components: Dict[str, float] = field(default_factory=dict)
    weight_reason: Optional[str] = None


@dataclass
class EvidenceHypothesisExclusionItem:
    excluded_candidate_id: str
    excluded_candidate_human_label: Optional[str] = None
    excluded_reason: Optional[str] = None
    excluded_at_stage: Optional[str] = None


@dataclass
class EvidenceHypothesisInteractionItem:
    user_feedback_raw: Optional[str] = None
    mapped_confirmation_type: Optional[str] = None
    interaction_effect_on_hypothesis: Optional[str] = None


@dataclass
class EvidenceHypothesisUserVisibleExplanation:
    user_visible_reason_evidence: Optional[str] = None
    user_visible_reason_hypothesis: Optional[str] = None
    user_visible_excluded_alternative: Optional[str] = None
    user_visible_feedback_impact: Optional[str] = None


@dataclass
class EvidenceHypothesisWhiteboxTraceResult:
    reasoning_steps: List[EvidenceHypothesisReasoningStep] = field(default_factory=list)
    weight_allocation: List[EvidenceHypothesisWeightItem] = field(default_factory=list)
    exclusion_log: List[EvidenceHypothesisExclusionItem] = field(default_factory=list)
    interaction_trace: List[EvidenceHypothesisInteractionItem] = field(default_factory=list)
    user_visible_explanation: Optional[EvidenceHypothesisUserVisibleExplanation] = None
    # Memory vs Novel Information Channel M0 (light attach): one-line source channel summary
    information_channel_summary: Optional[str] = None
    whitebox_summary: Optional[str] = None
    whitebox_applied: bool = False


HYP_HUMAN = {
    "container_candidate": "容器假设",
    "occluded_object_candidate": "遮挡假设",
    "path_continuation_candidate": "路径延续假设",
    "interaction_target_candidate": "交互目标假设",
}


def _hyp_human(hyp_type: str) -> str:
    return HYP_HUMAN.get(hyp_type or "", hyp_type or "—")


def _weight_hypothesis(
    hyp: Any,
    ledger_entries: List[Any],
    *,
    confirmation_input_type: Optional[str],
    confirmation_raw: Optional[str],
) -> EvidenceHypothesisWeightItem:
    hyp_type = _s(_get(hyp, "hypothesis_type")) or "unknown"
    hyp_sum = _s(_get(hyp, "hypothesis_summary")) or ""
    base = float(_get(hyp, "hypothesis_confidence", 0.0) or 0.0)

    comps: Dict[str, float] = {}
    # base confidence（来自 hypothesis_layer 输出）
    comps["base_confidence"] = round(base, 3)

    # evidence hints
    claim_texts = []
    for e in ledger_entries[:3]:
        claim_texts.append(_s(_get(e, "claim_summary")) or "")
    joined = " | ".join([t for t in claim_texts if t])
    if hyp_type == "container_candidate" and ("容器候选" in joined or "容器" in joined):
        comps["container_alignment_bonus"] = 0.18
    if hyp_type == "occluded_object_candidate" and ("遮挡候选" in joined or "遮挡" in joined):
        comps["occlusion_alignment_bonus"] = 0.18

    # object_search_hint bonus (if evidence contains object_search_hint)
    if "object_search_hint" in joined:
        comps["object_search_hint_bonus"] = 0.10

    # weak evidence penalty (very low evidence confidence)
    try:
        ev0 = ledger_entries[0]
        ev_conf = float(_get(ev0, "evidence_confidence", 0.0) or 0.0)
    except Exception:
        ev_conf = 0.0
    if ev_conf < 0.35:
        comps["weak_evidence_penalty"] = -0.12

    # conflicting signal penalty
    conflict_n = 0
    for e in ledger_entries[:2]:
        conflict_n += len(_get(e, "conflicting_evidence") or [])
    if conflict_n >= 2:
        comps["conflicting_signal_penalty"] = -0.10

    # feedback support/penalty
    effect = None
    if confirmation_raw:
        if confirmation_input_type in ("opened_container", "checked_and_not_found", "target_not_found"):
            if hyp_type == "container_candidate":
                comps["user_denied_penalty"] = -0.20
                effect = "用户反馈使“容器”假设降权"
        if confirmation_input_type in ("occlusion_cleared", "checked_and_not_found", "target_not_found"):
            if hyp_type == "occluded_object_candidate":
                comps["user_denied_penalty"] = -0.16
                effect = "用户反馈使“遮挡”假设降权"
        if confirmation_input_type in ("target_found", "confirmed_yes"):
            comps["feedback_support_bonus"] = 0.10
            effect = "用户反馈对当前假设提供正向支撑"

    total = float(sum(comps.values()))
    reason = f"type={hyp_type} base={base:.2f}"
    if effect:
        reason += f" | {effect}"
    return EvidenceHypothesisWeightItem(
        candidate_id=hyp_type,
        candidate_human_label=_hyp_human(hyp_type),
        weight_total=round(total, 3),
        weight_components=comps,
        weight_reason=reason,
    )


def build_evidence_hypothesis_whitebox_trace(
    *,
    evidence_ledger: Any,
    hypothesis_layer: Any,
    confirmation_input_bridge: Any = None,
) -> EvidenceHypothesisWhiteboxTraceResult:
    entries = list(_get(evidence_ledger, "entries") or [])
    hyps = list(_get(hypothesis_layer, "hypotheses") or [])
    dominant = _s(_get(hypothesis_layer, "dominant_hypothesis_type"))
    reason_sum = _s(_get(hypothesis_layer, "hypothesis_reason_summary"))

    raw = _s(_get(confirmation_input_bridge, "confirmation_input_raw_text"))
    ctype = _s(_get(confirmation_input_bridge, "confirmation_input_type"))

    steps: List[EvidenceHypothesisReasoningStep] = []
    steps.append(
        EvidenceHypothesisReasoningStep(
            1,
            "read_evidence_ledger",
            step_input_summary=f"entries={len(entries)}",
            step_output_summary=_s(_get(entries[0], "claim_summary")) if entries else "—",
        )
    )
    steps.append(
        EvidenceHypothesisReasoningStep(
            2,
            "read_hypothesis_layer",
            step_input_summary=f"hypotheses={len(hyps)} dominant={dominant or '—'}",
            step_output_summary=reason_sum or "—",
        )
    )
    fb_out = "no_feedback"
    if raw:
        fb_out = f"feedback_type={ctype or '—'} raw={raw[:40]}"
    steps.append(
        EvidenceHypothesisReasoningStep(
            3,
            "apply_feedback_signal",
            step_input_summary=raw or "—",
            step_output_summary=fb_out,
        )
    )

    weights: List[EvidenceHypothesisWeightItem] = []
    for h in hyps[:4]:
        weights.append(
            _weight_hypothesis(
                h,
                entries,
                confirmation_input_type=ctype,
                confirmation_raw=raw,
            )
        )

    # sort by weight_total desc
    weights.sort(key=lambda w: float(w.weight_total), reverse=True)
    top = weights[0] if weights else None

    exclusions: List[EvidenceHypothesisExclusionItem] = []
    # ensure at least one exclusion: pick the lowest (if >=2)
    if len(weights) >= 2:
        low = weights[-1]
        exclusions.append(
            EvidenceHypothesisExclusionItem(
                excluded_candidate_id=low.candidate_id,
                excluded_candidate_human_label=low.candidate_human_label,
                excluded_reason="权重较低/与当前证据或反馈不一致",
                excluded_at_stage="hypothesis_selection",
            )
        )

    # add exclusions for hypotheses not equal to dominant when present
    for w in weights[1:3]:
        if dominant and w.candidate_id == dominant:
            continue
        if top and w.candidate_id == top.candidate_id:
            continue
        if all(x.excluded_candidate_id != w.candidate_id for x in exclusions):
            exclusions.append(
                EvidenceHypothesisExclusionItem(
                    excluded_candidate_id=w.candidate_id,
                    excluded_candidate_human_label=w.candidate_human_label,
                    excluded_reason="未成为主导解释（备选分支）",
                    excluded_at_stage="dominant_selection",
                )
            )

    interactions: List[EvidenceHypothesisInteractionItem] = []
    if raw or ctype:
        interactions.append(
            EvidenceHypothesisInteractionItem(
                user_feedback_raw=raw,
                mapped_confirmation_type=ctype,
                interaction_effect_on_hypothesis="反馈信号已纳入权重组件（规则版）" if raw else "—",
            )
        )

    uv = EvidenceHypothesisUserVisibleExplanation(
        user_visible_reason_evidence=(
            f"我先基于当前证据账本（{len(entries)} 条）判断可优先关注的线索。"
            if entries
            else "当前证据较少，我只能先用保守的默认线索推进。"
        ),
        user_visible_reason_hypothesis=(
            f"目前更像是「{_hyp_human((top.candidate_id if top else dominant) or '')}」："
            f"{(top.weight_reason if top else (reason_sum or ''))[:80] or '—'}"
            if (top or dominant)
            else "当前缺少足够证据生成稳定假设，我会先补证再判断。"
        ),
        user_visible_excluded_alternative=(
            f"我暂时没有优先采用「{exclusions[0].excluded_candidate_human_label}」，因为：{exclusions[0].excluded_reason}"
            if exclusions
            else "暂无明显需要排除的备选解释。"
        ),
        user_visible_feedback_impact=(
            "你刚才的反馈会影响我对“容器/遮挡/一般搜索”等解释的权重，从而改变后续优先检查方向。"
            if raw
            else "当前还没有用户反馈，因此我只依据证据与默认规则选择假设。"
        ),
    )

    whitebox_summary = f"hypotheses={len(hyps)} dominant={dominant or (top.candidate_id if top else '—')} excl={len(exclusions)}"
    info_ch = None
    try:
        mn = frame.get("memory_novel_information_channel") if isinstance(frame, dict) else None
        if isinstance(mn, dict):
            dr = _s(mn.get("dominant_reasoning_channel"))
            dd = _s(mn.get("dominant_decision_channel"))
            if dr or dd:
                info_ch = f"channel reasoning={dr or '—'} decision={dd or '—'}"
    except Exception:
        info_ch = None
    return EvidenceHypothesisWhiteboxTraceResult(
        reasoning_steps=steps,
        weight_allocation=weights,
        exclusion_log=exclusions,
        interaction_trace=interactions,
        user_visible_explanation=uv,
        information_channel_summary=info_ch,
        whitebox_summary=whitebox_summary,
        whitebox_applied=True,
    )

