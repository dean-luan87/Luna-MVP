# -*- coding: utf-8 -*-
"""
Provider types (Stage-2).
"""

from __future__ import annotations

from typing import Protocol

from capabilities.voice.output.tts_provider_runtime import TTSProviderResult


class LocalTTSProvider(Protocol):
    name: str

    def synthesize(self, *, text: str, preset_name: str, preset: dict, timeout_ms: int) -> TTSProviderResult:
        ...

