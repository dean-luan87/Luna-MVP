# -*- coding: utf-8 -*-
"""
VisionEvent: capability-agnostic vision event schema (Stage-0).

要求：
- OCR / detection / tracking 等可共用同一基础事件风格
- 不同视觉模型差异必须压在 adapter/provider 层
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Union


@dataclass(frozen=True)
class VisionEvent:
    event_id: str
    timestamp: float
    source: str
    provider_name: str
    model_name: str
    event_type: str
    confidence: Optional[float] = None
    frame_id: Optional[Union[str, int]] = None
    task_context_id: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

