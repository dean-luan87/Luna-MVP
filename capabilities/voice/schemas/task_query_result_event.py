# -*- coding: utf-8 -*-
"""
TaskQueryResultEvent (Stage-1 placeholder).

Core -> Voice：对 Voice 发起的 TaskContextQuery 的结果事件。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class TaskQueryResultEvent:
    event_id: str
    timestamp: float
    query_id: str
    ok: bool
    result_text: Optional[str] = None
    task_context_id: Optional[str] = None
    task_chain_id: Optional[str] = None
    trace_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

