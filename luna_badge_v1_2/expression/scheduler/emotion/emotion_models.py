"""
Emotion Models

情感模型（二期接口）

NON-NEGOTIABLE CORE RULE:

Vision is the primary clock of the system.

- Visual rhythm defines all timing decisions.
- Emotion can modulate, but never override.
- GPS is verification-only.
- Speech follows vision, never leads it.

Emotion Engine has NO authority over:
- delay time
- scheduling order
- interruption
- output triggering

⚠️ 任何实现不得违反以上规则，否则视为错误实现。
"""

from dataclasses import dataclass
from typing import Literal


@dataclass
class EmotionModulation:
    """
    情感调制（二期唯一允许输出的结构）
    
    禁止扩展字段：
    - delay / delay_ms
    - priority
    - interrupt
    - enqueue
    - schedule_hint
    
    情感只能调制，不能覆盖视觉节奏。
    """
    emotional_state: Literal[
        "CALM",
        "FOCUSED",
        "ANXIOUS",
        "CONFUSED",
        "REASSURED",
        "URGENT"
    ]
    
    tempo_bias: Literal[
        "SLOWER",
        "NEUTRAL",
        "FASTER"
    ]
    
    verbosity_bias: Literal[
        "LESS",
        "NORMAL",
        "MORE"
    ]
    
    language_style: Literal[
        "PLAIN",
        "SOFT",
        "FIRM",
        "ENCOURAGING"
    ]
    
    confidence: float  # 0.0 ~ 1.0
