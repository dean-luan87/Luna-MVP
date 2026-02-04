"""
Toy Companion Translator (v1.4.8 Step 11)

玩具伴侣转译器：将 WorldFact 转译为适合玩具伴侣的表达意图
"""

from ..translator_base import ExpressionTranslator
from ..world_fact import WorldFact
from ..expression_intent import ExpressionIntent
from typing import Optional


class ToyCompanionTranslator(ExpressionTranslator):
    """
    玩具伴侣转译器
    """
    
    def supports(self, product_type: str) -> bool:
        """
        检查是否支持玩具伴侣产品类型
        
        Args:
            product_type: 产品类型
            
        Returns:
            bool: 如果 product_type == "toy_companion" 则返回 True
        """
        return product_type == "toy_companion"
    
    def translate(self, fact: WorldFact) -> Optional[ExpressionIntent]:
        """
        将 WorldFact 转译为 ExpressionIntent
        
        Args:
            fact: 世界事实
            
        Returns:
            ExpressionIntent: 如果成功转译，返回 ExpressionIntent；否则返回 None
        """
        if fact.fact_type == "LANDMARK_DETECTED":
            return ExpressionIntent(
                intent_type="INFORM",
                urgency=1,
                target="USER",
                semantic_payload={
                    "hint": "something_interesting_ahead"
                },
                constraints={"soft": True}
            )
        return None
