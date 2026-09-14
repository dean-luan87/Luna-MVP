from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AdviceCandidate:
    kind: str
    is_safety: bool
    value: float
    source: str


@dataclass
class AdviceDecision:
    allow: bool
    urgency: str
    cooldown_s: float
    reason: str
