# -*- coding: utf-8 -*-
"""
白盒展示层告警等级（Alert Level）：叠在底层 severity 之上，供排序与首页摘要。

不替代 severity；severity 仍来自 request_trace_issue_analyzer 规则。
"""

from __future__ import annotations

from capabilities.voice.observations.request_trace_issue import (
    ISSUE_NONE,
    ISSUE_OUTPUT_DELIVERY_FAILURE,
    ISSUE_PLAYBACK_FAILURE,
    ISSUE_PROVIDER_CHAIN_FAILURE,
    ISSUE_PROVIDER_UNAVAILABLE,
    ISSUE_REQUEST_SUPPRESSED,
    RequestTraceIssue,
)

# 面向白盒展示的统一等级（与 UI 颜色解耦；本轮仅为字符串）
ALERT_LEVEL_NORMAL = "normal"
ALERT_LEVEL_NOTICE = "notice"
ALERT_LEVEL_WARNING = "warning"
ALERT_LEVEL_HIGH_RISK = "high_risk"
ALERT_LEVEL_CRITICAL = "critical"

# 数值越大越优先（与 prioritizer 一致）
ALERT_LEVEL_SORT_WEIGHT: dict[str, int] = {
    ALERT_LEVEL_NORMAL: 0,
    ALERT_LEVEL_NOTICE: 1,
    ALERT_LEVEL_WARNING: 2,
    ALERT_LEVEL_HIGH_RISK: 3,
    ALERT_LEVEL_CRITICAL: 4,
}

# 与 RequestTraceIssue.severity 的默认映射（无场景覆盖时使用）
_SEVERITY_TO_ALERT = {
    "info": ALERT_LEVEL_NORMAL,
    "warning": ALERT_LEVEL_NOTICE,
    "degraded": ALERT_LEVEL_WARNING,
    "error": ALERT_LEVEL_HIGH_RISK,
    "critical": ALERT_LEVEL_CRITICAL,
}


def severity_to_alert_level(severity: str) -> str:
    """底层 severity → 展示层 alert_level（默认表）。"""
    s = (severity or "").strip().lower()
    return _SEVERITY_TO_ALERT.get(s, ALERT_LEVEL_NOTICE)


def presentation_alert_level_from_issue(issue: RequestTraceIssue) -> str:
    """
    白盒展示用 alert_level：在 severity 映射基础上，按终态/issue 类型做场景覆盖。

    与 LUNA_VOICE_ALERT_AND_PROBLEM_SUMMARY_GUIDE_V1.md 中「问题提炼类型」一致。
    """
    fs = (issue.final_status or "").strip().lower()
    it = issue.primary_issue_type or ""

    # 播放/无输出：最高展示优先级
    if it in (ISSUE_PLAYBACK_FAILURE, ISSUE_OUTPUT_DELIVERY_FAILURE):
        return ALERT_LEVEL_CRITICAL

    # 抑制：治理层拦截，通常低于硬失败
    if fs == "suppressed" or it == ISSUE_REQUEST_SUPPRESSED:
        return ALERT_LEVEL_NOTICE

    # 纯成功
    if it == ISSUE_NONE and fs == "success":
        return ALERT_LEVEL_NORMAL

    # fallback 成功（降级但产出）
    if fs == "degraded_success" and it == ISSUE_PROVIDER_UNAVAILABLE:
        return ALERT_LEVEL_WARNING

    # rollback 成功：主链失败但 legacy 救回 → 展示层标为高关注
    if fs == "rollback_success" and it == ISSUE_PROVIDER_CHAIN_FAILURE:
        return ALERT_LEVEL_HIGH_RISK

    # 其他 provider 链失败类（未归类到上面）
    if it == ISSUE_PROVIDER_CHAIN_FAILURE and fs == "failed":
        return ALERT_LEVEL_HIGH_RISK

    return severity_to_alert_level(issue.severity)
