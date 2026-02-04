"""
Expression Output (v1.4.8 Step 11)

转译层最终输出（仍不绑定 TTS / UI）
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ExpressionOutput:
    """
    转译层最终输出（仍不绑定 TTS / UI）
    """
    intent_type: str
    urgency: int
    payload: Dict[str, Any]
    constraints: Dict[str, Any]
