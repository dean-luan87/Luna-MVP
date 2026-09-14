from __future__ import annotations

from typing import List

from roi_learning_c1.schema import ROIPromotionProposal
from roi_confirmation_c2.schema import ROIDefaultEntry
from roi_confirmation_c2.policy import AutoConfirmPolicy


class ROIConfirmer:
    def __init__(self, policy: AutoConfirmPolicy):
        self.policy = policy

    def confirm(
        self,
        proposals: List[ROIPromotionProposal],
        version: str,
    ) -> List[ROIDefaultEntry]:
        confirmed = []
        for p in proposals:
            if self.policy.should_auto_confirm(p):
                confirmed.append(
                    ROIDefaultEntry(
                        roi_kind=p.roi_kind,
                        mode="AUTO",
                        version=version,
                        reason={
                            "score": p.score,
                            "confidence": p.confidence,
                            "evidence": p.evidence,
                        },
                    )
                )
        return confirmed
