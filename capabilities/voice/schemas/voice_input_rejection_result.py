# -*- coding: utf-8 -*-
"""
VoiceInputRejectionResult：输入被拒时的轻量可追踪对象（白盒/观测用）。

不等价于裁决；仅表示 Voice 输入层未进入受控 proposal/query 路径。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class VoiceInputRejectionResult:
    request_id: str
    reason: str
    router_stage: str  # 如 voice_input | voice_input_bridge
    raw_text: Optional[str]
    normalized_text: Optional[str]
    is_task_mode: bool
    source_type: str
    reason_code: str = ""
