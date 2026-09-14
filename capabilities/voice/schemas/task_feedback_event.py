# -*- coding: utf-8 -*-
"""
TaskFeedbackEvent (Stage-1 placeholder).

Core/TaskChain -> Voice：任务执行反馈事件（用于受控交互与主动沟通决策输入）。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class TaskFeedbackEvent:
    event_id: str
    timestamp: float
    task_context_id: Optional[str] = None
    task_chain_id: Optional[str] = None
    task_phase: Optional[str] = None
    feedback_type: str = ""
    feedback_text: Optional[str] = None
    trace_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

