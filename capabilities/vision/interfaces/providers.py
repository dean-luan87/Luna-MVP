# -*- coding: utf-8 -*-
"""
Vision providers interfaces (Stage-0 placeholder).

目标：固化 Vision 能力板块 provider 边界（Detection/OCR/Tracking 等）。
禁止：在此处实现具体模型/厂商逻辑。
"""

from __future__ import annotations

from typing import Protocol

from capabilities.vision.schemas.vision_event import VisionEvent


class VisionProvider(Protocol):
    name: str
    model_name: str


class DetectionProvider(VisionProvider, Protocol):
    def detect(self, frame_bytes: bytes) -> list[VisionEvent]:
        ...


class OCRProvider(VisionProvider, Protocol):
    def ocr(self, frame_bytes: bytes) -> list[VisionEvent]:
        ...


class TrackingProvider(VisionProvider, Protocol):
    def track(self, frame_bytes: bytes) -> list[VisionEvent]:
        ...

