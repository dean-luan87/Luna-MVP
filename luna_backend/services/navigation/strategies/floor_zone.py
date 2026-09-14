"""
楼层/分区判断策略 (FloorZoneStrategy) v1.2.0
用于医院/商场等室内导航，当检测到区域错误时提供引导
"""

from ..base_strategy import BaseStrategy


class FloorZoneStrategy(BaseStrategy):
    """楼层/分区判断策略"""
    
    STRATEGY_NAME = "FLOOR_ZONE"
    
    def should_execute(self) -> bool:
        """
        判断是否应该执行楼层/分区策略
        
        条件：
        - 当前步骤标记为错误区域
        - 或者当前区域与目标区域不匹配
        """
        if self.ctx.current_step and self.ctx.current_step.get("status") == "WRONG_ZONE":
            return True
        
        if self.ctx.current_zone and self.ctx.target_zone:
            return self.ctx.current_zone != self.ctx.target_zone
        
        return False
    
    def execute(self) -> dict:
        """
        执行楼层/分区策略
        
        Returns:
            策略执行结果
        """
        self.log("NAV:WRONG_ZONE", {
            "current_zone": self.ctx.current_zone,
            "target_zone": self.ctx.target_zone,
            "position": self.ctx.position,
        })
        
        # 根据当前步骤信息生成引导
        if self.ctx.next_step:
            direction = self.ctx.next_step.get("direction", "前方")
            zone_name = self.ctx.target_zone or "目标区域"
            text = f"您当前所在区域不正确，请向{direction}进入{zone_name}。"
        else:
            text = "您当前所在区域不正确，请按照指示前往目标区域。"
        
        return {
            "success": True,
            "action": "ZONE_GUIDE",
            "text": text,
            "current_zone": self.ctx.current_zone,
            "target_zone": self.ctx.target_zone,
        }



