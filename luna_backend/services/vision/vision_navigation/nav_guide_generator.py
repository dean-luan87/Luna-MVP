"""
视觉导航：基于视觉结果生成可读指令 (v1.2.0)
E.g. "前方 1.2 米有台阶，下台阶 3 级"
"""

from typing import List, Dict, Any, Optional
from utils.logger import vision_log


class VisualGuideGenerator:
    """视觉导航指引生成器"""
    
    def __init__(self):
        """初始化视觉指引生成器"""
        pass
    
    def generate_step_tip(self, step_info: Dict[str, Any]) -> str:
        """
        生成台阶提示
        
        Args:
            step_info: 台阶信息字典，包含 distance, height, direction 等
        
        Returns:
            台阶提示文本
        """
        distance = step_info.get("distance", 0.0)
        height = step_info.get("height", 0.0)
        direction = step_info.get("direction", "前方")
        step_count = step_info.get("step_count", 0)
        
        if step_count > 0:
            return f"{direction} {distance:.1f} 米有台阶，共 {step_count} 级，高度约 {height:.1f} 厘米"
        else:
            return f"{direction} {distance:.1f} 米有台阶，高度约 {height:.1f} 厘米"
    
    def generate_obstacle_tip(self, obs: Dict[str, Any]) -> str:
        """
        生成障碍物提示
        
        Args:
            obs: 障碍物信息字典，包含 direction, distance, type 等
        
        Returns:
            障碍物提示文本
        """
        direction = obs.get("direction", "前方")
        distance = obs.get("distance", 0.0)
        obs_type = obs.get("type", "障碍物")
        risk_level = obs.get("risk_level", "medium")
        
        risk_text = ""
        if risk_level == "high":
            risk_text = "危险"
        elif risk_level == "critical":
            risk_text = "非常危险"
        
        if risk_text:
            return f"{direction}方向 {distance:.1f} 米有{risk_text}的{obs_type}"
        else:
            return f"{direction}方向 {distance:.1f} 米有{obs_type}"
    
    def generate_sign_tip(self, sign: Dict[str, Any]) -> str:
        """
        生成标识牌提示
        
        Args:
            sign: 标识牌信息字典，包含 category, direction, distance, text 等
        
        Returns:
            标识牌提示文本
        """
        category = sign.get("category", "标识牌")
        direction = sign.get("direction", "前方")
        distance = sign.get("distance", 0.0)
        text = sign.get("text", "")
        
        if text:
            return f"检测到{category}标识「{text}」，在{direction}方向 {distance:.1f} 米"
        else:
            return f"检测到{category}标识，在{direction}方向 {distance:.1f} 米"
    
    def generate_facility_tip(self, facility: Dict[str, Any]) -> str:
        """
        生成公共设施提示
        
        Args:
            facility: 公共设施信息字典，包含 type, direction, distance, label 等
        
        Returns:
            公共设施提示文本
        """
        facility_type = facility.get("type", "设施")
        direction = facility.get("direction", "前方")
        distance = facility.get("distance", 0.0)
        label = facility.get("label", "")
        
        if label:
            return f"{direction}方向 {distance:.1f} 米有{facility_type}「{label}」"
        else:
            return f"{direction}方向 {distance:.1f} 米有{facility_type}"
    
    def generate_traffic_light_tip(self, traffic_light: Dict[str, Any]) -> str:
        """
        生成红绿灯提示
        
        Args:
            traffic_light: 红绿灯信息字典，包含 state, direction, distance 等
        
        Returns:
            红绿灯提示文本
        """
        state = traffic_light.get("state", "unknown")
        direction = traffic_light.get("direction", "前方")
        distance = traffic_light.get("distance", 0.0)
        
        state_map = {
            "red": "红灯",
            "green": "绿灯",
            "yellow": "黄灯",
            "unknown": "未知状态"
        }
        
        state_text = state_map.get(state, "未知状态")
        return f"{direction}方向 {distance:.1f} 米处是{state_text}"
    
    def generate_all(self, vision_bundle: Dict[str, Any]) -> List[str]:
        """
        生成所有视觉提示
        
        Args:
            vision_bundle: 视觉结果包，包含 steps, obstacles, signs, facilities, traffic_light 等
        
        Returns:
            提示文本列表
        """
        tips = []
        
        # 台阶提示
        steps = vision_bundle.get("steps", [])
        if steps:
            if isinstance(steps, list):
                for step in steps:
                    tip = self.generate_step_tip(step if isinstance(step, dict) else step.to_dict() if hasattr(step, 'to_dict') else {})
                    if tip:
                        tips.append(tip)
            else:
                tip = self.generate_step_tip(steps if isinstance(steps, dict) else steps.to_dict() if hasattr(steps, 'to_dict') else {})
                if tip:
                    tips.append(tip)
        
        # 障碍物/危险提示
        obstacles = vision_bundle.get("obstacles", [])
        hazards = vision_bundle.get("hazards", [])
        all_obstacles = obstacles + hazards
        
        if all_obstacles:
            for obs in all_obstacles:
                obs_dict = obs if isinstance(obs, dict) else obs.to_dict() if hasattr(obs, 'to_dict') else {}
                tip = self.generate_obstacle_tip(obs_dict)
                if tip:
                    tips.append(tip)
        
        # 标识牌提示
        signs = vision_bundle.get("signs", [])
        signboards = vision_bundle.get("signboards", [])
        all_signs = signs + signboards
        
        if all_signs:
            for sign in all_signs:
                sign_dict = sign if isinstance(sign, dict) else sign.to_dict() if hasattr(sign, 'to_dict') else {}
                tip = self.generate_sign_tip(sign_dict)
                if tip:
                    tips.append(tip)
        
        # 公共设施提示
        facilities = vision_bundle.get("facilities", [])
        if facilities:
            for facility in facilities:
                facility_dict = facility if isinstance(facility, dict) else facility.to_dict() if hasattr(facility, 'to_dict') else {}
                tip = self.generate_facility_tip(facility_dict)
                if tip:
                    tips.append(tip)
        
        # 红绿灯提示
        traffic_light = vision_bundle.get("traffic_light")
        if traffic_light:
            traffic_dict = traffic_light if isinstance(traffic_light, dict) else traffic_light.to_dict() if hasattr(traffic_light, 'to_dict') else {}
            tip = self.generate_traffic_light_tip(traffic_dict)
            if tip:
                tips.append(tip)
        
        vision_log("GUIDE_GENERATED", {"tip_count": len(tips)})
        
        return tips



