"""
Task modules for Luna Badge v1.4.2
"""

# v1.4.2 新模块（独立导入，无依赖）
from .task_transition_manager import (
    TaskTransitionManager,
    TaskDecision,
    PositionState,
    UserIntentState,
    TaskContext as TransitionTaskContext,
)
from .multi_target_buffer import MultiTargetBuffer, Target
from .query_bus import QueryBus, Query, QueryStatus

# 旧模块（延迟导入，避免依赖问题）
try:
    from .task_engine import TaskContext, TaskEngine
    from .task_chain import TaskChain
    from .task_cache_manager import TaskCacheManager
    from .task_debugger import TaskDebugger
    _has_legacy_modules = True
except ImportError:
    _has_legacy_modules = False

__all__ = [
    # v1.4.2 新模块
    "TaskTransitionManager",
    "TaskDecision",
    "PositionState",
    "UserIntentState",
    "TransitionTaskContext",
    "MultiTargetBuffer",
    "Target",
    "QueryBus",
    "Query",
    "QueryStatus",
]

# 如果旧模块可用，也导出
if _has_legacy_modules:
    __all__.extend([
        "TaskContext",
        "TaskEngine",
        "TaskChain",
        "TaskCacheManager",
        "TaskDebugger",
    ])

