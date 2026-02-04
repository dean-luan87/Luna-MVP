from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, Optional, List


@dataclass(frozen=True)
class InterpretationKey:
    roi_kind: str
    category: str
    meaning: str


@dataclass
class InterpretationStats:
    appear_count: int = 0
    confirm_count: int = 0
    contradict_count: int = 0
    last_seen_ts: Optional[float] = None


@dataclass
class StabilityScore:
    stability: float
    confidence: float
    evidence: Dict[str, Any]


@dataclass
class StableInterpretationProfile:
    key: InterpretationKey
    score: StabilityScore
    suggestion: str
    scope: str
    environment_id: str


@dataclass
class SemanticObservation:
    roi_kind: str
    meaning: str
    confidence: float
    ambiguity: List[str]
    uncertainty: float
    source: str
    category: Optional[str] = None
