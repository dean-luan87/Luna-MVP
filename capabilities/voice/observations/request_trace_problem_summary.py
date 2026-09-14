# -*- coding: utf-8 -*-
"""
单条请求的最小问题摘要：供简洁模式列表、归档摘要、后续搜索排序复用。

规则化字段；summary_text 为模板句，非大模型生成。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class RequestTraceProblemSummary:
    """一条链上的问题提炼结果（可排序、可聚合）。"""

    problem_id: str
    request_id: str
    trace_id: Optional[str] = None
    chain_type: str = ""
    provider_name: Optional[str] = None
    final_execution_mode: Optional[str] = None
    alert_level: str = ""
    primary_issue_type: str = ""
    primary_issue_reason: str = ""
    failed_stage: Optional[str] = None
    status: str = ""
    severity: str = ""
    summary_text: str = ""
    recommended_checkpoints: List[str] = field(default_factory=list)
    is_action_required: bool = False
    priority_score: int = 0
    priority_reason: str = ""
    # 供排序器计算新鲜度（可选）
    ended_at: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "problem_id": self.problem_id,
            "request_id": self.request_id,
            "trace_id": self.trace_id,
            "chain_type": self.chain_type,
            "provider_name": self.provider_name,
            "final_execution_mode": self.final_execution_mode,
            "alert_level": self.alert_level,
            "primary_issue_type": self.primary_issue_type,
            "primary_issue_reason": self.primary_issue_reason,
            "failed_stage": self.failed_stage,
            "status": self.status,
            "severity": self.severity,
            "summary_text": self.summary_text,
            "recommended_checkpoints": list(self.recommended_checkpoints),
            "is_action_required": self.is_action_required,
            "priority_score": self.priority_score,
            "priority_reason": self.priority_reason,
            "ended_at": self.ended_at,
        }
