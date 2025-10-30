#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 隐私区域识别与摄像头锁定模块
当进入洗手间等隐私区域时，自动锁定摄像头
"""

import logging
import time
import json
import os
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import threading

logger = logging.getLogger(__name__)

class PrivacyZoneType(Enum):
    """隐私区域类型"""
    TOILET = "toilet"               # 洗手间
    CHANGING_ROOM = "changing_room" # 更衣室
    LOCKER_ROOM = "locker_room"     # 储物室
    HOSPITAL_ROOM = "hospital_room" # 病房

class LockStatus(Enum):
    """锁定状态"""
    UNLOCKED = "unlocked"           # 未锁定
    LOCKED = "locked"               # 已锁定
    LOCKED_PERMANENTLY = "locked_permanently"  # 永久锁定

@dataclass
class GPSCoordinate:
    """GPS坐标"""
    latitude: float    # 纬度
    longitude: float   # 经度
    altitude: float = 0.0  # 海拔（可选）

@dataclass
class PrivacyZonePOI:
    """隐私区域POI点"""
    zone_type: PrivacyZoneType
    name: str
    position: GPSCoordinate
    radius: float = 5.0  # 触发半径（米）

@dataclass
class LockEvent:
    """锁定事件日志"""
    timestamp: float
    reason: str                    # 锁定原因
    zone_type: str                 # 区域类型
    gps_location: Optional[Dict[str, float]]  # GPS位置
    detection_method: str          # 检测方法 (GPS/Visual)
    is_permanent: bool             # 是否永久锁定
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)

class PrivacyProtectionManager:
    """隐私保护管理器"""
    
    def __init__(self, log_file: str = "logs/privacy_locks.json"):
        """
        初始化隐私保护管理器
        
        Args:
            log_file: 日志文件路径
        """
        self.log_file = log_file
        self.lock_status = LockStatus.UNLOCKED
        self.lock_reason = ""
        self.lock_timestamp = 0.0
        
        # GPS相关
        self.current_gps: Optional[GPSCoordinate] = None
        self.privacy_pois: list[PrivacyZonePOI] = []
        
        # 摄像头控制
        self.camera_locked = False
        self.camera_lock_permanent = False
        
        # 事件日志
        self.lock_events: list[LockEvent] = []
        
        # 线程锁
        self.lock_mutex = threading.Lock()
        
        self.logger = logging.getLogger(__name__)
        self._load_lock_events()
        self.logger.info("🔒 隐私保护管理器初始化完成")
    
    def update_gps(self, latitude: float, longitude: float, altitude: float = 0.0):
        """
        更新GPS位置
        
        Args:
            latitude: 纬度
            longitude: 经度
            altitude: 海拔
        """
        with self.lock_mutex:
            self.current_gps = GPSCoordinate(latitude, longitude, altitude)
            self.logger.debug(f"📍 GPS更新: ({latitude}, {longitude})")
    
    def add_privacy_poi(self, poi: PrivacyZonePOI):
        """
        添加隐私区域POI
        
        Args:
            poi: POI点信息
        """
        self.privacy_pois.append(poi)
        self.logger.info(f"➕ 添加隐私区域POI: {poi.name} ({poi.zone_type.value})")
    
    def check_gps_proximity(self) -> Tuple[bool, Optional[PrivacyZonePOI]]:
        """
        检查GPS是否在隐私区域附近
        
        Returns:
            Tuple[bool, PrivacyZonePOI]: (是否触发, POI信息)
        """
        if not self.current_gps:
            return False, None
        
        for poi in self.privacy_pois:
            distance = self._calculate_distance(
                self.current_gps.latitude, self.current_gps.longitude,
                poi.position.latitude, poi.position.longitude
            )
            
            if distance <= poi.radius:
                self.logger.warning(f"⚠️ GPS触发: 距离 {poi.name} {distance:.2f}米")
                return True, poi
        
        return False, None
    
    def check_visual_privacy_zone(self, image) -> Tuple[bool, PrivacyZoneType]:
        """
        视觉检测隐私区域
        
        Args:
            image: 输入图像
            
        Returns:
            Tuple[bool, PrivacyZoneType]: (是否检测到, 区域类型)
        """
        # 这里应该调用洗手间识别模块
        # from core.signboard_detector import detect_signboards
        # results = detect_signboards(image)
        # for result in results:
        #     if result.type == SignboardType.TOILET:
        #         return True, PrivacyZoneType.TOILET
        
        # 暂时返回False
        return False, PrivacyZoneType.TOILET
    
    def trigger_privacy_lock(self, detection_method: str, zone_type: PrivacyZoneType,
                           reason: str = "", is_permanent: bool = False):
        """
        触发隐私锁定
        
        Args:
            detection_method: 检测方法 (GPS/Visual)
            zone_type: 隐私区域类型
            reason: 锁定原因
            is_permanent: 是否永久锁定
        """
        with self.lock_mutex:
            # 如果已经是永久锁定，不能再被触发
            if self.camera_lock_permanent:
                self.logger.warning("⚠️ 摄像头已永久锁定，无法再次触发")
                return
            
            # 检查是否已经锁定
            if self.camera_locked:
                self.logger.info("ℹ️ 摄像头已经处于锁定状态")
                return
            
            # 锁定摄像头
            self.camera_locked = True
            self.camera_lock_permanent = is_permanent
            self.lock_status = LockStatus.LOCKED_PERMANENTLY if is_permanent else LockStatus.LOCKED
            self.lock_timestamp = time.time()
            self.lock_reason = reason or f"{detection_method}检测到{zone_type.value}"
            
            # 记录事件
            gps_loc = None
            if self.current_gps:
                gps_loc = {
                    "latitude": self.current_gps.latitude,
                    "longitude": self.current_gps.longitude,
                    "altitude": self.current_gps.altitude
                }
            
            event = LockEvent(
                timestamp=self.lock_timestamp,
                reason=self.lock_reason,
                zone_type=zone_type.value,
                gps_location=gps_loc,
                detection_method=detection_method,
                is_permanent=is_permanent
            )
            
            self.lock_events.append(event)
            self._save_lock_event(event)
            
            self.logger.warning(f"🔒 摄像头已锁定: {self.lock_reason}")
            
            # 可选：语音播报
            # self._announce_privacy_lock()
    
    def check_privacy_zone(self, image=None) -> bool:
        """
        检查是否在隐私区域（GPS或视觉）
        
        Args:
            image: 可选，输入图像用于视觉检测
            
        Returns:
            bool: 是否触发锁定
        """
        # 方法1: GPS检测
        gps_triggered, poi = self.check_gps_proximity()
        if gps_triggered and poi:
            self.trigger_privacy_lock(
                detection_method="GPS",
                zone_type=poi.zone_type,
                reason=f"GPS接近{poi.name}",
                is_permanent=False  # GPS检测可以非永久锁定
            )
            return True
        
        # 方法2: 视觉检测
        if image is not None:
            visual_triggered, zone_type = self.check_visual_privacy_zone(image)
            if visual_triggered:
                self.trigger_privacy_lock(
                    detection_method="Visual",
                    zone_type=zone_type,
                    reason=f"视觉识别到{zone_type.value}标识",
                    is_permanent=True  # 视觉检测永久锁定
                )
                return True
        
        return False
    
    def is_camera_locked(self) -> bool:
        """检查摄像头是否已锁定"""
        return self.camera_locked
    
    def is_camera_permanently_locked(self) -> bool:
        """检查摄像头是否永久锁定"""
        return self.camera_lock_permanent
    
    def try_unlock_camera(self) -> bool:
        """
        尝试解锁摄像头（仅当非永久锁定时有效）
        
        Returns:
            bool: 是否解锁成功
        """
        with self.lock_mutex:
            if self.camera_lock_permanent:
                self.logger.warning("❌ 摄像头永久锁定，无法解锁")
                return False
            
            if not self.camera_locked:
                self.logger.info("ℹ️ 摄像头未锁定")
                return True
            
            # 可以添加时间检查逻辑
            # 例如：锁定后需要等待一定时间才能解锁
            lock_duration = time.time() - self.lock_timestamp
            
            # 如果锁定时间超过5分钟，允许解锁
            if lock_duration > 300:
                self.camera_locked = False
                self.lock_status = LockStatus.UNLOCKED
                self.lock_reason = ""
                self.logger.info("✅ 摄像头已解锁")
                return True
            else:
                self.logger.info(f"⏳ 需要等待 {300 - lock_duration:.0f} 秒才能解锁")
                return False
    
    def force_unlock_camera(self, reason: str = "管理员解锁"):
        """
        强制解锁摄像头（管理员权限）
        
        Args:
            reason: 解锁原因
        """
        with self.lock_mutex:
            self.camera_locked = False
            self.camera_lock_permanent = False
            self.lock_status = LockStatus.UNLOCKED
            self.lock_reason = ""
            
            # 记录解锁事件
            event = LockEvent(
                timestamp=time.time(),
                reason=f"解锁: {reason}",
                zone_type="none",
                gps_location=None,
                detection_method="Admin",
                is_permanent=False
            )
            
            self.lock_events.append(event)
            self._save_lock_event(event)
            
            self.logger.warning(f"🔓 摄像头已强制解锁: {reason}")
    
    def get_lock_status(self) -> Dict[str, Any]:
        """获取锁定状态"""
        return {
            "locked": self.camera_locked,
            "permanently_locked": self.camera_lock_permanent,
            "lock_reason": self.lock_reason,
            "lock_timestamp": self.lock_timestamp,
            "lock_duration": time.time() - self.lock_timestamp if self.camera_locked else 0
        }
    
    def get_lock_history(self, limit: int = 10) -> list[LockEvent]:
        """
        获取锁定历史记录
        
        Args:
            limit: 返回记录数量限制
            
        Returns:
            list[LockEvent]: 锁定事件列表
        """
        return self.lock_events[-limit:] if limit > 0 else self.lock_events
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        计算两点间的距离（米）
        
        Args:
            lat1, lon1: 点1的经纬度
            lat2, lon2: 点2的经纬度
            
        Returns:
            float: 距离（米）
        """
        from math import radians, cos, sin, asin, sqrt
        
        # 转换为弧度
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        
        # Haversine公式
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371000  # 地球半径（米）
        
        return c * r
    
    def _save_lock_event(self, event: LockEvent):
        """保存锁定事件到日志"""
        try:
            os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
            
            # 读取现有事件
            events = []
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    events = json.load(f)
            
            # 添加新事件
            events.append(event.to_dict())
            
            # 保存（保留最近100条记录）
            events = events[-100:]
            
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(events, f, ensure_ascii=False, indent=2)
            
        except Exception as e:
            self.logger.error(f"❌ 保存锁定事件失败: {e}")
    
    def _load_lock_events(self):
        """加载锁定事件历史"""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    events_data = json.load(f)
                    for event_data in events_data:
                        event = LockEvent(**event_data)
                        self.lock_events.append(event)
                self.logger.info(f"📂 加载了 {len(self.lock_events)} 条锁定事件记录")
        except Exception as e:
            self.logger.error(f"❌ 加载锁定事件失败: {e}")
    
    def _announce_privacy_lock(self):
        """语音播报隐私锁定"""
        try:
            # 集成语音播报模块
            announcement = "进入隐私区，摄像头已关闭"
            self.logger.info(f"🔊 播报: {announcement}")
            
            # 实际实现应该调用TTS模块
            # from hal_mac.hardware_mac import speak
            # asyncio.run(speak(announcement))
            
        except Exception as e:
            self.logger.error(f"❌ 语音播报失败: {e}")


# 全局隐私保护管理器实例
global_privacy_manager = PrivacyProtectionManager()

def check_privacy_zone(image=None) -> bool:
    """检查隐私区域的便捷函数"""
    return global_privacy_manager.check_privacy_zone(image)

def is_camera_locked() -> bool:
    """检查摄像头是否锁定的便捷函数"""
    return global_privacy_manager.is_camera_locked()


if __name__ == "__main__":
    # 测试隐私保护管理器
    import logging
    logging.basicConfig(level=logging.INFO)
    
    # 创建管理器
    manager = PrivacyProtectionManager()
    
    # 模拟GPS更新
    print("📍 模拟GPS位置更新...")
    manager.update_gps(39.9042, 116.4074)  # 北京天安门
    
    # 添加隐私区域POI
    print("\n➕ 添加隐私区域POI...")
    toilet_poi = PrivacyZonePOI(
        zone_type=PrivacyZoneType.TOILET,
        name="公共洗手间",
        position=GPSCoordinate(39.9040, 116.4070),
        radius=5.0
    )
    manager.add_privacy_poi(toilet_poi)
    
    # 模拟GPS接近
    print("\n📍 模拟GPS接近隐私区域...")
    manager.update_gps(39.9039, 116.4071)  # 接近洗手间
    
    # 检查隐私区域
    print("\n🔍 检查隐私区域...")
    triggered = manager.check_privacy_zone()
    print(f"触发结果: {triggered}")
    
    # 检查锁定状态
    print("\n🔒 检查锁定状态...")
    status = manager.get_lock_status()
    print(f"锁定状态: {status}")
    
    # 尝试解锁
    print("\n🔓 尝试解锁摄像头...")
    unlocked = manager.try_unlock_camera()
    print(f"解锁结果: {unlocked}")
    
    # 强制解锁
    print("\n🔓 强制解锁摄像头...")
    manager.force_unlock_camera("管理员测试解锁")
    
    # 获取锁定历史
    print("\n📜 获取锁定历史...")
    history = manager.get_lock_history(5)
    for event in history:
        print(f"  - {event.to_dict()}")
