"""
导航管理模块 - 处理导航中断、恢复、状态监控
支持实时语音播报（转弯、障碍提示等）
"""

import logging
import time
from typing import Optional, Dict, Any, List, Callable
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
    route_segments: Optional[List[Dict[str, Any]]] = None  # 路径段列表
    current_segment_index: int = 0  # 当前路径段索引
    last_guidance_time: float = 0.0  # 上次播报时间
    guidance_interval: float = 50.0  # 播报间隔（米）


class NavigationManager:
    """导航管理器"""
    
    def __init__(self, idle_timeout: int = 180, tts_callback: Optional[Callable] = None):
        """
        初始化导航管理器
        
        Args:
            idle_timeout: 空闲超时时间（秒），默认3分钟
            tts_callback: TTS播报回调函数，接收(text: str, style: str)参数
        """
        self.idle_timeout = idle_timeout
        self.current_navigation: Optional[NavigationState] = None
        self.last_position: Optional[Dict[str, float]] = None  # {"lat": x, "lng": y}
        self.position_update_time = 0.0
        self.tts_callback = tts_callback  # TTS播报回调
        
        # 导航提示相关
        self.guidance_distance_threshold = 10.0  # 距离节点多少米时播报（米）
        self.last_guidance_node = None  # 上次播报的节点
        
        logger.info("🧭 导航管理器初始化完成")
    
    def start_navigation(self, destination: str, route_segments: Optional[List[Dict[str, Any]]] = None) -> bool:
        """
        开始导航
        
        Args:
            destination: 目的地
            route_segments: 路径段列表（可选）
        
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
            last_movement_time=time.time(),
            route_segments=route_segments or [],
            current_segment_index=0,
            last_guidance_time=time.time()
        )
        
        logger.info(f"🧭 开始导航到: {destination}")
        
        # 播报开始导航
        if self.tts_callback:
            try:
                self.tts_callback(f"开始导航到{destination}，请跟随指引", "calm")
            except Exception as e:
                logger.warning(f"⚠️ 语音播报失败: {e}")
        
        return True
    
    def update_position(self, lat: float, lng: float, detected_hazards: Optional[List[Dict[str, Any]]] = None):
        """
        更新当前位置（检测移动、转弯、障碍）
        
        Args:
            lat: 纬度
            lng: 经度
            detected_hazards: 检测到的障碍/危险列表（可选）
        """
        current_time = time.time()
        
        # 检测是否移动
        distance_moved = 0.0
        if self.last_position:
            distance_moved = self._calculate_distance(
                self.last_position["lat"], self.last_position["lng"],
                lat, lng
            )
            
            # 如果移动超过3米，视为有移动
            if distance_moved > 3.0:
                if self.current_navigation:
                    self.current_navigation.last_movement_time = current_time
                logger.debug(f"📍 检测到移动: {distance_moved:.1f}米")
        
        self.last_position = {"lat": lat, "lng": lng}
        self.position_update_time = current_time
        
        # 如果导航正在进行中，检查是否需要播报
        if self.current_navigation and self.current_navigation.status == NavigationStatus.ACTIVE:
            self._check_and_broadcast_guidance(distance_moved, detected_hazards)
    
    def _check_and_broadcast_guidance(self, distance_moved: float, detected_hazards: Optional[List[Dict[str, Any]]]):
        """检查并播报导航指引"""
        if not self.current_navigation or not self.tts_callback:
            return
        
        current_time = time.time()
        nav = self.current_navigation
        
        # 检查是否有障碍需要播报
        if detected_hazards:
            for hazard in detected_hazards:
                severity = hazard.get('severity', 'low')
                hazard_type = hazard.get('type', '障碍')
                
                # 只播报中等及以上严重程度的障碍
                if severity in ['medium', 'high', 'critical']:
                    message = self._generate_hazard_message(hazard_type, severity)
                    try:
                        self.tts_callback(message, "urgent")
                        nav.last_guidance_time = current_time
                        logger.info(f"🔊 障碍播报: {message}")
                        return  # 优先播报障碍
                    except Exception as e:
                        logger.warning(f"⚠️ 障碍播报失败: {e}")
        
        # 检查路径指引
        if nav.route_segments and nav.current_segment_index < len(nav.route_segments):
            segment = nav.route_segments[nav.current_segment_index]
            end_node = segment.get('end_node', '')
            
            # 检查是否接近下一个节点（需要转弯）
            # 这里简化处理：如果移动距离超过阈值，播报下一个指引
            if distance_moved > nav.guidance_interval:
                guidance_message = self._generate_turn_guidance(segment)
                if guidance_message:
                    try:
                        self.tts_callback(guidance_message, "calm")
                        nav.last_guidance_time = current_time
                        logger.info(f"🔊 导航指引: {guidance_message}")
                    except Exception as e:
                        logger.warning(f"⚠️ 导航指引播报失败: {e}")
    
    def _generate_turn_guidance(self, segment: Dict[str, Any]) -> Optional[str]:
        """生成转弯指引消息"""
        start_node = segment.get('start_node', '')
        end_node = segment.get('end_node', '')
        distance = segment.get('distance', 0.0)
        
        # 尝试从节点信息中提取方向信息
        # 这里可以根据实际数据结构调整
        if distance > 0:
            if distance < 20:
                return f"前方{int(distance)}米到达{end_node}"
            else:
                return f"继续前行，前往{end_node}"
        
        return None
    
    def _generate_hazard_message(self, hazard_type: str, severity: str) -> str:
        """生成障碍提示消息"""
        severity_map = {
            'medium': '请注意',
            'high': '小心',
            'critical': '危险'
        }
        prefix = severity_map.get(severity, '请注意')
        
        type_map = {
            'step': '台阶',
            'obstacle': '障碍物',
            'hazard': '危险区域',
            'edge': '边缘',
            'stairs': '楼梯'
        }
        hazard_name = type_map.get(hazard_type.lower(), hazard_type)
        
        return f"{prefix}，前方有{hazard_name}"
    
    def advance_to_next_segment(self):
        """前进到下一个路径段"""
        if not self.current_navigation:
            return False
        
        nav = self.current_navigation
        if nav.route_segments and nav.current_segment_index < len(nav.route_segments) - 1:
            nav.current_segment_index += 1
            logger.info(f"📍 前进到路径段 {nav.current_segment_index + 1}/{len(nav.route_segments)}")
            return True
        
        return False
    
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
        
        # 播报完成消息
        if self.tts_callback:
            try:
                self.tts_callback(f"已到达目的地{self.current_navigation.destination}", "cheerful")
            except Exception as e:
                logger.warning(f"⚠️ 完成播报失败: {e}")
        
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
        
        nav = self.current_navigation
        idle_duration = time.time() - nav.last_movement_time
        
        status_dict = {
            "status": nav.status.value,
            "destination": nav.destination,
            "start_time": nav.start_time,
            "last_movement_time": nav.last_movement_time,
            "idle_duration": idle_duration,
            "pause_reason": nav.pause_reason,
            "cancel_reason": nav.cancel_reason
        }
        
        # 添加路径信息
        if nav.route_segments:
            status_dict["route_segments"] = nav.route_segments
            status_dict["current_segment_index"] = nav.current_segment_index
            status_dict["total_segments"] = len(nav.route_segments)
            if nav.current_segment_index < len(nav.route_segments):
                status_dict["current_segment"] = nav.route_segments[nav.current_segment_index]
                status_dict["next_node"] = nav.route_segments[nav.current_segment_index].get('end_node', '')
        
        return status_dict
    
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

