# -*- coding: utf-8 -*-
"""
RequestRuntimeObservation (Stage-2.2).

定义 request 生命周期的“真状态事件”（不等同 speaking/playback 真源）。
用于：
- 串起 request_created/request_submitted/... 的状态事实
- 以 request_id 为主键被抽链器消费
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class RequestRuntimeObservation:
    request_id: str
    timestamp: float
    event: str  # request_created | request_submitted | request_submit_failed | request_submit_rejected | request_terminal_observed
    status: str = "ok"  # ok | fail | rejected
    reason: str = ""
    terminal_mode: Optional[str] = None  # provider_chain | legacy_fallback | failed_no_output | dry_run_ok | unknown
    metadata: Dict[str, Any] = field(default_factory=dict)

