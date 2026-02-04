"""
TTS System - 文本转语音系统模块

提供统一的 TTS 抽象层，支持多种输出通道。
"""

from .utterance import Utterance
from .tts_manager import TtsManager, tts_manager
from .runtime_driver import TTSRuntimeDriver
from .tts_policy import (
    TTSCategory,
    TTSPolicy,
    TTS_POLICY_TABLE,
    get_policy,
    make_utterance,
    apply_policy_to_utterance,
)
from .tts_shortcuts import (
    speak_safety,
    speak_navigation,
    speak_system,
    speak_task,
    speak_chat,
)
from .router_facade import TTSRouterFacade, get_tts_router_facade
from .priority_bands import PriorityBand
from .priority_scheduler import PriorityScheduler

__all__ = [
    "Utterance",
    "TtsManager",
    "tts_manager",
    "TTSRuntimeDriver",
    "TTSCategory",
    "TTSPolicy",
    "TTS_POLICY_TABLE",
    "get_policy",
    "make_utterance",
    "apply_policy_to_utterance",
    "speak_safety",
    "speak_navigation",
    "speak_system",
    "speak_task",
    "speak_chat",
    "TTSRouterFacade",
    "get_tts_router_facade",
    "PriorityBand",
    "PriorityScheduler",
]

