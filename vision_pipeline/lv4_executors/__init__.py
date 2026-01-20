# -*- coding: utf-8 -*-
"""
LV4: 并行执行层（Executors）

职责：
- 真正消耗算力的地方，必须严格调度
- LV4.1: Navigation Executor（主线）
- LV4.2: World Modeling Executor（异步）

设计原则：
- LV4.1 最高优先级，可抢占其他 LV4 任务
- LV4.2 异步执行，可暂停/降频，在导航激活时自动让路
"""

from .navigation_executor import NavigationExecutor, NavigationResult
from .modeling_executor import ModelingExecutor, ModelingResult

__all__ = [
    "NavigationExecutor",
    "NavigationResult",
    "ModelingExecutor",
    "ModelingResult",
]


