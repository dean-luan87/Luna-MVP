# -*- coding: utf-8 -*-
"""
专业模式视图模型：组合链全量 + issue + diagnostic + 可选 manifest，无排障逻辑。

契约见 docs/architecture/voice/LUNA_VOICE_WHITEBOX_VIEW_CONTRACT_V1.md。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from capabilities.voice.observations.request_trace_archive_manifest import RequestTraceArchiveManifest
from capabilities.voice.observations.request_trace_chain import RequestTraceChain
from capabilities.voice.observations.request_trace_concise_view import RequestTraceConciseView
from capabilities.voice.observations.request_trace_diagnostic_summary import RequestTraceDiagnosticSummary
from capabilities.voice.observations.request_trace_issue import RequestTraceIssue
from capabilities.voice.observations.request_trace_summary import RequestTraceSummary, build_request_trace_summary


@dataclass
class RequestTraceProfessionalView:
    """白盒专业模式单链详情：顶部 concise 快照 + 全量下钻对象。"""

    concise: RequestTraceConciseView
    chain: RequestTraceChain
    issue: RequestTraceIssue
    diagnostic: RequestTraceDiagnosticSummary
    archive_manifest: Optional[RequestTraceArchiveManifest] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "concise": self.concise.to_dict(),
            "chain": self.chain.to_dict(),
            "issue": self.issue.to_dict(),
            "diagnostic": self.diagnostic.to_dict(),
            "archive_manifest": self.archive_manifest.to_dict() if self.archive_manifest else None,
        }

    @classmethod
    def from_parts(
        cls,
        *,
        chain: RequestTraceChain,
        issue: RequestTraceIssue,
        diagnostic: RequestTraceDiagnosticSummary,
        summary: Optional[RequestTraceSummary] = None,
        archive_manifest: Optional[RequestTraceArchiveManifest] = None,
    ) -> RequestTraceProfessionalView:
        sm = summary if summary is not None else build_request_trace_summary(chain)
        concise = RequestTraceConciseView.from_parts(summary=sm, issue=issue, diagnostic=diagnostic)
        return cls(
            concise=concise,
            chain=chain,
            issue=issue,
            diagnostic=diagnostic,
            archive_manifest=archive_manifest,
        )
