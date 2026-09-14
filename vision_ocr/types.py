from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple

BBox = Tuple[int, int, int, int]


@dataclass(frozen=True)
class OcrSignal:
    """
    来自 OCR/Detector 的原始信号（不等于事实）
    """

    text: str
    score: float = 0.0
    bbox: Optional[BBox] = None
    lang: str = "unknown"
    source: str = "ocr"
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SemanticToken:
    """
    OCR 归一化后的“意义 token”
    """

    key: str
    value: Optional[str] = None
    confidence: float = 0.0
    bbox: Optional[BBox] = None
    raw_text: str = ""
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ReferenceCard:
    """
    世界模型 reference 卡片：只作为参考，不进入 vision facts / stable_world
    """

    kind: str
    meaning: str
    confidence: float
    bbox: Optional[BBox] = None
    attrs: Dict[str, Any] = field(default_factory=dict)
