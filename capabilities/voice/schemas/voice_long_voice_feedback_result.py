# -*- coding: utf-8 -*-
"""
长语音解析后的统一反馈结果占位（供白盒 / 图书馆 / 后续策略与情感层消费）。

不绑定 TTS；`feedback_text_candidate` 为规则层或模型层可覆写候选。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class VoiceLongVoiceFeedbackResult:
    """
    与 parse 结果对齐的一层「打算怎么回用户」的声明式对象。

    related_plan_version：v1 | v2 | final | none（none 表示无计划或仅保留非任务）。
    """

    feedback_mode: str
    feedback_text_candidate: str = ""
    requires_user_response: bool = False
    related_plan_version: str = "v1"
    non_task_acknowledged: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "feedback_mode": self.feedback_mode,
            "feedback_text_candidate": self.feedback_text_candidate,
            "requires_user_response": self.requires_user_response,
            "related_plan_version": self.related_plan_version,
            "non_task_acknowledged": self.non_task_acknowledged,
            "metadata": dict(self.metadata),
        }
