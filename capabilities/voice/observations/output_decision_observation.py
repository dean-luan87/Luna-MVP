# -*- coding: utf-8 -*-
"""
OutputDecisionObservation (Stage-1 placeholder).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class OutputDecisionObservation:
    observation_id: str
    timestamp: float
    request_id: str
    accepted: bool
    reason: str
    cooldown_key: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

