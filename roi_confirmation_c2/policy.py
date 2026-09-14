from __future__ import annotations

from roi_learning_c1.schema import ROIPromotionProposal


class AutoConfirmPolicy:
    """
    v0：简单阈值策略
    """

    def __init__(self, min_score=0.65, min_confidence=0.7):
        self.min_score = min_score
        self.min_confidence = min_confidence

    def should_auto_confirm(self, proposal: ROIPromotionProposal) -> bool:
        return (
            proposal.suggestion == "PROMOTE_TO_DEFAULT"
            and proposal.score >= self.min_score
            and proposal.confidence >= self.min_confidence
        )
