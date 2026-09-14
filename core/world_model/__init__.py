# -*- coding: utf-8 -*-
"""
v1.8.5: World Model（世界模型）

职责：
- 提供统一的世界模型后端骨架（Scene / Memory / Library / Map）
- 防污染、可追责、可长期演化

核心模块：
- SceneRegistry：场景锚点 + 渐变切换 + 稳定闸门
- MemoryRegistry：体验资产 + 事实候选池
- FactCandidatePool：事实候选池（承接 Memory → 候选事实）
- LibraryRegistry：慢确认事实 + 知识唤醒
- MapRegistry：从 Memory / Library 提取权重，生成可用 map bias

统一 Registry 协作接口（为后续中台/任务链用）：
- 所有 Registry 都遵循"只读原则"（MapRegistry 只读 Memory / Library）
- 所有 Registry 都遵循"稳定闸门"（位置不稳定时不写）
- 所有 Registry 都遵循"防污染铁律"（慢确认、可追责）
"""

from core.world_model.common import WorldModelDB, PositionState, EnvironmentContext
from core.world_model.scene import SceneRegistry, SceneState, SceneCandidate
from core.world_model.memory import MemoryRegistry, FactCandidatePool, FactCandidate, ExperienceMemory
from core.world_model.library import LibraryRegistry, LibraryHint
from core.world_model.map import MapRegistry, MapHint

__all__ = [
    # Common
    "WorldModelDB",
    "PositionState",
    "EnvironmentContext",
    # Scene
    "SceneRegistry",
    "SceneState",
    "SceneCandidate",
    # Memory
    "MemoryRegistry",
    "FactCandidatePool",
    "FactCandidate",
    "ExperienceMemory",
    # Library
    "LibraryRegistry",
    "LibraryHint",
    # Map
    "MapRegistry",
    "MapHint",
]
