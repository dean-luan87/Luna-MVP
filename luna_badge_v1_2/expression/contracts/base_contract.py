"""
Base Contract (C-1)

通用字段规范（字典/常量即可）

定义 BaseExpressionContract（dataclass）
"""

from dataclasses import dataclass
from typing import Dict, Any
import time

# 通用字段常量
FIELD_INTENT_TYPE = "intent_type"
FIELD_CONFIDENCE = "confidence"
FIELD_URGENCY = "urgency"
FIELD_TIMESTAMP = "timestamp"
FIELD_SOURCE = "source"

# 通用字段规范（字典/常量）
BASE_CONTRACT_FIELDS = {
    FIELD_INTENT_TYPE: str,
    FIELD_CONFIDENCE: float,
    FIELD_URGENCY: int,
    FIELD_TIMESTAMP: float,
    FIELD_SOURCE: str
}


@dataclass
class BaseExpressionContract:
    """
    BaseExpressionContract（dataclass）
    
    必须字段：
    - intent_type: str            # e.g. navigation / safety
    - source: str                 # fsm / vision / map / system
    - confidence: float           # 0.0 ~ 1.0
    - timestamp: float            # time.time()
    """
    intent_type: str            # e.g. "navigation" / "safety"
    source: str                 # "fsm" / "vision" / "map" / "system"
    confidence: float           # 0.0 ~ 1.0
    timestamp: float            # time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典
        
        Returns:
            Dict[str, Any]: 合约字典
        """
        return {
            "intent_type": self.intent_type,
            "source": self.source,
            "confidence": self.confidence,
            "timestamp": self.timestamp
        }


def validate_base_fields(contract: Dict[str, Any]) -> bool:
    """
    验证基础字段是否存在
    
    Args:
        contract: 合约字典
        
    Returns:
        bool: 是否通过验证
    """
    for field in BASE_CONTRACT_FIELDS.keys():
        if field not in contract:
            return False
    return True
