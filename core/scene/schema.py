# -*- coding: utf-8 -*-
"""
v1.8.5: Scene Modeling Layer - Schema（场景建模层数据结构）

职责：
- 定义场景建模层的核心数据结构
- 从记忆系统中抽离"世界 / 场景"这一维度
- 为多中台提供统一的事实层接口

原则：
- 所有字段 Optional（Phase A 阶段数据为空）
- 明确字段来源、生命周期、是否可为空
- 不参与决策，只提供事实
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class StaticStructure:
    """
    静态结构（护栏、台阶、建筑等）
    
    字段说明：
    - type: 结构类型（guardrail / stairs / building / bridge）
    - geometry: 几何类型（POINT / LINE / AREA）
    - confidence: 置信度（0~1）
    
    来源：离线地图 / 视觉识别 / 手动标注
    生命周期：长期不变
    是否可为空：是（Phase A 阶段为空）
    """
    type: Optional[str] = None  # guardrail / stairs / building / bridge
    geometry: Optional[str] = None  # POINT / LINE / AREA
    confidence: Optional[float] = None  # 0~1


@dataclass
class StaticScene:
    """
    静态场景模型（长期不变或变化极慢的现实结构）
    
    字段说明：
    - terrain_type: 地形类型（road / slope / stairs / water）
    - structures: 结构列表（护栏、台阶、建筑等）
    - source: 数据来源（offline_map / vision / manual）
    
    来源：离线地图 / 视觉识别 / 手动标注
    生命周期：长期（可缓存）
    是否可为空：是（Phase A 阶段为空）
    """
    terrain_type: Optional[str] = None  # road / slope / stairs / water
    structures: Optional[List[StaticStructure]] = field(default_factory=list)
    source: Optional[str] = None  # offline_map / vision / manual


@dataclass
class DynamicScene:
    """
    动态场景模型（与时间、事件强相关的变化）
    
    字段说明：
    - traffic_level: 交通水平（low / medium / high）
    - crowd_density: 人群密度（sparse / normal / dense）
    - temporary_events: 临时事件列表（construction / road_block / market）
    - scene_phase: 场景时段（morning_peak / daytime / night）
    - expires_at: 过期时间戳（可选）
    
    来源：实时感知 / 外部数据 / 时间推断
    生命周期：短期（有衰减逻辑）
    是否可为空：是（Phase A 阶段为空）
    """
    traffic_level: Optional[str] = None  # low / medium / high
    crowd_density: Optional[str] = None  # sparse / normal / dense
    temporary_events: Optional[List[str]] = field(default_factory=list)  # construction / road_block / market
    scene_phase: Optional[str] = None  # morning_peak / daytime / night
    expires_at: Optional[float] = None  # 过期时间戳


@dataclass
class SceneMemory:
    """
    场景绑定记忆（"这个场景对我来说意味着什么"）
    
    字段说明：
    - visited_count: 访问次数
    - last_visited: 最后访问时间戳
    - observed_risks: 观察到的风险列表（heavy_traffic / confusing_path）
    - useful_places: 有用地点列表（早餐店、商店等）
    - notes: 备注（可选）
    
    来源：用户行为 / 任务执行 / 风险告知反写
    生命周期：长期（强绑定 scene_id）
    是否可为空：是（Phase A 阶段为空）
    
    说明：
    - 不是全局记忆
    - 强绑定 scene_id
    - 可反向修正 Static / Dynamic
    """
    visited_count: Optional[int] = None
    last_visited: Optional[float] = None
    observed_risks: Optional[List[str]] = field(default_factory=list)  # heavy_traffic / confusing_path
    useful_places: Optional[List[Dict[str, Any]]] = field(default_factory=list)  # [{"type": "breakfast_shop", "confidence": 0.8}]
    notes: Optional[str] = None


@dataclass
class SceneState:
    """
    场景状态（统一对外接口）
    
    字段说明：
    - scene_id: 场景唯一标识（必需）
    - scene_type: 场景类型（lake_side / road / mall / hospital / home）
    - geo_anchor: 地理锚点（lat / lng / area_id）
    - static_model: 静态场景模型
    - dynamic_model: 动态场景模型
    - scene_memory: 场景绑定记忆
    - confidence: 置信度（0~1）
    - timestamp: 时间戳
    
    来源：Scene Registry（Phase A 阶段为 Stub）
    生命周期：场景切换时更新
    是否可为空：scene_id 必需，其他可选（Phase A 阶段大部分为空）
    """
    scene_id: str
    scene_type: Optional[str] = None  # lake_side / road / mall / hospital / home
    geo_anchor: Optional[Dict[str, Any]] = None  # {"lat": float, "lng": float, "area_id": str}
    static_model: Optional[StaticScene] = None
    dynamic_model: Optional[DynamicScene] = None
    scene_memory: Optional[SceneMemory] = None
    confidence: Optional[float] = None  # 0~1
    timestamp: Optional[float] = None


