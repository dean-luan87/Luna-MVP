"""
目标点确认策略 (DestinationCheckStrategy) v1.2.0
当接近目标点时，提示用户确认是否到达目的地
"""

from ..base_strategy import BaseStrategy


class DestinationCheckStrategy(BaseStrategy):
    """目标点确认策略"""
    
    STRATEGY_NAME = "DESTINATION_CHECK"
    
    # 接近目标的距离阈值（米）
    APPROACH_DISTANCE = 10.0
    
    def should_execute(self) -> bool:
        """
        判断是否应该执行目标点确认
        
        条件：
        - 下一步骤标记为确认目标
        - 或者距离目标点很近
        """
        if self.ctx.next_step and self.ctx.next_step.get("action") == "CONFIRM_DEST":
            return True
        
        # 检查是否接近目标（如果有位置信息）
        if self.ctx.position and self.ctx.current_step:
            # TODO: 计算实际距离
            # 这里简化处理，如果next_step存在且距离很近，则认为需要确认
            return True
        
        return False
    
    def execute(self) -> dict:
        """
        执行目标点确认策略
        
        Returns:
            策略执行结果
        """
        self.log("NAV:DESTINATION_APPROACH", {
            "position": self.ctx.position,
            "current_step_index": self.ctx.current_step_index,
        })
        
        # 根据当前步骤信息生成确认提示
        destination_name = self.ctx.current_step.get("destination", "目的地") if self.ctx.current_step else "目的地"
        
        return {
            "success": True,
            "action": "CONFIRM",
            "text": f"即将到达{destination_name}，请确认是否进入目的地。",
            "destination": destination_name,
            "approaching": True,
        }



