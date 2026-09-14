# -*- coding: utf-8 -*-
"""
TaskActionProposal (Stage-1 placeholder).

Voice -> Core proposal：表达任务生命周期动作候选，不可直接执行。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class TaskActionProposal:
    proposal_id: str
    source_event_id: str
    task_action: str
    confidence: float
    needs_confirmation: bool = True
    may_change_task_state: bool = True
    rationale: Optional[str] = None
    task_context_id: Optional[str] = None
    task_chain_id: Optional[str] = None
    trace_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

