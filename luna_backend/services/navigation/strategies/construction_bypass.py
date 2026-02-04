"""
施工绕行策略 (ConstructionBypassStrategy) v1.2.0
当检测到施工时，触发重新规划绕行路线
"""

from ..base_strategy import BaseStrategy


class ConstructionBypassStrategy(BaseStrategy):
    """施工绕行策略"""
    
    STRATEGY_NAME = "CONSTRUCTION_BYPASS"
    
    def should_execute(self) -> bool:
        """
        判断是否应该执行施工绕行
        
        条件：
        - 检测到施工
        """
        return self.ctx.construction is True
    
    def execute(self) -> dict:
        """
        执行施工绕行策略
        
        Returns:
            策略执行结果
        """
        self.log("NAV:CONSTRUCTION_DETECTED", {
            "position": self.ctx.position,
        })
        
        return {
            "success": True,
            "action": "REROUTE",
            "text": "前方道路施工，我已为您规划绕行路线，请按照新的路线前行。",
            "reroute_reason": "construction",
        }



