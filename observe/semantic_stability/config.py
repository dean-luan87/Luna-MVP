from __future__ import annotations

from dataclasses import dataclass


@dataclass
class StabilityConfig:
    alpha: float = 1.0
    beta: float = 3.0
    half_life_s: float = 7 * 24 * 3600
    min_appear_for_observe: int = 3
    promote_threshold: float = 0.75
    observe_threshold: float = 0.55
    confidence_cap_count: int = 20
