# -*- coding: utf-8 -*-
"""
v1.8.5 Phase B: Scene Segment（场景段）

职责：
- 定义场景段的最小工程单位
- 一段在"决策约束上保持一致"的现实片段

原则：
- Scene Segment = 在一段时间内，决策前提保持一致的现实段
- 不是 GPS 点、固定半径、视觉帧
- 是一个稳定段（Stable Segment），由多锚点共同支撑
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, Literal
import time


@dataclass
class SceneAnchors:
    """
    场景锚点（4 个工程锚点）
    
    多锚点联合确认的稳定段：
    - geometry_anchor: 几何锚点（GPS / 惯导 / 视觉推断）
    - semantic_anchor: 语义锚点（离线地图 / OCR / 视觉标识）
    - behavior_anchor: 行为锚点（用户行为稳定性）
    - memory_anchor: 记忆锚点（Scene Memory）
    """
    geometry_anchor: Optional[Dict[str, Any]] = None  # polyline / area（粗）
    semantic_anchor: Optional[Dict[str, Any]] = None  # place_type / building / zone
    behavior_anchor: Optional[Dict[str, Any]] = None  # 行为稳定性（停/走/往返）
    memory_anchor: Optional[Dict[str, Any]] = None  # 过往记忆摘要


@dataclass
class SceneSegment:
    """
    场景段（Scene Segment）
    
    Scene Segment = 在一段时间内，决策前提保持一致的现实段
    
    字段说明：
    - scene_id: 场景唯一标识
    - anchors: 4 个工程锚点（几何 / 语义 / 行为 / 记忆）
    - confidence: 置信度（0.0 ~ 1.0）
    - first_seen_ts: 首次出现时间戳
    - last_confirmed_ts: 最后确认时间戳
    - lifecycle_state: 生命周期状态（ACTIVE / CANDIDATE / FADING）
    """
    scene_id: str
    anchors: SceneAnchors = field(default_factory=SceneAnchors)
    confidence: float = 0.0  # 0.0 ~ 1.0
    first_seen_ts: float = field(default_factory=time.time)
    last_confirmed_ts: float = field(default_factory=time.time)
    lifecycle_state: Literal["ACTIVE", "CANDIDATE", "FADING"] = "CANDIDATE"
    
    def update_confidence(self, new_confidence: float, now_ts: Optional[float] = None):
        """
        更新置信度
        
        Args:
            new_confidence: 新置信度（0.0 ~ 1.0）
            now_ts: 当前时间戳（如果为 None 则使用 time.time()）
        """
        self.confidence = max(0.0, min(1.0, new_confidence))
        if now_ts is None:
            now_ts = time.time()
        self.last_confirmed_ts = now_ts
    
    def is_stable(self, min_confidence: float = 0.7, min_stable_time: float = 5.0) -> bool:
        """
        判断场景段是否稳定
        
        Args:
            min_confidence: 最小置信度阈值
            min_stable_time: 最小稳定时间（秒）
        
        Returns:
            bool: 是否稳定
        """
        if self.confidence < min_confidence:
            return False
        
        stable_duration = time.time() - self.first_seen_ts
        return stable_duration >= min_stable_time


