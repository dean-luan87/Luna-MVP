# -*- coding: utf-8 -*-
"""
统一问题检索入口：CLI / 后续 API 的查询条件结构（结构化，无全文检索）。

与 TraceQuery 区别：增加问题导向字段（alert_level、presentation_semantic、problem_focus 等）。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class RequestTraceSearchEntry:
    """当前可检索条件；未设置的字段不参与过滤（视为通配）。"""

    request_id: Optional[str] = None
    trace_id: Optional[str] = None
    chain_type: Optional[str] = None
    provider_name: Optional[str] = None
    final_execution_mode: Optional[str] = None
    status: Optional[str] = None
    failure_type: Optional[str] = None
    failure_signature: Optional[str] = None
    primary_issue_type: Optional[str] = None
    alert_level: Optional[str] = None
    presentation_semantic: Optional[str] = None
    has_fallback: Optional[bool] = None
    has_rollback: Optional[bool] = None
    archive_tier: Optional[str] = None
    start_after: Optional[float] = None
    start_before: Optional[float] = None

    is_action_required: Optional[bool] = None
    priority_min: Optional[int] = None
    only_main_provider_related: Optional[bool] = None

    # 问题导向快捷：rollback | fallback | high_risk | main_provider | action_required
    problem_focus: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {}
        for k, v in self.__dict__.items():
            if v is not None:
                d[k] = v
        return d


def parse_alert_level_filter(s: Optional[str]) -> List[str]:
    """支持 'high_risk|critical' 或逗号分隔。"""
    if not s:
        return []
    raw = s.replace(",", "|").split("|")
    return [x.strip().lower() for x in raw if x.strip()]


def parse_presentation_filter(s: Optional[str]) -> List[str]:
    if not s:
        return []
    raw = s.replace(",", "|").split("|")
    return [x.strip().lower() for x in raw if x.strip()]
