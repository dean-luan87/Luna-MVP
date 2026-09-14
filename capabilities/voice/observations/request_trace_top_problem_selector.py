# -*- coding: utf-8 -*-
"""
从一组 RequestTraceProblemSummary 中规则化选出「当前最值得关注」的一条（top_problem）。

不随机、不只看最新；与 prioritize_problems 分数一致，并生成可读原因（中文）。
"""

from __future__ import annotations

import time
from typing import List, Optional, Tuple

from capabilities.voice.observations.request_trace_problem_aggregator import is_pure_success_noise
from capabilities.voice.observations.request_trace_problem_prioritizer import (
    DEFAULT_MAIN_PROVIDER,
    prioritize_problems,
)
from capabilities.voice.observations.request_trace_problem_summary import RequestTraceProblemSummary

# 视为「有高优先级」的 alert（用于「无高优先级」空态）
_HIGH_ALERTS = frozenset({"warning", "high_risk", "critical"})
_ACTION_ISSUES = frozenset(
    {
        "playback_failure",
        "output_delivery_failure",
        "provider_chain_failure",
        "request_suppressed",
        "observation_gap",
        "unknown_failure",
    }
)


def select_top_problem(
    items: List[RequestTraceProblemSummary],
    *,
    now: Optional[float] = None,
) -> Tuple[Optional[RequestTraceProblemSummary], str]:
    """
    返回 (top_problem 或 None, 中文原因说明)。

    若全部为纯成功链，返回 (None, 「当前无高优先级问题」类说明)。
    """
    if not items:
        return None, "无可用问题摘要，无法选择 top_problem。"

    ranked = prioritize_problems(list(items), now=now)

    # 排除纯成功噪声后取首条
    for p in ranked:
        if not is_pure_success_noise(p):
            reason = _explain_top(p, ranked)
            return p, reason

    return None, "当前无高优先级问题：样本均为链级成功且无归因问题。"


def _explain_top(chosen: RequestTraceProblemSummary, ranked: List[RequestTraceProblemSummary]) -> str:
    parts: List[str] = []
    parts.append(f"priority_score={chosen.priority_score} 最高（同批内规则排序）")
    parts.append(f"alert_level={chosen.alert_level}")
    if chosen.is_action_required:
        parts.append("需要人工跟进（is_action_required）")
    prov = (chosen.provider_name or "").strip().lower()
    if prov == DEFAULT_MAIN_PROVIDER and chosen.alert_level in _HIGH_ALERTS:
        parts.append(f"影响当前默认主样本 provider（{DEFAULT_MAIN_PROVIDER}）")
    if chosen.final_execution_mode == "failed_no_output":
        parts.append("存在 failed_no_output 终态")
    pos = ranked.index(chosen) + 1
    parts.append(f"在 prioritize_problems 全序中位列第 {pos} 位")
    return "；".join(parts)


def has_any_high_priority(items: List[RequestTraceProblemSummary]) -> bool:
    """是否存在需要强提醒的问题（用于空态判断辅助）。"""
    for p in items:
        if is_pure_success_noise(p):
            continue
        if p.alert_level in _HIGH_ALERTS or p.is_action_required:
            return True
        if p.primary_issue_type in _ACTION_ISSUES and p.alert_level != "normal":
            return True
    return False
