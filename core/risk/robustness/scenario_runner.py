# -*- coding: utf-8 -*-
"""
v1.8.4: 极端场景脚本运行器（Scenario Runner）

目标：
不是"模拟平均情况"，而是模拟你最不希望系统乱说话的情况。

设计为"脚本驱动"，可扩展
"""

from __future__ import annotations
from typing import List, Tuple, Optional, Callable
from dataclasses import dataclass
import time

XY = Tuple[float, float]


@dataclass
class ScenarioStep:
    """场景步骤"""
    xy: XY
    duration_s: float  # 该步骤持续时间（秒）


@dataclass
class Scenario:
    """场景定义"""
    name: str
    description: str
    steps: List[ScenarioStep]
    expected_behavior: str = ""  # 期望行为描述
    
    def create_generator(self) -> Callable[[], Optional[XY]]:
        """
        创建位置生成器
        
        Returns:
            Callable: 位置生成器函数，返回 None 表示场景结束
        """
        step_index = [0]  # 使用列表以在闭包中修改
        step_start_time = [None]
        
        def generator() -> Optional[XY]:
            if step_index[0] >= len(self.steps):
                return None  # 场景结束
            
            current_step = self.steps[step_index[0]]
            
            # 初始化步骤开始时间
            if step_start_time[0] is None:
                step_start_time[0] = time.time()
            
            # 检查是否应该进入下一步
            elapsed = time.time() - step_start_time[0]
            if elapsed >= current_step.duration_s:
                step_index[0] += 1
                step_start_time[0] = None
                if step_index[0] >= len(self.steps):
                    return None
                current_step = self.steps[step_index[0]]
                step_start_time[0] = time.time()
            
            return current_step.xy
        
        return generator


class ScenarioLibrary:
    """
    场景库
    
    包含 5 个必须实现的场景
    """
    
    @staticmethod
    def hover_near_threshold() -> Scenario:
        """
        场景 1：阈值附近来回晃
        
        dist = 3.1 → 2.9 → 3.0 → 2.8
        
        验收：最多 1 次 advisory，甚至 0 次
        """
        return Scenario(
            name="hover_near_threshold",
            description="在阈值附近（2.9m → 3.1m）来回移动",
            steps=[
                ScenarioStep((5.0, 3.1), 2.0),
                ScenarioStep((5.0, 2.9), 2.0),
                ScenarioStep((5.0, 3.0), 2.0),
                ScenarioStep((5.0, 2.8), 2.0),
            ],
            expected_behavior="最多 1 次 advisory，甚至 0 次"
        )
    
    @staticmethod
    def approach_and_leave_fast() -> Scenario:
        """
        场景 2：快速靠近 → 立刻离开
        
        5.0 → 2.0 → 5.0
        
        验收：可以不说；说了也只能一次
        """
        return Scenario(
            name="approach_and_leave_fast",
            description="快速靠近又立刻离开（5.0m → 2.0m → 5.0m）",
            steps=[
                ScenarioStep((5.0, 6.0), 1.0),
                ScenarioStep((5.0, 2.0), 0.5),
                ScenarioStep((5.0, 6.0), 2.0),
            ],
            expected_behavior="可以不说；说了也只能一次"
        )
    
    @staticmethod
    def static_stay() -> Scenario:
        """
        场景 3：静态停留（最重要）
        
        2.5 → 2.5 → 2.5（持续 30 秒）
        
        验收铁律：静态停留绝不能反复说
        """
        return Scenario(
            name="static_stay",
            description="在 2.5m 位置持续停留 30 秒",
            steps=[
                ScenarioStep((5.0, 2.5), 30.0),
            ],
            expected_behavior="静态停留绝不能反复说"
        )
    
    @staticmethod
    def dynamic_window_switch() -> Scenario:
        """
        场景 4：动态区域时间窗切换
        
        07:59 → 08:00（dynamic_active False → True）
        
        验收：dynamic_active 切换 ≠ delta_risk 上升
        
        注意：这个场景需要配合时间戳使用，这里只提供位置生成器
        """
        return Scenario(
            name="dynamic_window_switch",
            description="动态区域时间窗切换（07:59 → 08:00）",
            steps=[
                ScenarioStep((15.0, 2.0), 5.0),  # 07:59
                ScenarioStep((15.0, 2.0), 5.0),  # 08:00
            ],
            expected_behavior="dynamic_active 切换 ≠ delta_risk 上升"
        )
    
    @staticmethod
    def multi_risk_overlap() -> Scenario:
        """
        场景 5：多风险叠加
        
        WATER_EDGE + CROWD + CONSTRUCTION
        
        验收：不应多风险叠加导致多次播报
        
        注意：这个场景需要在外部创建多个风险对象
        """
        return Scenario(
            name="multi_risk_overlap",
            description="同时接近多个风险区域",
            steps=[
                ScenarioStep((15.0, 2.5), 5.0),
            ],
            expected_behavior="不应多风险叠加导致多次播报"
        )


