"""
Expert Debug Translator (v1.4.8 Step 11)

专家调试转译器：将 WorldFact 转译为适合调试的表达意图
"""

from ..translator_base import ExpressionTranslator
from ..world_fact import WorldFact
from ..expression_intent import ExpressionIntent
from typing import Optional


class ExpertDebugTranslator(ExpressionTranslator):
    """
    专家调试转译器
    """
    
    def supports(self, product_type: str) -> bool:
        """
        检查是否支持调试产品类型
        
        Args:
            product_type: 产品类型
            
        Returns:
            bool: 如果 product_type == "debug" 则返回 True
        """
        return product_type == "debug"
    
    def translate(self, fact: WorldFact) -> Optional[ExpressionIntent]:
        """
        将 WorldFact 转译为 ExpressionIntent
        
        Args:
            fact: 世界事实
            
        Returns:
            ExpressionIntent: 总是返回 ExpressionIntent（调试模式转译所有事实）
        """
        return ExpressionIntent(
            intent_type="INFORM",
            urgency=0,
            target="DEBUG",
            semantic_payload={
                "fact_type": fact.fact_type,
                "confidence": fact.confidence,
                "source": fact.source,
                "raw_ref_id": fact.raw_ref_id
            },
            constraints={}
        )
