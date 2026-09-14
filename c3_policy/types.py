from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class ObservationRule:
    roi_kind: str
    priority: int
    ttl_s: Optional[int] = None
    source: str = "c3"
    conditions: Dict = field(default_factory=dict)


@dataclass
class ObservationPolicy:
    policy_id: str
    version: int
    generated_at: float
    environment: str
    rules: List[ObservationRule]
    evidence: Dict = field(default_factory=dict)
