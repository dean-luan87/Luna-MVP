"""
偏航纠正策略 (DeviationCorrectionStrategy) v1.2.0
当检测到偏离路线时，提供纠正建议
"""

from ..base_strategy import BaseStrategy


class DeviationCorrectionStrategy(BaseStrategy):
    """偏航纠正策略"""
    
    STRATEGY_NAME = "DEVIATION_CORRECTION"
    
    def should_execute(self) -> bool:
        """
        判断是否应该执行偏航纠正
        
        条件：
        - 需要重新规划路线
        - 没有检测到施工（施工场景由ConstructionBypassStrategy处理）
        """
        return self.ctx.need_reroute and not self.ctx.construction
    
    def execute(self) -> dict:
        """
        执行偏航纠正策略
        
        Returns:
            策略执行结果
        """
        self.log("NAV:DEVIATION_CORRECTION", {
            "position": self.ctx.position,
            "off_route_distance": self.ctx.off_route_distance,
            "heading_error": self.ctx.heading_error,
        })
        
        # 根据偏离距离和角度决定纠正方式
        if self.ctx.off_route_distance > 50:
            # 严重偏离，建议调头
            action = "TURN_BACK"
            text = "您已严重偏离路线，建议在前方安全处调头返回。"
        elif abs(self.ctx.heading_error) > 60:
            # 角度偏差大，建议大幅转向
            if self.ctx.heading_error > 0:
                action = "TURN_RIGHT"
                text = "您偏离了方向，请向右转调整方向。"
            else:
                action = "TURN_LEFT"
                text = "您偏离了方向，请向左转调整方向。"
        else:
            # 轻微偏离，建议小幅调整
            action = "ADJUST_COURSE"
            text = "您稍微偏离了路线，请向前方继续前行并稍作调整。"
        
        return {
            "success": True,
            "action": action,
            "text": text,
            "off_route_distance": self.ctx.off_route_distance,
            "heading_error": self.ctx.heading_error,
        }



