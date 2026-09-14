"""
视觉导航模块 (v1.2.0)
负责视觉辅助指引（视觉导航 → 文本化指引 → 与主导航模块联动）
"""

from .nav_guide_generator import VisualGuideGenerator
from .nav_hint_builder import NavHintBuilder
from .nav_merge_strategy import NavMergeStrategy
from .interfaces.visual_nav_interface import VisualNavigationInterface
from .interfaces.nav_hint_protocol import (
    NavHintProtocol,
    StandardNavHintProtocol,
    CompactNavHintProtocol,
    DetailedNavHintProtocol
)

__all__ = [
    'VisualGuideGenerator',
    'NavHintBuilder',
    'NavMergeStrategy',
    'VisualNavigationInterface',
    'NavHintProtocol',
    'StandardNavHintProtocol',
    'CompactNavHintProtocol',
    'DetailedNavHintProtocol'
]



