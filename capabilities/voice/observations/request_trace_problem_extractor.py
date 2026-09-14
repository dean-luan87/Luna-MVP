# -*- coding: utf-8 -*-
"""
从 RequestTraceIssue / RequestTraceDiagnosticSummary 提炼 RequestTraceProblemSummary。

规则化：中文摘要句、是否需行动、展示层 alert_level；不调用 LLM，不改分析器逻辑。
"""

from __future__ import annotations

from typing import Optional, Tuple

from capabilities.voice.observations.request_trace_alert_level import presentation_alert_level_from_issue
from capabilities.voice.observations.request_trace_chain import RequestTraceChain
from capabilities.voice.observations.request_trace_diagnostic_summary import RequestTraceDiagnosticSummary
from capabilities.voice.observations.request_trace_issue import (
    ISSUE_NONE,
    ISSUE_OBSERVATION_GAP,
    ISSUE_OUTPUT_DELIVERY_FAILURE,
    ISSUE_PLAYBACK_FAILURE,
    ISSUE_PROVIDER_CHAIN_FAILURE,
    ISSUE_PROVIDER_UNAVAILABLE,
    ISSUE_REQUEST_SUPPRESSED,
    ISSUE_UNKNOWN,
    RequestTraceIssue,
)
from capabilities.voice.observations.request_trace_problem_prioritizer import compute_priority_score
from capabilities.voice.observations.request_trace_problem_summary import RequestTraceProblemSummary
from capabilities.voice.observations.request_trace_summary import build_request_trace_summary


def _problem_id(issue: RequestTraceIssue) -> str:
    tid = issue.trace_id or "notrace"
    return f"{issue.request_id}:{issue.primary_issue_type}:{tid}"


def _rule_summary_zh(issue: RequestTraceIssue, diagnostic: RequestTraceDiagnosticSummary) -> Tuple[str, bool]:
    """
    返回 (中文摘要句, is_action_required)。
    优先按终态 + issue 类型覆盖；否则压缩 diagnostic 信息。
    """
    fs = (issue.final_status or "").strip().lower()
    it = issue.primary_issue_type or ""

    if it == ISSUE_NONE and fs == "success":
        return "链级成功，无归因问题。", False

    if fs == "suppressed" or it == ISSUE_REQUEST_SUPPRESSED:
        return "请求被治理层抑制，未进入执行链。", False

    if fs == "degraded_success" and it == ISSUE_PROVIDER_UNAVAILABLE:
        return "主 provider 失败，已由 fallback provider 成功接管。", False

    if fs == "rollback_success" and it == ISSUE_PROVIDER_CHAIN_FAILURE:
        return "provider chain 失败，已回滚到 legacy。", True

    if it in (ISSUE_PLAYBACK_FAILURE, ISSUE_OUTPUT_DELIVERY_FAILURE):
        return "请求未形成有效播报输出。", True

    if it == ISSUE_OBSERVATION_GAP:
        return "观测覆盖不足，难以完整归因；建议补日志与抽链规则。", True

    if it == ISSUE_UNKNOWN:
        return "问题未归类，请对照阶段链与错误列表。", True

    # 退化：保留 diagnostic 英文摘要前缀 + 短提示
    base = (diagnostic.summary_text or "").strip()
    if base:
        return f"（规则摘要）{base[:200]}", issue.severity in ("error", "critical")

    return (issue.primary_issue_reason or "无摘要")[:280], issue.severity in ("error", "critical")


def extract_problem_summary(
    chain: RequestTraceChain,
    issue: RequestTraceIssue,
    diagnostic: RequestTraceDiagnosticSummary,
) -> RequestTraceProblemSummary:
    """
    输入单链 + 已由 analyze_request_trace_issue 得到的 issue/diagnostic，输出问题摘要。

    若仅有 issue/diagnostic 而无 chain，无法计算规范化 status；请尽量传入 chain。
    """
    sm = build_request_trace_summary(chain)
    alert = presentation_alert_level_from_issue(issue)
    summary_zh, action = _rule_summary_zh(issue, diagnostic)

    # 规则覆盖 is_action_required（与 _rule_summary_zh 对齐；可对 high_risk 强制 true）
    if alert == "high_risk" and issue.final_status == "rollback_success":
        action = True

    checkpoints = list(diagnostic.recommended_checkpoints or issue.recommended_checkpoints)[:8]

    prob = RequestTraceProblemSummary(
        problem_id=_problem_id(issue),
        request_id=issue.request_id,
        trace_id=issue.trace_id,
        chain_type=issue.chain_type,
        provider_name=issue.provider_name,
        final_execution_mode=issue.final_execution_mode,
        alert_level=alert,
        primary_issue_type=issue.primary_issue_type,
        primary_issue_reason=issue.primary_issue_reason,
        failed_stage=issue.failed_stage,
        status=sm.status,
        severity=issue.severity,
        summary_text=summary_zh,
        recommended_checkpoints=checkpoints,
        is_action_required=action,
        priority_score=0,
        priority_reason="",
        ended_at=chain.ended_at,
    )
    sc, rs = compute_priority_score(prob)
    prob.priority_score = sc
    prob.priority_reason = rs
    return prob


def extract_problem_summary_from_parts(
    issue: RequestTraceIssue,
    diagnostic: RequestTraceDiagnosticSummary,
    *,
    status_fallback: str = "unknown",
    ended_at: Optional[float] = None,
) -> RequestTraceProblemSummary:
    """无 chain 时的降级入口：status 用占位，优先级新鲜度可能缺失。"""
    alert = presentation_alert_level_from_issue(issue)
    summary_zh, action = _rule_summary_zh(issue, diagnostic)
    if alert == "high_risk" and issue.final_status == "rollback_success":
        action = True

    prob = RequestTraceProblemSummary(
        problem_id=_problem_id(issue),
        request_id=issue.request_id,
        trace_id=issue.trace_id,
        chain_type=issue.chain_type,
        provider_name=issue.provider_name,
        final_execution_mode=issue.final_execution_mode,
        alert_level=alert,
        primary_issue_type=issue.primary_issue_type,
        primary_issue_reason=issue.primary_issue_reason,
        failed_stage=issue.failed_stage,
        status=status_fallback,
        severity=issue.severity,
        summary_text=summary_zh,
        recommended_checkpoints=list(diagnostic.recommended_checkpoints or issue.recommended_checkpoints)[:8],
        is_action_required=action,
        priority_score=0,
        priority_reason="",
        ended_at=ended_at,
    )
    sc, rs = compute_priority_score(prob)
    prob.priority_score = sc
    prob.priority_reason = rs
    return prob
