from typing import List

from .threshold_metrics import ThresholdMetrics
from .threshold_store import ThresholdVersion


class ThresholdProposer:
    def propose(
        self,
        base_version: ThresholdVersion,
        metrics: ThresholdMetrics,
    ) -> List[ThresholdVersion]:
        """Reserved for future evolution algorithms (e.g., ant/mold-inspired)."""
        return []
