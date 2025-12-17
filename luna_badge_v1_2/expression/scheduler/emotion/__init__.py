"""
Emotion Takeover Protocol (ETP v0.1)

情感接管协议
"""

from .emotion_models import EmotionModulation
from .emotion_takeover_protocol import EmotionTakeoverLevel, decide_takeover_level
from .emotion_adapter import EmotionModulationAdapter

__all__ = [
    "EmotionModulation",
    "EmotionTakeoverLevel",
    "decide_takeover_level",
    "EmotionModulationAdapter",
]
