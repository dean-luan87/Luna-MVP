# -*- coding: utf-8 -*-
"""
TTSCutoverObservation (Stage-2.1).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(frozen=True)
class TTSCutoverObservation:
    request_id: str
    timestamp: float
    cutover_enabled: bool
    cutover_mode: str
    selector_hit: bool
    provider_chain_ok: bool
    final_execution_mode: str  # provider_chain | legacy_fallback | failed_no_output
    final_executor: str
    metadata: Dict[str, Any] = field(default_factory=dict)

