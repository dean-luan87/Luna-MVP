# -*- coding: utf-8 -*-
"""
v1.8.4: 位置噪声注入器（Noise Position Provider）

目标：
模拟真实模型最常见的三类脏数据：
1. 连续小抖动
2. 偶发跳变
3. 回弹（错误 → 修正）

设计为"可插拔 Provider"，不改 risk 核心
"""

from __future__ import annotations
from typing import Tuple
import random

XY = Tuple[float, float]


class NoisePositionProvider:
    """
    位置噪声注入器
    
    用于鲁棒性测试，模拟真实模型的脏数据：
    - 连续小抖动（识别误差）
    - 偶发跳变（识别错误）
    - 回弹（错误 → 修正）
    
    验收标准（写进注释）：
    在开启 Noise Injector 时：
    snapshot 中 delta_risk 不应频繁为正，advisory_triggered 应极少出现
    """
    
    def __init__(
        self,
        base_xy: XY,
        jitter_radius: float = 0.3,
        jump_prob: float = 0.05,
        jump_radius: float = 2.0,
    ):
        """
        初始化噪声位置生成器
        
        Args:
            base_xy: 基础位置
            jitter_radius: 连续小抖动半径（米）
            jump_prob: 偶发跳变概率（0~1）
            jump_radius: 跳变幅度（米）
        """
        self.base_xy = base_xy
        self.jitter_radius = jitter_radius
        self.jump_prob = jump_prob
        self.jump_radius = jump_radius
    
    def sample(self) -> XY:
        """
        生成带噪声的位置样本
        
        Returns:
            XY: 带噪声的位置 (x, y)
        """
        x, y = self.base_xy
        
        # 连续小抖动（识别误差）
        dx = random.uniform(-self.jitter_radius, self.jitter_radius)
        dy = random.uniform(-self.jitter_radius, self.jitter_radius)
        
        # 偶发大跳变（识别错误）
        if random.random() < self.jump_prob:
            dx += random.uniform(-self.jump_radius, self.jump_radius)
            dy += random.uniform(-self.jump_radius, self.jump_radius)
        
        return (x + dx, y + dy)
    
    def update_base(self, new_base_xy: XY):
        """
        更新基础位置（用于模拟移动）
        
        Args:
            new_base_xy: 新的基础位置
        """
        self.base_xy = new_base_xy


