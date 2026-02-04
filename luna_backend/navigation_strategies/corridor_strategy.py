"""
走廊策略 (v1.2.0)
特别适合医院走廊场景：
- 判断走廊宽度
- 走廊左右门牌变化趋势
- 判断是否越走越偏
- 自然语言播报走廊方向（左手边/右手边）
"""

import re
from typing import Dict, Any, Optional
from .base_strategy import NavigationStrategy


class CorridorStrategy(NavigationStrategy):
    """走廊导航策略"""
    
    STRATEGY_NAME = "CORRIDOR"
    
    def is_applicable(self, env: Dict[str, Any]) -> bool:
        """
        视觉特征：
        - corridor = True
        - 大量竖直结构（墙体检测）
        - 室内但没有服务台、电梯等强特征
        
        Args:
            env: 环境信息字典
        
        Returns:
            是否适用
        """
        vision = env.get("vision", {})
        return vision.get("environment") == "indoor" and vision.get("is_corridor")
    
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
        
        room_num = vision.get("room_num")
        target_room = status.get("target_room")
        
        # 判断趋势（递增 or 递减）
        trend = vision.get("room_trend")  # up/down
        
        if room_num and target_room:
            try:
                rn = int(room_num)
                tr = int(target_room)
                
                if rn < tr and trend == "up":
                    return {
                        "action": "walk_forward",
                        "description": f"沿走廊继续前行，房间号数字逐渐接近 {target_room}",
                        "reason": "corridor_room_trend_match",
                    }
                
                if rn > tr and trend == "down":
                    return {
                        "action": "walk_forward",
                        "description": f"继续直行，房间号逐渐接近 {target_room}",
                        "reason": "corridor_room_trend_match",
                    }
                
            except:
                pass
        
        # 如果视觉识别到目标科室
        if "department" in vision:
            return {
                "action": "approach_department",
                "description": f"靠近目标科室：{vision['department']}",
                "reason": "department_detected",
            }
        
        return {
            "action": "walk_forward",
            "description": "沿走廊继续前行",
            "reason": "corridor_default",
        }
    
    def should_advance_step(self, status: Dict[str, Any], env: Dict[str, Any]) -> bool:
        """
        如果门牌号趋势靠近目标 → 进入下一步
        
        Args:
            status: 导航状态字典
            env: 环境信息字典
        
        Returns:
            是否应该推进到下一步
        """
        target_room = status.get("target_room")
        current_room = env.get("vision", {}).get("room_num")
        
        if not target_room or not current_room:
            return False
        
        # 简化：房间号差值小于一定范围视为靠近目标
        try:
            return abs(int(current_room) - int(target_room)) < 3
        except:
            return False
    
    def suggest_switch(self, status: Dict[str, Any], env: Dict[str, Any]) -> Optional[str]:
        """
        如果离开走廊环境，建议切换到室内策略
        
        Args:
            status: 导航状态字典
            env: 环境信息字典
        
        Returns:
            建议的策略名称
        """
        vision = env.get("vision", {})
        if vision.get("environment") != "corridor":
            return "INDOOR"
        
        return None

