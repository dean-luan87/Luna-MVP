from __future__ import annotations

from typing import Optional

from .types import InterpretationStats, StabilityScore
from .config import StabilityConfig


def _decay_factor(now_ts: float, last_seen_ts: Optional[float], half_life_s: float) -> float:
    if last_seen_ts is None:
        return 1.0
    dt = max(0.0, now_ts - last_seen_ts)
    if half_life_s <= 0:
        return 1.0
    return 0.5 ** (dt / half_life_s)


def compute_stability_score(
    stats: InterpretationStats,
    cfg: StabilityConfig,
    now_ts: float,
) -> StabilityScore:
    base = (stats.confirm_count + cfg.alpha) / (stats.appear_count + cfg.beta)
    penalty = 1.0 / (1.0 + stats.contradict_count)
    decay = _decay_factor(now_ts, stats.last_seen_ts, cfg.half_life_s)

    stability = max(0.0, min(1.0, base * penalty * decay))

    cap = max(1, cfg.confidence_cap_count)
    confidence = max(0.0, min(1.0, stats.appear_count / cap))

    return StabilityScore(
        stability=stability,
        confidence=confidence,
        evidence={
            "appear_count": stats.appear_count,
            "confirm_count": stats.confirm_count,
            "contradict_count": stats.contradict_count,
            "base": base,
            "penalty": penalty,
            "decay": decay,
            "last_seen_ts": stats.last_seen_ts,
        },
    )
