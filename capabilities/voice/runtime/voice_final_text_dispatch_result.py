# -*- coding: utf-8 -*-
"""
切段完成后的统一分流结果（语音主线 v1）。

单出口：白盒、日志、Bridge、图书馆后续均可从本对象读取短链 / 长链 / reject。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from capabilities.voice.bridge.bridge_decision import BridgeDecision
from capabilities.voice.bridge.voice_input_to_bridge import bridge_decision_to_trace_dict
from capabilities.voice.schemas.voice_input_event import VoiceInputEvent
from capabilities.voice.schemas.voice_input_rejection_result import VoiceInputRejectionResult
from capabilities.voice.schemas.voice_long_input_parse_result import VoiceLongInputParseResult


@dataclass
class VoiceFinalTextDispatchResult:
    """process_final_text 后的分流结果（三类之一生效）。"""

    request_id: str
    session_id: str
    dispatch_type: str  # short_controlled_input | long_task_planning_input | rejected_input

    short_controlled_input: bool = False
    long_task_planning_input: bool = False
    rejected_input: bool = False

    voice_input_event: Optional[VoiceInputEvent] = None
    bridge_decision: Optional[BridgeDecision] = None
    long_input_parse_result: Optional[VoiceLongInputParseResult] = None
    rejection_result: Optional[VoiceInputRejectionResult] = None

    dispatch_reason_code: str = ""
    notes: str = ""

    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "session_id": self.session_id,
            "dispatch_type": self.dispatch_type,
            "short_controlled_input": self.short_controlled_input,
            "long_task_planning_input": self.long_task_planning_input,
            "rejected_input": self.rejected_input,
            "voice_input_event": self.voice_input_event.to_dict() if self.voice_input_event else None,
            "bridge_decision": (
                bridge_decision_to_trace_dict(self.bridge_decision)
                if self.bridge_decision is not None
                else None
            ),
            "long_input_parse_result": (
                self.long_input_parse_result.to_dict() if self.long_input_parse_result else None
            ),
            "rejection_result": rejection_result_to_dict(self.rejection_result),
            "dispatch_reason_code": self.dispatch_reason_code,
            "notes": self.notes,
            "metadata": dict(self.metadata),
        }


def rejection_result_to_dict(rej: Optional[VoiceInputRejectionResult]) -> Optional[Dict[str, Any]]:
    if rej is None:
        return None
    return {
        "request_id": rej.request_id,
        "reason": rej.reason,
        "router_stage": rej.router_stage,
        "raw_text": rej.raw_text,
        "normalized_text": rej.normalized_text,
        "is_task_mode": rej.is_task_mode,
        "source_type": rej.source_type,
        "reason_code": rej.reason_code,
    }
