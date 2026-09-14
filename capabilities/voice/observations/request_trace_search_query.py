# -*- coding: utf-8 -*-
"""
统一问题检索：在链 + problem summary 上结构化过滤（无全文、无 DB）。

入口：RequestTraceSearchEntry；输出：RequestTraceSearchResult 列表（默认 concise）。
"""

from __future__ import annotations

from typing import Dict, List, Optional

from capabilities.voice.observations.request_trace_alert_presentation import alert_level_to_presentation_semantic
from capabilities.voice.observations.request_trace_chain import RequestTraceChain
from capabilities.voice.observations.request_trace_issue_analyzer import analyze_request_trace_issue
from capabilities.voice.observations.request_trace_problem_extractor import extract_problem_summary
from capabilities.voice.observations.request_trace_problem_prioritizer import DEFAULT_MAIN_PROVIDER, compute_priority_score
from capabilities.voice.observations.request_trace_problem_summary import RequestTraceProblemSummary
from capabilities.voice.observations.request_trace_query import TraceQuery, matches_query
from capabilities.voice.observations.request_trace_search_entry import (
    RequestTraceSearchEntry,
    parse_alert_level_filter,
    parse_presentation_filter,
)
from capabilities.voice.observations.request_trace_search_result import RequestTraceSearchResult
from capabilities.voice.observations.request_trace_search_result_builder import build_search_result
from capabilities.voice.observations.request_trace_summary import RequestTraceSummary, build_request_trace_summary

# 与 request_trace_problem_aggregator 对齐
def _problem_affects_main_provider(ps: RequestTraceProblemSummary) -> bool:
    prov = (ps.provider_name or "").strip().lower()
    if prov != DEFAULT_MAIN_PROVIDER:
        return False
    pres = (ps.alert_level or "").strip().lower()
    return pres in ("warning", "high_risk", "critical")


def _failure_signature(chain: RequestTraceChain, ps: RequestTraceProblemSummary) -> str:
    parts = [
        ps.primary_issue_type or "",
        ps.failed_stage or "",
        chain.chain_type or "",
    ]
    if chain.errors:
        parts.append(chain.errors[0].error_type or "")
    return "_".join(parts).lower()


def _matches_problem_focus(
    entry: RequestTraceSearchEntry,
    chain: RequestTraceChain,
    summary: RequestTraceSummary,
    ps: RequestTraceProblemSummary,
) -> bool:
    pf = (entry.problem_focus or "").strip().lower()
    if not pf:
        return True
    ct = (chain.chain_type or "").lower()
    if pf == "rollback":
        return "legacy_rollback" in ct or summary.has_rollback
    if pf == "fallback":
        return "provider_fallback" in ct or summary.has_fallback
    if pf == "high_risk":
        return ps.alert_level in ("high_risk", "critical") or alert_level_to_presentation_semantic(
            ps.alert_level
        ) in ("warning", "danger")
    if pf == "main_provider":
        return _problem_affects_main_provider(ps)
    if pf == "action_required":
        return ps.is_action_required
    return True


def matches_search_entry(
    chain: RequestTraceChain,
    summary: RequestTraceSummary,
    ps: RequestTraceProblemSummary,
    entry: RequestTraceSearchEntry,
) -> bool:
    """结构化 AND；problem_focus 为单维度快捷（内部 OR/规则）。"""
    tq = TraceQuery(
        request_id=entry.request_id,
        trace_id=entry.trace_id,
        chain_type=entry.chain_type,
        provider_name=entry.provider_name,
        final_execution_mode=entry.final_execution_mode,
        status=entry.status,
        failure_type=entry.failure_type,
        has_fallback=entry.has_fallback,
        has_rollback=entry.has_rollback,
        start_after=entry.start_after,
        start_before=entry.start_before,
    )
    if not matches_query(chain, summary, tq):
        return False

    if entry.primary_issue_type is not None:
        want = entry.primary_issue_type.strip().lower()
        got = (ps.primary_issue_type or "").lower()
        if want and want not in got and got != want:
            return False

    if entry.alert_level is not None:
        allowed = parse_alert_level_filter(entry.alert_level)
        if allowed and (ps.alert_level or "").lower() not in allowed:
            return False

    if entry.presentation_semantic is not None:
        want = parse_presentation_filter(entry.presentation_semantic)
        cur = alert_level_to_presentation_semantic(ps.alert_level).lower()
        if want and cur not in want:
            return False

    if entry.failure_signature is not None:
        sig = _failure_signature(chain, ps)
        needle = entry.failure_signature.strip().lower()
        if needle and needle not in sig and not sig.startswith(needle):
            return False

    if entry.is_action_required is not None and ps.is_action_required != entry.is_action_required:
        return False

    if entry.priority_min is not None and ps.priority_score < entry.priority_min:
        return False

    if entry.only_main_provider_related is True and not _problem_affects_main_provider(ps):
        return False

    if not _matches_problem_focus(entry, chain, summary, ps):
        return False

    return True


def search_chains_to_results(
    chains: List[RequestTraceChain],
    entry: RequestTraceSearchEntry,
    *,
    archive_tier_by_request_id: Optional[Dict[str, str]] = None,
    result_mode: str = "concise",
    recompute_priority: bool = True,
) -> List[RequestTraceSearchResult]:
    """
    对链列表执行检索，返回 RequestTraceSearchResult（默认 concise）。

    archive_tier_by_request_id：可选，request_id -> tier（来自 manifest 等）。
    """
    archive_tier_by_request_id = archive_tier_by_request_id or {}
    out: List[RequestTraceSearchResult] = []

    for chain in chains:
        if entry.archive_tier is not None:
            tier = archive_tier_by_request_id.get(chain.request_id)
            if tier is None or tier != entry.archive_tier:
                continue

        issue, diag = analyze_request_trace_issue(chain)
        ps = extract_problem_summary(chain, issue, diag)
        if recompute_priority:
            sc, rs = compute_priority_score(ps)
            ps.priority_score = sc
            ps.priority_reason = rs
        summary = build_request_trace_summary(chain)

        if not matches_search_entry(chain, summary, ps, entry):
            continue

        tier = archive_tier_by_request_id.get(chain.request_id)
        out.append(
            build_search_result(
                chain,
                ps,
                summary,
                archive_tier=tier,
                result_mode=result_mode,
            )
        )

    out.sort(key=lambda r: (-r.priority_score, r.request_id))
    return out
