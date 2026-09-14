# -*- coding: utf-8 -*-
"""
诊断摘要（展示与排查入口）：比 issue 更短、更偏「一眼能跟进」。

summary_text 为规则模板填充，非大模型生成。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class RequestTraceDiagnosticSummary:
    request_id: str
    chain_type: str = ""
    provider_name: Optional[str] = None
    final_execution_mode: Optional[str] = None
    final_status: str = ""
    primary_issue_type: str = ""
    primary_issue_reason: str = ""
    failed_stage: Optional[str] = None
    severity: str = ""
    summary_text: str = ""
    recommended_checkpoints: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "chain_type": self.chain_type,
            "provider_name": self.provider_name,
            "final_execution_mode": self.final_execution_mode,
            "final_status": self.final_status,
            "primary_issue_type": self.primary_issue_type,
            "primary_issue_reason": self.primary_issue_reason,
            "failed_stage": self.failed_stage,
            "severity": self.severity,
            "summary_text": self.summary_text,
            "recommended_checkpoints": list(self.recommended_checkpoints),
        }
