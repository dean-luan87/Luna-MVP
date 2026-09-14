# -*- coding: utf-8 -*-
"""
PlaybackRuntimeObservation (Stage-2.3).

playback/speaking 真源事件（V1）：
- 必须绑定 request_id
- 必须来自 playback/result 执行层观测点（本 repo 先以最小 playback 执行器作为执行层锚点）
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(frozen=True)
class PlaybackRuntimeObservation:
    request_id: str
    timestamp: float
    event: str  # playback_started | playback_finished | playback_failed | playback_cancelled
    status: str = "ok"  # ok | fail | cancelled
    reason: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

