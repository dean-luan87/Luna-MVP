"""
Expression Calibrator (C-2.5)

用什么认知协议说（专业/口语/共识词/引导）
"""

from .protocol import ExpressionProtocol
from .calibrator_models import CalibratorInput, CalibratorOutput
from .calibrator_engine import CalibratorEngine
from .hooks_emotion_engine import EmotionEngineHooks

__all__ = [
    "ExpressionProtocol",
    "CalibratorInput",
    "CalibratorOutput",
    "CalibratorEngine",
    "EmotionEngineHooks",
]
