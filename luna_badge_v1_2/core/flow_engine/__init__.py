"""
Flow Engine Module

负责任务链的定义、规划、执行和运行时管理
"""

from .flow_types import (
    FlowNode,
    FlowEdge,
    FlowContext,
    FlowDefinition,
    FlowInstance,
    FlowNodeType,
    PlanningInput,
)
from .runtime import FlowRuntime

__all__ = [
    "FlowNode",
    "FlowEdge",
    "FlowContext",
    "FlowDefinition",
    "FlowInstance",
    "FlowNodeType",
    "PlanningInput",
    "FlowRuntime",
]

# FlowPlanner 延迟导入，避免循环依赖
def __getattr__(name):
    if name == "FlowPlanner":
        from .planner import FlowPlanner
        return FlowPlanner
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

