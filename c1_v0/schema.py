from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass(frozen=True)
class ROIProposalEvidence:
    appear_count: int
    hit_rate: float
    avg_latency_s: float
    stability: float
    value_hits: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class ROIPromotionProposal:
    roi_kind: str
    evidence: ROIProposalEvidence
    score: float
    suggestion: str
    confidence: float
