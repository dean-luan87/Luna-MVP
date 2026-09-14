from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass(frozen=True)
class ObjectCard:
    """Trusted or candidate description for an object/facility/marker."""

    object_type: str
    tags: List[str]
    possible_states: List[str]
    change_types: List[str]
    notes: List[str] = field(default_factory=list)
    trust_level: str = "unverified"
    sources: List[Dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class ObservationSignal:
    """Raw signal from OCR/vision/web/API. Not a fact."""

    signal_type: str
    payload: Dict[str, Any]
    provider: str
    ts: float


@dataclass(frozen=True)
class ChangeDemand:
    """System demand for a change type, created by Task/Risk."""

    demand_type: str
    priority: int
    constraints: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ObservationCandidate:
    """Candidate observation plan derived from ChangeDemand and ObjectCard."""

    candidate_id: str
    demand: ChangeDemand
    object_type: str
    strategy_hint: Dict[str, Any]
    confidence: float
    evidence: List[Dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class InterpretationExperienceCard:
    roi_kind: str
    category: str
    meaning: str
    stability: float
    confidence: float
    environment_id: str
    scope: str
    source: str
    evidence: Dict[str, Any]
    version: int
