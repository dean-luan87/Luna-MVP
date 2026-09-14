# -*- coding: utf-8 -*-
"""
TaskContextQuery (Stage-1 placeholder).

Voice -> Core query：请求补全/澄清任务上下文（不带执行权）。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class TaskContextQuery:
    query_id: str
    source_event_id: str
    query_type: str
    query_text: str
    task_context_id: Optional[str] = None
    task_chain_id: Optional[str] = None
    trace_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

