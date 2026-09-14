# -*- coding: utf-8 -*-
"""
VoiceOutputPlane (Stage-1 placeholder).

统一发声出口：任何模块只能提交 SpeechRequest，不得直连 TTS。
Stage-1 不做接线，只固化接口边界。
"""

from __future__ import annotations

from typing import Protocol, Tuple

from capabilities.voice.schemas.speech_request import SpeechRequest


class VoiceOutputPlane(Protocol):
    def submit(self, request: SpeechRequest) -> Tuple[bool, str]:
        """提交输出请求，返回 (accepted, reason)。"""

