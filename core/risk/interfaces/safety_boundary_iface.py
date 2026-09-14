# -*- coding: utf-8 -*-
"""
v1.8.4: 安全边界接口（接口桩）

职责：
- 定义安全边界接口（越界事件）
- 为后续世界模型集成预留接口

说明：
- 1.8.4 只做接口桩，不实现具体逻辑
- 后续世界模型可提供 SafetyBoundary 定义（护栏内外、警戒线）
"""

from typing import Optional, List, Tuple
from abc import ABC, abstractmethod


class SafetyBoundaryInterface(ABC):
    """
    安全边界接口
    
    安全边界可提供：
    1. 护栏内侧 / 警戒线外 → Safe
    2. 越过警戒线 / 护栏外侧 → Unsafe
    3. 是否越界是离散事件
    """
    
    @abstractmethod
    def is_breached(
        self,
        user_location: Tuple[float, float],
        risk_type: str
    ) -> bool:
        """
        判断是否越过安全边界
        
        Args:
            user_location: 用户位置 (x, y)
            risk_type: 风险类型
        
        Returns:
            bool: 是否越过安全边界
        """
        pass
    
    @abstractmethod
    def get_boundary_polygon(
        self,
        risk_type: str
    ) -> Optional[List[Tuple[float, float]]]:
        """
        获取安全边界多边形
        
        Args:
            risk_type: 风险类型
        
        Returns:
            Optional[List[Tuple[float, float]]]: 边界多边形顶点列表，如果为 None 则无边界定义
        """
        pass


class DefaultSafetyBoundary(SafetyBoundaryInterface):
    """
    默认安全边界（接口桩实现）
    
    1.8.4: 不提供任何边界判断，返回 False
    """
    
    def is_breached(
        self,
        user_location: Tuple[float, float],
        risk_type: str
    ) -> bool:
        """1.8.4: 不提供边界判断"""
        return False
    
    def get_boundary_polygon(
        self,
        risk_type: str
    ) -> Optional[List[Tuple[float, float]]]:
        """1.8.4: 不提供边界定义"""
        return None


