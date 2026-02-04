from __future__ import annotations

from typing import List

from observe.semantic_stability.types import StableInterpretationProfile
from dynamic_view.attention_preferences import AttentionPreference


def stability_to_attention_preferences(
    profiles: List[StableInterpretationProfile],
) -> List[AttentionPreference]:
    prefs: List[AttentionPreference] = []

    for p in profiles:
        if p.suggestion not in ("OBSERVE", "PROMOTE"):
            continue

        base = 0.6 if p.suggestion == "OBSERVE" else 0.85
        weight = base * p.score.stability * p.score.confidence

        prefs.append(
            AttentionPreference(
                roi_kind=p.key.roi_kind,
                weight=min(1.0, weight),
                source="learned_c3_1",
                environment_id=p.environment_id,
            )
        )

    return prefs
