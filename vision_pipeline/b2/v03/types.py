# vision_pipeline/b2/v03/types.py

"""
NOTE:
B2 v0.4+ 不再输出 WORLD / SCENE 级别语义
所有世界信息仅作为 evidence，不得升级为 decision
- WORLD 级别已被废弃（deprecated）
- ENV 因子只能进入 reasons / evidence，不得参与 level 判定
- 所有 decision 必须基于"是否影响 C 的行为"
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, Any, List
import time


class WorldChangeLevel(Enum):
    """
    世界变化等级（B2 v0.3 的最高输出）
    """
    NONE = auto()          # 无显著变化
    LOCAL = auto()         # 局部属性变化（路面、人群）
    # WORLD = auto()       # ❌ deprecated: 世界性质变化不符合 DTL 设计，禁止使用
    EVENT = auto()         # 突发事件（高优先级）


@dataclass
class WorldState:
    """
    B2 对"当前世界"的理解
    """
    world_id: str
    scene: str
    space_id: str
    ts: float = field(default_factory=lambda: time.time())


@dataclass
class WorldChange:
    """
    B2 v0.3 的最终产物（给 C 用，但不是指令）
    """
    level: WorldChangeLevel
    confidence: float

    # 变化原因（来自哪些因子）
    factors: Dict[str, Any]

    # 是否需要立刻打断 C
    interrupt: bool = False

    # 调试 / 记录
    ts: float = field(default_factory=lambda: time.time())
