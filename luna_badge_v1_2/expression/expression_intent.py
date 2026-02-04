"""
Expression Intent (v1.4.8 Step 11)

表达意图：已经决定"要不要说 + 说什么"，但尚未决定"怎么说"
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ExpressionIntent:
    """
    表达意图：已经决定"要不要说 + 说什么"，但尚未决定"怎么说"
    """
    intent_type: str                # "WARN" / "GUIDE" / "INFORM" / "SILENT"
    urgency: int                    # 0-3
    target: str                     # "USER" / "SYSTEM" / "DEBUG"
    
    semantic_payload: Dict[str, Any]
    constraints: Dict[str, Any]     # 节奏、是否可打断、优先级等
