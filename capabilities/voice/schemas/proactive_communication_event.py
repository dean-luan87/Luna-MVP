# -*- coding: utf-8 -*-
"""
ProactiveCommunicationEvent (Stage-1 placeholder).

Core -> Voice：主动沟通来源事件（风险/任务链节点/设备状态/治理层等）。
注意：这是“受控输出机制”的输入，不得直连 TTS。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class ProactiveCommunicationEvent:
    event_id: str
    timestamp: float
    source: str
    category: str
    message_candidate: str
    priority: int = 0
    task_context_id: Optional[str] = None
    session_id: Optional[str] = None
    trace_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

