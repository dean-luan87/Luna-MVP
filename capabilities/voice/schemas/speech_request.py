# -*- coding: utf-8 -*-
"""
SpeechRequest (Stage-1 placeholder).

统一输出面：各模块只能提交输出请求，禁止直连 TTS。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class SpeechRequest:
    request_id: str
    source_module: str
    output_category: str
    text_candidate: str
    priority: int = 0
    interruptible: bool = True
    dedup_allowed: bool = True
    cooldown_key: Optional[str] = None
    task_context_id: Optional[str] = None
    risk_context: Optional[Dict[str, Any]] = None
    trace_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

