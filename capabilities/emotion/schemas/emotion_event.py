# -*- coding: utf-8 -*-
"""
EmotionEvent (Stage-0 placeholder).

注意：情感系统本轮不实现，仅提供未来适配/接入的稳定 schema 占位。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class EmotionEvent:
    event_id: str
    timestamp: float
    source: str
    provider_name: str
    model_name: str
    emotion_label: Optional[str] = None
    confidence: Optional[float] = None
    task_context_id: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

