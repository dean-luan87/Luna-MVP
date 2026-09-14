# -*- coding: utf-8 -*-
"""
TTSProvider (Stage-1 placeholder).

注意：Stage-1 不接入真实 TTS，只固化接口边界。
"""

from __future__ import annotations

from typing import Protocol


class TTSProvider(Protocol):
    name: str
    model_name: str

    def synthesize(self, *, text: str) -> bytes:
        ...

    def say(self, *, text: str) -> None:
        ...

