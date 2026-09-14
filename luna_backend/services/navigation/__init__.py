"""
导航服务模块 (v1.2.0)
导出导航相关的核心类和策略
"""

from .navigation_context import NavigationContext
from .base_strategy import BaseStrategy
from .strategy_engine import StrategyEngine

# 导出所有策略
from .strategies import (
    DeviationCorrectionStrategy,
    ConstructionBypassStrategy,
    CrowdAvoidStrategy,
    HazardAvoidStrategy,
    TrafficLightStrategy,
    BusDirectionStrategy,
    FloorZoneStrategy,
    DestinationCheckStrategy,
    EmotionToneStrategy,
)

__all__ = [
    "NavigationContext",
    "BaseStrategy",
    "StrategyEngine",
    "DeviationCorrectionStrategy",
    "ConstructionBypassStrategy",
    "CrowdAvoidStrategy",
    "HazardAvoidStrategy",
    "TrafficLightStrategy",
    "BusDirectionStrategy",
    "FloorZoneStrategy",
    "DestinationCheckStrategy",
    "EmotionToneStrategy",
]
