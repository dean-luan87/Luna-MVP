"""
Debug Expression Logger (v1.4.8 Step 12)

表达意图日志记录器

说明：
这是 Step 12 唯一允许的"输出行为"
"""

from typing import Optional
from expression.expression_intent import ExpressionIntent


def log_expression_intent(intent: Optional[ExpressionIntent]) -> None:
    """
    记录 ExpressionIntent 日志
    
    Args:
        intent: 表达意图（可选）
    """
    if not intent:
        return
    
    print(
        "[EXPRESSION_INTENT]",
        f"type={intent.intent_type}",
        f"urgency={intent.urgency}",
        f"target={intent.target}",
        f"payload={intent.semantic_payload}",
        f"constraints={intent.constraints}"
    )






