# -*- coding: utf-8 -*-
"""
TTSRollbackObservation (Stage-2.1).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(frozen=True)
class TTSRollbackObservation:
    request_id: str
    timestamp: float
    rollback_trigger: str  # selector_failure | provider_chain_failure | invalid_audio_chain | timeout_chain
    rollback_reason: str
    provider_chain_status: str
    final_execution_mode: str  # provider_chain | legacy_fallback | failed_no_output
    metadata: Dict[str, Any] = field(default_factory=dict)

