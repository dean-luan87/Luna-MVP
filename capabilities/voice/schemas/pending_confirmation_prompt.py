# -*- coding: utf-8 -*-
"""
PendingConfirmationPrompt (Stage-1 placeholder).

Core -> Voice：系统发起的待确认提示（用于确认后执行）。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class PendingConfirmationPrompt:
    confirmation_id: str
    timestamp: float
    confirmation_type: str
    prompt_text: str
    task_context_id: Optional[str] = None
    task_chain_id: Optional[str] = None
    trace_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

