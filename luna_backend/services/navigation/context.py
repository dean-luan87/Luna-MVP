"""
导航上下文 (NavigationContext) v1.2.0
导航状态容器，存储当前导航的所有状态信息（包含医院场景扩展）
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field


@dataclass
class NavigationContext:
    """
    导航上下文
    存储导航过程中的所有状态信息，供策略系统使用
    """
    
    # ========== 通用导航字段 ==========
    scene_type: str = "unknown"  # "street" / "hospital" / "metro" / "mall" ...
    current_step: str = "idle"
    deviation_angle: float = 0.0
    front_distance: Optional[float] = None
    people_density: float = 0.0
    path_blocked: bool = False
    hazards: List[Dict[str, Any]] = field(default_factory=list)
    
    # ========== 位置信息 ==========
    position: Optional[Dict[str, float]] = None  # GPS or SLAM位置 {"lat": 0.0, "lng": 0.0}
    heading: Optional[float] = None  # 朝向角度（度）
    
    # ========== 路径信息 ==========
    next_step: Optional[Dict[str, Any]] = None  # 下一步骤信息
    route_segments: List[Dict[str, Any]] = field(default_factory=list)  # 路径段列表
    current_step_index: int = 0  # 当前步骤索引
    
    # ========== 环境信息 ==========
    construction: bool = False  # 是否检测到施工
    traffic_light_state: Optional[str] = None  # 红绿灯状态: "RED", "GREEN", "YELLOW", None
    
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
    bus_line: Optional[str] = None  # 公交线路
    zone_state: Optional[str] = None  # 区域状态（如"B区"）
    sign_text: Optional[str] = None  # 标识文本
    
    # ========== 多目标路径规划 ==========
    start_point: Optional[str] = None  # 起点
    multi_targets: Optional[List[Dict[str, Any]]] = None  # 多目标列表
    planned_routes: Optional[List[Dict[str, Any]]] = None  # 规划好的路线列表
    multi_targets_ordered: Optional[List[Dict[str, Any]]] = None  # 排序后的目标列表
    
    # ========== 医院专用字段 ==========
    hospital_name: Optional[str] = None
    hospital_stage: str = "unknown"  # "entering" / "registration" / "waiting" / "in_exam" / "leaving"
    is_first_visit: bool = True
    has_registered: bool = False
    department_name: Optional[str] = None  # 目标科室，如 "眼科"
    department_room: Optional[str] = None  # 门牌号，如 "305"
    registration_ticket_no: Optional[str] = None
    called_ticket_no: Optional[str] = None
    queue_len_estimate: Optional[int] = None
    has_report_to_collect: bool = False
    has_followup_task: bool = False
    
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
        if vision_data.get("environment"):
            self.scene_type = vision_data.get("environment")
    
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
            "scene_type": self.scene_type,
            "current_step": self.current_step,
            "position": self.position,
            "heading": self.heading,
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
            "steps": self.steps,
            "bus_line": self.bus_line,
            "zone_state": self.zone_state,
            "sign_text": self.sign_text,
            "start_point": self.start_point,
            "multi_targets": self.multi_targets,
            "hospital_name": self.hospital_name,
            "hospital_stage": self.hospital_stage,
            "is_first_visit": self.is_first_visit,
            "has_registered": self.has_registered,
            "department_name": self.department_name,
            "department_room": self.department_room,
            "registration_ticket_no": self.registration_ticket_no,
            "called_ticket_no": self.called_ticket_no,
            "queue_len_estimate": self.queue_len_estimate,
            "has_report_to_collect": self.has_report_to_collect,
            "has_followup_task": self.has_followup_task,
        }



