# -*- coding: utf-8 -*-
"""
v1.8.4: 危险评估与告知系统（Risk Advisory System）

模块职责：
- 评估环境的危险程度
- 判断危险态势是否上升
- 在阈值触发时进行一次性告知

核心原则：
- 只提示"危险态势上升"，不推断行为、不放大风险、不做安全承诺
- 警告 ≠ 真实危险 ≠ 事故预测
"""

from core.risk.risk_types import RiskType, RISK_TYPE_CONFIG
from core.risk.risk_object import RiskObject, RiskGeometry, RiskRuntime, DynamicProfile
from core.risk.dynamic_evaluator import is_active, apply_hazard_modifier
from core.risk.hazard_evaluator import HazardEvaluator
from core.risk.geometry_utils import (
    distance_to_geometry,
    is_inside_area,
    polyline_length
)
from core.risk.risk_engine import RiskEngine
from core.risk.warning_policy import WarningPolicy
from core.risk.risk_registry import RiskRegistry
from core.risk.user_position_provider import UserPositionProvider, PositionSample
from core.risk.risk_object_factory import RiskObjectFactory
from core.risk.risk_advisory_service import RiskAdvisoryService
from core.risk.risk_debug import RiskDebugSnapshot, RiskObjectSnapshot

__all__ = [
    "RiskType",
    "RISK_TYPE_CONFIG",
    "RiskObject",
    "RiskGeometry",
    "RiskRuntime",
    "DynamicProfile",
    "HazardEvaluator",
    "distance_to_geometry",
    "is_inside_area",
    "polyline_length",
    "RiskEngine",
    "WarningPolicy",
    "RiskRegistry",
    "UserPositionProvider",
    "PositionSample",
    "RiskObjectFactory",
    "RiskAdvisoryService",
    "is_active",
    "apply_hazard_modifier",
    "RiskDebugSnapshot",
    "RiskObjectSnapshot",
]

