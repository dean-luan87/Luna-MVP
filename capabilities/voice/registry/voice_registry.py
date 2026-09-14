# -*- coding: utf-8 -*-
"""
VoiceCapabilityRegistry (Stage-0 placeholder).

目标：
- capability 层内部统一管理 ASR/TTS/VoiceInput provider
- Core 通过 capability facade/bridge 交互，不直接依赖具体 provider 实现
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from capabilities.voice.interfaces.providers import ASRProvider, TTSProvider, VoiceInputProvider
from shared.registry.provider_registry import ProviderRegistry


@dataclass
class VoiceCapabilityRegistry:
    asr: ProviderRegistry[ASRProvider]
    tts: ProviderRegistry[TTSProvider]
    voice_input: ProviderRegistry[VoiceInputProvider]
    default_asr: Optional[str] = None
    default_tts: Optional[str] = None
    default_voice_input: Optional[str] = None

    @classmethod
    def empty(cls) -> "VoiceCapabilityRegistry":
        return cls(
            asr=ProviderRegistry(),
            tts=ProviderRegistry(),
            voice_input=ProviderRegistry(),
        )

