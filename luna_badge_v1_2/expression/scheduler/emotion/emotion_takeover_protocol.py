"""
Emotion Takeover Protocol (ETP v0.1)

情感接管协议（主权控制层）

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

📌 注意：
不存在 FULL / OVERRIDE 等级，这是硬约束。
"""

from enum import Enum
from typing import Literal


class EmotionTakeoverLevel(Enum):
    """
    情感接管等级
    
    注意：不存在 FULL / OVERRIDE 等级
    这是硬约束：情感永远不能完全接管
    """
    IGNORE = 0  # 忽略情感，纯视觉模式
    WEAK = 1    # 弱调制
    STRONG = 2  # 强调制（但仍受视觉约束）


def decide_takeover_level(
    vision_state: str,
    emotion_confidence: float,
) -> EmotionTakeoverLevel:
    """
    决定情感接管等级
    
    规则：
    - 视觉不稳定（TURNING, SEARCHING, UNSTABLE）→ 忽略情感
    - 情感置信度 < 0.6 → 忽略情感
    - 情感置信度 < 0.85 → 弱调制
    - 情感置信度 >= 0.85 → 强调制（但仍受视觉约束）
    
    Args:
        vision_state: 视觉状态
        emotion_confidence: 情感置信度
        
    Returns:
        EmotionTakeoverLevel: 接管等级
    """
    # 视觉不稳定时，忽略所有情感
    if vision_state in ("TURNING", "SEARCHING", "UNSTABLE"):
        return EmotionTakeoverLevel.IGNORE
    
    # 情感置信度太低，忽略
    if emotion_confidence < 0.6:
        return EmotionTakeoverLevel.IGNORE
    
    # 情感置信度中等，弱调制
    if emotion_confidence < 0.85:
        return EmotionTakeoverLevel.WEAK
    
    # 情感置信度高，强调制（但仍受视觉约束）
    return EmotionTakeoverLevel.STRONG
