"""
导航上下文 (NavigationContext) v1.2.0
导航状态容器，存储当前导航的所有状态信息
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field


@dataclass
class NavigationContext:
    """
    导航上下文
    存储导航过程中的所有状态信息，供策略系统使用
    """
    
    # ========== 位置信息 ==========
    position: Optional[Dict[str, float]] = None  # GPS or SLAM位置 {"lat": 0.0, "lng": 0.0}
    heading: Optional[float] = None  # 朝向角度（度）
    
    # ========== 路径信息 ==========
    current_step: Optional[Dict[str, Any]] = None  # 当前步骤信息
    next_step: Optional[Dict[str, Any]] = None  # 下一步骤信息
    route_segments: List[Dict[str, Any]] = field(default_factory=list)  # 路径段列表
    current_step_index: int = 0  # 当前步骤索引
    
    # ========== 环境信息 ==========
    hazards: List[Dict[str, Any]] = field(default_factory=list)  # 障碍物/危险信息
    construction: bool = False  # 是否检测到施工
    people_density: float = 0.0  # 人群密度 (0.0-1.0)
    traffic_light_state: Optional[str] = None  # 红绿灯状态: "RED", "GREEN", "YELLOW", None
    path_blocked: bool = False  # 路径是否被阻塞
    
    # ========== 导航状态 ==========
    need_reroute: bool = False  # 是否需要重新规划
    off_route_distance: float = 0.0  # 偏离路线距离（米）
    heading_error: float = 0.0  # 朝向误差（度）
    
    # ========== 特殊场景 ==========
    bus_direction_ok: bool = True  # 公交方向是否正确
    current_zone: Optional[str] = None  # 当前区域（如"东区"、"3楼"）
    target_zone: Optional[str] = None  # 目标区域
    is_indoor: bool = False  # 是否在室内
    is_subway: bool = False  # 是否在地铁站
    
    # ========== 情绪状态 ==========
    emotion_state: Optional[str] = None  # 情绪状态: "normal", "anxious", "panic", "calm"
    
    # ========== 视觉检测结果 ==========
    vision_data: Dict[str, Any] = field(default_factory=dict)  # 视觉检测结果
    door_detected: bool = False  # 是否检测到门
    room_num: Optional[str] = None  # 门牌号
    department: Optional[str] = None  # 科室名称
    step_detected: bool = False  # 是否检测到台阶
    steps: int = 0  # 台阶数量
    front_distance: float = 0.0  # 前方距离（米）
    deviation_angle: float = 0.0  # 偏航角度（度）
    bus_line: Optional[str] = None  # 公交线路
    zone_state: Optional[str] = None  # 区域状态（如"B区"）
    sign_text: Optional[str] = None  # 标识文本
    
    def update_from_vision(self, vision_data: Dict[str, Any]):
        """
        从视觉数据更新上下文
        
        Args:
            vision_data: 视觉检测结果
        """
        self.vision_data = vision_data
        self.door_detected = vision_data.get("door_detected", False)
        self.room_num = vision_data.get("room_num")
        self.department = vision_data.get("department")
        self.step_detected = vision_data.get("step_detected", False)
        self.path_blocked = vision_data.get("path_blocked", False)
        self.is_indoor = vision_data.get("environment") == "indoor"
        self.is_subway = vision_data.get("environment") == "subway"
    
    def update_from_gps(self, lat: float, lng: float, heading: Optional[float] = None):
        """
        从GPS数据更新上下文
        
        Args:
            lat: 纬度
            lng: 经度
            heading: 朝向（可选）
        """
        self.position = {"lat": lat, "lng": lng}
        if heading is not None:
            self.heading = heading
    
    def update_from_navigation_raw(self, nav_raw: Dict[str, Any]):
        """
        从导航原始数据更新上下文
        
        Args:
            nav_raw: 导航原始数据
        """
        self.off_route_distance = nav_raw.get("off_route_distance", 0.0)
        self.heading_error = nav_raw.get("heading_error", 0.0)
        self.need_reroute = (
            self.off_route_distance > 40.0 or abs(self.heading_error) > 45.0
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典
        
        Returns:
            上下文字典
        """
        return {
            "position": self.position,
            "heading": self.heading,
            "current_step": self.current_step,
            "next_step": self.next_step,
            "current_step_index": self.current_step_index,
            "hazards": self.hazards,
            "construction": self.construction,
            "people_density": self.people_density,
            "traffic_light_state": self.traffic_light_state,
            "path_blocked": self.path_blocked,
            "need_reroute": self.need_reroute,
            "off_route_distance": self.off_route_distance,
            "heading_error": self.heading_error,
            "bus_direction_ok": self.bus_direction_ok,
            "current_zone": self.current_zone,
            "target_zone": self.target_zone,
            "is_indoor": self.is_indoor,
            "is_subway": self.is_subway,
            "emotion_state": self.emotion_state,
            "door_detected": self.door_detected,
            "room_num": self.room_num,
            "department": self.department,
            "step_detected": self.step_detected,
        }

