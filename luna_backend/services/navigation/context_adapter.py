"""
导航上下文适配器 (NavigationContextAdapter) v1.2.0
将视觉识别结果自动填入NavigationContext，让策略系统真正动起来
"""

from typing import Dict, Any
from .navigation_context import NavigationContext

# 延迟导入以避免循环依赖
def _get_logger():
    try:
        from luna_backend.utils.logger import system_log
        return system_log
    except ImportError:
        try:
            from utils.logger import system_log
            return system_log
        except ImportError:
            def _dummy_log(tag, extra):
                pass
            return _dummy_log


class NavigationContextAdapter:
    """
    导航上下文适配器
    
    负责将视觉识别、GPS、传感器等数据转换为NavigationContext可用的格式
    """
    
    def __init__(self, ctx: NavigationContext):
        """
        初始化适配器
        
        Args:
            ctx: 导航上下文实例
        """
        self.ctx = ctx
    
    def apply_vision_result(self, data: Dict[str, Any]):
        """
        应用视觉识别结果到上下文
        
        data = {
            "hazards": [...],
            "steps": 1,
            "front_distance": 0.7,
            "people_density": 0.4,
            "path_blocked": false,
            "deviation_angle": -15,
            "bus": {"match": false, "line": "147"},
            "ocr": {"zone": "B区", "text": "检验科 →"},
            "construction": false,
            "traffic_light_state": "GREEN",
            "step_detected": true,
            ...
        }
        
        Args:
            data: 视觉识别结果字典
        """
        system_log = _get_logger()
        
        # 危险信息
        if "hazards" in data:
            self.ctx.hazards = data["hazards"] if isinstance(data["hazards"], list) else []
        
        # 台阶信息
        if "steps" in data:
            self.ctx.steps = int(data["steps"]) if data["steps"] else 0
        
        if "step_detected" in data:
            self.ctx.step_detected = bool(data["step_detected"])
        
        # 前方距离
        if "front_distance" in data:
            self.ctx.front_distance = float(data["front_distance"]) if data["front_distance"] else 0.0
        
        # 人群密度
        if "people_density" in data:
            density = data["people_density"]
            if isinstance(density, (int, float)):
                self.ctx.people_density = float(density)
            elif isinstance(density, dict):
                # 如果是从crowd_density_detector返回的字典格式
                self.ctx.people_density = float(density.get("density", 0.0))
        
        # 路径阻塞
        if "path_blocked" in data:
            self.ctx.path_blocked = bool(data["path_blocked"])
        
        # 偏航角度
        if "deviation_angle" in data:
            self.ctx.deviation_angle = float(data["deviation_angle"]) if data["deviation_angle"] else 0.0
        
        # 公交信息
        if "bus" in data:
            bus_info = data["bus"]
            if isinstance(bus_info, dict):
                self.ctx.bus_direction_ok = bus_info.get("match", True)
                self.ctx.bus_line = bus_info.get("line")
            else:
                self.ctx.bus_direction_ok = bool(bus_info)
        
        # OCR识别结果
        if "ocr" in data:
            ocr_info = data["ocr"]
            if isinstance(ocr_info, dict):
                self.ctx.zone_state = ocr_info.get("zone")
                self.ctx.sign_text = ocr_info.get("text")
        
        # 施工状态
        if "construction" in data:
            self.ctx.construction = bool(data["construction"])
        
        # 红绿灯状态
        if "traffic_light_state" in data:
            state = data["traffic_light_state"]
            if state in ["RED", "GREEN", "YELLOW"]:
                self.ctx.traffic_light_state = state
            else:
                self.ctx.traffic_light_state = None
        
        # 门牌号
        if "room_num" in data:
            self.ctx.room_num = str(data["room_num"]) if data["room_num"] else None
        
        # 科室名称
        if "department" in data:
            self.ctx.department = str(data["department"]) if data["department"] else None
        
        # 门检测
        if "door_detected" in data:
            self.ctx.door_detected = bool(data["door_detected"])
        
        # 环境类型
        if "environment" in data:
            env = data["environment"]
            if env == "indoor":
                self.ctx.is_indoor = True
            elif env == "subway":
                self.ctx.is_subway = True
        
        # 记录日志
        system_log("CTX-ADAPTER", {
            "updated_fields": list(data.keys()),
            "context_snapshot": {
                "hazards_count": len(self.ctx.hazards),
                "people_density": self.ctx.people_density,
                "path_blocked": self.ctx.path_blocked,
                "construction": self.ctx.construction,
            }
        })
    
    def apply_gps_result(self, lat: float, lng: float, heading: Optional[float] = None):
        """
        应用GPS结果到上下文
        
        Args:
            lat: 纬度
            lng: 经度
            heading: 朝向（可选）
        """
        self.ctx.update_from_gps(lat, lng, heading)
    
    def apply_navigation_raw(self, nav_raw: Dict[str, Any]):
        """
        应用导航原始数据到上下文
        
        Args:
            nav_raw: 导航原始数据
        """
        self.ctx.update_from_navigation_raw(nav_raw)



