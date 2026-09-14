# -*- coding: utf-8 -*-
"""
DeviceStatusFeedbackEvent (Stage-1 placeholder).

Core/Device layer -> Voice：设备状态反馈事件（电量/网络/传感器/受限模式等）。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class DeviceStatusFeedbackEvent:
    event_id: str
    timestamp: float
    status_type: str
    status_text: str
    restricted_device_mode: bool = False
    session_id: Optional[str] = None
    trace_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

