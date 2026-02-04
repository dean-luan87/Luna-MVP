# -*- coding: utf-8 -*-
from typing import Dict
from .types import PendingBelief, Belief


class C3Store:
    def __init__(self):
        self.pending: Dict[str, PendingBelief] = {}
        self.beliefs: Dict[str, Belief] = {}

    def upsert_pending(self, pb: PendingBelief) -> None:
        self.pending[pb.belief_id] = pb

    def promote(self, belief: Belief) -> None:
        self.beliefs[belief.belief_id] = belief
        self.pending.pop(belief.belief_id, None)
