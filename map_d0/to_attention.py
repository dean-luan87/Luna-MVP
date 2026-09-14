from __future__ import annotations

from typing import List

from map_d0.types import MapCandidate
from dynamic_view.attention import AttentionWindow


def map_candidates_to_attention(cands: List[MapCandidate]) -> List[AttentionWindow]:
    return [
        AttentionWindow(
            area_type=c.area_type,
            hint=c.hint,
            constraints=c.constraints,
            ttl_frames=30,
            source="map_candidate",
        )
        for c in cands
    ]
