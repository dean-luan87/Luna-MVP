from __future__ import annotations

from typing import List

from roi_learning_c1.schema import ROIPromotionProposal
from roi_confirmation_c2.policy import AutoConfirmPolicy
from roi_confirmation_c2.confirmer import ROIConfirmer
from roi_confirmation_c2.registry import ROIDefaultRegistry


def run_c2_confirm(
    proposals: List[ROIPromotionProposal],
    registry: ROIDefaultRegistry,
    version: str = "c2-v0",
):
    policy = AutoConfirmPolicy()
    confirmer = ROIConfirmer(policy)

    entries = confirmer.confirm(proposals, version=version)
    for e in entries:
        registry.upsert(e)

    return entries
