# -*- coding: utf-8 -*-
"""
v1.8.5: Scene Modeling（场景建模）

职责：
- Scene Segment 的定义与管理
- SceneRegistry 状态机（渐变切换、抗污染）
- Position Stability Gate（抗抖动）

原则：
- Scene 的最小单位 = "人在其中不需要重新判断行为规则的空间语义段"
- 不瞬时切换、不直接覆盖、不立即删除
"""

# v1.8.5: 新的 SceneRegistry 实现
from .scene_registry import SceneRegistry, SceneState, SceneCandidate, PendingScene

__all__ = [
    "SceneRegistry",
    "SceneState",
    "SceneCandidate",
    "PendingScene",
]

