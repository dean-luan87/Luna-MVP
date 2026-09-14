"""
视觉危险策略 (v1.2.0)
专门处理视觉 hazard：
- 台阶
- 障碍物
- 前方多人靠近
- 狭窄通道
- 施工
- 十字路口/弯道

并决定是否暂停 + TTS 播报 + 任务链介入。
"""

from typing import Dict, Any, List
from .base_strategy import NavigationStrategy


class HazardStrategy(NavigationStrategy):
    """危险处理策略"""
    
    STRATEGY_NAME = "HAZARD"
    
    def is_applicable(self, env: Dict[str, Any]) -> bool:
        """
        判断是否有危险需要处理
        
        Args:
            env: 环境信息字典
        
        Returns:
            是否适用
        """
        vision = env.get("vision", {})
        hazards = vision.get("hazards", [])
        
        # 如果有危险，此策略适用
        return len(hazards) > 0
    
    def should_pause(self, status: Dict[str, Any], env: Dict[str, Any]) -> bool:
        """
        有危险 → 必须暂停
        
        Args:
            status: 导航状态字典
            env: 环境信息字典
        
        Returns:
            是否建议暂停（有危险时总是返回True）
        """
        return True  # 有危险 → 必须暂停
    
    def get_next_action(self, status: Dict[str, Any], env: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取下一步动作建议（处理危险）
        
        Args:
            status: 导航状态字典
            env: 环境信息字典
        
        Returns:
            动作建议字典
        """
        hazards = env.get("hazards", [])
        
        if not hazards:
            return {
                "action": "continue",
                "description": "继续前进",
                "reason": "no_hazard",
            }
        
        hi = hazards[0]  # 最高危险等级的 hazard
        
        return {
            "action": "stop_and_warn",
            "description": f"前方危险：{hi.get('type', 'unknown')}，请停下",
            "severity": hi.get("severity", "unknown"),
            "reason": "hazard_detected",
        }
    
    def should_advance_step(self, status: Dict[str, Any], env: Dict[str, Any]) -> bool:
        """
        不允许前进
        
        Args:
            status: 导航状态字典
            env: 环境信息字典
        
        Returns:
            总是返回False（不允许前进）
        """
        return False  # 不允许前进
    
    def should_reroute(self, status: Dict[str, Any], env: Dict[str, Any]) -> bool:
        """
        如果 hazard 类型可绕行，则建议重新规划
        
        Args:
            status: 导航状态字典
            env: 环境信息字典
        
        Returns:
            是否应该重新规划
        """
        # 如果 hazard 类型可绕行，则建议重新规划
        return any(h.get("block") for h in env.get("hazards", []))
    
    def _risk_priority(self, risk_level: str) -> int:
        """
        获取风险优先级（数字越大优先级越高）
        
        Args:
            risk_level: 风险级别
        
        Returns:
            优先级数字
        """
        priority_map = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4,
        }
        return priority_map.get(risk_level.lower(), 0)

