# -*- coding: utf-8 -*-
"""
ASRProvider (Stage-1 placeholder).

注意：Stage-1 不接入真实 ASR，只固化接口边界。
"""

from __future__ import annotations

from typing import Protocol

from capabilities.voice.schemas.voice_input_event import VoiceInputEvent


class ASRProvider(Protocol):
    name: str
    model_name: str

    def transcribe(self, *, audio_bytes: bytes, is_final: bool = True) -> VoiceInputEvent:
        """音频 -> VoiceInputEvent（标准输入对象）。"""

