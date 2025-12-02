"""
室内医院 / 商场导航策略 (v1.2.0)
主要依据视觉识别：
- "门牌号"（room_num）
- "科室名称"（department）
- "楼层牌"
- "电梯/扶梯"
- "服务台"
- "洗手间"
- "挂号 / 缴费 / 取药"
"""

from typing import Dict, Any
from .base_strategy import NavigationStrategy


class IndoorStrategy(NavigationStrategy):
    """室内导航策略"""
    
    STRATEGY_NAME = "INDOOR"
    
    def is_applicable(self, env: Dict[str, Any]) -> bool:
        """
        判断是否适用于室内环境
        
        Args:
            env: 环境信息字典
        
        Returns:
            是否适用
        """
        vision = env.get("vision", {})
        return vision.get("environment") == "indoor"
    
    def get_next_action(self, status: Dict[str, Any], env: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取下一步动作建议
        
        Args:
            status: 导航状态字典
            env: 环境信息字典
        
        Returns:
            动作建议字典
        """
        vision = env.get("vision", {})
        elems = vision.get("elements", [])
        
        # 服务台检测
        if "service_desk" in elems or "reception" in elems:
            return {
                "action": "move_to_service_desk",
                "description": "靠近服务台，以确认方向",
                "reason": "service_desk_detected",
            }
        
        # 电梯检测
        if "lift" in elems or "elevator" in elems:
            return {
                "action": "use_elevator",
                "description": "靠近电梯准备乘坐",
                "reason": "elevator_detected",
            }
        
        # 门牌/科室识别
        door_label = vision.get("doorplate") or vision.get("room_num")
        if door_label:
            return {
                "action": "move_toward_room",
                "description": f"朝 {door_label} 方向前进",
                "reason": "doorplate_detected",
            }
        
        return {
            "action": "follow_corridor",
            "description": "沿走廊继续前进",
            "reason": "indoor_navigation",
        }



