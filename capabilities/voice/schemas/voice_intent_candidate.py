# -*- coding: utf-8 -*-
"""
VoiceIntentCandidate (Stage-1 placeholder).

说明：
- 只表达轻意图候选，不做宽推理，不做裁决。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class VoiceIntentCandidate:
    candidate_id: str
    source_event_id: str
    intent_type: str
    intent_action: str
    confidence: float
    ambiguity_level: str = "unknown"
    needs_confirmation: bool = False
    may_change_task_state: bool = False
    may_change_system_state: bool = False
    conflict_detected: bool = False
    notes: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

