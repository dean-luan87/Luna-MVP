"""
Output Governance Boundary (C-4)

表达输出治理边界

职责：
- 不改写语义
- 不生成表达
- 只决定：说 / 不说 / 什么时候说

这是 C-4 的核心模块，专门用于控制"生成好的表达是否、何时、以什么方式对人输出"
"""

from dataclasses import dataclass
from typing import Optional, Dict
import time


@dataclass
class GovernanceDecision:
    """
    治理决策
    
    - action: "allow" | "block" | "delay"
    - reason: 原因说明
    - delay_ms: 延迟毫秒数（仅当 action="delay" 时有效）
    """
    action: str  # "allow" | "block" | "delay"
    reason: str
    delay_ms: int = 0


class OutputGovernanceBoundary:
    """
    C-4 核心：表达输出治理边界
    
    职责：
    - 不改写语义
    - 不生成表达
    - 只决定：说 / 不说 / 什么时候说
    
    这是系统"像不像一个靠谱的人"的关键
    """
    
    def __init__(self):
        """初始化输出治理边界"""
        self._last_output_time: Dict[str, float] = {}
    
    def evaluate(
        self,
        *,
        rendered_text: str,
        contract_id: str,
        scene: str,
        urgency: str,
        duplicate_key: Optional[str] = None
    ) -> GovernanceDecision:
        """
        评估输出治理决策
        
        Args:
            rendered_text: C-3 已完成的文本
            contract_id: 表达意图来源（如 "nav.turn.left"）
            scene: 场景标签（"navigation" / "safety" / "system" / "toy"）
            urgency: 紧急程度（"low" / "normal" / "high"）
            duplicate_key: 用于防刷、防重复播报（如 "nav_turn_left_road_023"）
            
        Returns:
            GovernanceDecision: 治理决策
        """
        now = time.time()
        
        # 1. 重复播报治理（一期最重要）
        if duplicate_key:
            last = self._last_output_time.get(duplicate_key)
            if last and now - last < 3.0:
                return GovernanceDecision(
                    action="block",
                    reason="duplicate_suppressed"
                )
        
        # 2. 场景级别限制（一期简单版）
        if scene == "navigation" and urgency == "low":
            # 导航中低优先级内容不打断
            return GovernanceDecision(
                action="delay",
                reason="navigation_low_priority",
                delay_ms=800
            )
        
        # 3. 默认放行
        if duplicate_key:
            self._last_output_time[duplicate_key] = now
        
        return GovernanceDecision(
            action="allow",
            reason="passed"
        )
    
    def execute(self, decision: GovernanceDecision, output_callable):
        """
        统一执行出口
        
        Args:
            decision: 治理决策
            output_callable: 输出回调函数（无参数）
        """
        if decision.action == "block":
            return
        
        if decision.action == "delay":
            time.sleep(decision.delay_ms / 1000.0)
        
        output_callable()
    
    def reset(self, duplicate_key: Optional[str] = None):
        """
        重置状态
        
        Args:
            duplicate_key: 要重置的键（None 表示重置所有）
        """
        if duplicate_key is None:
            self._last_output_time.clear()
        elif duplicate_key in self._last_output_time:
            del self._last_output_time[duplicate_key]


class DummyPassThrough:
    """
    临时回滚用的空实现
    
    用于在需要时关闭 C-4 治理功能
    """
    
    def evaluate(self, **kwargs) -> GovernanceDecision:
        """直接放行"""
        return GovernanceDecision(action="allow", reason="bypassed")
    
    def execute(self, decision: GovernanceDecision, output_callable):
        """直接执行"""
        output_callable()
    
    def reset(self, duplicate_key: Optional[str] = None):
        """空操作"""
        pass
