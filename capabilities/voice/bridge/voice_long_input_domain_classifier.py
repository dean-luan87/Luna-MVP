# -*- coding: utf-8 -*-
"""
长输入任务域分类（规则版 v1）。

不接模型；输出 DomainClassificationResult，与 LUNA_TASK_DOMAIN_CLASSIFICATION_V1 一致。
"""

from __future__ import annotations

import re
from typing import List, Optional, Tuple

from shared.schemas.domain_classification import DomainClassificationResult
from shared.schemas.task_domain_v1 import (
    CONFIRMATION_FEEDBACK,
    DEVICE_CONTROL,
    NAVIGATION,
    NO_TASK_OBSERVATION,
    OBSERVATION,
    TASK_CONTROL,
    TASK_QUERY,
    UNSUPPORTED_OR_REJECT,
)

# 不支持 / 越权（先于其它域）
_UNSUPPORTED_PATTERNS: List[Tuple[str, str]] = [
    (r"自动挂号", "external_registration_not_supported"),
    (r"替.+发消息|发消息给", "messaging_not_supported"),
    (r"下单买药|替我下单", "commerce_not_supported"),
]

_DEVICE_PAT = re.compile(r"音量|静音|关机|设备.{0,4}怎么样|大声|小声")
_TASK_CTRL_PAT = re.compile(r"暂停任务|继续任务|结束当前任务|结束任务|切换任务|切换成|先做这个")
_TASK_QUERY_PAT = re.compile(r"到哪了|接下来做什么|当前状态|还有多远|任务做到")
_CONF_PAT = re.compile(r"^(是|对|不是|不对|不用了)$")
_NAV_PAT = re.compile(r"带我去|导航|去医院|去商场|去便利店|走到哪|还有多久|先去|再去|去医院|去\s*\w+")
_OBS_PAT = re.compile(
    r"找手机|前面是什么|左边|右边|附近|扫描|持续看|有没有便利店|找便利店|买点吃的|顺便|路上|便利店"
)
_CASUAL_PAT = re.compile(r"^前面是什么$|^附近有什么$|^旁边")  # 极短无任务观察


def _try_unsupported(text: str) -> Optional[str]:
    t = text.strip()
    for pat, reason in _UNSUPPORTED_PATTERNS:
        if re.search(pat, t):
            return reason
    return None


def classify_long_input_text(text: str) -> DomainClassificationResult:
    """规则版域分类。"""
    t = (text or "").strip()
    if not t:
        return DomainClassificationResult(
            primary_domain=UNSUPPORTED_OR_REJECT,
            intent_complexity="ambiguous",
            can_map_to_system_tasks=False,
            needs_clarification=True,
            should_reject=False,
            confidence=0.2,
            metadata={"reason": "empty_text"},
        )

    reason = _try_unsupported(t)
    if reason:
        return DomainClassificationResult(
            primary_domain=UNSUPPORTED_OR_REJECT,
            secondary_domains=[],
            intent_complexity="single_step",
            can_map_to_system_tasks=False,
            should_reject=True,
            rejection_reason_candidate=reason,
            confidence=0.9,
            metadata={"rule": "unsupported_pattern"},
        )

    secondary: List[str] = []

    if _CONF_PAT.match(t):
        return DomainClassificationResult(
            primary_domain=CONFIRMATION_FEEDBACK,
            intent_complexity="single_step",
            can_map_to_system_tasks=True,
            confidence=0.75,
        )

    if _DEVICE_PAT.search(t):
        return DomainClassificationResult(
            primary_domain=DEVICE_CONTROL,
            intent_complexity="single_step",
            can_map_to_system_tasks=True,
            confidence=0.8,
        )

    if _TASK_CTRL_PAT.search(t):
        return DomainClassificationResult(
            primary_domain=TASK_CONTROL,
            intent_complexity="multi_step" if ("先" in t and "再" in t) else "single_step",
            can_map_to_system_tasks=True,
            confidence=0.82,
        )

    if _TASK_QUERY_PAT.search(t):
        return DomainClassificationResult(
            primary_domain=TASK_QUERY,
            intent_complexity="single_step",
            can_map_to_system_tasks=True,
            confidence=0.85,
        )

    # 多域线索：导航 + 观察
    nav_hit = _NAV_PAT.search(t)
    obs_hit = _OBS_PAT.search(t)
    if nav_hit and obs_hit and ("顺便" in t or "路上" in t):
        secondary.append(OBSERVATION)
        return DomainClassificationResult(
            primary_domain=NAVIGATION,
            secondary_domains=secondary,
            intent_complexity="multi_step",
            can_map_to_system_tasks=True,
            confidence=0.78,
            metadata={"mixed": "navigation_with_observation"},
        )

    if nav_hit or "去" in t[:4] or "导航" in t:
        return DomainClassificationResult(
            primary_domain=NAVIGATION,
            secondary_domains=secondary,
            intent_complexity="multi_step" if ("再" in t or "然后" in t or "，" in t) else "single_step",
            can_map_to_system_tasks=True,
            confidence=0.8,
        )

    if obs_hit:
        return DomainClassificationResult(
            primary_domain=OBSERVATION,
            intent_complexity="multi_step" if ("再" in t or "然后" in t) else "single_step",
            can_map_to_system_tasks=True,
            confidence=0.8,
        )

    if _CASUAL_PAT.search(t):
        return DomainClassificationResult(
            primary_domain=NO_TASK_OBSERVATION,
            intent_complexity="single_step",
            can_map_to_system_tasks=True,
            confidence=0.65,
        )

    # 默认：尝试观察或需澄清
    return DomainClassificationResult(
        primary_domain=OBSERVATION,
        intent_complexity="ambiguous",
        can_map_to_system_tasks=False,
        needs_clarification=True,
        confidence=0.4,
        metadata={"rule": "fallback_ambiguous"},
    )
