# -*- coding: utf-8 -*-
"""
对一组 RequestTraceProblemSummary 做最小规则聚合（无聚类、无 LLM）。

回答：哪类 issue 最多、多少影响主样本 provider、多少属于已兜住/降级路径。
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from capabilities.voice.observations.request_trace_problem_prioritizer import DEFAULT_MAIN_PROVIDER
from capabilities.voice.observations.request_trace_problem_summary import RequestTraceProblemSummary


def problem_affects_main_provider(p: RequestTraceProblemSummary) -> bool:
    """当前默认主样本为 piper：其上的非 ok 语义问题视为影响主链叙事。"""
    prov = (p.provider_name or "").strip().lower()
    if prov != DEFAULT_MAIN_PROVIDER:
        return False
    pres = (p.alert_level or "").strip().lower()
    return pres in ("warning", "high_risk", "critical")


def is_degraded_but_handled(p: RequestTraceProblemSummary) -> bool:
    """
    降级或回退但已产出/已救回：不应与「直接失败」混在 active 列表。

    规则：fallback 降级成功、rollback 成功路径。
    """
    ct = (p.chain_type or "").lower()
    st = (p.status or "").lower()
    if "provider_fallback" in ct and st == "degraded_success":
        return True
    if "legacy_rollback" in ct and p.alert_level == "high_risk" and st == "success":
        return True
    if p.primary_issue_type == "provider_unavailable" and st == "degraded_success":
        return True
    return False


def is_suppressed_or_low_priority(p: RequestTraceProblemSummary) -> bool:
    """治理抑制或可归为低优先观察的问题。"""
    it = (p.primary_issue_type or "").lower()
    st = (p.status or "").lower()
    if st == "suppressed" or it == "request_suppressed":
        return True
    if p.alert_level == "normal" and it in ("none", ""):
        return True
    if p.alert_level == "notice" and it == "request_suppressed":
        return True
    return False


def is_pure_success_noise(p: RequestTraceProblemSummary) -> bool:
    """纯成功链：不参与 top/active 竞争。"""
    return p.alert_level == "normal" and (p.primary_issue_type or "") in ("none", "")


@dataclass
class ProblemAggregationSummary:
    """聚合统计结果，供 problem board 与报表复用。"""

    counts_by_alert_level: Dict[str, int] = field(default_factory=dict)
    counts_by_issue_type: Dict[str, int] = field(default_factory=dict)
    counts_by_provider: Dict[str, int] = field(default_factory=dict)
    counts_by_final_execution_mode: Dict[str, int] = field(default_factory=dict)
    most_common_issue_type: Optional[str] = None
    affects_main_provider_count: int = 0
    degraded_but_handled_count: int = 0
    suppressed_or_low_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "counts_by_alert_level": dict(self.counts_by_alert_level),
            "counts_by_issue_type": dict(self.counts_by_issue_type),
            "counts_by_provider": dict(self.counts_by_provider),
            "counts_by_final_execution_mode": dict(self.counts_by_final_execution_mode),
            "most_common_issue_type": self.most_common_issue_type,
            "affects_main_provider_count": self.affects_main_provider_count,
            "degraded_but_handled_count": self.degraded_but_handled_count,
            "suppressed_or_low_count": self.suppressed_or_low_count,
        }


def aggregate_problems(problems: List[RequestTraceProblemSummary]) -> ProblemAggregationSummary:
    if not problems:
        return ProblemAggregationSummary()

    al = Counter((p.alert_level or "unknown") for p in problems)
    it = Counter((p.primary_issue_type or "unknown") for p in problems)
    pv = Counter((p.provider_name or "unknown") for p in problems)
    fm = Counter((p.final_execution_mode or "unknown") for p in problems)

    mc = it.most_common(1)[0][0] if it else None

    aff = sum(1 for p in problems if problem_affects_main_provider(p))
    dh = sum(1 for p in problems if is_degraded_but_handled(p))
    sl = sum(1 for p in problems if is_suppressed_or_low_priority(p))

    return ProblemAggregationSummary(
        counts_by_alert_level=dict(al),
        counts_by_issue_type=dict(it),
        counts_by_provider=dict(pv),
        counts_by_final_execution_mode=dict(fm),
        most_common_issue_type=mc,
        affects_main_provider_count=aff,
        degraded_but_handled_count=dh,
        suppressed_or_low_count=sl,
    )
