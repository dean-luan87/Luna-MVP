# -*- coding: utf-8 -*-
"""
长语音输入模式与非任务载荷（v1.1）。

长语音入口 ≠ 仅任务入口：需区分任务型 / 混合型 / 非任务型，并为情感引擎预留 non_task_payload。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class InputModeJudgement:
    """长语音总分流：任务 / 混合 / 非任务。"""

    mode: str  # task_only | mixed_task_and_non_task | non_task_only
    has_task_content: bool = False
    has_non_task_content: bool = False
    should_generate_task_plan: bool = False
    should_preserve_non_task_payload: bool = False
    reason_notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mode": self.mode,
            "has_task_content": self.has_task_content,
            "has_non_task_content": self.has_non_task_content,
            "should_generate_task_plan": self.should_generate_task_plan,
            "should_preserve_non_task_payload": self.should_preserve_non_task_payload,
            "reason_notes": self.reason_notes,
        }


@dataclass
class NonTaskSegment:
    segment_type: str  # emotional_context | narrative | other
    content: str

    def to_dict(self) -> Dict[str, Any]:
        return {"segment_type": self.segment_type, "content": self.content}


@dataclass
class NonTaskPayload:
    """不进入任务计划、不执行；预留给情感引擎 / 非任务长对话。"""

    exists: bool = False
    segments: List[NonTaskSegment] = field(default_factory=list)
    handoff_candidate: str = "emotion_engine_future"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "exists": self.exists,
            "segments": [s.to_dict() for s in self.segments],
            "handoff_candidate": self.handoff_candidate,
        }
