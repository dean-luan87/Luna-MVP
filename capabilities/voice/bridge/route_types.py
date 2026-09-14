# -*- coding: utf-8 -*-
"""
Route types for Dialogue Bridge (Stage-1 placeholder).
"""

from __future__ import annotations

from enum import Enum


class BridgeRouteType(str, Enum):
    DEVICE_CONTROL = "device_control"
    TASK_LIFECYCLE = "task_lifecycle"
    TASK_CONTEXT_ENHANCEMENT = "task_context_enhancement"
    CONFIRMATION = "confirmation"
    FEEDBACK_RESPONSE = "feedback_response"
    RESTRICTED_DEVICE_MODE = "restricted_device_mode"
    RESERVED_OPEN_DIALOGUE = "reserved_open_dialogue"
    # 输入接线 v1：仅唤醒、无任务提案；以及输入被拒（可追踪）
    SESSION_WAKE = "session_wake"
    INPUT_REJECTED = "input_rejected"

