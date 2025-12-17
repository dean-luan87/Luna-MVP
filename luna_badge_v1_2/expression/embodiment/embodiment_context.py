"""
Embodiment Context (C-2.1)

身体形态上下文
"""

from dataclasses import dataclass
from .embodiment_types import EmbodimentType


@dataclass
class EmbodimentContext:
    """
    EmbodimentContext 数据类
    
    身体形态上下文：
    - embodiment: 身体类型
    - has_screen: 是否有屏幕
    - has_voice: 是否有语音
    - has_haptics: 是否有触觉反馈
    - mobility: 移动性（"wearable" / "handheld" / "static"）
    """
    embodiment: EmbodimentType
    has_screen: bool
    has_voice: bool
    has_haptics: bool
    mobility: str  # "wearable" | "handheld" | "static"
