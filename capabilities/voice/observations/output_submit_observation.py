# -*- coding: utf-8 -*-
"""
OutputSubmitObservation (Stage-2.2 minimal).

用于证明：SpeechRequest 已被输出平面 submit 调用。
不代表已开始播放（speaking/runtime 另行建设）。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(frozen=True)
class OutputSubmitObservation:
    request_id: str
    timestamp: float
    accepted: bool
    reason: str
    output_plane: str = "voice_output_plane_v1"
    metadata: Dict[str, Any] = field(default_factory=dict)

