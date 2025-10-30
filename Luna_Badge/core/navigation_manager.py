"""
导航管理模块 - 处理导航中断、恢复、状态监控
"""

import logging
import time
from typing import Optional, Dict, Any
from enum import Enum
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class NavigationStatus(Enum):
    """导航状态"""
    ACTIVE = "active"           # 进行中
    PAUSED = "paused"          # 已暂停
    CANCELLED = "cancelled"    # 已取消
    COMPLETED = "completed"    # 已完成


@dataclass
class NavigationState:
    """导航状态数据"""
    status: NavigationStatus
    destination: str
    start_time: float
    last_movement_time: float
    pause_reason: Optional[str] = None
    cancel_reason: Optional[str] = None


class NavigationManager:
    """导航管理器"""
    
    def __init__(self, idle_timeout: int = 180):
        """
        初始化导航管理器
        
        Args:
            idle_timeout: 空闲超时时间（秒），默认3分钟
        """
        self.idle_timeout = idle_timeout
        self.current_navigation: Optional[NavigationState] = None
        self.last_position: Optional[Dict[str, float]] = None  # {"lat": x, "lng": y}
        self.position_update_time = 0.0
        
        logger.info("🧭 导航管理器初始化完成")
    
    def start_navigation(self, destination: str) -> bool:
        """
        开始导航
        
        Args:
            destination: 目的地
        
        Returns:
            bool: 是否成功启动
        """
        if self.current_navigation and self.current_navigation.status == NavigationStatus.ACTIVE:
            logger.warning("⚠️ 已有导航在进行中")
            return False
        
        self.current_navigation = NavigationState(
            status=NavigationStatus.ACTIVE,
            destination=destination,
            start_time=time.time(),
            last_movement_time=time.time()
        )
        
        logger.info(f"🧭 开始导航到: {destination}")
        return True
    
    def update_position(self, lat: float, lng: float):
        """
        更新当前位置（检测移动）
        
        Args:
            lat: 纬度
            lng: 经度
        """
        current_time = time.time()
        
        # 检测是否移动
        if self.last_position:
            distance = self._calculate_distance(
                self.last_position["lat"], self.last_position["lng"],
                lat, lng
            )
            
            # 如果移动超过3米，视为有移动
            if distance > 3.0:
                if self.current_navigation:
                    self.current_navigation.last_movement_time = current_time
                logger.debug(f"📍 检测到移动: {distance:.1f}米")
        
        self.last_position = {"lat": lat, "lng": lng}
        self.position_update_time = current_time
    
    def check_idle(self) -> bool:
        """
        检查是否空闲（静止）
        
        Returns:
            bool: 是否空闲
        """
        if not self.current_navigation:
            return False
        
        if self.current_navigation.status != NavigationStatus.ACTIVE:
            return False
        
        idle_duration = time.time() - self.current_navigation.last_movement_time
        
        return idle_duration >= self.idle_timeout
    
    def pause_navigation(self, reason: str = "用户暂停") -> bool:
        """
        暂停导航
        
        Args:
            reason: 暂停原因
        
        Returns:
            bool: 是否成功暂停
        """
        if not self.current_navigation:
            logger.warning("⚠️ 当前没有进行中的导航")
            return False
        
        if self.current_navigation.status != NavigationStatus.ACTIVE:
            logger.warning(f"⚠️ 导航状态为 {self.current_navigation.status.value}，无法暂停")
            return False
        
        self.current_navigation.status = NavigationStatus.PAUSED
        self.current_navigation.pause_reason = reason
        
        logger.info(f"⏸️ 导航已暂停: {reason}")
        return True
    
    def resume_navigation(self) -> bool:
        """
        恢复导航
        
        Returns:
            bool: 是否成功恢复
        """
        if not self.current_navigation:
            logger.warning("⚠️ 当前没有导航")
            return False
        
        if self.current_navigation.status != NavigationStatus.PAUSED:
            logger.warning(f"⚠️ 导航状态为 {self.current_navigation.status.value}，无法恢复")
            return False
        
        self.current_navigation.status = NavigationStatus.ACTIVE
        self.current_navigation.last_movement_time = time.time()
        self.current_navigation.pause_reason = None
        
        logger.info("▶️ 导航已恢复")
        return True
    
    def cancel_navigation(self, reason: str = "用户取消") -> bool:
        """
        取消导航
        
        Args:
            reason: 取消原因
        
        Returns:
            bool: 是否成功取消
        """
        if not self.current_navigation:
            logger.warning("⚠️ 当前没有导航")
            return False
        
        self.current_navigation.status = NavigationStatus.CANCELLED
        self.current_navigation.cancel_reason = reason
        
        logger.info(f"❌ 导航已取消: {reason}")
        return True
    
    def complete_navigation(self) -> bool:
        """完成导航"""
        if not self.current_navigation:
            return False
        
        self.current_navigation.status = NavigationStatus.COMPLETED
        logger.info("✅ 导航已完成")
        return True
    
    def get_status(self) -> Optional[Dict[str, Any]]:
        """
        获取当前导航状态
        
        Returns:
            Optional[Dict[str, Any]]: 导航状态信息
        """
        if not self.current_navigation:
            return None
        
        idle_duration = time.time() - self.current_navigation.last_movement_time
        
        return {
            "status": self.current_navigation.status.value,
            "destination": self.current_navigation.destination,
            "start_time": self.current_navigation.start_time,
            "last_movement_time": self.current_navigation.last_movement_time,
            "idle_duration": idle_duration,
            "pause_reason": self.current_navigation.pause_reason,
            "cancel_reason": self.current_navigation.cancel_reason
        }
    
    def _calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """
        计算两点间距离（米）
        
        Args:
            lat1, lng1: 第一个点坐标
            lat2, lng2: 第二个点坐标
        
        Returns:
            float: 距离（米）
        """
        from math import radians, cos, sin, asin, sqrt
        
        # Haversine公式
        R = 6371000  # 地球半径（米）
        
        lat1_rad = radians(lat1)
        lat2_rad = radians(lat2)
        delta_lat = radians(lat2 - lat1)
        delta_lng = radians(lng2 - lng1)
        
        a = sin(delta_lat / 2) ** 2 + \
            cos(lat1_rad) * cos(lat2_rad) * sin(delta_lng / 2) ** 2
        c = 2 * asin(sqrt(a))
        
        return R * c


# 全局导航管理器实例
_global_nav_manager: Optional[NavigationManager] = None


def get_navigation_manager() -> NavigationManager:
    """获取全局导航管理器实例"""
    global _global_nav_manager
    if _global_nav_manager is None:
        _global_nav_manager = NavigationManager()
    return _global_nav_manager


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("🧭 导航管理器测试")
    print("=" * 70)
    
    manager = NavigationManager(idle_timeout=10)  # 10秒超时用于测试
    
    # 开始导航
    manager.start_navigation("虹口医院")
    print(f"\n✅ 导航已启动: {manager.get_status()}")
    
    # 更新位置（模拟移动）
    manager.update_position(31.2304, 121.4737)
    time.sleep(1)
    manager.update_position(31.2305, 121.4738)  # 移动了一点
    print(f"\n📍 位置已更新: {manager.get_status()}")
    
    # 模拟空闲
    print(f"\n⏰ 等待空闲检测...")
    time.sleep(2)
    if manager.check_idle():
        print("⏸️ 检测到空闲")
    else:
        print("✅ 仍在移动")
    
    # 暂停导航
    manager.pause_navigation("等待用户确认")
    print(f"\n⏸️ 导航已暂停: {manager.get_status()}")
    
    # 恢复导航
    manager.resume_navigation()
    print(f"\n▶️ 导航已恢复: {manager.get_status()}")
    
    # 取消导航
    manager.cancel_navigation("用户取消")
    print(f"\n❌ 导航已取消: {manager.get_status()}")
    
    print("\n" + "=" * 70)

