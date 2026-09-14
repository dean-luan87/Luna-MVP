"""
B2 - 上帝视角的大场景观察器 + 未来 5-10 秒任务链预演器

B2 不控制 C，只提供信息与置信度
"""

from .b2_types import (
    B2Output,
    FutureSegmentBuffer,
    Advisory,
    ConfidenceReport,
    WorldModelPatch,
    TaskCorridor,
    ImpactEvent,
)

from .b2_controller import B2Controller
from .b2_integration import SharedBlackboard
from .b2_config import B2_V01_ENABLED
from .b2_world_update_builder import build_b2_world_update, build_b2_impact_events

# B2 v0.2 新增模块
from .b2_world_accumulator import WorldAccumulator
from .b2_task_corridor_builder import TaskCorridorBuilder
from .b2_future_simulator import FutureSimulator, FutureWorld
from .b2_advisory_generator import B2AdvisoryGenerator

__all__ = [
    "B2Output",
    "FutureSegmentBuffer",
    "Advisory",
    "ConfidenceReport",
    "WorldModelPatch",
    "TaskCorridor",
    "ImpactEvent",
    "B2Controller",
    "SharedBlackboard",
    "B2_V01_ENABLED",
    "build_b2_world_update",
    "build_b2_impact_events",
    # B2 v0.2 新增
    "WorldAccumulator",
    "TaskCorridorBuilder",
    "FutureSimulator",
    "FutureWorld",
    "B2AdvisoryGenerator",
]

