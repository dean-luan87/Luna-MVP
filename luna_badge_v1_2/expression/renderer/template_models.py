"""
Template Models (C-3.2)

模板数据结构
"""

from dataclasses import dataclass
from typing import List


@dataclass
class ExpressionTemplate:
    """
    ExpressionTemplate 数据类
    
    表达模板：
    - template_id: 模板 ID
    - supported_actions: 支持的动作列表
    - min_precision: 最小精确度
    - max_precision: 最大精确度
    - language: 语言（"zh" / "en"）
    - pattern: 模板模式（如 "{distance}{unit}后，{direction}转"）
    """
    template_id: str
    supported_actions: List[str]
    min_precision: int
    max_precision: int
    language: str  # "zh" / "en"
    pattern: str   # "{distance}{unit}后，{direction}转"
