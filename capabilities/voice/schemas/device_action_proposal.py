# -*- coding: utf-8 -*-
"""
DeviceActionProposal (Stage-1 placeholder).

Voice -> Core proposal：表达设备动作候选，不可直接执行。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class DeviceActionProposal:
    proposal_id: str
    source_event_id: str
    device_action: str
    confidence: float
    needs_confirmation: bool = True
    restricted_mode_required: bool = False
    rationale: Optional[str] = None
    trace_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

