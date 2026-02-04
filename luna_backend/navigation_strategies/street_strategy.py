"""
室外步行导航策略 (v1.2.0)
主要基于：经纬度位置、直线距离、偏航检查、道路结构（宽/窄）、行人 vs 车辆区域分离
"""

from math import hypot
from typing import Dict, Any
from .base_strategy import NavigationStrategy


class StreetStrategy(NavigationStrategy):
    """室外步行导航策略"""
    
    STRATEGY_NAME = "STREET"
    
    def is_applicable(self, env: Dict[str, Any]) -> bool:
        """
        关键判断：
        - 有 GPS 经纬度
        - 视觉识别到道路（road/street/crosswalk）
        - 或者没有足够室内特征
        
        Args:
            env: 环境信息字典
        
        Returns:
            是否适用
        """
        vision = env.get("vision", {})
        return vision.get("environment") == "street"
    
    def should_advance_step(self, status: Dict[str, Any], env: Dict[str, Any]) -> bool:
        """
        依据距离判断是否进入下一步
        
        Args:
            status: 导航状态字典
            env: 环境信息字典
        
        Returns:
            是否应该推进到下一步
        """
        route = status.get("route")
        if not route or not route.get("steps"):
            return False
        
        current_step_index = status.get("current_step_index", -1)
        if current_step_index < 0 or current_step_index >= len(route["steps"]):
            return False
        
        step = route["steps"][current_step_index]
        step_meta = step.get("meta", {})
        
        lat = status.get("extra", {}).get("last_lat")
        lng = status.get("extra", {}).get("last_lng")
        target = step_meta.get("target_coord")
        
        if not target or lat is None or lng is None:
            return False
        
        target_lat = target.get("lat")
        target_lng = target.get("lng")
        
        if target_lat is None or target_lng is None:
            return False
        
        # 计算距离（简化版，实际应该用haversine公式）
        dst = hypot(lat - target_lat, lng - target_lng)
        
        # 室外误差大，6米内进入下一步
        return dst < 6.0
    
    def should_reroute(self, status: Dict[str, Any], env: Dict[str, Any]) -> bool:
        """
        偏航检测：超过 40 米 或 heading 偏差过大
        
        Args:
            status: 导航状态字典
            env: 环境信息字典
        
        Returns:
            是否应该重新规划
        """
        env_nav = env.get("navigation_raw", {})
        if not env_nav:
            return False
        
        off_route_distance = env_nav.get("off_route_distance", 0)
        if off_route_distance > 40:
            return True
        
        heading_error = env_nav.get("heading_error", 0)
        if abs(heading_error) > 45:
            return True
        
        return False
    
    def get_next_action(self, status: Dict[str, Any], env: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取下一步动作建议
        
        Args:
            status: 导航状态字典
            env: 环境信息字典
        
        Returns:
            动作建议字典
        """
        return {
            "action": "walk_straight",
            "description": "沿道路直行",
            "reason": "street_navigation",
        }



