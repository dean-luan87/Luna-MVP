# -*- coding: utf-8 -*-
"""
ProviderFallbackObservation (Stage-2).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class ProviderFallbackObservation:
    request_id: str
    timestamp: float
    primary_provider: str
    fallback_provider: str
    fallback_reason: str
    failure_type: str
    final_provider_used: Optional[str] = None
    latency_ms: Optional[int] = None
    output_valid: Optional[bool] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

