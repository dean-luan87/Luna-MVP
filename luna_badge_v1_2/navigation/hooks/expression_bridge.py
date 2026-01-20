"""
Expression Bridge (v1.4.8 Step 12)

导航系统 → 表达系统 的唯一桥梁
"""

from typing import Optional
from expression.translator_registry import TranslatorRegistry
from expression.expression_intent import ExpressionIntent
from expression.world_fact import WorldFact


class ExpressionBridge:
    """
    导航系统 → 表达系统 的唯一桥梁
    """
    
    def __init__(self, product_type: str, registry: TranslatorRegistry):
        """
        初始化桥梁
        
        Args:
            product_type: 产品类型（如 "blind_navigation", "toy_companion", "debug"）
            registry: 转译器注册表
        """
        self.product_type = product_type
        self.registry = registry
    
    def handle_fact(self, fact: WorldFact) -> Optional[ExpressionIntent]:
        """
        处理 WorldFact，转译为 ExpressionIntent
        
        Args:
            fact: 世界事实
            
        Returns:
            ExpressionIntent: 如果成功转译，返回 ExpressionIntent；否则返回 None
        """
        return self.registry.translate(
            product_type=self.product_type,
            fact=fact
        )






