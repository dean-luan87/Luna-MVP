from __future__ import annotations

from typing import Dict, List

from observe.semantic_stability.types import StableInterpretationProfile
from dynamic_view.attention_preferences import AttentionPreference
from dynamic_view.from_semantic_stability import stability_to_attention_preferences


def merge_attention_preferences(
    base_attention: Dict[str, float],
    learned_prefs: List[AttentionPreference],
    *,
    max_boost_ratio: float = 0.5,
    enabled: bool = True,
) -> Dict[str, float]:
    if not enabled:
        return dict(base_attention)

    merged = dict(base_attention)
    for pref in learned_prefs:
        if pref.roi_kind not in merged:
            continue
        base = float(merged[pref.roi_kind])
        boost = min(base * max_boost_ratio, pref.weight)
        merged[pref.roi_kind] = min(1.0, base + boost)
    return merged


def evolve_attention_from_profiles(
    base_attention: Dict[str, float],
    profiles: List[StableInterpretationProfile],
    *,
    enabled: bool = True,
    max_boost_ratio: float = 0.5,
) -> Dict[str, float]:
    learned = stability_to_attention_preferences(profiles)
    return merge_attention_preferences(
        base_attention,
        learned,
        enabled=enabled,
        max_boost_ratio=max_boost_ratio,
    )
