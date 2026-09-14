# -*- coding: utf-8 -*-
"""
TTS provider runtime primitives (Stage-2).

目标：
- Provider 返回结构化成功/失败，供 fallback 判断
- 禁止静默 fallback
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class TTSFailure:
    failure_type: str  # timeout | exception | invalid_audio | not_available | config_error | unknown
    reason: str
    detail: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TTSProviderResult:
    ok: bool
    provider_name: str
    preset_name: str
    audio_bytes: Optional[bytes] = None
    latency_ms: Optional[int] = None
    failure: Optional[TTSFailure] = None

