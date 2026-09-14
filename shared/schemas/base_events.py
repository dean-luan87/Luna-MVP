# -*- coding: utf-8 -*-
"""
Shared schema primitives (Stage-0 placeholder).

目的：提供跨 capability 的最小事件基类/字段约束。
注意：仅占位，不绑定任何 provider，不引入运行时行为。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class BaseEvent:
    event_id: str
    timestamp: float
    source: str
    provider_name: str
    model_name: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class BaseContextRef:
    task_context_id: Optional[str] = None
    session_id: Optional[str] = None

