# -*- coding: utf-8 -*-
"""
Experience Governance Whitebox Trace M0（经验治理白盒轨迹）

沿用已冻结 Whitebox Trace Schema（五块骨架）+ 用户可见解释层：
- reasoning_steps
- weight_allocation
- exclusion_log
- interaction_trace
- user_visible_explanation
- whitebox_summary / whitebox_applied

定位：
- 只解释，不改写 experience_evolution 主逻辑
- 明确：为什么进入 watchlist/promotable/blocked/rejected，scope/contradiction/repeat/feedback 的影响
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
class ExperienceGovernanceReasoningStep:
    step_index: int
    step_name: str
    step_input_summary: Optional[str] = None
    step_output_summary: Optional[str] = None


@dataclass
class ExperienceGovernanceWeightItem:
    governance_outcome_id: str
    governance_outcome_label: Optional[str] = None
    weight_total: float = 0.0
    weight_components: Dict[str, float] = field(default_factory=dict)
    weight_reason: Optional[str] = None


@dataclass
class ExperienceGovernanceExclusionItem:
    excluded_outcome_id: str
    excluded_outcome_label: Optional[str] = None
    excluded_reason: Optional[str] = None
    excluded_at_stage: Optional[str] = None


@dataclass
class ExperienceGovernanceInteractionItem:
    user_feedback_raw: Optional[str] = None
    mapped_confirmation_type: Optional[str] = None
    interaction_effect_on_experience: Optional[str] = None


@dataclass
class ExperienceGovernanceUserVisibleExplanation:
    user_visible_reason_status: Optional[str] = None
    user_visible_reason_scope: Optional[str] = None
    user_visible_excluded_alternative: Optional[str] = None
    user_visible_feedback_impact: Optional[str] = None


@dataclass
class ExperienceGovernanceWhiteboxTraceResult:
    reasoning_steps: List[ExperienceGovernanceReasoningStep] = field(default_factory=list)
    weight_allocation: List[ExperienceGovernanceWeightItem] = field(default_factory=list)
    exclusion_log: List[ExperienceGovernanceExclusionItem] = field(default_factory=list)
    interaction_trace: List[ExperienceGovernanceInteractionItem] = field(default_factory=list)
    user_visible_explanation: Optional[ExperienceGovernanceUserVisibleExplanation] = None
    # Memory vs Novel Information Channel M0 (light attach): one-line source channel summary
    information_channel_summary: Optional[str] = None
    whitebox_summary: Optional[str] = None
    whitebox_applied: bool = False


OUTCOME_HUMAN = {
    "watchlist": "观察列表",
    "promotable": "可升格",
    "blocked": "阻断",
    "rejected": "拒绝",
    "candidate": "候选",
}


def _outcome_human(o: str) -> str:
    return OUTCOME_HUMAN.get(o or "", o or "—")


def _score_outcomes(
    cand: Any,
    *,
    confirmation_input_type: Optional[str],
    confirmation_raw: Optional[str],
) -> List[ExperienceGovernanceWeightItem]:
    """
    规则版：根据 experience_evolution 候选字段，构造四类 outcome 的权重解释。
    """
    support = int(_get(cand, "supporting_events_count", 0) or 0)
    repeat = int(_get(cand, "repeated_pattern_count", 0) or 0)
    confirm = int(_get(cand, "user_confirmed_count", 0) or 0)
    fallback = int(_get(cand, "fallback_count", 0) or 0)
    contradict = int(_get(cand, "contradiction_count", 0) or 0)
    contradict_src = list(_get(cand, "contradiction_sources") or [])
    scope = _s(_get(cand, "future_use_scope"))
    status = _s(_get(cand, "evolution_status")) or "candidate"

    # base components
    base: Dict[str, float] = {}
    if repeat >= 2:
        base["repeat_bonus"] = 0.25
    elif repeat >= 1:
        base["repeat_bonus"] = 0.12
    if support >= 1:
        base["support_bonus"] = 0.18
    if confirm >= 1:
        base["confirmation_bonus"] = 0.18
    if contradict >= 1 or ("user_denied" in contradict_src):
        base["contradiction_penalty"] = -0.28
    if fallback >= 2:
        base["fallback_penalty"] = -0.18
    if "blocked_context" in contradict_src:
        base["blocked_context_penalty"] = -0.16
    if confirmation_raw and confirmation_input_type in ("target_not_found", "confirmed_no"):
        base["user_denied_penalty"] = -0.10

    def mk(outcome: str, extra: Dict[str, float]) -> ExperienceGovernanceWeightItem:
        comps = dict(base)
        comps.update(extra)
        total = float(sum(comps.values()))
        r = f"status={status} repeat={repeat} support={support} confirm={confirm} fallback={fallback} contradict={contradict}"
        if scope:
            r += f" scope={scope}"
        return ExperienceGovernanceWeightItem(
            governance_outcome_id=outcome,
            governance_outcome_label=_outcome_human(outcome),
            weight_total=round(total, 3),
            weight_components=comps,
            weight_reason=r,
        )

    # outcome biases (keep rule-simple)
    items = [
        mk("promotable", {"promotable_bias": 0.10}),
        mk("watchlist", {"watchlist_bias": 0.08}),
        mk("blocked", {"blocked_bias": 0.06}),
        mk("rejected", {"rejected_bias": 0.04}),
    ]
    items.sort(key=lambda x: float(x.weight_total), reverse=True)
    return items


def build_experience_governance_whitebox_trace(
    *,
    experience_evolution: Any,
    confirmation_input_bridge: Any = None,
) -> ExperienceGovernanceWhiteboxTraceResult:
    cands = list(_get(experience_evolution, "candidates") or [])
    cand0 = cands[0] if cands else None
    status = _s(_get(cand0, "evolution_status")) if cand0 else None
    reason = _s(_get(cand0, "evolution_reason")) if cand0 else None
    scope = _s(_get(cand0, "future_use_scope")) if cand0 else None

    raw = _s(_get(confirmation_input_bridge, "confirmation_input_raw_text"))
    ctype = _s(_get(confirmation_input_bridge, "confirmation_input_type"))

    steps: List[ExperienceGovernanceReasoningStep] = []
    steps.append(
        ExperienceGovernanceReasoningStep(
            1,
            "read_experience_candidates",
            step_input_summary=f"candidates={len(cands)}",
            step_output_summary=f"status={status or '—'} scope={scope or '—'}",
        )
    )
    steps.append(
        ExperienceGovernanceReasoningStep(
            2,
            "derive_governance_outcome",
            step_input_summary=(reason or "—")[:120] if reason else "—",
            step_output_summary=f"outcome={status or '—'}",
        )
    )
    fb_out = "no_feedback"
    if raw:
        fb_out = f"feedback_type={ctype or '—'} raw={raw[:40]}"
    steps.append(
        ExperienceGovernanceReasoningStep(
            3,
            "apply_feedback_signal",
            step_input_summary=raw or "—",
            step_output_summary=fb_out,
        )
    )

    weights: List[ExperienceGovernanceWeightItem] = []
    if cand0:
        weights = _score_outcomes(cand0, confirmation_input_type=ctype, confirmation_raw=raw)

    exclusions: List[ExperienceGovernanceExclusionItem] = []
    # ensure at least one exclusion: outcome not selected but near-top
    if weights:
        selected = status or weights[0].governance_outcome_id
        for w in weights:
            if w.governance_outcome_id != selected:
                exclusions.append(
                    ExperienceGovernanceExclusionItem(
                        excluded_outcome_id=w.governance_outcome_id,
                        excluded_outcome_label=w.governance_outcome_label,
                        excluded_reason="与当前支撑/冲突/重复度/风险闸门不匹配（规则版）",
                        excluded_at_stage="governance_selection",
                    )
                )
                break

    interactions: List[ExperienceGovernanceInteractionItem] = []
    if raw or ctype:
        interactions.append(
            ExperienceGovernanceInteractionItem(
                user_feedback_raw=raw,
                mapped_confirmation_type=ctype,
                interaction_effect_on_experience="反馈将影响 contradiction/confirm 计数与后续升降级（当前为展示层规则解释）"
                if raw
                else "—",
            )
        )

    uv = ExperienceGovernanceUserVisibleExplanation(
        user_visible_reason_status=(
            f"这条经验目前处于「{_outcome_human(status or 'candidate')}」：{(reason or '—')[:90]}"
            if status
            else "当前没有可治理的经验候选，因此不会做升格/拒绝。"
        ),
        user_visible_reason_scope=(
            f"它的未来适用范围是「{scope}」，避免在不相似场景中误用。"
            if scope
            else "当前范围信息不足，我会先保持局部适用，不做跨场景推广。"
        ),
        user_visible_excluded_alternative=(
            f"我没有直接给到「{exclusions[0].excluded_outcome_label}」，因为：{exclusions[0].excluded_reason}"
            if exclusions
            else "暂无明确需要排除的治理结果备选。"
        ),
        user_visible_feedback_impact=(
            "你的反馈会影响经验的“确认/否认/回退/冲突来源”统计，从而改变它未来是升格还是被阻断/拒绝。"
            if raw
            else "当前无用户反馈，本轮经验治理只依据已观测到的支撑/冲突与风险闸门。"
        ),
    )

    whitebox_summary = f"candidates={len(cands)} outcome={status or '—'} scope={scope or '—'} excl={len(exclusions)}"
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
    return ExperienceGovernanceWhiteboxTraceResult(
        reasoning_steps=steps,
        weight_allocation=weights,
        exclusion_log=exclusions,
        interaction_trace=interactions,
        user_visible_explanation=uv,
        information_channel_summary=info_ch,
        whitebox_summary=whitebox_summary,
        whitebox_applied=True,
    )

