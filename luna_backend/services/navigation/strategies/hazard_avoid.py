"""
障碍物风险策略 (HazardAvoidStrategy) v1.2.0
当检测到障碍物或危险时，提供规避建议
"""

from ..base_strategy import BaseStrategy


class HazardAvoidStrategy(BaseStrategy):
    """障碍物风险策略"""
    
    STRATEGY_NAME = "HAZARD_AVOID"
    
    def should_execute(self) -> bool:
        """
        判断是否应该执行障碍物规避
        
        条件：
        - 检测到障碍物或危险
        """
        return len(self.ctx.hazards) > 0
    
    def execute(self) -> dict:
        """
        执行障碍物规避策略
        
        Returns:
            策略执行结果
        """
        # 获取最危险的障碍物
        h = self.ctx.hazards[0]
        hazard_type = h.get("type", "unknown")
        severity = h.get("severity", "medium")
        distance = h.get("distance", 0.0)
        
        self.log("NAV:HAZARD_DETECTED", {
            "hazard_type": hazard_type,
            "severity": severity,
            "distance": distance,
            "position": self.ctx.position,
        })
        
        # 根据危险类型和严重程度决定动作
        if severity == "high" or severity == "critical":
            # 高风险，建议停止或大幅绕行
            if hazard_type in ["construction", "block"]:
                action = "STOP_AND_WARN"
                text = f"前方{distance:.1f}米有严重障碍物，请立即停止并寻找替代路线。"
            else:
                action = "AVOID_SEVERE"
                text = f"前方{distance:.1f}米有危险障碍物，请立即向{h.get('avoid_direction', '右侧')}绕行。"
        else:
            # 一般风险，建议小幅绕行
            avoid_direction = h.get("avoid_direction", "右侧")
            action = "AVOID"
            text = f"前方{distance:.1f}米有障碍物，建议稍微向{avoid_direction}绕行。"
        
        return {
            "success": True,
            "action": action,
            "text": text,
            "hazard": h,
            "hazard_type": hazard_type,
            "severity": severity,
            "distance": distance,
        }



