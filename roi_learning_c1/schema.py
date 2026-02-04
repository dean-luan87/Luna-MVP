from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Literal


Suggestion = Literal["PROMOTE_TO_DEFAULT", "OBSERVE", "IGNORE"]


@dataclass(frozen=True)
class ROIPromotionProposal:
    roi_kind: str
    evidence: Dict[str, Any]
    score: float
    suggestion: Suggestion
    confidence: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
