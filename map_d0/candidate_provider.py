from __future__ import annotations

from typing import List

from common.change_demand import ChangeDemand
from map_d0.types import MapCandidate, MapContext
from map_d0.rules import candidates_from_change_demand


class MapCandidateProvider:
    """
    只读 Provider：
    ChangeDemand -> MapCandidate
    """

    def __init__(self, context: MapContext | None = None):
        self.context = context or MapContext()

    def propose(self, demands: List[ChangeDemand]) -> List[MapCandidate]:
        candidates: List[MapCandidate] = []
        for d in demands:
            candidates.extend(candidates_from_change_demand(d))
        return candidates
