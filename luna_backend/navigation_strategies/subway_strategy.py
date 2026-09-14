"""
地铁策略 (v1.2.0)
用于：站台识别、方向识别（往浦东机场/往莘庄）、地铁口 → 闸机 → 安检 → 站台 → 选对方向
"""

from typing import Dict, Any
from .base_strategy import NavigationStrategy


class SubwayStrategy(NavigationStrategy):
    """地铁导航策略"""
    
    STRATEGY_NAME = "SUBWAY"
    
    def is_applicable(self, env: Dict[str, Any]) -> bool:
        """
        判断是否适用于地铁环境
        
        Args:
            env: 环境信息字典
        
        Returns:
            是否适用
        """
        vision = env.get("vision", {})
        return vision.get("environment") == "subway"
    
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
        elements = vision.get("elements", [])
        
        # 阶段判断：是否在闸机前
        if "gate" in elements or "gate_machine" in elements:
            return {
                "action": "approach_gate",
                "description": "前往闸机，并准备进站",
                "reason": "subway_gate_detected",
            }
        
        # 站台方向判断
        direction = vision.get("platform_direction")
        if direction:
            return {
                "action": "choose_platform",
                "description": f"前往 {direction} 方向的站台",
                "reason": "subway_platform_detected",
            }
        
        return {
            "action": "follow_signs",
            "description": "沿指示牌前往地铁站台",
            "reason": "subway_navigation",
        }
    
    def should_pause(self, status: Dict[str, Any], env: Dict[str, Any]) -> bool:
        """
        在地铁站台前建议暂停，等待确认方向
        
        Args:
            status: 导航状态字典
            env: 环境信息字典
        
        Returns:
            是否建议暂停
        """
        vision = env.get("vision", {})
        elements = vision.get("elements", [])
        
        # 在站台前暂停
        if "platform" in elements or "platform_direction" in vision:
            return True
        
        return False



