# -*- coding: utf-8 -*-
"""
VoiceEvent: capability-agnostic speech event schema (Stage-0).

要求：
- 标准对象，不面向某个模型厂商私有字段
- 未来不同 ASR/TTS/实时语音模型都必须通过 adapter 适配到该对象
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class VoiceEvent:
    event_id: str
    timestamp: float
    source: str
    provider_name: str
    model_name: str
    text: Optional[str] = None
    confidence: Optional[float] = None
    is_final: bool = True
    interruptible: bool = True
    task_context_id: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

