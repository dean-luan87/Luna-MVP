# -*- coding: utf-8 -*-
"""
简洁模式视图模型：仅字段分层与组装，不抽链、不分析。

契约见 docs/architecture/voice/LUNA_VOICE_WHITEBOX_VIEW_CONTRACT_V1.md。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from capabilities.voice.observations.request_trace_chain import RequestTraceChain
from capabilities.voice.observations.request_trace_diagnostic_summary import RequestTraceDiagnosticSummary
from capabilities.voice.observations.request_trace_issue import RequestTraceIssue
from capabilities.voice.observations.request_trace_summary import RequestTraceSummary, build_request_trace_summary


def _final_status_to_concise_status(final_status: str) -> str:
    """将 issue.final_status 映射为与 RequestTraceSummary.status 同一套查询口径。"""
    m = {
        "success": "success",
        "degraded_success": "degraded_success",
        "rollback_success": "degraded_success",
        "suppressed": "suppressed",
        "failed": "failed",
        "unknown": "unknown",
    }
    return m.get(final_status, "unknown")


@dataclass
class RequestTraceConciseView:
    """白盒简洁模式单链行（列表/卡片）。"""

    request_id: str
    trace_id: Optional[str] = None
    chain_type: str = ""
    provider_name: Optional[str] = None
    final_execution_mode: Optional[str] = None
    status: str = ""
    primary_issue_type: str = ""
    primary_issue_reason: str = ""
    severity: str = ""
    has_fallback: bool = False
    has_rollback: bool = False
    duration_ms: Optional[float] = None
    diagnostic_summary_text: str = ""
    attribution_source: str = "issue"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "trace_id": self.trace_id,
            "chain_type": self.chain_type,
            "provider_name": self.provider_name,
            "final_execution_mode": self.final_execution_mode,
            "status": self.status,
            "primary_issue_type": self.primary_issue_type,
            "primary_issue_reason": self.primary_issue_reason,
            "severity": self.severity,
            "has_fallback": self.has_fallback,
            "has_rollback": self.has_rollback,
            "duration_ms": self.duration_ms,
            "diagnostic_summary_text": self.diagnostic_summary_text,
            "attribution_source": self.attribution_source,
        }

    @classmethod
    def from_parts(
        cls,
        *,
        summary: RequestTraceSummary,
        issue: Optional[RequestTraceIssue] = None,
        diagnostic: Optional[RequestTraceDiagnosticSummary] = None,
    ) -> RequestTraceConciseView:
        diag_text = diagnostic.summary_text if diagnostic else ""
        if issue is not None:
            ct = issue.chain_type or summary.chain_type
            return cls(
                request_id=issue.request_id,
                trace_id=issue.trace_id,
                chain_type=ct,
                provider_name=issue.provider_name if issue.provider_name is not None else summary.provider_name,
                final_execution_mode=issue.final_execution_mode
                if issue.final_execution_mode is not None
                else summary.final_execution_mode,
                status=_final_status_to_concise_status(issue.final_status),
                primary_issue_type=issue.primary_issue_type,
                primary_issue_reason=issue.primary_issue_reason,
                severity=issue.severity,
                has_fallback=issue.has_fallback,
                has_rollback=issue.has_rollback,
                duration_ms=summary.duration_ms,
                diagnostic_summary_text=diag_text,
                attribution_source="issue",
            )
        return cls(
            request_id=summary.request_id,
            trace_id=summary.trace_id,
            chain_type=summary.chain_type,
            provider_name=summary.provider_name,
            final_execution_mode=summary.final_execution_mode,
            status=summary.status,
            primary_issue_type=summary.primary_error_type or "",
            primary_issue_reason=summary.primary_error_reason or "",
            severity="info",
            has_fallback=summary.has_fallback,
            has_rollback=summary.has_rollback,
            duration_ms=summary.duration_ms,
            diagnostic_summary_text=diag_text,
            attribution_source="summary",
        )

    @classmethod
    def from_chain(
        cls,
        chain: RequestTraceChain,
        *,
        issue: Optional[RequestTraceIssue] = None,
        diagnostic: Optional[RequestTraceDiagnosticSummary] = None,
    ) -> RequestTraceConciseView:
        sm = build_request_trace_summary(chain)
        return cls.from_parts(summary=sm, issue=issue, diagnostic=diagnostic)
