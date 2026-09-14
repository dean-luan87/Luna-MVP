# -*- coding: utf-8 -*-
"""
BridgeDecision (Stage-1 placeholder).

用于记录 Bridge 路由与执行权限建议（不等于裁决）。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from capabilities.voice.bridge.route_types import BridgeRouteType


@dataclass(frozen=True)
class BridgeDecision:
    decision_id: str
    source_event_id: str
    route: BridgeRouteType
    execution_class: str  # "direct" | "confirm_then_execute" | "reject_or_degrade"
    reason: str
    proposal: Optional[object] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

