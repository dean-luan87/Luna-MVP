from __future__ import annotations

from typing import Protocol, List

from predictive_attention.context import PalContext
from predictive_attention.schema import PathStackState, AttentionHint


class RoiPredictor(Protocol):
    def propose(self, ctx: PalContext, paths: PathStackState) -> List[AttentionHint]:
        """Return attention hints (ROI) with TTL. Must be ignorable and safe."""
