"""
默认策略 = 兜底 (v1.2.0)
用于：环境无法判断类型、视觉数据不足、环境状态无法识别、或正在初始化
"""

from typing import Dict, Any
from .base_strategy import NavigationStrategy


class DefaultStrategy(NavigationStrategy):
    """默认策略（兜底）"""
    
    STRATEGY_NAME = "DEFAULT"
    
    def is_applicable(self, env: Dict[str, Any]) -> bool:
        """
        默认策略永远可用（兜底）
        
        Args:
            env: 环境信息字典
        
        Returns:
            总是返回True
        """
        return True
    
    def get_next_action(self, status: Dict[str, Any], env: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取下一步动作建议（默认：继续当前路径）
        
        Args:
            status: 导航状态字典
            env: 环境信息字典
        
        Returns:
            动作建议字典
        """
        return {
            "action": "follow_route",
            "description": "继续当前导航路径",
            "reason": "default_strategy",
        }



