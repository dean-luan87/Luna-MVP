"""
公交方向正确性判断模块
判断用户乘坐的公交车是否方向正确
"""

import logging
import math
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum
import time

logger = logging.getLogger(__name__)


class BusDirectionStatus(Enum):
    """公交方向状态"""
    CORRECT = "correct"           # 方向正确
    WRONG_DIRECTION = "wrong_direction"  # 方向错误
    WRONG_LINE = "wrong_line"     # 线路错误
    UNCERTAIN = "uncertain"       # 无法确定


@dataclass
class BusInfo:
    """公交信息"""
    line_number: str              # 线路号（如"123路"）
    direction: str                # 方向（如"往XX站"）
    current_position: Tuple[float, float]  # 当前位置 (lat, lng)
    target_direction: Tuple[float, float]  # 目标方向向量 (lat, lng)


@dataclass
class DirectionCheckResult:
    """方向检查结果"""
    status: BusDirectionStatus
    confidence: float
    message: Optional[str] = None
    gps_trajectory_angle: Optional[float] = None  # GPS轨迹角度
    target_angle: Optional[float] = None  # 目标角度
    angle_difference: Optional[float] = None  # 角度差
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "status": self.status.value,
            "confidence": self.confidence,
            "message": self.message,
            "gps_trajectory_angle": self.gps_trajectory_angle,
            "target_angle": self.target_angle,
            "angle_difference": self.angle_difference
        }


class BusDirectionChecker:
    """公交方向检查器"""
    
    def __init__(self):
        """初始化公交方向检查器"""
        self.logger = logging.getLogger(__name__)
        
        # GPS轨迹历史（用于分析方向）
        self.gps_history: List[Tuple[float, float, float]] = []  # [(lat, lng, timestamp), ...]
        self.history_size = 10
        
        # 角度阈值（度）
        self.angle_threshold = 90.0  # 90度以上视为方向相反
        
        self.logger.info("🚌 公交方向检查器初始化完成")
    
    def check_bus_direction(self,
                           bus_info: BusInfo,
                           target_station_position: Tuple[float, float],
                           current_gps: Tuple[float, float]) -> DirectionCheckResult:
        """
        检查公交方向是否正确
        
        Args:
            bus_info: 公交信息
            target_station_position: 目标站点位置 (lat, lng)
            current_gps: 当前GPS位置 (lat, lng)
        
        Returns:
            DirectionCheckResult: 方向检查结果
        """
        # 更新GPS历史
        self.gps_history.append((current_gps[0], current_gps[1], time.time()))
        if len(self.gps_history) > self.history_size:
            self.gps_history.pop(0)
        
        # 检查1: 公交线路号是否匹配
        # TODO: 实际应该与导航目标中的线路号比较
        line_match = True  # 简化：假设匹配
        
        # 检查2: GPS轨迹方向 vs 目标方向
        trajectory_check = self._check_gps_trajectory(
            target_station_position,
            current_gps
        )
        
        # 综合判断
        if not line_match:
            return DirectionCheckResult(
                status=BusDirectionStatus.WRONG_LINE,
                confidence=0.9,
                message="您上的车线路与目标不一致，建议您在下一站下车换乘。",
                gps_trajectory_angle=trajectory_check.get("gps_trajectory_angle"),
                target_angle=trajectory_check.get("target_angle"),
                angle_difference=trajectory_check.get("angle_difference")
            )
        
        if trajectory_check["angle_difference"] and trajectory_check["angle_difference"] > self.angle_threshold:
            return DirectionCheckResult(
                status=BusDirectionStatus.WRONG_DIRECTION,
                confidence=trajectory_check["confidence"],
                message="您上的车方向与目标不一致，建议您在下一站下车换乘。",
                gps_trajectory_angle=trajectory_check.get("gps_trajectory_angle"),
                target_angle=trajectory_check.get("target_angle"),
                angle_difference=trajectory_check.get("angle_difference")
            )
        
        if trajectory_check["angle_difference"] and trajectory_check["angle_difference"] > 45.0:
            return DirectionCheckResult(
                status=BusDirectionStatus.UNCERTAIN,
                confidence=trajectory_check["confidence"],
                message="方向可能存在偏差，请注意观察路线。",
                gps_trajectory_angle=trajectory_check.get("gps_trajectory_angle"),
                target_angle=trajectory_check.get("target_angle"),
                angle_difference=trajectory_check.get("angle_difference")
            )
        
        return DirectionCheckResult(
            status=BusDirectionStatus.CORRECT,
            confidence=0.95,
            message=None,
            gps_trajectory_angle=trajectory_check.get("gps_trajectory_angle"),
            target_angle=trajectory_check.get("target_angle"),
            angle_difference=trajectory_check.get("angle_difference")
        )
    
    def _check_gps_trajectory(self,
                              target_position: Tuple[float, float],
                              current_position: Tuple[float, float]) -> Dict[str, Any]:
        """
        检查GPS轨迹方向
        
        Args:
            target_position: 目标位置 (lat, lng)
            current_position: 当前位置 (lat, lng)
        
        Returns:
            Dict[str, Any]: 轨迹检查结果
        """
        if len(self.gps_history) < 2:
            return {
                "confidence": 0.5,
                "gps_trajectory_angle": None,
                "target_angle": None,
                "angle_difference": None
            }
        
        # 计算GPS移动方向（最近两个点）
        recent_points = self.gps_history[-2:]
        p1_lat, p1_lng = recent_points[0][0], recent_points[0][1]
        p2_lat, p2_lng = recent_points[1][0], recent_points[1][1]
        
        # 计算GPS轨迹角度
        gps_angle = self._calculate_bearing(p1_lat, p1_lng, p2_lat, p2_lng)
        
        # 计算目标方向角度
        target_angle = self._calculate_bearing(
            current_position[0], current_position[1],
            target_position[0], target_position[1]
        )
        
        # 计算角度差
        angle_diff = abs(gps_angle - target_angle)
        if angle_diff > 180:
            angle_diff = 360 - angle_diff
        
        confidence = 1.0 - (angle_diff / 180.0)  # 角度差越大，置信度越低
        
        return {
            "confidence": max(0.3, confidence),
            "gps_trajectory_angle": gps_angle,
            "target_angle": target_angle,
            "angle_difference": angle_diff
        }
    
    def _calculate_bearing(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """
        计算两点间的方位角（度）
        
        Args:
            lat1, lng1: 起点坐标
            lat2, lng2: 终点坐标
        
        Returns:
            float: 方位角（0-360度）
        """
        from math import radians, degrees, atan2, sin, cos
        
        lat1_rad = radians(lat1)
        lat2_rad = radians(lat2)
        delta_lng = radians(lng2 - lng1)
        
        y = sin(delta_lng) * cos(lat2_rad)
        x = cos(lat1_rad) * sin(lat2_rad) - sin(lat1_rad) * cos(lat2_rad) * cos(delta_lng)
        
        bearing = atan2(y, x)
        bearing_degrees = degrees(bearing)
        bearing_normalized = (bearing_degrees + 360) % 360
        
        return bearing_normalized
    
    def update_bus_status(self, bus_info: BusInfo):
        """更新公交信息"""
        self.current_bus = bus_info
        self.logger.info(f"🚌 公交信息已更新: {bus_info.line_number} - {bus_info.direction}")
    
    def reset_history(self):
        """重置GPS历史"""
        self.gps_history = []
        self.logger.debug("🔄 GPS历史已重置")


# 全局公交方向检查器实例
_global_bus_checker: Optional[BusDirectionChecker] = None


def get_bus_direction_checker() -> BusDirectionChecker:
    """获取全局公交方向检查器实例"""
    global _global_bus_checker
    if _global_bus_checker is None:
        _global_bus_checker = BusDirectionChecker()
    return _global_bus_checker


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("🚌 公交方向检查器测试")
    print("=" * 70)
    
    checker = get_bus_direction_checker()
    
    # 模拟GPS轨迹（方向错误）
    bus_info = BusInfo(
        line_number="123路",
        direction="往XX站",
        current_position=(31.2304, 121.4737),
        target_direction=(31.2400, 121.4800)
    )
    
    # 模拟GPS移动（与目标方向相反）
    target_station = (31.2400, 121.4800)
    
    print("\n1. 模拟GPS轨迹（方向正确）...")
    for i in range(5):
        lat = 31.2304 + i * 0.002
        lng = 121.4737 + i * 0.002
        result = checker.check_bus_direction(bus_info, target_station, (lat, lng))
    
    final_result = checker.check_bus_direction(bus_info, target_station, (31.2404, 121.4817))
    print(f"   状态: {final_result.status.value}")
    if final_result.message:
        print(f"   消息: {final_result.message}")
    
    print("\n2. 模拟GPS轨迹（方向错误）...")
    checker.reset_history()
    for i in range(5):
        lat = 31.2304 - i * 0.002  # 反方向移动
        lng = 121.4737 - i * 0.002
        result = checker.check_bus_direction(bus_info, target_station, (lat, lng))
    
    final_result2 = checker.check_bus_direction(bus_info, target_station, (31.2216, 121.4617))
    print(f"   状态: {final_result2.status.value}")
    if final_result2.message:
        print(f"   消息: {final_result2.message}")
    
    print("\n" + "=" * 70)
