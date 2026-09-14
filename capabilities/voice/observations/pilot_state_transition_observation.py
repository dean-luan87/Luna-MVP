# -*- coding: utf-8 -*-
"""
PilotStateTransitionObservation (V1)

用于记录试点“状态切换发生过”这一运行态治理事实，供聚合工具直接统计：
- level2b_to_level2a
- level2a_to_level1
- any_to_level0
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class PilotStateTransitionObservation:
    timestamp: float
    transition: str
    reason: str
    related_request_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

