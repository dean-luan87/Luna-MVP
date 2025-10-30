#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 人流方向判断模块
判断当前人流与用户方向是否一致
"""

import logging
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import math
import time

logger = logging.getLogger(__name__)

class DangerLevel(Enum):
    """危险等级"""
    SAFE = "safe"              # 安全
    LOW = "low"                # 低风险
    MEDIUM = "medium"          # 中等风险
    HIGH = "high"              # 高风险
    CRITICAL = "critical"      # 极高风险

class FlowDirection(Enum):
    """人流方向"""
    SAME = "same"              # 同向
    COUNTER = "counter"        # 逆向
    CROSSING = "crossing"      # 交叉
    UNKNOWN = "unknown"        # 未知

@dataclass
class FlowAnalysis:
    """人流方向分析结果"""
    flow_direction: FlowDirection    # 人流方向
    danger_level: DangerLevel       # 危险等级
    counterflow_percentage: float   # 逆向人流百分比
    dominant_angle: float           # 主导角度
    timestamp: float                # 检测时间戳
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "flow_direction": self.flow_direction.value,
            "danger_level": self.danger_level.value,
            "counterflow_percentage": self.counterflow_percentage,
            "dominant_angle": self.dominant_angle,
            "timestamp": self.timestamp
        }

class FlowDirectionAnalyzer:
    """人流方向分析器"""
    
    def __init__(self, user_direction: float = 0.0):
        """
        初始化分析器
        
        Args:
            user_direction: 用户方向（度），0度表示正前方
        """
        self.logger = logging.getLogger(__name__)
        self.user_direction = user_direction
        
        # 角度容差（度）
        self.angle_tolerance = 45.0
        
        # 危险等级阈值
        self.danger_thresholds = {
            DangerLevel.SAFE: 0.2,        # < 20% 逆向
            DangerLevel.LOW: 0.4,         # 20-40% 逆向
            DangerLevel.MEDIUM: 0.6,       # 40-60% 逆向
            DangerLevel.HIGH: 0.8,        # 60-80% 逆向
            DangerLevel.CRITICAL: 1.0     # > 80% 逆向
        }
        
        self.logger.info("👥 人流方向分析器初始化完成")
    
    def analyze_flow(self, trajectories: List[List[Tuple[float, float]]]) -> FlowAnalysis:
        """
        分析人流方向
        
        Args:
            trajectories: 轨迹列表，每个轨迹是一系列(x, y)点
            
        Returns:
            FlowAnalysis: 分析结果
        """
        if len(trajectories) == 0:
            return FlowAnalysis(
                flow_direction=FlowDirection.UNKNOWN,
                danger_level=DangerLevel.SAFE,
                counterflow_percentage=0.0,
                dominant_angle=0.0,
                timestamp=time.time()
            )
        
        # 分析每个轨迹的方向
        angles = []
        for trajectory in trajectories:
            angle = self._calculate_trajectory_angle(trajectory)
            if angle is not None:
                angles.append(angle)
        
        if len(angles) == 0:
            return FlowAnalysis(
                flow_direction=FlowDirection.UNKNOWN,
                danger_level=DangerLevel.SAFE,
                counterflow_percentage=0.0,
                dominant_angle=0.0,
                timestamp=time.time()
            )
        
        # 计算逆向人流百分比
        counterflow_count = self._count_counterflow(angles)
        counterflow_percentage = counterflow_count / len(angles)
        
        # 确定人流方向
        flow_direction = self._determine_flow_direction(counterflow_percentage)
        
        # 评估危险等级
        danger_level = self._assess_danger(counterflow_percentage)
        
        # 计算主导角度
        dominant_angle = self._calculate_dominant_angle(angles)
        
        result = FlowAnalysis(
            flow_direction=flow_direction,
            danger_level=danger_level,
            counterflow_percentage=counterflow_percentage,
            dominant_angle=dominant_angle,
            timestamp=time.time()
        )
        
        self.logger.info(f"👥 人流分析: 方向={flow_direction.value}, "
                        f"危险={danger_level.value}, "
                        f"逆向={counterflow_percentage:.1%}")
        
        return result
    
    def _calculate_trajectory_angle(self, trajectory: List[Tuple[float, float]]) -> Optional[float]:
        """
        计算轨迹的运动方向角度
        
        Args:
            trajectory: 轨迹点列表
            
        Returns:
            Optional[float]: 角度（度），如果没有足够点则返回None
        """
        if len(trajectory) < 2:
            return None
        
        # 使用起点和终点计算方向
        start = trajectory[0]
        end = trajectory[-1]
        
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        
        # 计算角度（0-360度）
        angle = math.degrees(math.atan2(-dy, dx))  # 注意y轴是反向的
        angle = (angle + 360) % 360
        
        return angle
    
    def _count_counterflow(self, angles: List[float]) -> int:
        """
        统计逆向人流数量
        
        Args:
            angles: 运动角度列表
            
        Returns:
            int: 逆向人流数量
        """
        user_angle = self.user_direction
        counterflow_count = 0
        
        for angle in angles:
            # 计算角度差
            angle_diff = abs(angle - user_angle)
            angle_diff = min(angle_diff, 360 - angle_diff)  # 处理0度和360度的边界
            
            # 如果角度差大于180度减去容差，认为是逆向
            if angle_diff > (180 - self.angle_tolerance):
                counterflow_count += 1
        
        return counterflow_count
    
    def _determine_flow_direction(self, counterflow_percentage: float) -> FlowDirection:
        """
        确定人流方向
        
        Args:
            counterflow_percentage: 逆向人流百分比
            
        Returns:
            FlowDirection: 人流方向
        """
        if counterflow_percentage < 0.3:
            return FlowDirection.SAME
        elif counterflow_percentage < 0.7:
            return FlowDirection.CROSSING
        elif counterflow_percentage >= 0.7:
            return FlowDirection.COUNTER
        else:
            return FlowDirection.UNKNOWN
    
    def _assess_danger(self, counterflow_percentage: float) -> DangerLevel:
        """
        评估危险等级
        
        Args:
            counterflow_percentage: 逆向人流百分比
            
        Returns:
            DangerLevel: 危险等级
        """
        if counterflow_percentage < self.danger_thresholds[DangerLevel.SAFE]:
            return DangerLevel.SAFE
        elif counterflow_percentage < self.danger_thresholds[DangerLevel.LOW]:
            return DangerLevel.LOW
        elif counterflow_percentage < self.danger_thresholds[DangerLevel.MEDIUM]:
            return DangerLevel.MEDIUM
        elif counterflow_percentage < self.danger_thresholds[DangerLevel.HIGH]:
            return DangerLevel.HIGH
        else:
            return DangerLevel.CRITICAL
    
    def _calculate_dominant_angle(self, angles: List[float]) -> float:
        """
        计算主导角度
        
        Args:
            angles: 角度列表
            
        Returns:
            float: 主导角度（度）
        """
        # 将角度转换为单位向量，然后计算平均方向
        angles_rad = np.array([math.radians(a) for a in angles])
        
        # 计算单位向量的平均
        mean_x = np.mean(np.cos(angles_rad))
        mean_y = np.mean(np.sin(angles_rad))
        
        # 计算主导角度
        dominant_angle = math.degrees(math.atan2(mean_y, mean_x))
        dominant_angle = (dominant_angle + 360) % 360
        
        return float(dominant_angle)


# 全局分析器实例
global_flow_analyzer = FlowDirectionAnalyzer()

def analyze_flow_direction(trajectories: List[List[Tuple[float, float]]]) -> FlowAnalysis:
    """分析人流方向的便捷函数"""
    return global_flow_analyzer.analyze_flow(trajectories)


if __name__ == "__main__":
    # 测试人流方向分析
    import logging
    logging.basicConfig(level=logging.INFO)
    
    analyzer = FlowDirectionAnalyzer(user_direction=0.0)  # 用户向前走
    
    # 测试1: 同向人流
    print("\n测试1: 同向人流")
    trajectories = [
        [(100, 100), (105, 95), (110, 90)],   # 向前
        [(150, 150), (155, 145), (160, 140)], # 向前
        [(200, 200), (205, 195), (210, 190)]  # 向前
    ]
    result = analyzer.analyze_flow(trajectories)
    print(f"  方向: {result.flow_direction.value}")
    print(f"  危险: {result.danger_level.value}")
    print(f"  逆向比例: {result.counterflow_percentage:.1%}")
    
    # 测试2: 逆向人流
    print("\n测试2: 逆向人流")
    trajectories = [
        [(200, 100), (195, 105), (190, 110)], # 向后
        [(150, 150), (145, 155), (140, 160)],  # 向后
        [(300, 200), (295, 205), (290, 210)]   # 向后
    ]
    result = analyzer.analyze_flow(trajectories)
    print(f"  方向: {result.flow_direction.value}")
    print(f"  危险: {result.danger_level.value}")
    print(f"  逆向比例: {result.counterflow_percentage:.1%}")
    
    # 测试3: 交叉人流
    print("\n测试3: 交叉人流")
    trajectories = [
        [(100, 100), (105, 95), (110, 90)],    # 向前
        [(200, 200), (195, 205), (190, 210)],  # 向后
        [(150, 150), (155, 145), (160, 140)],  # 向前
    ]
    result = analyzer.analyze_flow(trajectories)
    print(f"  方向: {result.flow_direction.value}")
    print(f"  危险: {result.danger_level.value}")
    print(f"  逆向比例: {result.counterflow_percentage:.1%}")
    
    print("\n" + "=" * 60)
