# -*- coding: utf-8 -*-
"""
VoiceInputObservation (Stage-1 placeholder).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class VoiceInputObservation:
    observation_id: str
    timestamp: float
    source_event_id: str
    accepted: bool
    reject_reason: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

