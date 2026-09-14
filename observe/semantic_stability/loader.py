from __future__ import annotations

import json
from typing import List

from .types import (
    InterpretationKey,
    StabilityScore,
    StableInterpretationProfile,
)


def load_profiles(path: str) -> List[StableInterpretationProfile]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    profiles: List[StableInterpretationProfile] = []
    for item in data:
        key = InterpretationKey(
            roi_kind=item["roi_kind"],
            category=item["category"],
            meaning=item["meaning"],
        )
        score = StabilityScore(
            stability=float(item.get("stability") or 0.0),
            confidence=float(item.get("confidence") or 0.0),
            evidence=item.get("evidence") or {},
        )
        profiles.append(
            StableInterpretationProfile(
                key=key,
                score=score,
                suggestion=item.get("suggestion") or "IGNORE",
                scope=item.get("scope") or "device_local",
                environment_id=item.get("environment_id") or "device_default",
            )
        )

    return profiles
