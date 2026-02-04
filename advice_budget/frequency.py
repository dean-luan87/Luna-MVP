from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FrequencyPolicy:
    cooldown_s: float
    quota_per_min: int


@dataclass
class FrequencyState:
    last_emit_ts: float = 0.0
    window_start_ts: float = 0.0
    used_in_window: int = 0
