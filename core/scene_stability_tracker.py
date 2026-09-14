# -*- coding: utf-8 -*-
"""
场景稳定器（Scene Stability Tracker）

v1.8.2: 基于 hash 的场景稳定判断
"""

from typing import List


class SceneStabilityTracker:
    """场景稳定器"""
    
    def __init__(self, stable_threshold: int = 2):
        """
        初始化场景稳定器
        
        Args:
            stable_threshold: 稳定阈值（连续相同 hash 的次数），默认 2
        """
        self.last_scene_hash = None
        self.stable_count = 0
        self.stable_threshold = stable_threshold
    
    def update(self, objects: List[str], signs: List[str]) -> bool:
        """
        更新场景并返回是否稳定
        
        Args:
            objects: 物体列表
            signs: 标志牌列表
        
        Returns:
            bool: True 表示场景稳定，False 表示场景不稳定
        """
        scene_hash = hash(tuple(sorted(objects) + sorted(signs)))
        
        if scene_hash != self.last_scene_hash:
            self.last_scene_hash = scene_hash
            self.stable_count = 0
            return False
        
        self.stable_count += 1
        return self.stable_count >= self.stable_threshold
