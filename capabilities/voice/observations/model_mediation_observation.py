# -*- coding: utf-8 -*-
"""
ModelMediationObservation (Stage-1 placeholder).

用于记录：Luna 原始内容 / 模型候选内容 / 最终输出内容，以及 accept/reject/rewrite。
Stage-1 不接外部模型，只固化观察对象边界。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class ModelMediationObservation:
    observation_id: str
    timestamp: float
    luna_input_ref: str
    model_candidate_ref: Optional[str] = None
    final_output_ref: Optional[str] = None
    decision: str = ""  # accept | reject | rewrite
    reason: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

