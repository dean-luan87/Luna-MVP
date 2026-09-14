# -*- coding: utf-8 -*-
"""
问题检索返回行：简洁可读，非完整链 JSON；供列表与后续 UI 复用。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class RequestTraceSearchResult:
    """搜索默认视图（concise）；detailed 仍不返回全链，仅多几个字段占位。"""

    request_id: str
    trace_id: Optional[str] = None
    provider_name: Optional[str] = None
    chain_type: str = ""
    final_execution_mode: Optional[str] = None
    status: str = ""
    primary_issue_type: str = ""
    primary_issue_reason: str = ""
    summary_text: str = ""
    alert_level: str = ""
    presentation_semantic: str = ""
    priority_score: int = 0
    priority_reason: str = ""
    is_action_required: bool = False
    has_fallback: bool = False
    has_rollback: bool = False
    archive_tier: Optional[str] = None
    occurred_at: Optional[float] = None
    result_mode: str = "concise"
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "trace_id": self.trace_id,
            "provider_name": self.provider_name,
            "chain_type": self.chain_type,
            "final_execution_mode": self.final_execution_mode,
            "status": self.status,
            "primary_issue_type": self.primary_issue_type,
            "primary_issue_reason": self.primary_issue_reason,
            "summary_text": self.summary_text,
            "alert_level": self.alert_level,
            "presentation_semantic": self.presentation_semantic,
            "priority_score": self.priority_score,
            "priority_reason": self.priority_reason,
            "is_action_required": self.is_action_required,
            "has_fallback": self.has_fallback,
            "has_rollback": self.has_rollback,
            "archive_tier": self.archive_tier,
            "occurred_at": self.occurred_at,
            "result_mode": self.result_mode,
            "notes": list(self.notes),
        }
