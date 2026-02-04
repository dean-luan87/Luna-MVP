"""
Translator Base (v1.4.8 Step 11)

转译器基类：WorldFact → ExpressionIntent
"""

from abc import ABC, abstractmethod
from typing import Optional
from .world_fact import WorldFact
from .expression_intent import ExpressionIntent


class ExpressionTranslator(ABC):
    """
    转译器基类：WorldFact → ExpressionIntent
    """
    
    @abstractmethod
    def supports(self, product_type: str) -> bool:
        """
        检查是否支持指定的产品类型
        
        Args:
            product_type: 产品类型（如 "blind_navigation", "toy_companion", "debug"）
            
        Returns:
            bool: 是否支持
        """
        pass
    
    @abstractmethod
    def translate(self, fact: WorldFact) -> Optional[ExpressionIntent]:
        """
        将 WorldFact 转译为 ExpressionIntent
        
        Args:
            fact: 世界事实
            
        Returns:
            ExpressionIntent: 如果成功转译，返回 ExpressionIntent；否则返回 None
        """
        pass
