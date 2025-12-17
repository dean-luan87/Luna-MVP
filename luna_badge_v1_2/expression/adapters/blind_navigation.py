"""
Blind Navigation Translator (v1.4.8 Step 11)

盲人导航转译器：将 WorldFact 转译为适合盲人导航的表达意图
"""

from ..translator_base import ExpressionTranslator
from ..world_fact import WorldFact
from ..expression_intent import ExpressionIntent
from typing import Optional


class BlindNavigationTranslator(ExpressionTranslator):
    """
    盲人导航转译器
    """
    
    def supports(self, product_type: str) -> bool:
        """
        检查是否支持盲人导航产品类型
        
        Args:
            product_type: 产品类型
            
        Returns:
            bool: 如果 product_type == "blind_navigation" 则返回 True
        """
        return product_type == "blind_navigation"
    
    def translate(self, fact: WorldFact) -> Optional[ExpressionIntent]:
        """
        将 WorldFact 转译为 ExpressionIntent
        
        Args:
            fact: 世界事实
            
        Returns:
            ExpressionIntent: 如果成功转译，返回 ExpressionIntent；否则返回 None
        """
        if fact.fact_type == "PATH_BLOCKED":
            return ExpressionIntent(
                intent_type="WARN",
                urgency=3,
                target="USER",
                semantic_payload={
                    "direction": fact.spatial_ref.get("direction"),
                    "distance": fact.spatial_ref.get("distance")
                },
                constraints={"interrupt": True}
            )
        return None
