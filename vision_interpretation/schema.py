from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class RawTextCandidate:
    text: str
    confidence: float
    bbox: Optional[Dict] = None


@dataclass
class InterpretedMeaning:
    meaning: str
    confidence: float
    ambiguity: List[str]
    evidence: Dict


@dataclass
class VisionInterpretation:
    roi_kind: str
    raw_text_candidates: List[RawTextCandidate]
    interpreted_meanings: List[InterpretedMeaning]
    uncertainty: float
    source: str
