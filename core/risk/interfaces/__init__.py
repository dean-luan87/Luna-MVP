# -*- coding: utf-8 -*-
"""
v1.8.4: 接口模块（世界模型、安全边界等接口桩）

职责：
- 定义世界模型接口（护栏高度/完整性等）
- 定义安全边界接口（越界事件）
- 为后续世界模型集成预留接口
"""

from core.risk.interfaces.world_model_iface import WorldModelInterface
from core.risk.interfaces.safety_boundary_iface import SafetyBoundaryInterface

__all__ = [
    "WorldModelInterface",
    "SafetyBoundaryInterface",
]


