"""
Expression Protocol (C-2.5)

用什么认知协议说（专业/口语/共识词/引导）
"""

from enum import Enum


class ExpressionProtocol(Enum):
    """
    ExpressionProtocol Enum
    
    表达协议类型：
    - PROFESSIONAL: 专业术语
    - COLLOQUIAL: 口语化
    - CONSENSUS: 共识词
    - GUIDED: 引导式
    """
    PROFESSIONAL = "professional"
    COLLOQUIAL = "colloquial"
    CONSENSUS = "consensus"
    GUIDED = "guided"
