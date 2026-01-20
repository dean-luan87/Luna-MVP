"""
Navigation Hooks (v1.4.8 Step 12)

导航系统与表达系统的桥接层
"""

from .world_fact_emitter import WorldFactEmitter
from .expression_bridge import ExpressionBridge
from .debug_expression_logger import log_expression_intent

__all__ = [
    "WorldFactEmitter",
    "ExpressionBridge",
    "log_expression_intent",
]






