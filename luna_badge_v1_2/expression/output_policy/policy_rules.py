"""
Policy Rules (v1.4.8 Step 13)

规则集合（第一版规则集，极简但正确）

注意：
这不是最终规则，只是第一块"骨架钢梁"
"""

from typing import Dict
from expression.expression_intent import ExpressionIntent


class PolicyRules:
    """
    表达治理规则集合
    """
    
    def apply(self, intent: ExpressionIntent) -> Dict:
        """
        应用规则到 ExpressionIntent
        
        Args:
            intent: 表达意图
            
        Returns:
            Dict: 决策结果，包含 approved, priority, can_interrupt, ttl_ms, reason
        """
        # 1️⃣ 紧急安全优先
        if intent.urgency >= 3:  # urgency 0-3，3 为最高
            return {
                "approved": True,
                "priority": 100,
                "can_interrupt": True,
                "ttl_ms": 2000,
                "reason": "critical_urgency"
            }
        
        # 2️⃣ 导航常规播报
        if intent.intent_type == "NAV_GUIDANCE":
            return {
                "approved": True,
                "priority": 50,
                "can_interrupt": False,
                "ttl_ms": 5000,
                "reason": "navigation_flow"
            }
        
        # 3️⃣ WARN 类型（中等优先级）
        if intent.intent_type == "WARN":
            return {
                "approved": True,
                "priority": 70,
                "can_interrupt": True,
                "ttl_ms": 3000,
                "reason": "warning"
            }
        
        # 4️⃣ GUIDE 类型（导航引导）
        if intent.intent_type == "GUIDE":
            return {
                "approved": True,
                "priority": 60,
                "can_interrupt": False,
                "ttl_ms": 4000,
                "reason": "guidance"
            }
        
        # 5️⃣ 状态提示（可丢弃）
        if intent.intent_type == "STATUS_HINT" or intent.intent_type == "INFORM":
            return {
                "approved": True,
                "priority": 20,
                "can_interrupt": False,
                "ttl_ms": 3000,
                "reason": "low_priority_hint"
            }
        
        # 默认拒绝
        return {
            "approved": False,
            "priority": 0,
            "can_interrupt": False,
            "ttl_ms": 0,
            "reason": "filtered"
        }
