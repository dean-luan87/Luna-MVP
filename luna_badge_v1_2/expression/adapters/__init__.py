"""
Expression Adapters (C-4)

输出通道映射（voice/haptic/debug），一期先做 debug/voice_text 文本输出即可
"""

from .output_channel_models import OutputChannel
from .output_router import OutputRouter

__all__ = [
    "OutputChannel",
    "OutputRouter",
]
