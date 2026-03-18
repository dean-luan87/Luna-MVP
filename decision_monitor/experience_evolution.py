# -*- coding: utf-8 -*-
"""
经验演化约束层 M0/M1：Experience / Evidence Evolution。

M0：单轮审计与约束，避免单次幸运成功被误当成稳定经验。
M1：多轮经验候选治理——同类聚合、contradiction_sources、watchlist/promotable/blocked/rejected 细化、
    evolution_confidence_band、future_use_scope、审计报告式 reason。
不做学习系统、不做长期经验库、不做自动策略更新、不跨会话持久化。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional

EXPERIENCE_TYPES = (
    "object_search_path_pattern",
    "container_candidate_pattern",
    "occlusion_resolution_pattern",
    "pocket_check_pattern",
    "recheck_effectiveness_pattern",
)

EVOLUTION_STATUSES = ("candidate", "watchlist", "promotable", "blocked", "rejected")

CONFIDENCE_TRENDS = ("up", "flat", "down")

EVOLUTION_HINTS = ("preferred", "cautious", "neutral", "unreliable", "review_required")

# M1：last_outcome_type
LAST_OUTCOME_TYPES = ("found", "unresolved", "fallback", "user_confirmed", "user_denied", "cancelled")

# M1：contradiction 具体来源
CONTRADICTION_SOURCES = (
    "user_denied",
    "repeated_fallback",
    "blocked_context",
    "unresolved_after_recheck",
    "container_candidate_rejected",
    "pocket_check_failed",
)

# M1：置信度带与未来适用范围
EVOLUTION_CONFIDENCE_BANDS = ("low", "medium", "high")
FUTURE_USE_SCOPES = ("local_only", "same_flow_only", "same_object_type_only", "review_required")

MIN_SUPPORTING_FOR_PROMOTABLE = 2
MAX_FALLBACK_FOR_PROMOTABLE = 1
MAX_CONTRADICTION_FOR_PROMOTABLE = 0
# M1：同组模式重复至少 N 次才可升格
MIN_REPEATED_PATTERN_FOR_PROMOTABLE = 2


@dataclass
class ExperienceCandidate:
    """单条经验候选：类型、来源、支撑/冲突/确认/回退、趋势、状态与阻断原因；M1 含聚合与治理字段。"""
    experience_type: str
    source_module: Optional[str] = None
    source_path: Optional[str] = None
    source_summary: Optional[str] = None
    supporting_events_count: int = 0
    contradiction_count: int = 0
    user_confirmed_count: int = 0
    fallback_count: int = 0
    confidence_trend: str = "flat"
    evolution_status: str = "candidate"
    evolution_reason: Optional[str] = None
    promotion_blocked: bool = True
    promotion_block_reason: Optional[str] = None
    evolution_hint_for_future: str = "neutral"
    # M1：聚合与治理
    experience_group_key: Optional[str] = None
    aggregated_source_paths: List[str] = field(default_factory=list)
    repeated_pattern_count: int = 0
    last_observed_ts: Optional[float] = None
    last_outcome_type: Optional[str] = None
    contradiction_sources: List[str] = field(default_factory=list)
    watchlist_reason: Optional[str] = None
    promotable_score: float = 0.0
    evolution_confidence_band: str = "low"
    future_use_scope: str = "local_only"


@dataclass
class ExperienceEvolutionResult:
    """经验演化 M0/M1：1~3 条经验候选的审计与治理结果；M1 含 snapshot_for_next 供下一轮聚合。"""
    candidates: List[ExperienceCandidate] = field(default_factory=list)
    snapshot_for_next: Optional[List[dict]] = None  # M1：供下一帧聚合用 [{group_key, source_path, repeated_pattern_count, experience_type, aggregated_source_paths}]


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _flow_stem(path_list: List[str]) -> str:
    """从 path 提取主干用于 group_key：container / occlusion / pocket / last_location / description / recheck。"""
    if not path_list:
        return "generic"
    for p in path_list:
        p = (p or "").strip()
        if "container_check_flow" in p:
            return "container"
        if "occlusion_clear_flow" in p or "clearing_occlusion" in p:
            return "occlusion"
        if "pocket_check_flow" in p:
            return "pocket"
        if "last_location_flow" in p:
            return "last_location"
        if "description_bootstrap_flow" in p:
            return "description"
        if "rechecking" in p:
            return "recheck"
    return "generic"


def _last_outcome_type(
    terminal: str,
    user_confirmed: bool,
    user_denied: bool,
    has_fallback: bool,
) -> str:
    if user_denied:
        return "user_denied"
    if user_confirmed:
        return "user_confirmed"
    if terminal == "cancelled":
        return "cancelled"
    if terminal == "blocked":
        return "blocked_context"
    if has_fallback:
        return "fallback"
    if terminal == "found":
        return "found"
    return "unresolved"


def _contradiction_sources(
    user_denied: bool,
    terminal: str,
    fallback_count: int,
    high_risk: bool,
    path_list: List[str],
    search_user_container_answer: Optional[str] = None,
) -> List[str]:
    out: List[str] = []
    if user_denied:
        out.append("user_denied")
    if fallback_count >= 2:
        out.append("repeated_fallback")
    if high_risk or terminal == "blocked":
        out.append("blocked_context")
    if terminal not in ("found", "cancelled", "blocked") and "rechecking" in (path_list or []):
        out.append("unresolved_after_recheck")
    if (search_user_container_answer or "").strip().lower() in ("no", "n", "否"):
        out.append("container_candidate_rejected")
    if "pocket_check_flow" in (path_list or []) and fallback_count >= 1:
        out.append("pocket_check_failed")
    return out


def _governance_m1(
    exp_type: str,
    flow_stem: str,
    source_mod: str,
    source_path_s: Optional[str],
    source_sum: Optional[str],
    support: int,
    contradict: int,
    contradict_sources: List[str],
    confirm: int,
    fallback: int,
    risk: bool,
    repeated_pattern: int,
    aggregated_paths: List[str],
    last_outcome: str,
    current_ts: Optional[float],
) -> ExperienceCandidate:
    """M1：治理规则——watchlist/promotable/blocked/rejected、confidence_band、future_use_scope、审计式 reason。"""
    # confidence_trend
    if confirm >= 1 and contradict == 0 and fallback <= 1:
        trend = "up"
    elif contradict >= 1 or fallback >= 2:
        trend = "down"
    else:
        trend = "flat"

    # evolution_confidence_band
    if repeated_pattern >= 2 and support >= 1 and confirm >= 1 and contradict == 0 and fallback <= 1:
        band = "high"
    elif support >= 1 and (contradict == 0 or fallback <= 1):
        band = "medium"
    else:
        band = "low"

    # promotable_score 0~1
    score = 0.0
    if support >= 1:
        score += 0.25
    if confirm >= 1:
        score += 0.25
    if repeated_pattern >= MIN_REPEATED_PATTERN_FOR_PROMOTABLE:
        score += 0.25
    if contradict == 0 and fallback <= 1:
        score += 0.25
    if risk or "blocked_context" in contradict_sources:
        score *= 0.5

    # future_use_scope
    if risk or "blocked_context" in contradict_sources:
        scope = "review_required"
    elif repeated_pattern >= 2 and contradict == 0:
        scope = "same_flow_only"
    elif flow_stem in ("container", "pocket") and confirm >= 1:
        scope = "same_object_type_only"
    else:
        scope = "local_only"

    # status + blocked + reasons
    watchlist_reason_val: Optional[str] = None
    evolution_reason_parts: List[str] = []
    block_reason_val: Optional[str] = None
    status = "candidate"
    blocked = True
    hint = "neutral"

    # rejected：用户否认明确、口袋多次失败、容器多次被拒
    if "user_denied" in contradict_sources:
        status = "rejected"
        evolution_reason_parts.append("用户明确否认该路径或候选")
        block_reason_val = "user_denied"
        hint = "unreliable"
    elif "container_candidate_rejected" in contradict_sources and "pocket_check_failed" in contradict_sources:
        status = "rejected"
        evolution_reason_parts.append("容器候选被拒且口袋检查流多次失败")
        block_reason_val = "contradiction_sources"
        hint = "unreliable"
    elif "repeated_fallback" in contradict_sources or fallback >= 2:
        status = "blocked"
        evolution_reason_parts.append(f"回退次数较多（{fallback} 次），暂不推荐沉淀")
        block_reason_val = "repeated_fallback"
        hint = "cautious"
    elif "blocked_context" in contradict_sources or risk:
        status = "blocked"
        evolution_reason_parts.append("高风险或阻断语境，本轮不升格")
        block_reason_val = "blocked_context"
        hint = "review_required"
    elif "unresolved_after_recheck" in contradict_sources:
        status = "blocked"
        evolution_reason_parts.append("补证后仍未解决，暂列 blocked")
        block_reason_val = "unresolved_after_recheck"
        hint = "cautious"
    # promotable
    elif (
        repeated_pattern >= MIN_REPEATED_PATTERN_FOR_PROMOTABLE
        and support >= 1
        and confirm >= 1
        and contradict <= MAX_CONTRADICTION_FOR_PROMOTABLE
        and fallback <= MAX_FALLBACK_FOR_PROMOTABLE
        and not risk
    ):
        status = "promotable"
        blocked = False
        block_reason_val = None
        evolution_reason_parts.append(
            f"该模式在近 {repeated_pattern} 次任务中重复出现，且均有用户确认支撑，当前可进入 promotable"
        )
        hint = "preferred"
    # watchlist
    elif support >= 1 and (confirm >= 1 or repeated_pattern >= 1) and fallback <= 1:
        status = "watchlist"
        watchlist_reason_val = "有一定支撑或重复度但尚不足升格，进入观察列表"
        evolution_reason_parts.append(watchlist_reason_val)
        block_reason_val = "single_success_with_confirm_or_repeat"
        hint = "cautious"
    # 单次成功不升格
    else:
        evolution_reason_parts.append("仅单次成功或缺少重复支撑与用户确认，暂不升格")
        block_reason_val = "single_success_not_enough"

    evolution_reason_str = "；".join(evolution_reason_parts)
    if aggregated_paths:
        evolution_reason_str += f"。聚合路径数：{len(aggregated_paths)}"
    if contradict_sources:
        evolution_reason_str += f"。冲突来源：{','.join(contradict_sources)}"

    group_key = f"{exp_type}:{flow_stem}"

    return ExperienceCandidate(
        experience_type=exp_type,
        source_module=source_mod,
        source_path=source_path_s,
        source_summary=source_sum,
        supporting_events_count=support,
        contradiction_count=contradict,
        user_confirmed_count=confirm,
        fallback_count=fallback,
        confidence_trend=trend,
        evolution_status=status,
        evolution_reason=evolution_reason_str,
        promotion_blocked=blocked,
        promotion_block_reason=block_reason_val,
        evolution_hint_for_future=hint,
        experience_group_key=group_key,
        aggregated_source_paths=aggregated_paths,
        repeated_pattern_count=repeated_pattern,
        last_observed_ts=current_ts,
        last_outcome_type=last_outcome,
        contradiction_sources=contradict_sources,
        watchlist_reason=watchlist_reason_val,
        promotable_score=round(score, 2),
        evolution_confidence_band=band,
        future_use_scope=scope,
    )


def build_experience_evolution(
    evidence_ledger: Any,
    hypothesis_layer: Any,
    recheck_planner: Any,
    object_temporal_ledger: Any,
    object_search_interaction: Any,
    state: Any,
    object_user_confirmed_location: Optional[str] = None,
    object_user_denied_location: Optional[str] = None,
    prev_candidates_snapshot: Optional[List[dict]] = None,
    current_ts: Optional[float] = None,
) -> ExperienceEvolutionResult:
    """
    从已有模块结果生成 1~3 条经验候选并做审计与治理（M1 含聚合与 contradiction_sources）。
    仅读取已有结果，不修改 hypothesis / object_ledger / recheck 主逻辑。
    """
    candidates: List[ExperienceCandidate] = []

    path_list = _get(object_search_interaction, "search_resolution_path") or []
    if isinstance(path_list, str):
        path_list = [path_list] if path_list.strip() else []
    path_str = " → ".join(path_list) if path_list else None

    terminal = _get(object_search_interaction, "search_terminal_status") or "none"
    retry_count = _get(object_search_interaction, "interaction_retry_count") or 0
    fallback_count = retry_count
    has_fallback_action = bool(_get(object_search_interaction, "fallback_action"))

    user_confirmed = bool(object_user_confirmed_location)
    user_denied = bool(object_user_denied_location)
    user_confirmed_count = 1 if user_confirmed else 0
    contradiction_count = 1 if (user_denied or terminal in ("cancelled", "blocked")) else 0
    supporting_events_count = 1 if (
        terminal == "found" or (path_list and terminal not in ("cancelled", "blocked"))
    ) else 0
    if terminal == "cancelled" or user_denied:
        supporting_events_count = 0

    minimum_mode = _get(state, "minimum_mode_active") is True
    runtime_domain = (_get(state, "runtime_domain_state") or "").strip()
    high_risk = minimum_mode or runtime_domain == "frozen"

    last_outcome = _last_outcome_type(terminal, user_confirmed, user_denied, has_fallback_action)
    # 容器否认：从 ctx 传入或从 object_search 侧推断；此处用 object_user_denied 代表“有否认”
    search_container_answer = None  # 若 builder 传入可填
    contradict_sources = _contradiction_sources(
        user_denied, terminal, fallback_count, high_risk, path_list, search_container_answer
    )
    flow_stem = _flow_stem(path_list)

    # 上一轮 snapshot 按 group_key 索引
    prev_by_key: dict = {}
    for p in prev_candidates_snapshot or []:
        if isinstance(p, dict):
            gk = p.get("experience_group_key") or p.get("group_key")
            if gk:
                prev_by_key[gk] = p

    def _agg_and_repeat(exp_type: str, stem: str) -> tuple:
        group_key = f"{exp_type}:{stem}"
        prev = prev_by_key.get(group_key)
        prev_repeat = (prev.get("repeated_pattern_count") or 0) if prev else 0
        prev_paths = (prev.get("aggregated_source_paths") or prev.get("aggregated_paths") or []) if prev else []
        if not isinstance(prev_paths, list):
            prev_paths = [prev_paths] if prev_paths else []
        aggregated = (list(prev_paths) + [path_str or ""])[:3]
        repeated = 1 + prev_repeat
        return aggregated, repeated

    def _add(exp_type: str, source_mod: str, source_sum: Optional[str], stem: Optional[str] = None):
        s = stem or flow_stem
        agg_paths, rep = _agg_and_repeat(exp_type, s)
        c = _governance_m1(
            exp_type,
            s,
            source_mod,
            path_str,
            source_sum,
            supporting_events_count,
            contradiction_count,
            contradict_sources,
            user_confirmed_count,
            fallback_count,
            high_risk,
            rep,
            agg_paths,
            last_outcome,
            current_ts,
        )
        candidates.append(c)

    if path_list:
        _add("object_search_path_pattern", "object_search_interaction", path_str or "当前寻物路径")

    if len(candidates) < 3 and "container_check_flow" in (path_list or []):
        summary = "容器检查流"
        if _get(object_temporal_ledger, "focus_object_entry") and _get(
            _get(object_temporal_ledger, "focus_object_entry"), "current_container_candidate"
        ):
            summary = "容器候选路径：" + (path_str or "")
        _add("container_candidate_pattern", "object_temporal_ledger", summary, "container")

    if len(candidates) < 3 and ("occlusion_clear_flow" in (path_list or []) or "clearing_occlusion" in (path_list or [])):
        _add("occlusion_resolution_pattern", "object_search_interaction", "遮挡清理后 recheck 路径", "occlusion")

    if len(candidates) < 3 and "pocket_check_flow" in (path_list or []):
        _add("pocket_check_pattern", "object_search_interaction", "口袋检查流", "pocket")

    if len(candidates) < 3 and recheck_planner and _get(recheck_planner, "recheck_action") and terminal == "found":
        _add("recheck_effectiveness_pattern", "recheck_planner", "补证有效路径", "recheck")

    if not candidates:
        ledger_sum = ""
        if evidence_ledger and getattr(evidence_ledger, "entries", None):
            first = evidence_ledger.entries[0]
            ledger_sum = getattr(first, "claim_summary", "") or ""
        hyp_sum = ""
        if hypothesis_layer and getattr(hypothesis_layer, "hypotheses", None):
            first_h = hypothesis_layer.hypotheses[0]
            hyp_sum = getattr(first_h, "hypothesis_summary", "") or ""
        source_sum = (ledger_sum or hyp_sum or "当前帧无寻物路径")[:80]
        agg_paths, rep = _agg_and_repeat("object_search_path_pattern", "generic")
        c0 = _governance_m1(
            "object_search_path_pattern",
            "generic",
            "evidence_ledger",
            None,
            source_sum,
            0,
            contradiction_count,
            contradict_sources,
            user_confirmed_count,
            fallback_count,
            high_risk,
            rep,
            agg_paths,
            last_outcome,
            current_ts,
        )
        candidates.append(c0)

    candidates = candidates[:3]

    # M1：快照供下一轮聚合
    snapshot_for_next = []
    for c in candidates:
        snapshot_for_next.append({
            "experience_group_key": c.experience_group_key,
            "source_path": c.source_path,
            "repeated_pattern_count": c.repeated_pattern_count,
            "experience_type": c.experience_type,
            "aggregated_source_paths": c.aggregated_source_paths,
        })

    return ExperienceEvolutionResult(candidates=candidates, snapshot_for_next=snapshot_for_next)
