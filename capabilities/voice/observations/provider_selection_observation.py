# -*- coding: utf-8 -*-
"""
ProviderSelectionObservation (Stage-2).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass(frozen=True)
class ProviderSelectionObservation:
    request_id: str
    timestamp: float
    chosen_provider: str
    preset_name: str
    provider_order: List[str]
    selection_reason: str
    metadata: Dict[str, Any] = field(default_factory=dict)

