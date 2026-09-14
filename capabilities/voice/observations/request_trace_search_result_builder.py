# -*- coding: utf-8 -*-
"""
从 RequestTraceChain + RequestTraceProblemSummary 等组装 RequestTraceSearchResult。

默认 concise；不内嵌完整链 JSON。
"""

from __future__ import annotations

from typing import List, Optional

from capabilities.voice.observations.request_trace_alert_presentation import alert_level_to_presentation_semantic
from capabilities.voice.observations.request_trace_chain import RequestTraceChain
from capabilities.voice.observations.request_trace_problem_summary import RequestTraceProblemSummary
from capabilities.voice.observations.request_trace_search_result import RequestTraceSearchResult
from capabilities.voice.observations.request_trace_summary import RequestTraceSummary


def build_search_result(
    chain: RequestTraceChain,
    ps: RequestTraceProblemSummary,
    summary: RequestTraceSummary,
    *,
    archive_tier: Optional[str] = None,
    result_mode: str = "concise",
    notes: Optional[List[str]] = None,
) -> RequestTraceSearchResult:
    occurred = chain.ended_at if chain.ended_at is not None else chain.started_at
    pres = alert_level_to_presentation_semantic(ps.alert_level)
    return RequestTraceSearchResult(
        request_id=chain.request_id,
        trace_id=chain.trace_id,
        provider_name=chain.provider_name,
        chain_type=chain.chain_type,
        final_execution_mode=chain.final_execution_mode,
        status=summary.status,
        primary_issue_type=ps.primary_issue_type,
        primary_issue_reason=ps.primary_issue_reason,
        summary_text=ps.summary_text,
        alert_level=ps.alert_level,
        presentation_semantic=pres,
        priority_score=ps.priority_score,
        priority_reason=ps.priority_reason,
        is_action_required=ps.is_action_required,
        has_fallback=summary.has_fallback,
        has_rollback=summary.has_rollback,
        archive_tier=archive_tier,
        occurred_at=occurred,
        result_mode=result_mode,
        notes=list(notes or []),
    )
