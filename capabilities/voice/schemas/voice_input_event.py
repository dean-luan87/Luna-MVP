# -*- coding: utf-8 -*-
"""
VoiceInputEvent：统一语音输入对象（Stage-1 + 输入主线 v1 字段）。

硬约束：
- 输入必须先落标准对象
- 禁止裸文本直入主链

v1 主线扩展字段见 LUNA_VOICE_INPUT_MAINLINE_V1.md。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class VoiceInputEvent:
    event_id: str = ""
    request_id: str = ""
    timestamp: float = 0.0
    session_id: str = ""
    turn_id: str = ""
    source: str = "voice"
    text: Optional[str] = None
    normalized_text: Optional[str] = None
    asr_confidence: Optional[float] = None
    is_final: bool = True
    provider_name: str = ""
    model_name: str = ""
    interrupt_requested: bool = False
    task_context_id: Optional[str] = None
    task_chain_id: Optional[str] = None
    task_phase: Optional[str] = None
    current_mode: Optional[str] = None
    may_change_task_state: bool = False
    may_change_system_state: bool = False
    requires_confirmation_candidate: bool = False
    keywords: List[str] = field(default_factory=list)
    entities: Dict[str, Any] = field(default_factory=dict)
    raw_slots: Dict[str, Any] = field(default_factory=dict)
    trace_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    # —— 输入主线 v1 ——
    source_type: str = "asr"  # asr | text | simulated
    raw_text: Optional[str] = None
    wake_word: str = ""
    active_window: bool = False
    task_shortcut: bool = False
    is_task_mode: bool = False
    wake_word_detected: bool = False
    wake_word_stripped: str = ""
    shortcut_id: Optional[str] = None
    router_decision: str = ""
    context_resume_hint: Optional[str] = None

    # —— 时间治理 v1（长语音 vs 会话窗口）——
    is_forced_cutoff: bool = False
    cutoff_reason: str = ""
    continuation_allowed: bool = False
    voice_runtime_phase: str = ""

    def effective_raw_text(self) -> str:
        if self.raw_text is not None:
            return self.raw_text
        return self.text or ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "request_id": self.request_id or self.event_id,
            "timestamp": self.timestamp,
            "session_id": self.session_id,
            "turn_id": self.turn_id,
            "source": self.source,
            "text": self.text,
            "raw_text": self.effective_raw_text(),
            "normalized_text": self.normalized_text,
            "source_type": self.source_type,
            "wake_word": self.wake_word,
            "active_window": self.active_window,
            "task_shortcut": self.task_shortcut,
            "is_task_mode": self.is_task_mode,
            "asr_confidence": self.asr_confidence,
            "wake_word_detected": self.wake_word_detected,
            "wake_word_stripped": self.wake_word_stripped,
            "shortcut_id": self.shortcut_id,
            "router_decision": self.router_decision,
            "context_resume_hint": self.context_resume_hint,
            "is_forced_cutoff": self.is_forced_cutoff,
            "cutoff_reason": self.cutoff_reason,
            "continuation_allowed": self.continuation_allowed,
            "voice_runtime_phase": self.voice_runtime_phase,
            "provider_name": self.provider_name,
            "model_name": self.model_name,
            "trace_id": self.trace_id,
            "metadata": dict(self.metadata),
        }
