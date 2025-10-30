#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 人流聚集检测模块
分析人群密度判断是否为"拥挤区域"
"""

import logging
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import math
import time
from collections import deque

logger = logging.getLogger(__name__)

class DensityLevel(Enum):
    """密度等级"""
    SPARSE = "sparse"           # 稀疏
    NORMAL = "normal"           # 正常
    CROWDED = "crowded"         # 拥挤
    VERY_CROWDED = "very_crowded"  # 非常拥挤

@dataclass
class DensityDetection:
    """密度检测结果"""
    level: DensityLevel          # 密度等级
    density: float               # 密度值
    person_count: int            # 人数
    region: Tuple[int, int, int, int]  # 区域坐标 (x, y, w, h)
    timestamp: float             # 检测时间戳
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "level": self.level.value,
            "density": self.density,
            "person_count": self.person_count,
            "region": self.region,
            "timestamp": self.timestamp
        }

class CrowdDensityDetector:
    """人流聚集检测器"""
    
    def __init__(self):
        """初始化检测器"""
        self.logger = logging.getLogger(__name__)
        
        # 密度阈值（人/平方米）
        self.density_thresholds = {
            DensityLevel.SPARSE: 0.3,
            DensityLevel.NORMAL: 1.0,
            DensityLevel.CROWDED: 2.0,
            DensityLevel.VERY_CROWDED: 4.0
        }
        
        # 轨迹历史（用于分析密度变化）
        self.trajectory_history = deque(maxlen=30)
        
        # 时间窗口（秒）
        self.time_window = 10.0
        
        self.logger.info("👥 人流聚集检测器初始化完成")
    
    def detect_density(self, positions: List[Tuple[float, float]], 
                      image_shape: Tuple[int, int]) -> DensityDetection:
        """
        检测人群密度
        
        Args:
            positions: 人员位置列表
            image_shape: 图像尺寸 (height, width)
            
        Returns:
            DensityDetection: 检测结果
        """
        if len(positions) == 0:
            return DensityDetection(
                level=DensityLevel.SPARSE,
                density=0.0,
                person_count=0,
                region=(0, 0, image_shape[1], image_shape[0]),
                timestamp=time.time()
            )
        
        # 计算密度
        density = self._calculate_density(positions, image_shape)
        
        # 分析密度等级
        level = self._classify_density(density)
        
        # 计算区域范围
        region = self._calculate_region(positions, image_shape)
        
        # 记录到历史
        self.trajectory_history.append({
            "positions": positions,
            "timestamp": time.time()
        })
        
        result = DensityDetection(
            level=level,
            density=density,
            person_count=len(positions),
            region=region,
            timestamp=time.time()
        )
        
        self.logger.info(f"👥 密度检测: {level.value}, "
                        f"密度={density:.2f}, 人数={len(positions)}")
        
        return result
    
    def check_capability_degradation(self, 
                                     detection_result: DensityDetection,
                                     yolo_failed: bool = False,
                                     front_distance: float = 5.0) -> Dict[str, Any]:
        """
        检查能力降级（人流密集导致识别能力下降）
        
        Args:
            detection_result: 密度检测结果
            yolo_failed: YOLO识别是否失败
            front_distance: 前方检测距离（米）
        
        Returns:
            Dict[str, Any]: 降级检测结果
        """
        degradation_detected = False
        message = None
        
        # 判断条件1: YOLO识别失败
        if yolo_failed:
            degradation_detected = True
            message = "前方为人流密集区域，我可能无法准确识别周围，请您寻求工作人员协助。"
            self.logger.warning("⚠️ YOLO识别失败，触发能力降级提示")
        
        # 判断条件2: 前方5米内人数≥10人
        if detection_result.person_count >= 10 and front_distance <= 5.0:
            degradation_detected = True
            if not message:
                message = "前方为人流密集区域，我可能无法准确识别周围，请您寻求工作人员协助。"
            self.logger.warning(f"⚠️ 检测到密集人群（{detection_result.person_count}人），触发能力降级提示")
        
        # 判断条件3: 密度非常高
        if detection_result.level in [DensityLevel.CROWDED, DensityLevel.VERY_CROWDED]:
            if detection_result.person_count >= 8:
                degradation_detected = True
                if not message:
                    message = "前方为人流密集区域，请注意安全，必要时可寻求协助。"
                self.logger.warning("⚠️ 密度等级为拥挤以上，触发提醒")
        
        return {
            "degradation_detected": degradation_detected,
            "message": message,
            "person_count": detection_result.person_count,
            "density_level": detection_result.level.value,
            "yolo_failed": yolo_failed
        }
    
    def _calculate_density(self, positions: List[Tuple[float, float]],
                          image_shape: Tuple[int, int]) -> float:
        """
        计算人群密度
        
        Args:
            positions: 人员位置
            image_shape: 图像尺寸
            
        Returns:
            float: 密度值（人/平方米）
        """
        if len(positions) == 0:
            return 0.0
        
        # 计算人群覆盖的区域面积
        positions_array = np.array(positions)
        
        # 计算边界框
        min_x, min_y = np.min(positions_array, axis=0)
        max_x, max_y = np.max(positions_array, axis=0)
        
        # 估算检测范围面积（假设检测范围是 5m x 3m）
        detection_area = 5.0 * 3.0  # 平方米
        
        # 计算密度
        density = len(positions) / detection_area
        
        return density
    
    def _classify_density(self, density: float) -> DensityLevel:
        """
        分类密度等级
        
        Args:
            density: 密度值
            
        Returns:
            DensityLevel: 密度等级
        """
        if density < self.density_thresholds[DensityLevel.SPARSE]:
            return DensityLevel.SPARSE
        elif density < self.density_thresholds[DensityLevel.NORMAL]:
            return DensityLevel.NORMAL
        elif density < self.density_thresholds[DensityLevel.CROWDED]:
            return DensityLevel.CROWDED
        else:
            return DensityLevel.VERY_CROWDED
    
    def _calculate_region(self, positions: List[Tuple[float, float]],
                        image_shape: Tuple[int, int]) -> Tuple[int, int, int, int]:
        """
        计算人群区域
        
        Args:
            positions: 人员位置
            image_shape: 图像尺寸
            
        Returns:
            Tuple[int, int, int, int]: (x, y, w, h)
        """
        if len(positions) == 0:
            return (0, 0, image_shape[1], image_shape[0])
        
        positions_array = np.array(positions)
        
        # 计算边界框
        x_min = int(np.min(positions_array[:, 0]))
        y_min = int(np.min(positions_array[:, 1]))
        x_max = int(np.max(positions_array[:, 0]))
        y_max = int(np.max(positions_array[:, 1]))
        
        # 添加一些边距
        margin = 20
        x = max(0, x_min - margin)
        y = max(0, y_min - margin)
        w = min(image_shape[1], x_max + margin) - x
        h = min(image_shape[0], y_max + margin) - y
        
        return (x, y, w, h)
    
    def get_density_trend(self) -> Dict[str, Any]:
        """
        获取密度变化趋势
        
        Returns:
            Dict[str, Any]: 趋势信息
        """
        if len(self.trajectory_history) < 2:
            return {
                "trend": "stable",
                "change_rate": 0.0
            }
        
        # 计算最近的平均密度
        recent_densities = []
        for record in list(self.trajectory_history)[-10:]:
            if record.get('positions'):
                # 简化的密度计算
                density = len(record['positions']) / 15.0  # 假设检测区域15平方米
                recent_densities.append(density)
        
        if len(recent_densities) < 2:
            return {"trend": "stable", "change_rate": 0.0}
        
        # 计算变化率
        change_rate = (recent_densities[-1] - recent_densities[0]) / len(recent_densities)
        
        if change_rate > 0.1:
            trend = "increasing"
        elif change_rate < -0.1:
            trend = "decreasing"
        else:
            trend = "stable"
        
        return {
            "trend": trend,
            "change_rate": float(change_rate),
            "current_density": float(recent_densities[-1])
        }


# 全局检测器实例
global_crowd_detector = CrowdDensityDetector()

def detect_crowd_density(positions: List[Tuple[float, float]], 
                         image_shape: Tuple[int, int]) -> DensityDetection:
    """检测人群密度的便捷函数"""
    return global_crowd_detector.detect_density(positions, image_shape)


if __name__ == "__main__":
    # 测试人流聚集检测
    import logging
    logging.basicConfig(level=logging.INFO)
    
    detector = CrowdDensityDetector()
    image_shape = (480, 640)
    
    # 测试1: 稀疏人群
    print("\n测试1: 稀疏人群")
    positions = [(100, 100), (200, 150)]
    result = detector.detect_density(positions, image_shape)
    print(f"  密度等级: {result.level.value}")
    print(f"  密度值: {result.density:.2f} 人/平方米")
    print(f"  人数: {result.person_count}")
    
    # 测试2: 正常人群
    print("\n测试2: 正常人群")
    positions = [(100, 100), (150, 120), (200, 140), (250, 160)]
    result = detector.detect_density(positions, image_shape)
    print(f"  密度等级: {result.level.value}")
    print(f"  密度值: {result.density:.2f} 人/平方米")
    
    # 测试3: 拥挤人群
    print("\n测试3: 拥挤人群")
    positions = [
        (50, 50), (80, 60), (110, 70),
        (60, 100), (90, 110), (120, 120),
        (70, 150), (100, 160), (130, 170),
        (80, 200), (110, 210), (140, 220)
    ]
    result = detector.detect_density(positions, image_shape)
    print(f"  密度等级: {result.level.value}")
    print(f"  密度值: {result.density:.2f} 人/平方米")
    print(f"  人数: {result.person_count}")
    
    print("\n" + "=" * 60)
