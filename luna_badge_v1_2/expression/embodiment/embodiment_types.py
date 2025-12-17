"""
Embodiment Types (C-2.1)

身体类型枚举
"""

from enum import Enum


class EmbodimentType(Enum):
    """
    EmbodimentType Enum
    
    身体类型：
    - BLIND_BADGE: 视障徽章
    - TOY: 玩具
    - MOBILE_APP: 手机
    - DESKTOP: 桌面
    - GENERIC: 保底
    """
    BLIND_BADGE = "blind_badge"     # 视障徽章
    TOY = "toy"                     # 玩具
    MOBILE_APP = "mobile_app"       # 手机
    DESKTOP = "desktop"             # 桌面
    GENERIC = "generic"             # 保底
