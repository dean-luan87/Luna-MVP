#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 排队检测模块
检测前方是否为排队状态（线性阵列、静止人群）
"""

import logging
import numpy as np
import cv2
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import math
from collections import defaultdict

logger = logging.getLogger(__name__)

class QueueDirection(Enum):
    """排队方向"""
    HORIZONTAL = "horizontal"  # 横向（左右排列）
    VERTICAL = "vertical"      # 纵向（前后排列）
    DIAGONAL = "diagonal"      # 对角
    UNKNOWN = "unknown"        # 未知

@dataclass
class QueueDetection:
    """排队检测结果"""
    detected: bool                    # 是否检测到排队
    direction: QueueDirection         # 排队方向
    person_count: int                 # 人数
    density: float                     # 密度 (人/米)
    queue_length: float               # 队列长度（米）
    confidence: float                  # 置信度
    positions: List[Tuple[float, float]]  # 人员位置列表
    is_moving: bool                   # 是否移动队列
    timestamp: float                  # 检测时间戳
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "detected": self.detected,
            "direction": self.direction.value,
            "person_count": self.person_count,
            "density": self.density,
            "queue_length": self.queue_length,
            "confidence": self.confidence,
            "positions": self.positions,
            "is_moving": self.is_moving,
            "timestamp": self.timestamp
        }

class QueueDetector:
    """排队检测器"""
    
    def __init__(self):
        """初始化排队检测器"""
        self.logger = logging.getLogger(__name__)
        
        # 检测阈值
        self.min_persons = 2              # 最少人数
        self.max_distance_ratio = 0.3     # 最大距离比（用于判断是否成队列）
        self.direction_tolerance = 45     # 方向容差（度）
        self.linearity_threshold = 0.7    # 线性度阈值
        
        # 历史检测记录
        self.history = []
        
        self.logger.info("👥 排队检测器初始化完成")
    
    def detect_queue(self, positions: List[Tuple[float, float]], 
                    image_shape: Tuple[int, int] = None) -> QueueDetection:
        """
        检测排队状态
        
        Args:
            positions: 人员位置列表 [(x1, y1), (x2, y2), ...]
            image_shape: 图像尺寸 (height, width)
            
        Returns:
            QueueDetection: 检测结果
        """
        if len(positions) < self.min_persons:
            return QueueDetection(
                detected=False,
                direction=QueueDirection.UNKNOWN,
                person_count=len(positions),
                density=0.0,
                queue_length=0.0,
                confidence=0.0,
                positions=positions,
                is_moving=False,
                timestamp=0.0
            )
        
        # 分析位置分布
        positions_array = np.array(positions)
        
        # 计算主方向
        direction = self._analyze_direction(positions_array)
        
        # 计算线性度
        linearity = self._calculate_linearity(positions_array, direction)
        
        # 计算队列长度
        queue_length = self._calculate_queue_length(positions_array, direction)
        
        # 估算密度
        density = len(positions) / max(queue_length, 0.1)
        
        # 判断是否移动
        is_moving = self._check_movement()
        
        # 计算置信度
        confidence = self._calculate_confidence(
            len(positions), linearity, queue_length
        )
        
        # 判断是否检测到排队
        detected = (
            len(positions) >= self.min_persons and
            linearity >= self.linearity_threshold and
            confidence > 0.6
        )
        
        result = QueueDetection(
            detected=detected,
            direction=direction,
            person_count=len(positions),
            density=density,
            queue_length=queue_length,
            confidence=confidence,
            positions=positions,
            is_moving=is_moving,
            timestamp=0.0
        )
        
        # 记录到历史
        self.history.append(result)
        
        self.logger.info(f"👥 检测到 {'排队' if detected else '非排队'}: "
                        f"{len(positions)}人, 方向={direction.value}, "
                        f"置信度={confidence:.2f}")
        
        return result
    
    def _analyze_direction(self, positions: np.ndarray) -> QueueDirection:
        """
        分析人员排列方向
        
        Args:
            positions: 位置数组
            
        Returns:
            QueueDirection: 排队方向
        """
        if len(positions) < 2:
            return QueueDirection.UNKNOWN
        
        # 计算所有点之间的向量
        vectors = []
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                vec = positions[j] - positions[i]
                vectors.append(vec)
        
        vectors = np.array(vectors)
        
        # 计算主方向角度
        if len(vectors) > 0:
            angles = np.arctan2(vectors[:, 1], vectors[:, 0]) * 180 / np.pi
            angle_std = np.std(angles)
            
            # 计算平均方向
            mean_angle = np.mean(angles)
            
            # 判断方向
            mean_angle_abs = abs(mean_angle)
            
            if angle_std < 30:  # 方向一致
                if mean_angle_abs < 30 or mean_angle_abs > 150:
                    return QueueDirection.HORIZONTAL
                elif 60 < mean_angle_abs < 120:
                    return QueueDirection.VERTICAL
                else:
                    return QueueDirection.DIAGONAL
        
        return QueueDirection.UNKNOWN
    
    def _calculate_linearity(self, positions: np.ndarray, 
                            direction: QueueDirection) -> float:
        """
        计算线性度
        
        Args:
            positions: 位置数组
            direction: 排队方向
            
        Returns:
            float: 线性度 (0-1)
        """
        if len(positions) < 3:
            return 1.0
        
        try:
            # 使用最小二乘法拟合直线
            if direction == QueueDirection.HORIZONTAL:
                # 拟合 y = ax + b
                coeffs = np.polyfit(positions[:, 0], positions[:, 1], 1)
                line = np.poly1d(coeffs)
                distances = np.abs(positions[:, 1] - line(positions[:, 0]))
            else:
                # 拟合 x = ay + b
                coeffs = np.polyfit(positions[:, 1], positions[:, 0], 1)
                line = np.poly1d(coeffs)
                distances = np.abs(positions[:, 0] - line(positions[:, 1]))
            
            # 计算平均距离
            mean_distance = np.mean(distances)
            max_distance = np.max(np.abs(positions))
            
            # 线性度 = 1 - 平均偏差 / 最大距离
            linearity = 1.0 - (mean_distance / max_distance)
            
            return max(0.0, min(1.0, linearity))
            
        except Exception as e:
            self.logger.error(f"计算线性度失败: {e}")
            return 0.5
    
    def _calculate_queue_length(self, positions: np.ndarray, 
                                direction: QueueDirection) -> float:
        """
        计算队列长度
        
        Args:
            positions: 位置数组
            direction: 排队方向
            
        Returns:
            float: 队列长度
        """
        if len(positions) < 2:
            return 0.0
        
        # 根据方向计算队列长度
        if direction == QueueDirection.HORIZONTAL:
            length = np.max(positions[:, 0]) - np.min(positions[:, 0])
        elif direction == QueueDirection.VERTICAL:
            length = np.max(positions[:, 1]) - np.min(positions[:, 1])
        else:
            # 计算对角线长度
            dx = np.max(positions[:, 0]) - np.min(positions[:, 0])
            dy = np.max(positions[:, 1]) - np.min(positions[:, 1])
            length = math.sqrt(dx * dx + dy * dy)
        
        return float(length)
    
    def _check_movement(self) -> bool:
        """检查队列是否移动"""
        if len(self.history) < 2:
            return False
        
        # 检查最近两次检测的位置变化
        recent = self.history[-2:]
        positions_prev = np.array(recent[0].positions)
        positions_curr = np.array(recent[1].positions)
        
        if len(positions_prev) != len(positions_curr):
            return True
        
        # 计算位置变化
        movement = np.mean(np.abs(positions_curr - positions_prev))
        
        # 如果平均移动距离大于阈值，认为在移动
        return movement > 5.0
    
    def _calculate_confidence(self, person_count: int, 
                             linearity: float, 
                             queue_length: float) -> float:
        """
        计算检测置信度
        
        Args:
            person_count: 人数
            linearity: 线性度
            queue_length: 队列长度
            
        Returns:
            float: 置信度 (0-1)
        """
        # 人数权重
        count_score = min(1.0, person_count / 5.0)
        
        # 线性度权重
        linearity_score = linearity
        
        # 队列长度权重
        length_score = min(1.0, queue_length / 50.0)
        
        # 综合置信度
        confidence = (count_score * 0.4 + linearity_score * 0.4 + length_score * 0.2)
        
        return confidence
    
    def get_queue_statistics(self) -> Dict[str, Any]:
        """
        获取排队统计信息
        
        Returns:
            Dict[str, Any]: 统计信息
        """
        if not self.history:
            return {
                "total_detections": 0,
                "queue_detected_count": 0,
                "average_confidence": 0.0
            }
        
        queue_count = sum(1 for h in self.history if h.detected)
        avg_confidence = np.mean([h.confidence for h in self.history])
        
        return {
            "total_detections": len(self.history),
            "queue_detected_count": queue_count,
            "average_confidence": float(avg_confidence)
        }


# 全局检测器实例
global_queue_detector = QueueDetector()

def detect_queue(positions: List[Tuple[float, float]]) -> QueueDetection:
    """检测排队的便捷函数"""
    return global_queue_detector.detect_queue(positions)


if __name__ == "__main__":
    # 测试排队检测
    import logging
    logging.basicConfig(level=logging.INFO)
    
    detector = QueueDetector()
    
    # 模拟测试：纵向排队
    print("\n测试1: 纵向排队")
    positions = [
        (100, 100),
        (100, 120),
        (100, 140),
        (100, 160)
    ]
    result = detector.detect_queue(positions)
    print(f"  检测结果: {'是' if result.detected else '否'}")
    print(f"  方向: {result.direction.value}")
    print(f"  人数: {result.person_count}")
    print(f"  线性度: {result.confidence:.2f}")
    print(f"  队列长度: {result.queue_length:.1f}")
    
    # 模拟测试：横向排队
    print("\n测试2: 横向排队")
    positions = [
        (50, 100),
        (80, 100),
        (110, 100),
        (140, 100)
    ]
    result = detector.detect_queue(positions)
    print(f"  检测结果: {'是' if result.detected else '否'}")
    print(f"  方向: {result.direction.value}")
    print(f"  人数: {result.person_count}")
    print(f"  线性度: {result.confidence:.2f}")
    print(f"  队列长度: {result.queue_length:.1f}")
    
    # 模拟测试：分散人员
    print("\n测试3: 分散人员")
    positions = [
        (50, 100),
        (120, 80),
        (80, 150),
        (150, 120)
    ]
    result = detector.detect_queue(positions)
    print(f"  检测结果: {'是' if result.detected else '否'}")
    print(f"  方向: {result.direction.value}")
    print(f"  人数: {result.person_count}")
    print(f"  线性度: {result.confidence:.2f}")
    
    # 统计信息
    stats = detector.get_queue_statistics()
    print(f"\n统计信息: {stats}")

