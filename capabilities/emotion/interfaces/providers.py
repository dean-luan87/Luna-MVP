# -*- coding: utf-8 -*-
"""
Emotion providers interfaces (Stage-0 placeholder).

本轮仅占位，不实现。
"""

from __future__ import annotations

from typing import Protocol

from capabilities.emotion.schemas.emotion_event import EmotionEvent


class EmotionProvider(Protocol):
    name: str
    model_name: str

    def infer(self, *, text: str | None = None, audio_bytes: bytes | None = None) -> EmotionEvent:
        ...

