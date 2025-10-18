#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Voice 模块
语音合成和播报功能
"""

__version__ = "1.0.0"
__author__ = "Luna Team"

# 延迟导入，避免依赖问题
def get_tts_engine():
    """获取语音合成引擎"""
    from .tts_engine import TTSEngine
    return TTSEngine

def get_speaker():
    """获取语音播报器"""
    from .speaker import Speaker
    return Speaker

# 直接导入基础模块（无额外依赖）
try:
    from .tts_engine import TTSEngine
except ImportError:
    TTSEngine = None

try:
    from .speaker import Speaker
except ImportError:
    Speaker = None

__all__ = [
    'TTSEngine',
    'Speaker',
    'get_tts_engine',
    'get_speaker'
]