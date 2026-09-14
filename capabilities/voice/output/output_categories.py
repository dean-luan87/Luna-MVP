# -*- coding: utf-8 -*-
"""
Output categories (Stage-1 placeholder).
"""

from __future__ import annotations

from enum import Enum


class OutputCategory(str, Enum):
    SAFETY = "safety"
    TASK_PROGRESS = "task_progress"
    INTERACTION_RESULT = "interaction_result"
    DEVICE_STATUS = "device_status"
    PROACTIVE_COMMUNICATION = "proactive_communication"
    RESERVED_DIALOGUE = "reserved_dialogue"

