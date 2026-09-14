# -*- coding: utf-8 -*-
"""
v1.8.5: World Model Common Types（通用类型定义）

职责：
- PositionState：位置状态（对齐 Scene 的稳定性闸门）
- EnvironmentContext：环境上下文（时间/天气/季节）
"""

from dataclasses import dataclass
from typing import Optional, Tuple, Dict, Any


@dataclass
class PositionState:
    """
    位置状态
    
    字段说明：
    - position: 位置坐标 (x, y)，单位：米（局部坐标）
    - stability_score: 稳定性评分 [0.0 ~ 1.0]
    - stable: 稳定性闸门结果（gate result）
    - source: 位置来源（"vision" | "gps" | "fused"）
    - drift_suspected: 识别到失衡/漂移（NEW）
    - relocalizing: 正在重定位（NEW）
    - anchor_gps: GPS 弱锚点（可选，NEW）
    """
    position: Tuple[float, float]  # local (x,y) meters
    stability_score: float  # 0~1
    stable: bool  # gate result
    source: str = "vision"  # "vision" | "gps" | "fused"
    drift_suspected: bool = False  # NEW: 识别到失衡/漂移
    relocalizing: bool = False  # NEW: 正在重定位
    anchor_gps: Optional[Tuple[float, float]] = None  # NEW: GPS 弱锚点 (lat, lon)


@dataclass
class EnvironmentContext:
    """
    环境上下文（时间 / 天气 / 季节）
    
    字段说明：
    - season: 季节（SPRING/SUMMER/AUTUMN/WINTER）
    - time_of_day: 时间（DAY/NIGHT/DUSK）
    - weather: 天气（CLEAR/RAIN/SNOW/FOG）
    """
    season: Optional[str] = None  # SPRING/SUMMER/AUTUMN/WINTER
    time_of_day: Optional[str] = None  # DAY/NIGHT/DUSK
    weather: Optional[str] = None  # CLEAR/RAIN/SNOW/FOG


@dataclass
class WorldUpdate:
    """
    v1.8.5 Phase B: 结构化世界更新
    
    原则（写死）：
    - world_model 只接受"结构化事实"
    - 不接受 frame / image / bbox / ocr_text
    
    字段说明：
    - update_type: 更新类型（"entity" | "content" | "fact"）
    - structured_data: 结构化数据（字典）
    - confidence: 置信度 [0.0 ~ 1.0]
    - source: 来源（"modeling_executor" | "user_report"）
    """
    update_type: str  # "entity" | "content" | "fact"
    structured_data: Dict[str, Any]
    confidence: float = 0.0
    source: str = "modeling_executor"  # "modeling_executor" | "user_report"

