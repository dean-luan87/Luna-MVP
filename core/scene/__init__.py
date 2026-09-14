# -*- coding: utf-8 -*-
"""
v1.8.5: Scene Modeling Layer（场景建模层）

职责：
- 从记忆系统中抽离"世界 / 场景"这一维度
- 构建一个可被多中台共用的场景建模层
- 支撑风险告知、视角导航、情绪计算与任务链
- 但不直接参与中台决策与执行

原则：
- Scene 只提供事实，中台自己判断
- 防止 Scene 层被滥用成"隐形决策层"
"""

from .schema import (
    SceneState,
    StaticScene,
    StaticStructure,
    DynamicScene,
    SceneMemory,
)
from .scene_segment import SceneSegment, SceneAnchors
from .scene_inputs import SceneInputs
from .environment_context import EnvironmentContext
from .scene_registry import SceneRegistry
from .scene_read_adapter import (
    get_scene_for_risk,
    get_scene_for_task,
    get_scene_for_emotion,
)

__all__ = [
    "SceneState",
    "StaticScene",
    "StaticStructure",
    "DynamicScene",
    "SceneMemory",
    "SceneSegment",
    "SceneAnchors",
    "SceneInputs",
    "EnvironmentContext",
    "SceneRegistry",
    "get_scene_for_risk",
    "get_scene_for_task",
    "get_scene_for_emotion",
]

