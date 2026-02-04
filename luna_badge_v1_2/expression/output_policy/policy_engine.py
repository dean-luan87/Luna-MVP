"""
Policy Engine (v1.4.8 Step 13)

核心：决策引擎
"""

from expression.expression_intent import ExpressionIntent
from expression.output_policy.output_slot import OutputSlot
from expression.output_policy.policy_rules import PolicyRules


class PolicyEngine:
    """
    表达治理决策引擎
    
    职责：
    - 评估 ExpressionIntent
    - 生成 OutputSlot（被允许的"说话资格"）
    """
    
    def __init__(self):
        """初始化决策引擎"""
        self.rules = PolicyRules()
    
    def evaluate(self, intent: ExpressionIntent) -> OutputSlot:
        """
        评估 ExpressionIntent，生成 OutputSlot
        
        Args:
            intent: 表达意图
            
        Returns:
            OutputSlot: 输出槽位（包含是否批准、优先级、是否可打断等信息）
        """
        decision = self.rules.apply(intent)
        
        return OutputSlot(
            intent=intent,
            approved=decision["approved"],
            priority=decision["priority"],
            can_interrupt=decision["can_interrupt"],
            ttl_ms=decision["ttl_ms"],
            reason=decision["reason"]
        )
