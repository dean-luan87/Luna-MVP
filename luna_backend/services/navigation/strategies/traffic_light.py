"""
红绿灯判断策略 (TrafficLightStrategy) v1.2.0
当检测到红绿灯时，根据信号状态提供通行建议
"""

from ..base_strategy import BaseStrategy


class TrafficLightStrategy(BaseStrategy):
    """红绿灯判断策略"""
    
    STRATEGY_NAME = "TRAFFIC_LIGHT"
    
    def should_execute(self) -> bool:
        """
        判断是否应该执行红绿灯策略
        
        条件：
        - 检测到红绿灯状态
        """
        return self.ctx.traffic_light_state is not None
    
    def execute(self) -> dict:
        """
        执行红绿灯策略
        
        Returns:
            策略执行结果
        """
        state = self.ctx.traffic_light_state
        
        self.log("NAV:TRAFFIC_LIGHT", {
            "state": state,
            "position": self.ctx.position,
        })
        
        if state == "RED":
            return {
                "success": True,
                "action": "WAIT",
                "text": "红灯，请稍等，不要通行。",
                "traffic_light_state": state,
            }
        
        elif state == "GREEN":
            return {
                "success": True,
                "action": "GO",
                "text": "绿灯亮起，可以通行，请注意安全。",
                "traffic_light_state": state,
            }
        
        elif state == "YELLOW":
            return {
                "success": True,
                "action": "CAUTION",
                "text": "黄灯，请谨慎通行，如未进入路口请等待。",
                "traffic_light_state": state,
            }
        
        else:
            # 未知状态
            return {
                "success": True,
                "action": "CAUTION",
                "text": "前方有红绿灯，请观察信号后通行。",
                "traffic_light_state": state,
            }



