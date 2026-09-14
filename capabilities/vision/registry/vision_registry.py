# -*- coding: utf-8 -*-
"""
VisionCapabilityRegistry (Stage-0 placeholder).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from capabilities.vision.interfaces.providers import DetectionProvider, OCRProvider, TrackingProvider
from shared.registry.provider_registry import ProviderRegistry


@dataclass
class VisionCapabilityRegistry:
    detection: ProviderRegistry[DetectionProvider]
    ocr: ProviderRegistry[OCRProvider]
    tracking: ProviderRegistry[TrackingProvider]
    default_detection: Optional[str] = None
    default_ocr: Optional[str] = None
    default_tracking: Optional[str] = None

    @classmethod
    def empty(cls) -> "VisionCapabilityRegistry":
        return cls(
            detection=ProviderRegistry(),
            ocr=ProviderRegistry(),
            tracking=ProviderRegistry(),
        )

