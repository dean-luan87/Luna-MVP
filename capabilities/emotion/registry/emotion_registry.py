# -*- coding: utf-8 -*-
"""
EmotionCapabilityRegistry (Stage-0 placeholder).

本轮仅占位：用于未来管理 emotion provider。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from capabilities.emotion.interfaces.providers import EmotionProvider
from shared.registry.provider_registry import ProviderRegistry


@dataclass
class EmotionCapabilityRegistry:
    emotion: ProviderRegistry[EmotionProvider]
    default_emotion: Optional[str] = None

    @classmethod
    def empty(cls) -> "EmotionCapabilityRegistry":
        return cls(emotion=ProviderRegistry())

