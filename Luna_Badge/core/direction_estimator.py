#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 方向估算器
估算节点间的方向和相对距离
"""

import logging
import time
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class Direction:
    """方向描述"""
    turn: str         # 转向：直行/左转/右转/掉头
    distance: float   # 距离（米）
    duration: float   # 耗时（秒）
    description: str  # 完整描述
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "turn": self.turn,
            "distance": self.distance,
            "duration": self.duration,
            "description": self.description
        }

class DirectionEstimator:
    """方向估算器"""
    
    def __init__(self):
        """初始化方向估算器"""
        # 默认行走速度（米/秒）
        self.walking_speed = 1.0
        
        # 方向词汇
        self.direction_words = {
            "straight": ["直行", "向前", "继续", "go straight", "forward"],
            "left": ["左转", "向左", "left", "turn left"],
            "right": ["右转", "向右", "right", "turn right"],
            "turn_around": ["掉头", "回转", "turn around", "u-turn"],
        }
        
        logger.info("🧭 方向估算器初始化完成")
    
    def estimate_direction(self, time_interval: float, 
                          acceleration_data: List[float] = None) -> Direction:
        """
        估算方向
        
        Args:
            time_interval: 时间间隔（秒）
            acceleration_data: 加速度数据（可选）
            
        Returns:
            Direction: 方向描述
        """
        # 估算距离（简化：使用时间和速度）
        distance = time_interval * self.walking_speed
        
        # 估算转向（简化：默认直行）
        if acceleration_data and len(acceleration_data) >= 2:
            turn = self._estimate_turn_from_acceleration(acceleration_data)
        else:
            turn = "straight"
        
        # 生成描述
        description = self._generate_description(turn, distance)
        
        return Direction(
            turn=turn,
            distance=distance,
            duration=time_interval,
            description=description
        )
    
    def _estimate_turn_from_acceleration(self, accel_data: List[float]) -> str:
        """
        从加速度数据估算转向
        
        Args:
            accel_data: 加速度数据
            
        Returns:
            str: 转向类型
        """
        # 简化实现：基于加速度变化判断转向
        if len(accel_data) < 2:
            return "straight"
        
        # 这里简化处理，实际应该使用IMU或陀螺仪数据
        return "straight"
    
    def _generate_description(self, turn: str, distance: float) -> str:
        """
        生成方向描述
        
        Args:
            turn: 转向类型
            distance: 距离
            
        Returns:
            str: 描述文字
        """
        turn_map = {
            "straight": "直行",
            "left": "左转",
            "right": "右转",
            "turn_around": "掉头"
        }
        
        turn_text = turn_map.get(turn, "直行")
        
        if distance < 1:
            return f"{turn_text}"
        elif distance < 5:
            return f"{turn_text}前行{int(distance)}米"
        else:
            return f"{turn_text}前行约{int(distance)}米"
    
    def generate_path_directions(self, node_count: int, 
                                intervals: List[float] = None) -> List[Direction]:
        """
        生成整条路径的方向描述
        
        Args:
            node_count: 节点数量
            intervals: 时间间隔列表（可选）
            
        Returns:
            List[Direction]: 方向列表
        """
        directions = []
        
        # 如果没有提供时间间隔，使用默认值
        if intervals is None:
            intervals = [10.0] * (node_count - 1)  # 每段10秒
        
        for i, interval in enumerate(intervals):
            direction = self.estimate_direction(interval)
            directions.append(direction)
        
        return directions


if __name__ == "__main__":
    # 测试方向估算器
    import logging
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 60)
    print("🧭 方向估算器测试")
    print("=" * 60)
    
    estimator = DirectionEstimator()
    
    # 测试单段方向
    print("\n1. 测试单段方向估算:")
    direction = estimator.estimate_direction(15.0)
    print(f"   描述: {direction.description}")
    print(f"   距离: {direction.distance}米")
    print(f"   转向: {direction.turn}")
    
    # 测试路径方向
    print("\n2. 测试路径方向生成:")
    directions = estimator.generate_path_directions(5, [10, 8, 12, 6])
    for i, d in enumerate(directions, 1):
        print(f"   段{i}: {d.description}")
    
    print("\n" + "=" * 60)


