"""
重规划策略 (v1.2.0)
专门为偏航设计：
- off-route 距离、角度
- 持续静止
- 原路线被施工挡住（视觉）
- 行人密集不可通行

并决定是否触发 should_reroute。
"""

from typing import Dict, Any
import time
from .base_strategy import NavigationStrategy


class RerouteStrategy(NavigationStrategy):
    """重规划策略"""
    
    STRATEGY_NAME = "REROUTE"
    
    def __init__(self):
        """初始化重规划策略"""
        self.last_position_time = {}  # 记录位置更新时间
        self.stationary_count = {}  # 记录静止次数
    
    def is_applicable(self, env: Dict[str, Any]) -> bool:
        """
        基于：
        - 超过一定距离距离（off-route）
        - heading 偏差
        - 长时间静止
        - 道路被封堵（视觉）
        - 施工挡住路径
        - 缺少路线结构
        
        Args:
            env: 环境信息字典
        
        Returns:
            是否适用
        """
        nav_raw = env.get("navigation_raw", {})
        return (
            nav_raw.get("off_route_distance", 0) > 35 or   # 偏航距离
            nav_raw.get("heading_error", 0) > 35 or        # 偏航角度
            env.get("vision", {}).get("path_blocked")      # 道路被挡
        )
    
    def should_reroute(self, status: Dict[str, Any], env: Dict[str, Any]) -> bool:
        """
        判断是否应该重新规划路线
        
        Args:
            status: 导航状态字典
            env: 环境信息字典
        
        Returns:
            是否应该重新规划
        """
        nav_raw = env.get("navigation_raw", {})
        
        # 偏航距离超过阈值
        off_route_distance = nav_raw.get("off_route_distance", 0)
        if off_route_distance > 30:  # 超过30米需要重规划
            return True
        
        # 角度偏差过大
        heading_error = nav_raw.get("heading_error", 0)
        if abs(heading_error) > 45:  # 角度偏差超过45度
            return True
        
        # 检查持续静止（可能迷路）
        route_id = status.get("route", {}).get("destination", "unknown")
        current_time = time.time()
        last_pos = status.get("extra", {}).get("last_position_time")
        
        if last_pos:
            time_since_update = current_time - last_pos
            if time_since_update > 60:  # 60秒没有位置更新
                return True
        
        # 检查视觉阻塞
        vision = env.get("vision", {})
        hazards = vision.get("hazards", [])
        for hazard in hazards:
            if isinstance(hazard, dict):
                hazard_type = hazard.get("type", "")
                risk_level = hazard.get("risk_level", "medium")
                distance = hazard.get("distance", 999)
                
                # 施工或阻塞需要重规划
                if hazard_type in ("construction", "blocked"):
                    return True
                
                # 高风险障碍物且距离很近
                if hazard_type == "obstacle" and risk_level == "critical" and distance < 1.5:
                    return True
        
        return False
    
    def get_next_action(self, status: Dict[str, Any], env: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取下一步动作建议（重规划相关）
        
        Args:
            status: 导航状态字典
            env: 环境信息字典
        
        Returns:
            动作建议字典
        """
        return {
            "action": "trigger_reroute",
            "description": "检测到偏航或路径阻塞，将重新规划路线",
            "reason": "reroute_required",
        }

