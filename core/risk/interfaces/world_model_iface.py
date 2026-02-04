# -*- coding: utf-8 -*-
"""
v1.8.4: 世界模型接口（接口桩）

职责：
- 定义世界模型接口（护栏高度/完整性等）
- 为后续世界模型集成预留接口

说明：
- 1.8.4 只做接口桩，不实现具体逻辑
- 后续世界模型可提供更精细的 HazardLevel 计算
"""

from typing import Optional, Dict, Any
from abc import ABC, abstractmethod


class WorldModelInterface(ABC):
    """
    世界模型接口
    
    世界模型可提供：
    1. 更精细的 HazardLevel（护栏有无、高度、完整性）
    2. SafetyBoundary 定义（护栏内外、警戒线）
    3. 环境结构稳定性判断
    """
    
    @abstractmethod
    def get_hazard_correction(
        self,
        risk_type: str,
        scene_context: Optional[Dict[str, Any]] = None
    ) -> Optional[float]:
        """
        获取危险等级修正因子
        
        例如：有护栏则 hazard_level 下调
        
        Args:
            risk_type: 风险类型
            scene_context: 场景上下文（包含 objects, signs 等）
        
        Returns:
            Optional[float]: 修正因子（0.0 ~ 1.0），如果为 None 则不修正
        """
        pass
    
    @abstractmethod
    def get_safety_attributes(
        self,
        risk_type: str,
        location: tuple[float, float],
        scene_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        获取安全属性（护栏存在/未知等）
        
        Args:
            risk_type: 风险类型
            location: 位置 (x, y)
            scene_context: 场景上下文
        
        Returns:
            Dict[str, Any]: 安全属性字典
                - has_barrier: bool 是否有护栏
                - barrier_height: float 护栏高度（米）
                - barrier_integrity: float 护栏完整性（0~1）
        """
        pass


class DefaultWorldModel(WorldModelInterface):
    """
    默认世界模型（接口桩实现）
    
    1.8.4: 不提供任何修正，返回 None
    """
    
    def get_hazard_correction(
        self,
        risk_type: str,
        scene_context: Optional[Dict[str, Any]] = None
    ) -> Optional[float]:
        """1.8.4: 不提供修正"""
        return None
    
    def get_safety_attributes(
        self,
        risk_type: str,
        location: tuple[float, float],
        scene_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """1.8.4: 返回默认值"""
        return {
            "has_barrier": False,
            "barrier_height": 0.0,
            "barrier_integrity": 0.0,
        }


