"""
Render Models (C-3)

渲染器数据模型
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
from ..calibrator.protocol import ExpressionProtocol


@dataclass
class RenderedMessage:
    """
    RenderedMessage 数据类
    
    转译层最终输出（仍不绑定 TTS / UI）
    """
    text: str
    tags: Dict[str, Any]
    protocol: ExpressionProtocol
    embodiment: str
    
    # 可选扩展字段
    extra: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = {}
        if self.extra is None:
            self.extra = {}
