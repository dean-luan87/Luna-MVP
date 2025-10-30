"""
到达时间预估模块（ETA Calculator）
计算预计到达时间并格式化播报内容
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class RouteSegment:
    """路线段"""
    type: str  # "walk", "bus", "metro", "wait"
    duration_minutes: int
    description: str


@dataclass
class ETAResult:
    """ETA计算结果"""
    current_time: datetime
    total_duration_minutes: int
    estimated_arrival: datetime
    formatted_message: str
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "current_time": self.current_time.isoformat(),
            "total_duration_minutes": self.total_duration_minutes,
            "estimated_arrival": self.estimated_arrival.isoformat(),
            "formatted_message": self.formatted_message
        }


class ETACalculator:
    """ETA计算器"""
    
    def __init__(self):
        """初始化ETA计算器"""
        self.logger = logging.getLogger(__name__)
        
        # 默认速度（米/分钟）
        self.walking_speed = 70  # 约4.2公里/小时
        self.bus_speed = 400     # 约24公里/小时
        self.metro_speed = 800   # 约48公里/小时
        
        # 等待时间估算（分钟）
        self.bus_wait_time = 5
        self.metro_wait_time = 3
        
        self.logger.info("⏰ ETA计算器初始化完成")
    
    def calculate_eta(self, 
                     segments: List[RouteSegment],
                     destination: str,
                     current_time: Optional[datetime] = None) -> ETAResult:
        """
        计算到达时间
        
        Args:
            segments: 路线段列表
            destination: 目的地
            current_time: 当前时间（如果为None则使用系统时间）
        
        Returns:
            ETAResult: ETA计算结果
        """
        if current_time is None:
            current_time = datetime.now()
        
        # 计算总耗时（分钟）
        total_duration = sum(segment.duration_minutes for segment in segments)
        
        # 计算预计到达时间
        estimated_arrival = current_time + timedelta(minutes=total_duration)
        
        # 格式化当前时间
        current_time_str = self._format_time(current_time)
        
        # 格式化预计到达时间
        arrival_time_str = self._format_time(estimated_arrival)
        
        # 格式化总耗时
        duration_str = self._format_duration(total_duration)
        
        # 构建播报消息
        formatted_message = f"现在时间是{current_time_str}，预计耗时{duration_str}，您将于{arrival_time_str}抵达{destination}。"
        
        result = ETAResult(
            current_time=current_time,
            total_duration_minutes=total_duration,
            estimated_arrival=estimated_arrival,
            formatted_message=formatted_message
        )
        
        self.logger.info(f"⏰ ETA计算完成: {total_duration}分钟，预计{arrival_time_str}到达")
        
        return result
    
    def calculate_from_distance(self,
                               distance_meters: float,
                               route_type: str = "walk",
                               current_time: Optional[datetime] = None) -> ETAResult:
        """
        从距离计算ETA（简化版）
        
        Args:
            distance_meters: 距离（米）
            route_type: 路线类型（walk/bus/metro）
            current_time: 当前时间
        
        Returns:
            ETAResult: ETA计算结果
        """
        if current_time is None:
            current_time = datetime.now()
        
        # 根据路线类型选择速度
        speed_map = {
            "walk": self.walking_speed,
            "bus": self.bus_speed,
            "metro": self.metro_speed
        }
        
        speed = speed_map.get(route_type, self.walking_speed)
        
        # 计算步行时间（分钟）
        walking_time = int(distance_meters / speed)
        
        # 如果是公交/地铁，添加等待时间
        wait_time = 0
        if route_type == "bus":
            wait_time = self.bus_wait_time
        elif route_type == "metro":
            wait_time = self.metro_wait_time
        
        total_duration = walking_time + wait_time
        
        # 预计到达时间
        estimated_arrival = current_time + timedelta(minutes=total_duration)
        
        # 格式化消息
        current_time_str = self._format_time(current_time)
        arrival_time_str = self._format_time(estimated_arrival)
        duration_str = self._format_duration(total_duration)
        
        formatted_message = f"现在时间是{current_time_str}，预计耗时{duration_str}，您将于{arrival_time_str}到达。"
        
        return ETAResult(
            current_time=current_time,
            total_duration_minutes=total_duration,
            estimated_arrival=estimated_arrival,
            formatted_message=formatted_message
        )
    
    def _format_time(self, dt: datetime) -> str:
        """
        格式化时间为中文播报格式
        
        Args:
            dt: 日期时间对象
        
        Returns:
            str: 格式化的时间字符串
        """
        hour = dt.hour
        minute = dt.minute
        
        # 判断上午/下午/晚上
        if hour < 6:
            period = "凌晨"
            display_hour = hour
        elif hour < 12:
            period = "上午"
            display_hour = hour
        elif hour < 14:
            period = "中午"
            display_hour = hour
        elif hour < 18:
            period = "下午"
            display_hour = hour - 12 if hour > 12 else hour
        elif hour < 22:
            period = "晚上"
            display_hour = hour - 12
        else:
            period = "晚上"
            display_hour = hour - 12
        
        if minute == 0:
            return f"{period}{display_hour}点"
        else:
            return f"{period}{display_hour}点{minute}分"
    
    def _format_duration(self, minutes: int) -> str:
        """
        格式化耗时
        
        Args:
            minutes: 分钟数
        
        Returns:
            str: 格式化的耗时字符串
        """
        if minutes < 60:
            return f"{minutes}分钟"
        else:
            hours = minutes // 60
            mins = minutes % 60
            if mins == 0:
                return f"{hours}小时"
            else:
                return f"{hours}小时{mins}分钟"


# 全局ETA计算器实例
_global_eta_calculator: Optional[ETACalculator] = None


def get_eta_calculator() -> ETACalculator:
    """获取全局ETA计算器实例"""
    global _global_eta_calculator
    if _global_eta_calculator is None:
        _global_eta_calculator = ETACalculator()
    return _global_eta_calculator


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("⏰ ETA计算器测试")
    print("=" * 70)
    
    calculator = ETACalculator()
    
    # 测试1: 从路线段计算
    print("\n1. 测试路线段计算...")
    segments = [
        RouteSegment("walk", 10, "步行到公交站"),
        RouteSegment("wait", 5, "等车"),
        RouteSegment("bus", 20, "乘公交"),
        RouteSegment("walk", 10, "步行到目的地")
    ]
    
    result = calculator.calculate_eta(segments, "虹口医院")
    print(f"   当前时间: {result.current_time.strftime('%H:%M')}")
    print(f"   预计耗时: {result.total_duration_minutes}分钟")
    print(f"   预计到达: {result.estimated_arrival.strftime('%H:%M')}")
    print(f"   播报消息: {result.formatted_message}")
    
    # 测试2: 从距离计算
    print("\n2. 测试距离计算...")
    result2 = calculator.calculate_from_distance(5000, "walk", datetime.now())
    print(f"   播报消息: {result2.formatted_message}")
    
    print("\n" + "=" * 70)
