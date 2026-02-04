from __future__ import annotations

from typing import Any, Dict, List

from roi_learning_c1.schema import ROIPromotionProposal
from roi_learning_c1.scorer import score_evidence


def _suggestion(score: float) -> str:
    if score >= 0.65:
        return "PROMOTE_TO_DEFAULT"
    if score >= 0.45:
        return "OBSERVE"
    return "IGNORE"


def _confidence(score: float, appear_count: int) -> float:
    vol = min(1.0, appear_count / 30.0)
    c = 0.15 + 0.7 * score + 0.15 * vol
    return max(0.0, min(0.99, c))


def build_proposals(metrics: Dict[str, Dict[str, Any]]) -> List[ROIPromotionProposal]:
    proposals: List[ROIPromotionProposal] = []
    for roi_kind, e in metrics.items():
        s = score_evidence(e)
        sug = _suggestion(s)
        conf = _confidence(s, int(e.get("appear_count") or 0))
        proposals.append(
            ROIPromotionProposal(
                roi_kind=roi_kind,
                evidence=e,
                score=round(s, 4),
                suggestion=sug,  # type: ignore
                confidence=round(conf, 4),
            )
        )
    proposals.sort(
        key=lambda p: (-p.score, -(p.evidence.get("appear_count") or 0), p.roi_kind)
    )
    return proposals
