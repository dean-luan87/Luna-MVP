"""
GPS Quality Monitor (v1.4.8 StepB-2)

GPS 抖动治理：质量评估 + 自动降级

核心理念：
不是修 GPS，而是判断"GPS 是否值得信任"
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, List
from collections import deque
import time


class GPSQuality(Enum):
    """GPS 质量等级"""
    GOOD = "good"
    DEGRADED = "degraded"
    INVALID = "invalid"


@dataclass
class GPSReading:
    """GPS 读数数据结构"""
    lat: float
    lng: float
    accuracy_m: float
    timestamp: float


class GPSQualityMonitor:
    """
    GPS 质量监控器
    
    职责：
    - 评估 GPS 读数质量
    - 检测跳点、速度异常、精度劣化
    - 自动降级低质量 GPS
    """
    
    def __init__(
        self,
        event_bus=None,
        max_walking_speed_mps: float = 5.0,
        max_displacement_m: float = 10.0,
        max_displacement_window_s: float = 1.0,
        max_accuracy_m: float = 15.0,
        degraded_threshold: int = 3
    ):
        """
        初始化 GPS 质量监控器
        
        Args:
            event_bus: 事件总线（可选）
            max_walking_speed_mps: 最大步行速度（米/秒，默认 5.0）
            max_displacement_m: 最大位移（米，默认 10.0）
            max_displacement_window_s: 位移检测时间窗（秒，默认 1.0）
            max_accuracy_m: 最大允许精度（米，默认 15.0）
            degraded_threshold: 连续异常阈值（次数，默认 3）
        """
        self.event_bus = event_bus
        self.max_walking_speed_mps = max_walking_speed_mps
        self.max_displacement_m = max_displacement_m
        self.max_displacement_window_s = max_displacement_window_s
        self.max_accuracy_m = max_accuracy_m
        self.degraded_threshold = degraded_threshold
        
        # 历史读数（用于检测跳点和速度异常）
        self._readings: deque = deque(maxlen=10)
        self._current_quality: Optional[GPSQuality] = None
        self._degraded_count: int = 0
    
    def update(self, reading: GPSReading) -> GPSQuality:
        """
        输入一条 GPS 读数，返回当前质量等级
        
        质量判定规则：
        1. 速度异常检测：相邻两次 GPS 计算速度，若速度 > 5 m/s → DEGRADED
        2. 跳点检测：短时间内位移 > 10m / 1s → DEGRADED
        3. 精度劣化：accuracy_m > 15m → DEGRADED
        4. 连续异常：连续 3 次 DEGRADED → INVALID
        
        Args:
            reading: GPS 读数
            
        Returns:
            GPSQuality: GPS 质量等级
        """
        # 添加到历史记录
        self._readings.append(reading)
        
        # 质量评估
        quality = self._assess_quality(reading)
        
        # 如果质量发生变化，发布事件
        if self._current_quality != quality:
            self._current_quality = quality
            self._publish_quality_changed(quality)
        
        return quality
    
    def _assess_quality(self, reading: GPSReading) -> GPSQuality:
        """
        评估 GPS 读数质量
        
        Args:
            reading: GPS 读数
            
        Returns:
            GPSQuality: GPS 质量等级
        """
        # 1. 精度劣化检测
        if reading.accuracy_m > self.max_accuracy_m:
            self._degraded_count += 1
            if self._degraded_count >= self.degraded_threshold:
                return GPSQuality.INVALID
            return GPSQuality.DEGRADED
        
        # 2. 速度异常和跳点检测（需要至少 2 个读数）
        if len(self._readings) >= 2:
            prev_reading = self._readings[-2]
            
            # 计算时间差
            time_delta = reading.timestamp - prev_reading.timestamp
            if time_delta <= 0:
                time_delta = 0.1  # 避免除零
            
            # 计算距离（简化：使用直线距离）
            distance_m = self._calculate_distance(
                prev_reading.lat, prev_reading.lng,
                reading.lat, reading.lng
            )
            
            # 计算速度
            speed_mps = distance_m / time_delta
            
            # 速度异常检测
            if speed_mps > self.max_walking_speed_mps:
                self._degraded_count += 1
                if self._degraded_count >= self.degraded_threshold:
                    return GPSQuality.INVALID
                return GPSQuality.DEGRADED
            
            # 跳点检测（短时间内大位移）
            if time_delta <= self.max_displacement_window_s:
                if distance_m > self.max_displacement_m:
                    self._degraded_count += 1
                    if self._degraded_count >= self.degraded_threshold:
                        return GPSQuality.INVALID
                    return GPSQuality.DEGRADED
        
        # 如果通过所有检测，质量良好
        self._degraded_count = 0
        return GPSQuality.GOOD
    
    def _calculate_distance(
        self,
        lat1: float,
        lng1: float,
        lat2: float,
        lng2: float
    ) -> float:
        """
        计算两点间距离（米，简化版 Haversine）
        
        Args:
            lat1, lng1: 第一个点的经纬度
            lat2, lng2: 第二个点的经纬度
            
        Returns:
            float: 距离（米）
        """
        # 简化版 Haversine 公式（适用于短距离）
        import math
        
        R = 6371000  # 地球半径（米）
        
        dlat = math.radians(lat2 - lat1)
        dlng = math.radians(lng2 - lng1)
        
        a = (
            math.sin(dlat / 2) ** 2 +
            math.cos(math.radians(lat1)) *
            math.cos(math.radians(lat2)) *
            math.sin(dlng / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    def _publish_quality_changed(
        self,
        quality: GPSQuality,
        reason: Optional[str] = None
    ) -> None:
        """
        发布 GPS 质量变化事件
        
        Args:
            quality: GPS 质量等级
            reason: 原因（可选）
        """
        if self.event_bus:
            self.event_bus.publish(
                "nav.gps.quality.changed",
                {
                    "quality": quality,
                    "reason": reason or "quality_assessment",
                }
            )
        else:
            # 如果没有 event_bus，至少打印日志
            print(
                f"[GPS_QUALITY_MONITOR] quality={quality.value} reason={reason or 'quality_assessment'}"
            )
    
    def get_current_quality(self) -> Optional[GPSQuality]:
        """获取当前 GPS 质量"""
        return self._current_quality
    
    def force_degrade(self) -> None:
        """
        强制降级（用于测试或外部触发）
        """
        self._current_quality = GPSQuality.DEGRADED
        self._degraded_count = self.degraded_threshold
        self._publish_quality_changed(GPSQuality.DEGRADED, "force_degraded")






