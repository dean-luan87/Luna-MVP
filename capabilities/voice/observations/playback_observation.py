# -*- coding: utf-8 -*-
"""
PlaybackObservation (Stage-1 placeholder).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class PlaybackObservation:
    observation_id: str
    timestamp: float
    request_id: str
    started: bool
    finished: Optional[bool] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

