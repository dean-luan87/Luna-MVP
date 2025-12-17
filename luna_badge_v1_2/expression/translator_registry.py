"""
Translator Registry (v1.4.8 Step 11)

转译器注册表：管理多个转译器，支持产品类型路由
"""

from typing import List, Optional
from .translator_base import ExpressionTranslator
from .world_fact import WorldFact
from .expression_intent import ExpressionIntent


class TranslatorRegistry:
    """
    转译器注册表
    
    职责：
    - 注册多个转译器
    - 根据产品类型路由到合适的转译器
    """
    
    def __init__(self):
        """初始化注册表"""
        self._translators: List[ExpressionTranslator] = []
    
    def register(self, translator: ExpressionTranslator) -> None:
        """
        注册转译器
        
        Args:
            translator: 转译器实例
        """
        self._translators.append(translator)
    
    def translate(
        self,
        product_type: str,
        fact: WorldFact
    ) -> Optional[ExpressionIntent]:
        """
        转译 WorldFact 为 ExpressionIntent
        
        Args:
            product_type: 产品类型
            fact: 世界事实
            
        Returns:
            ExpressionIntent: 如果成功转译，返回 ExpressionIntent；否则返回 None
        """
        for t in self._translators:
            if t.supports(product_type):
                result = t.translate(fact)
                if result:
                    return result
        return None
