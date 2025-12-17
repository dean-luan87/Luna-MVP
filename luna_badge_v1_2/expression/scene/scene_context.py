"""
Scene Context (C-2.2)

场景上下文
"""

from dataclasses import dataclass
from .scene_types import SceneType


@dataclass
class SceneContext:
    """
    SceneContext 数据类
    
    场景上下文：
    - scene: 场景类型
    - confidence: 置信度 0~1
    - source: 数据源（"vision" / "fsm" / "system"）
    """
    scene: SceneType
    confidence: float
    source: str   # "vision" / "fsm" / "system"
