# -*- coding: utf-8 -*-
"""
v1.8.5: Stability Gate（稳定性闸门）

职责：
- Layer 1：稳定性闸门（抗抖动第一优先级）
- 位置/视角/场景不稳定时：冻结演化

原则：
- stability_score < threshold 时：
  - 不允许新场景关联
  - 不允许 relevance 上升
  - 只允许自然衰减
"""


class StabilityGate:
    """
    稳定性闸门（Layer 1：抗抖动）
    
    核心规则：
    - 位置/视角/场景不稳定时：冻结演化
    - 不允许新场景关联
    - 不允许 relevance 上升
    - 只允许自然衰减
    
    这是防污染的第一道防线。
    """
    
    def __init__(self, threshold: float = 0.7):
        """
        初始化稳定性闸门
        
        Args:
            threshold: 稳定性阈值（默认 0.7）
        """
        self.threshold = threshold
    
    def is_stable(self, stability_score: float) -> bool:
        """
        判断位置是否稳定
        
        Args:
            stability_score: 稳定性评分 [0.0 ~ 1.0]
        
        Returns:
            bool: 是否稳定（>= threshold）
        """
        return stability_score >= self.threshold


