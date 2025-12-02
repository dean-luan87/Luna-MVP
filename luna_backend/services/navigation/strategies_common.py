"""
通用导航策略 (Common Navigation Strategies) v1.2.0
一般导航策略：偏航/施工/人多等通用场景
"""

from typing import Dict, Any, Optional
from .strategies_base import BaseStrategy
from .context import NavigationContext
from .multi_target_planner import MultiTargetPlanner


class DeviationCorrectionStrategy(BaseStrategy):
    """偏航纠正策略"""
    
    STRATEGY_NAME = "DEVIATION_CORRECTION"
    
    def should_execute(self) -> bool:
        """判断是否应该执行偏航纠正"""
        return self.ctx.need_reroute and not self.ctx.construction
    
    def execute(self) -> Dict[str, Any]:
        """执行偏航纠正策略"""
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
            "strategy": self.STRATEGY_NAME,
        }


class ConstructionBypassStrategy(BaseStrategy):
    """施工绕行策略"""
    
    STRATEGY_NAME = "CONSTRUCTION_BYPASS"
    
    def should_execute(self) -> bool:
        """判断是否应该执行施工绕行"""
        return self.ctx.construction is True
    
    def execute(self) -> Dict[str, Any]:
        """执行施工绕行策略"""
        self.log("NAV:CONSTRUCTION_DETECTED", {
            "position": self.ctx.position,
        })
        
        return {
            "success": True,
            "action": "REROUTE",
            "text": "前方道路施工，我已为您规划绕行路线，请按照新的路线前行。",
            "reroute_reason": "construction",
            "strategy": self.STRATEGY_NAME,
        }


class CrowdAvoidStrategy(BaseStrategy):
    """拥挤人群规避策略"""
    
    STRATEGY_NAME = "CROWD_AVOID"
    CROWD_THRESHOLD = 0.65  # 65%以上认为拥挤
    
    def should_execute(self) -> bool:
        """判断是否应该执行拥挤规避"""
        return self.ctx.people_density >= self.CROWD_THRESHOLD
    
    def execute(self) -> Dict[str, Any]:
        """执行拥挤规避策略"""
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
            "strategy": self.STRATEGY_NAME,
        }


class MultiTargetNavStrategy(BaseStrategy):
    """
    多目标导航策略
    
    当用户说"先去711再去医院"时，把多目标信息写入 ctx，
    此策略负责调用 MultiTargetPlanner 并生成任务链。
    """
    
    STRATEGY_NAME = "MULTI_TARGET_NAV"
    
    def __init__(self, context: NavigationContext, base_planner=None):
        """
        初始化多目标导航策略
        
        Args:
            context: 导航上下文
            base_planner: 基础路径规划器（可选）
        """
        super().__init__(context)
        if base_planner:
            self.planner = MultiTargetPlanner(base_planner)
        else:
            self.planner = None
    
    def should_execute(self) -> bool:
        """判断是否应该执行多目标导航"""
        return (
            self.ctx.multi_targets is not None and
            len(self.ctx.multi_targets) > 0
        )
    
    def execute(self) -> Dict[str, Any]:
        """执行多目标导航策略"""
        if not self.planner:
            return {
                "success": False,
                "action": "ERROR",
                "text": "路径规划器未初始化",
                "strategy": self.STRATEGY_NAME,
            }
        
        if not self.ctx.start_point:
            self.ctx.start_point = "当前位置"
        
        result = self.planner.plan_sequence(
            self.ctx.start_point,
            self.ctx.multi_targets
        )
        
        # 更新上下文
        self.ctx.planned_routes = result["routes"]
        self.ctx.multi_targets_ordered = result["ordered"]
        
        return {
            "success": True,
            "action": "NAV_MULTI_TARGET",
            "text": "好的，我会先带你去第一个地点，再带你去下一个。",
            "meta": {
                "targets": [t.get("name", "") for t in result["ordered"]],
                "total_distance": result["total_distance"]
            },
            "strategy": self.STRATEGY_NAME,
        }



