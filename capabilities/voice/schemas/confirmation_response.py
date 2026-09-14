# -*- coding: utf-8 -*-
"""
ConfirmationResponse (Stage-1 placeholder).

Voice -> Core response：对系统待确认项的确认/否认/更正。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class ConfirmationResponse:
    response_id: str
    source_event_id: str
    pending_confirmation_id: str
    response: str  # "yes" | "no" | "repeat" | "correct" | ...
    confidence: float = 1.0
    notes: Optional[str] = None
    trace_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

