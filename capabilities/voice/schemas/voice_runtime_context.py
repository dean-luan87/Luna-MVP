# -*- coding: utf-8 -*-
"""
VoiceRuntimeContext (Stage-1 placeholder).

Core -> Voice：由 Core 注入当前会话/任务/模式/待确认等上下文。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class VoiceRuntimeContext:
    current_session_id: Optional[str] = None
    current_task_context_id: Optional[str] = None
    current_task_chain_id: Optional[str] = None
    current_task_phase: Optional[str] = None
    current_scene_context_id: Optional[str] = None
    pending_confirmation_id: Optional[str] = None
    pending_confirmation_type: Optional[str] = None
    conversation_window_state: Optional[Dict[str, Any]] = None
    task_shortcut_enabled: bool = False
    restricted_device_mode: bool = False
    output_busy_state: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

