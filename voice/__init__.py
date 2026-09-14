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

try:
    from .priority_manager import VoicePriorityManager, voice_priority_manager, VoiceType
    from .priority_manager import speak_navigation, speak_object_detection, speak_system, speak_custom
except ImportError:
    VoicePriorityManager = None
    voice_priority_manager = None
    VoiceType = None
    speak_navigation = None
    speak_object_detection = None
    speak_system = None
    speak_custom = None

try:
    from .speech_scheduler import SpeechScheduler, SpeechPriority, speech_scheduler
    from .speech_scheduler import speak_visual, speak_navigation as scheduler_navigation, speak_other
    from .speech_scheduler import interrupt_for_voice_input, resume_after_voice_input
except ImportError:
    SpeechScheduler = None
    SpeechPriority = None
    speech_scheduler = None
    speak_visual = None
    scheduler_navigation = None
    speak_other = None
    interrupt_for_voice_input = None
    resume_after_voice_input = None

__all__ = [
    'TTSEngine',
    'Speaker',
    'VoicePriorityManager',
    'voice_priority_manager',
    'VoiceType',
    'speak_navigation',
    'speak_object_detection',
    'speak_system',
    'speak_custom',
    'SpeechScheduler',
    'SpeechPriority',
    'speech_scheduler',
    'speak_visual',
    'scheduler_navigation',
    'speak_other',
    'interrupt_for_voice_input',
    'resume_after_voice_input',
    'get_tts_engine',
    'get_speaker'
]