# -*- coding: utf-8 -*-
"""
简洁模式「问题区」视图模型：聚合 top、活跃列表、已兜住、低优先收口。

不含 UI、不含颜色十六进制；展示语义见 request_trace_alert_presentation。
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from capabilities.voice.observations.request_trace_problem_aggregator import (
    ProblemAggregationSummary,
    aggregate_problems,
    is_degraded_but_handled,
    is_pure_success_noise,
    is_suppressed_or_low_priority,
)
from capabilities.voice.observations.request_trace_problem_prioritizer import DEFAULT_MAIN_PROVIDER, prioritize_problems
from capabilities.voice.observations.request_trace_problem_summary import RequestTraceProblemSummary
from capabilities.voice.observations.request_trace_top_problem_selector import select_top_problem


@dataclass
class RequestTraceConciseProblemBoard:
    """简洁模式问题区：可直接序列化给前端或 CLI。"""

    generated_at: float
    provider_name: str
    top_problem: Optional[RequestTraceProblemSummary]
    top_problem_reason: str
    top_problem_checkpoints_short: List[str]
    active_problems: List[RequestTraceProblemSummary]
    degraded_but_handled: List[RequestTraceProblemSummary]
    suppressed_or_low_priority: List[RequestTraceProblemSummary]
    counts_by_alert_level: Dict[str, int]
    counts_by_issue_type: Dict[str, int]
    counts_by_provider: Dict[str, int]
    aggregation: ProblemAggregationSummary
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "provider_name": self.provider_name,
            "top_problem": self.top_problem.to_dict() if self.top_problem else None,
            "top_problem_reason": self.top_problem_reason,
            "top_problem_checkpoints_short": list(self.top_problem_checkpoints_short),
            "active_problems": [p.to_dict() for p in self.active_problems],
            "degraded_but_handled": [p.to_dict() for p in self.degraded_but_handled],
            "suppressed_or_low_priority": [p.to_dict() for p in self.suppressed_or_low_priority],
            "counts_by_alert_level": dict(self.counts_by_alert_level),
            "counts_by_issue_type": dict(self.counts_by_issue_type),
            "counts_by_provider": dict(self.counts_by_provider),
            "aggregation": self.aggregation.to_dict(),
            "notes": list(self.notes),
        }


def build_concise_problem_board(
    problems: List[RequestTraceProblemSummary],
    *,
    default_provider_context: str = DEFAULT_MAIN_PROVIDER,
    active_limit: int = 5,
    now: Optional[float] = None,
) -> RequestTraceConciseProblemBoard:
    """
    从一批 problem summary 构建简洁模式问题区。

    - top_problem：规则见 request_trace_top_problem_selector
    - active_problems：排除「已兜住」「低优先/抑制」与纯成功，最多 active_limit 条
    - 两路分组与 active 互斥（同一 problem_id 不重复出现在多组，按分组优先级：已兜住 > 低优先）
    """
    t = now if now is not None else time.time()
    ranked = prioritize_problems(list(problems), now=t)
    agg = aggregate_problems(ranked)

    degraded: List[RequestTraceProblemSummary] = []
    suppressed: List[RequestTraceProblemSummary] = []
    for p in ranked:
        if is_degraded_but_handled(p):
            degraded.append(p)
        elif is_suppressed_or_low_priority(p):
            suppressed.append(p)

    active: List[RequestTraceProblemSummary] = []
    seen: set[str] = set()
    for p in ranked:
        if is_pure_success_noise(p):
            continue
        if is_degraded_but_handled(p) or is_suppressed_or_low_priority(p):
            continue
        pid = p.problem_id
        if pid in seen:
            continue
        seen.add(pid)
        active.append(p)
        if len(active) >= max(0, active_limit):
            break

    top, top_reason = select_top_problem(ranked, now=t)
    short_cp: List[str] = []
    if top is not None:
        short_cp = list(top.recommended_checkpoints or [])[:3]
        tid = top.problem_id
        degraded = [p for p in degraded if p.problem_id != tid]

    notes = [
        f"active_problems 上限 {active_limit} 条（规则：不含已兜住/抑制/纯成功）",
        f"默认主样本 provider 上下文：{default_provider_context}",
    ]

    return RequestTraceConciseProblemBoard(
        generated_at=t,
        provider_name=default_provider_context,
        top_problem=top,
        top_problem_reason=top_reason,
        top_problem_checkpoints_short=short_cp,
        active_problems=active,
        degraded_but_handled=degraded,
        suppressed_or_low_priority=suppressed,
        counts_by_alert_level=agg.counts_by_alert_level,
        counts_by_issue_type=agg.counts_by_issue_type,
        counts_by_provider=agg.counts_by_provider,
        aggregation=agg,
        notes=notes,
    )
