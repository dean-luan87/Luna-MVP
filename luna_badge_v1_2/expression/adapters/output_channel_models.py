"""
Output Channel Models (C-4)

输出通道模型
"""

from enum import Enum


class OutputChannel(Enum):
    """
    OutputChannel Enum
    
    输出通道类型：
    - DEBUG: 调试输出
    - VOICE_TEXT: 语音文本（一期先做文本输出）
    - （预留）HAPTIC: 触觉反馈
    """
    DEBUG = "debug"
    VOICE_TEXT = "voice_text"
    # HAPTIC = "haptic"  # 预留
