"""
C-5 Types

C-5 表达调度（一期收敛版）内部数据结构

NON-NEGOTIABLE RULES:

1. Vision is the only rhythm authority.
2. Expression must follow vision, never lead it.
3. GPS never affects expression timing.
4. No expression is emitted during visual TURNING unless critical.
5. This is a frozen v1.4.8 implementation. Do NOT extend features.
"""

from dataclasses import dataclass
from typing import Literal, Optional


VisionState = Literal[
    "STABLE",
    "LOCKED",
    "SEARCHING",
    "TURNING",
    "UNSTABLE"
]


@dataclass
class VisionRhythmContext:
    """
    视角节奏上下文
    
    所有节奏判断必须基于此。
    GPS 信息不得出现在节奏计算中。
    """
    vision_state: VisionState
    speed_mps: float
    last_vision_ts: float


@dataclass
class ExpressionCandidate:
    """
    表达式候选
    
    用于 C-5 调度的最小数据结构
    """
    contract_id: str
    urgency: Literal["high", "normal", "low"]
    is_critical: bool
    duplicate_key: Optional[str] = None
