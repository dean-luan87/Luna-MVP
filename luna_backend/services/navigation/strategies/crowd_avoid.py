"""
拥挤人群规避策略 (CrowdAvoidStrategy) v1.2.0
当检测到人群密度过高时，建议减速并靠边行走
"""

from ..base_strategy import BaseStrategy


class CrowdAvoidStrategy(BaseStrategy):
    """拥挤人群规避策略"""
    
    STRATEGY_NAME = "CROWD_AVOID"
    
    # 人群密度阈值
    CROWD_THRESHOLD = 0.65  # 65%以上认为拥挤
    
    def should_execute(self) -> bool:
        """
        判断是否应该执行拥挤规避
        
        条件：
        - 人群密度超过阈值
        """
        return self.ctx.people_density >= self.CROWD_THRESHOLD
    
    def execute(self) -> dict:
        """
        执行拥挤规避策略
        
        Returns:
            策略执行结果
        """
        self.log("NAV:CROWD_HIGH", {
            "density": self.ctx.people_density,
            "position": self.ctx.position,
        })
        
        # 根据密度等级决定提示强度
        if self.ctx.people_density >= 0.85:
            # 非常拥挤
            text = "前方人群非常拥挤，请减速慢行，注意安全，建议靠右侧行走。"
            action = "SLOW_DOWN_SEVERE"
        elif self.ctx.people_density >= 0.75:
            # 较拥挤
            text = "前方人群较拥挤，请减速并靠右行走。"
            action = "SLOW_DOWN_MODERATE"
        else:
            # 一般拥挤
            text = "前方人群较多，请减速并靠右行走。"
            action = "SLOW_DOWN"
        
        return {
            "success": True,
            "action": action,
            "text": text,
            "people_density": self.ctx.people_density,
        }



