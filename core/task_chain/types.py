# -*- coding: utf-8 -*-
"""
v1.8.5: Task Chain Types（任务链类型定义）

职责：
- 定义任务链消费的统一接口
- ContextBundle：上下文包（Scene / Map / Memory / Risk）
- RiskBias：风险偏置（来自 risk 模块）
- Path：路径选项
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any

from core.world_model.scene import SceneState
from core.world_model.map import MapHint
from core.world_model.memory import ExperienceMemory
from core.world_model.emotion import EmotionalContext


@dataclass
class RiskBias:
    """
    风险偏置（任务链视角）
    
    字段说明：
    - risk_level: 风险等级 [0.0 ~ 1.0]，区域综合风险
    - dominant_type: 主导风险类型（water_edge / stairs / crowd / ...）
    - source: 来源（固定为 "risk_module"）
    
    设计原则：
    - 只读
    - 不可反写
    - 用于评分，不用于播报
    """
    risk_level: float
    dominant_type: Optional[str] = None
    source: str = "risk_module"


@dataclass
class Path:
    """
    路径选项
    
    字段说明：
    - path_id: 路径 ID
    - length: 路径长度（米）
    - description: 路径描述
    """
    path_id: str
    length: float
    description: str = ""


@dataclass
class ContextBundle:
    """
    上下文包（任务链消费的统一接口）
    
    字段说明：
    - scene: 当前场景状态
    - map_hint: 地图提示（客观世界）
    - memory_bias: 体验记忆（主观体验）
    - risk_bias: 风险偏置（NEW：来自 risk 模块）
    """
    scene: Optional[SceneState]
    map_hint: MapHint
    memory_bias: Optional[ExperienceMemory] = None
    risk_bias: Optional[RiskBias] = None
    emotional_context: Optional[EmotionalContext] = None  # Phase D Lite: 情绪上下文（可选）

