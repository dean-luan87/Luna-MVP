from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class AdviceFeedback:
    kind: str
    source: str
    accepted: bool
    latency_s: Optional[float]
    context_hash: Optional[str]
