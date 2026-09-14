"""Memory retention hints derived from Self Rhythm without controlling Runtime."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MemoryBudgetHint:
    mode: str
    max_candidates: int
    retain_high_value_only: bool
    reason: str


class RhythmMemoryPolicy:
    def from_mode(self, mode: str) -> MemoryBudgetHint:
        profiles = {
            "active": (32, False),
            "focus": (48, False),
            "observe": (8, True),
            "maintain": (16, True),
            "recovery": (4, True),
            "low_power": (2, True),
        }
        if mode not in profiles:
            raise ValueError(f"unsupported rhythm mode: {mode}")
        limit, high_value = profiles[mode]
        return MemoryBudgetHint(mode, limit, high_value, "Self Rhythm advisory retention budget")
