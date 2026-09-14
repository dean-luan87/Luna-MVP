# -*- coding: utf-8 -*-
"""
主线 2 第二阶段 M0/M1.5：Local Goal Spatial Map（局部目标空间图）数据结构。

目标：把第一阶段的局部状态从文本/标签推进为结构化的“区域证据面”。
M1.5：接入 LOCAL_SPATIAL_SCALE_CONSTITUTION v1.0 最小精确标尺与派生标尺。
不做全局地图、不做 2.5D/3D、不做坐标系；方向扇区仅用基础集合（无 near_front 混维）。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

# 宪法 4.1：基础方向扇区（仅方向维度）；near_front 由 方向+距离带 在派生层组合，不作为基础扇区
BASE_SECTORS = ("front", "front_left", "front_right", "left", "right", "rear")
# 兼容旧引用（builder 与测试仅允许写入 BASE_SECTORS）
SECTORS = BASE_SECTORS

DISTANCE_BANDS = ("immediate", "near", "mid", "far")
OFFSET_BANDS = ("aligned", "slight_offset", "moderate_offset", "strong_offset")
SPEED_BANDS = ("stopped", "slow", "normal", "fast")
SCENE_PROFILES = ("outdoor", "indoor")


@dataclass
class SpatialRegion:
    region_type: str  # focus_region / traversable_region / risk_region / confirm_region
    sector: str  # one of BASE_SECTORS only
    confidence: float  # 0~1
    priority_rank: int = 1  # 1=主区域，2/3=次区域
    reason: Optional[str] = None
    ttl_ms: Optional[float] = None
    stability_score: Optional[float] = None  # 0~1（规则型短时稳定度）
    # M1.5 精确标尺（宪法 3.x）
    relative_bearing_deg: Optional[float] = None  # 相对当前行动前向，度
    distance_cm: Optional[float] = None
    staleness_ms: Optional[float] = None
    # M1.5 派生标尺（宪法 4.x）
    distance_band: Optional[str] = None  # immediate / near / mid / far
    offset_band: Optional[str] = None  # aligned / slight_offset / moderate_offset / strong_offset


@dataclass
class LocalGoalSpatialMap:
    goal_id: Optional[str] = None
    goal_type: Optional[str] = None
    produced_ts: Optional[float] = None
    staleness_ms: Optional[float] = None
    scene_profile: Optional[str] = None  # M1.5: outdoor / indoor
    focus_region: Optional[List[SpatialRegion]] = None
    traversable_region: Optional[List[SpatialRegion]] = None
    risk_region: Optional[List[SpatialRegion]] = None
    confirm_region: Optional[List[SpatialRegion]] = None
    summary: Optional[str] = None

