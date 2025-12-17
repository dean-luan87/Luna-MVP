"""
Output Slot (v1.4.8 Step 13)

被允许的"说话资格"
"""

from dataclasses import dataclass
from typing import Optional
from expression.expression_intent import ExpressionIntent


@dataclass
class OutputSlot:
    """
    被允许的"说话资格"
    """
    intent: ExpressionIntent
    approved: bool
    priority: int
    can_interrupt: bool
    ttl_ms: int
    reason: str
