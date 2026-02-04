"""
TTS Shortcuts: 标准化封装入口

提供 speak_safety / speak_navigation / speak_task / speak_chat / speak_system
等统一入口，业务模块通过这些入口发声，无需手写 priority / interrupt。
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from .tts_manager import tts_manager
from .tts_policy import TTSCategory, make_utterance
from .utterance import Utterance


def speak_safety(
    text: str,
    *,
    meta: Optional[Dict[str, Any]] = None,
    priority: Optional[int] = None,
    interrupt: Optional[bool] = None,
) -> Utterance:
    """
    安全播报统一入口：
    - 默认高优先级 + interrupt=True
    - 用于障碍物、危险环境、施工等提醒
    """
    utter = make_utterance(
        text,
        TTSCategory.SAFETY,
        meta=meta,
        priority=priority,
        interrupt=interrupt,
    )
    tts_manager.enqueue(utter)
    return utter


def speak_navigation(
    text: str,
    *,
    meta: Optional[Dict[str, Any]] = None,
    priority: Optional[int] = None,
    interrupt: Optional[bool] = None,
) -> Utterance:
    """
    导航播报统一入口：
    - 默认高优先级，但不打断
    - 用于"前方50米左转""已偏航，请调头"等
    """
    utter = make_utterance(
        text,
        TTSCategory.NAVIGATION,
        meta=meta,
        priority=priority,
        interrupt=interrupt,
    )
    tts_manager.enqueue(utter)
    return utter


def speak_system(
    text: str,
    *,
    meta: Optional[Dict[str, Any]] = None,
    priority: Optional[int] = None,
    interrupt: Optional[bool] = None,
) -> Utterance:
    """
    系统播报统一入口：
    - 系统错误、模块异常、不可用提醒
    """
    utter = make_utterance(
        text,
        TTSCategory.SYSTEM,
        meta=meta,
        priority=priority,
        interrupt=interrupt,
    )
    tts_manager.enqueue(utter)
    return utter


def speak_task(
    text: str,
    *,
    meta: Optional[Dict[str, Any]] = None,
    priority: Optional[int] = None,
    interrupt: Optional[bool] = None,
) -> Utterance:
    """
    任务播报统一入口：
    - 任务阶段反馈：如"已为您规划路线""挂号完成"
    """
    utter = make_utterance(
        text,
        TTSCategory.TASK,
        meta=meta,
        priority=priority,
        interrupt=interrupt,
    )
    tts_manager.enqueue(utter)
    return utter


def speak_chat(
    text: str,
    *,
    meta: Optional[Dict[str, Any]] = None,
    priority: Optional[int] = None,
    interrupt: Optional[bool] = None,
) -> Utterance:
    """
    闲聊播报统一入口：
    - 默认低优先级，不打断任何东西
    - 适合陪聊、氛围话术
    """
    utter = make_utterance(
        text,
        TTSCategory.CHAT,
        meta=meta,
        priority=priority,
        interrupt=interrupt,
    )
    tts_manager.enqueue(utter)
    return utter












