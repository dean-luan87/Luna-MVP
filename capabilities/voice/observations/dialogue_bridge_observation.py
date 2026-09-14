# -*- coding: utf-8 -*-
"""
DialogueBridgeObservation (Stage-1 placeholder).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class DialogueBridgeObservation:
    observation_id: str
    timestamp: float
    source_event_id: str
    route: str
    decision: str
    reason: str
    metadata: Dict[str, Any] = field(default_factory=dict)

