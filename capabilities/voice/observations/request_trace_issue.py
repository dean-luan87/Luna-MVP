# -*- coding: utf-8 -*-
"""
链级问题视图（归因）：一条 RequestTraceChain 上的整合结论。

不做自动修复；供诊断摘要与后续白盒复用。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

# 严重度（后续颜色分级可挂接；本轮仅规则化字符串）
SEVERITY_INFO = "info"
SEVERITY_WARNING = "warning"
SEVERITY_DEGRADED = "degraded"
SEVERITY_ERROR = "error"
SEVERITY_CRITICAL = "critical"

# 与 request_trace_issue_analyzer 中主因类型字符串一致（供导入与类型对照）
ISSUE_NONE = "none"
ISSUE_PROVIDER_UNAVAILABLE = "provider_unavailable"
ISSUE_PROVIDER_CHAIN_FAILURE = "provider_chain_failure"
ISSUE_REQUEST_SUPPRESSED = "request_suppressed"
ISSUE_PLAYBACK_FAILURE = "playback_failure"
ISSUE_OUTPUT_DELIVERY_FAILURE = "output_delivery_failure"
ISSUE_OBSERVATION_GAP = "observation_gap"
ISSUE_UNKNOWN = "unknown_failure"


@dataclass
class RequestTraceIssue:
    request_id: str
    trace_id: Optional[str] = None
    chain_type: str = ""
    provider_name: Optional[str] = None
    final_execution_mode: Optional[str] = None
    final_status: str = ""  # success | degraded_success | rollback_success | suppressed | failed | unknown
    primary_issue_type: str = ""
    primary_issue_reason: str = ""
    secondary_issue_type: Optional[str] = None
    secondary_issue_reason: Optional[str] = None
    failed_stage: Optional[str] = None
    severity: str = SEVERITY_INFO
    has_fallback: bool = False
    has_rollback: bool = False
    recommended_checkpoints: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "trace_id": self.trace_id,
            "chain_type": self.chain_type,
            "provider_name": self.provider_name,
            "final_execution_mode": self.final_execution_mode,
            "final_status": self.final_status,
            "primary_issue_type": self.primary_issue_type,
            "primary_issue_reason": self.primary_issue_reason,
            "secondary_issue_type": self.secondary_issue_type,
            "secondary_issue_reason": self.secondary_issue_reason,
            "failed_stage": self.failed_stage,
            "severity": self.severity,
            "has_fallback": self.has_fallback,
            "has_rollback": self.has_rollback,
            "recommended_checkpoints": list(self.recommended_checkpoints),
            "notes": list(self.notes),
        }
