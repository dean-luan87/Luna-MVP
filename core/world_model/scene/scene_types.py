# -*- coding: utf-8 -*-
"""
v1.8.5: Scene Types（场景类型定义）

职责：
- SceneSegment 的数据结构定义
- SceneGeometry 的几何表示（Phase B：简单矩形/圆形占位）

原则：
- geometry 是范围，不是点
- Phase B 先用简单几何，后续可扩展 AREA/POLYLINE
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class SceneGeometry:
    """
    场景几何（Phase B：简单几何占位）
    
    Phase B 阶段：
    - 使用 CIRCLE 或 RECT 作为占位
    - 后续可扩展为 AREA/POLYLINE
    
    注意：geometry 是范围，不是点
    """
    kind: str  # "CIRCLE" | "RECT"
    data: Dict[str, Any]


@dataclass
class SceneSegment:
    """
    场景段（Scene Segment）
    
    Scene 的最小单位定义：
    "人在其中不需要重新判断行为规则的空间语义段"
    
    字段说明：
    - scene_id: 场景唯一标识
    - geometry: 几何范围（AREA 或 POLYLINE，不是点）
    - scene_type: 场景类型（sidewalk / crossing / slope / indoor / open_area）
    - neighbors: 相邻 SceneSegment 的 scene_id 列表
    - env_sensitivity: 环境敏感度标签（low_visibility, rain_sensitive, winter_icy...）
    - risk_profile: 风险标签（water_edge, stairs, crowd...）
    """
    scene_id: str
    geometry: SceneGeometry
    scene_type: str
    neighbors: List[str]
    env_sensitivity: List[str]
    risk_profile: List[str]


