# -*- coding: utf-8 -*-
"""
Alert Level → 展示语义（Presentation Semantic）：供简洁模式与后续 UI 挂色用。

本模块只产出语义标签（ok / info / attention / warning / danger），不含十六进制颜色。
"""

from __future__ import annotations

from capabilities.voice.observations.request_trace_alert_level import (
    ALERT_LEVEL_CRITICAL,
    ALERT_LEVEL_HIGH_RISK,
    ALERT_LEVEL_NORMAL,
    ALERT_LEVEL_NOTICE,
    ALERT_LEVEL_WARNING,
)

# 展示语义标签（前端可 1:1 映射色板）
PRESENTATION_OK = "ok"
PRESENTATION_INFO = "info"
PRESENTATION_ATTENTION = "attention"
PRESENTATION_WARNING = "warning"
PRESENTATION_DANGER = "danger"

# alert_level → 展示语义（固定表，规则化）
_ALERT_TO_PRESENTATION: dict[str, str] = {
    ALERT_LEVEL_NORMAL: PRESENTATION_OK,
    ALERT_LEVEL_NOTICE: PRESENTATION_INFO,
    ALERT_LEVEL_WARNING: PRESENTATION_ATTENTION,
    ALERT_LEVEL_HIGH_RISK: PRESENTATION_WARNING,
    ALERT_LEVEL_CRITICAL: PRESENTATION_DANGER,
}


def alert_level_to_presentation_semantic(alert_level: str) -> str:
    """
    将白盒 alert_level 映射为展示语义。

    未知档位按 notice 档处理为 info，避免静默降级为 ok。
    """
    key = (alert_level or "").strip().lower()
    return _ALERT_TO_PRESENTATION.get(key, PRESENTATION_INFO)


def presentation_semantic_sort_weight(presentation: str) -> int:
    """排序权重：越大越醒目（仅用于同档内辅助，主排序仍用 priority_score）。"""
    m = {
        PRESENTATION_OK: 0,
        PRESENTATION_INFO: 1,
        PRESENTATION_ATTENTION: 2,
        PRESENTATION_WARNING: 3,
        PRESENTATION_DANGER: 4,
    }
    return m.get(presentation, 1)
