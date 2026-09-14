# -*- coding: utf-8 -*-
"""
v1.8.5 Phase B: Environment Context（环境上下文）

职责：
- 定义时间、天气、季节等环境因素
- 作为环境修正因子，不直接触发场景切换

原则：
- 时间/天气不是场景切换条件，而是"环境修正因子"
- 它们能改变风险权重、通行可信度、任务建议倾向
- 它们不能直接切 Scene 或生成新 SceneSegment
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Literal
import time


@dataclass
class EnvironmentContext:
    """
    环境上下文（时间 × 天气 × 季节）
    
    作用：
    - 改变风险权重（夜晚 + 无照明 → Risk confidence ↓）
    - 改变通行可信度（雨/雪 → 路面 hazard_multiplier ↑）
    - 改变任务建议倾向（冬季 + 东北 → 结冰概率 ↑）
    
    禁止：
    - ❌ 直接切 Scene
    - ❌ 直接生成新 SceneSegment
    
    这些规则的计算不在 SceneRegistry 内。
    SceneRegistry 只负责：把"当前环境状态"稳定地提供出去。
    """
    season: Optional[Literal["SPRING", "SUMMER", "AUTUMN", "WINTER"]] = None
    time_of_day: Optional[Literal["DAY", "NIGHT", "DUSK", "DAWN"]] = None
    weather: Optional[Literal["CLEAR", "RAIN", "SNOW", "FOG", "WINDY"]] = None
    temperature: Optional[float] = None  # 摄氏度
    timestamp: float = field(default_factory=time.time)
    
    def compute_modifier(self) -> float:
        """
        计算环境修正因子（用于 match() 的权重调整）
        
        原则：
        - 夜晚/恶劣天气 → 降低匹配置信度（但不否定匹配）
        - 白天/好天气 → 提升匹配置信度
        
        Returns:
            float: 修正因子（0.5 ~ 1.0）
        """
        modifier = 1.0
        
        # 时间修正
        if self.time_of_day == "NIGHT":
            modifier *= 0.8  # 夜晚降低置信度
        elif self.time_of_day == "DUSK" or self.time_of_day == "DAWN":
            modifier *= 0.9
        elif self.time_of_day == "DAY":
            modifier *= 1.0
        
        # 天气修正
        if self.weather == "RAIN" or self.weather == "SNOW":
            modifier *= 0.85  # 雨雪降低置信度
        elif self.weather == "FOG":
            modifier *= 0.75  # 雾天更低
        elif self.weather == "CLEAR":
            modifier *= 1.0
        
        # 温度修正（极端温度）
        if self.temperature is not None:
            if self.temperature < -10 or self.temperature > 40:
                modifier *= 0.9
        
        return max(0.5, min(1.0, modifier))  # 限制在 0.5 ~ 1.0


