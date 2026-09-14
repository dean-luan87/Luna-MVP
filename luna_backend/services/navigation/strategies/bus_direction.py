"""
公交方向判断策略 (BusDirectionStrategy) v1.2.0
当检测到公交方向错误时，建议下车换乘
"""

from ..base_strategy import BaseStrategy


class BusDirectionStrategy(BaseStrategy):
    """公交方向判断策略"""
    
    STRATEGY_NAME = "BUS_DIRECTION"
    
    def should_execute(self) -> bool:
        """
        判断是否应该执行公交方向策略
        
        条件：
        - 公交方向不正确
        """
        return self.ctx.bus_direction_ok is False
    
    def execute(self) -> dict:
        """
        执行公交方向策略
        
        Returns:
            策略执行结果
        """
        self.log("NAV:BUS_DIRECTION_WRONG", {
            "position": self.ctx.position,
        })
        
        return {
            "success": True,
            "action": "EXIT_BUS",
            "text": "您乘坐的方向不对，建议您尽快在下一站下车，换乘正确方向的车辆。",
            "bus_direction_ok": False,
        }

