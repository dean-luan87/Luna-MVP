# -*- coding: utf-8 -*-
"""
v1.8.5 Phase D Lite: Emotion Module（情绪模块）

职责：
- 定义情绪信号的数据结构
- 提供情绪信号入口（占位接口）
- 必须继承 Phase B/C 的护栏

设计原则：
- 情绪信号 → EmotionalContext → ContextBundle → TaskPlanner（软影响）
- 绝对禁止：EmotionalSignal → SceneRegistry/MapRegistry/LibraryRegistry
- 只允许：情绪 → 体验记忆（低权重、快衰减）
"""

from .emotional_signal import EmotionalSignal
from .emotional_context import EmotionalContext
from .emotion_port import EmotionPort

__all__ = [
    "EmotionalSignal",
    "EmotionalContext",
    "EmotionPort",
]


