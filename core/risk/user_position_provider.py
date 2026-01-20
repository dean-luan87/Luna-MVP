# -*- coding: utf-8 -*-
"""
v1.8.4: 用户位置提供器（PositionProvider）

职责：
- 统一对外提供用户位置（局部坐标，单位米）
- 1.8.4 不要求立刻完成 GPS/视觉融合；先做到"有一个可信输入源即可"
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Tuple
import time

XY = Tuple[float, float]


@dataclass
class PositionSample:
    """位置采样"""
    xy: XY
    ts: float
    confidence: float = 1.0


class UserPositionProvider:
    """
    统一对外提供用户位置（局部坐标，单位米）
    
    使用方式：
    1. 视觉/定位模块在主循环里每帧调用 provider.update(xy, ts, confidence)
    2. RiskEngine 调用 provider.get() 获取最新位置
    """
    
    def __init__(self) -> None:
        """初始化用户位置提供器"""
        self._last: Optional[PositionSample] = None
    
    def update(self, xy: XY, ts: Optional[float] = None, confidence: float = 1.0) -> None:
        """
        更新用户位置
        
        Args:
            xy: 用户位置 (x, y)（局部坐标，单位米）
            ts: 时间戳（如果为 None 则使用 time.time()）
            confidence: 位置置信度（0~1）
        """
        if ts is None:
            ts = time.time()
        self._last = PositionSample(xy=xy, ts=ts, confidence=confidence)
    
    def get(self) -> Optional[PositionSample]:
        """
        获取最新用户位置
        
        Returns:
            Optional[PositionSample]: 最新位置采样（如果不存在则返回 None）
        """
        return self._last
    
    def clear(self) -> None:
        """清空位置记录"""
        self._last = None


