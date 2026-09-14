# -*- coding: utf-8 -*-
"""长输入拆解总结果包装（供 Bridge / 白盒）。"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from shared.schemas.domain_classification import DomainClassificationResult
from shared.schemas.task_plan import TaskPlan

from capabilities.voice.schemas.voice_long_input_input_mode import (
    InputModeJudgement,
    NonTaskPayload,
)
from capabilities.voice.schemas.voice_long_input_instruction_candidate import (
    VoiceLongInputInstructionCandidate,
)
from capabilities.voice.schemas.voice_long_voice_feedback_result import VoiceLongVoiceFeedbackResult


@dataclass
class VoiceLongInputParseResult:
    request_id: str
    raw_text: str
    domain_result: DomainClassificationResult
    instruction_candidates: List[VoiceLongInputInstructionCandidate]
    task_plan_v1: Optional[TaskPlan]
    clarification_needed: bool
    rejection_needed: bool
    rejection_reason: Optional[str] = None
    notes: str = ""
    session_hint: str = ""
    # v1.1：长语音总分流（任务 / 混合 / 非任务）+ 情感引擎预留
    input_mode_judgement: Optional[InputModeJudgement] = None
    non_task_payload: Optional[NonTaskPayload] = None
    mixed_input_flag: bool = False
    # v1：解析后的统一反馈占位（规则推导，非 TTS）
    voice_feedback: Optional[VoiceLongVoiceFeedbackResult] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "raw_text": self.raw_text,
            "domain_result": self.domain_result.to_dict(),
            "instruction_candidates": [c.to_dict() for c in self.instruction_candidates],
            "task_plan_v1": self.task_plan_v1.to_dict() if self.task_plan_v1 else None,
            "clarification_needed": self.clarification_needed,
            "rejection_needed": self.rejection_needed,
            "rejection_reason": self.rejection_reason,
            "notes": self.notes,
            "session_hint": self.session_hint,
            "input_mode_judgement": self.input_mode_judgement.to_dict() if self.input_mode_judgement else None,
            "non_task_payload": self.non_task_payload.to_dict() if self.non_task_payload else None,
            "mixed_input_flag": self.mixed_input_flag,
            "voice_feedback": self.voice_feedback.to_dict() if self.voice_feedback else None,
        }
