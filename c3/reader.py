# -*- coding: utf-8 -*-
from typing import List, Dict
from .store import C3Store


class C3Reader:
    def __init__(self, store: C3Store):
        self.store = store

    def hints(self, *, safety: str) -> List[Dict]:
        return [
            {
                "belief_id": b.belief_id,
                "confidence": b.confidence,
                "applicable_env": b.env_tag.safety,
            }
            for b in self.store.beliefs.values()
            if b.env_tag.safety == safety
        ]
