from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple


@dataclass
class OCRToken:
    text: str
    bbox: Tuple[int, int, int, int]
    confidence: float


@dataclass
class VisualObject:
    object_type: str
    bbox: Tuple[int, int, int, int]
    confidence: float


@dataclass
class VisualContext:
    roi_kind: str
    scene_tags: List[str]
    objects: List[VisualObject]
    ocr_tokens: List[OCRToken]


@dataclass
class SemanticInterpretation:
    meaning: str
    category: str
    confidence: float
    evidence: Dict[str, str]
    ambiguity: Optional[str]


@dataclass
class InterpretationResult:
    interpretations: List[SemanticInterpretation]
    unresolved: bool
