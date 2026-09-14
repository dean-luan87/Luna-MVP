# -*- coding: utf-8 -*-
"""
对 RequestTraceProblemSummary 列表做规则化优先级排序（无学习、无 LLM）。

排序维度：alert_level、failed_no_output、主样本路径影响、fallback/rollback、需人工、新鲜度。
"""

from __future__ import annotations

import time
from typing import List, Optional, Tuple

from capabilities.voice.observations.request_trace_alert_level import ALERT_LEVEL_SORT_WEIGHT
from capabilities.voice.observations.request_trace_problem_summary import RequestTraceProblemSummary

# 当前默认主样本 provider（与白盒文档一致）
DEFAULT_MAIN_PROVIDER = "piper"


def _freshness_bonus(ended_at: Optional[float], now: float) -> Tuple[int, str]:
    """越新略优先；无时间则不加。"""
    if ended_at is None or ended_at <= 0:
        return 0, ""
    age_s = max(0.0, now - float(ended_at))
    # 24h 内满分衰减到 0
    bonus = max(0, int(400 * (1.0 - min(age_s, 86400.0) / 86400.0)))
    if bonus > 0:
        return bonus, "较新请求略优先"
    return 0, ""


def compute_priority_score(
    p: RequestTraceProblemSummary,
    *,
    now: Optional[float] = None,
) -> Tuple[int, str]:
    """
    返回 (priority_score, priority_reason)。

    分数越大越应先看；规则固定，便于回归。
    """
    t = now if now is not None else time.time()
    parts: List[str] = []
    score = 0

    w = ALERT_LEVEL_SORT_WEIGHT.get(p.alert_level, 1)
    score += w * 2000
    parts.append(f"alert_level={p.alert_level}(+{w * 2000})")

    fm = (p.final_execution_mode or "").strip().lower()
    if fm == "failed_no_output":
        score += 5000
        parts.append("final_mode=failed_no_output(+5000)")

    if p.primary_issue_type in ("playback_failure", "output_delivery_failure"):
        score += 3500
        parts.append("issue=playback_or_delivery(+3500)")

    prov = (p.provider_name or "").strip().lower()
    if prov == DEFAULT_MAIN_PROVIDER and p.alert_level in ("high_risk", "critical", "warning"):
        score += 1500
        parts.append("provider=piper_affected(+1500)")

    ct = (p.chain_type or "").lower()
    if "provider_fallback" in ct or "fallback" in ct:
        score += 800
        parts.append("path=fallback(+800)")
    if "legacy_rollback" in ct or "rollback" in ct:
        score += 1200
        parts.append("path=rollback(+1200)")

    if p.is_action_required:
        score += 600
        parts.append("action_required(+600)")

    fb, fr_note = _freshness_bonus(p.ended_at, t)
    score += fb
    if fr_note:
        parts.append(f"freshness(+{fb})")

    reason = "；".join(parts[:6])
    if len(reason) > 500:
        reason = reason[:497] + "..."
    return score, reason


def prioritize_problems(
    items: List[RequestTraceProblemSummary],
    *,
    now: Optional[float] = None,
) -> List[RequestTraceProblemSummary]:
    """原地填充 priority_score / priority_reason，并按分数降序稳定排序。"""
    out: List[RequestTraceProblemSummary] = []
    for p in items:
        sc, rs = compute_priority_score(p, now=now)
        p.priority_score = sc
        p.priority_reason = rs
        out.append(p)
    out.sort(key=lambda x: (-x.priority_score, x.request_id, x.problem_id))
    return out


def top_k_problems(
    items: List[RequestTraceProblemSummary],
    k: int,
    *,
    now: Optional[float] = None,
) -> List[RequestTraceProblemSummary]:
    """排序后取前 k 条。"""
    ranked = prioritize_problems(list(items), now=now)
    return ranked[: max(0, k)]


def most_critical_problem(
    items: List[RequestTraceProblemSummary],
    *,
    now: Optional[float] = None,
) -> Optional[RequestTraceProblemSummary]:
    """多条摘要中当前最值得关注的一条（排序后首条）。"""
    if not items:
        return None
    return prioritize_problems(list(items), now=now)[0]
