"""
Vision modules for Luna Badge v1.4.2
"""

# 尝试导入现有模块（如果存在）
try:
    from .vision_scheduler import VisionScheduler, SchedulerContext, SchedulerMode
except ImportError:
    VisionScheduler = None
    SchedulerContext = None
    SchedulerMode = None

try:
    from .vision_fail_safe import VisionFailSafe, FailSafeConfig, FailSafeState, VisionErrorCounters
except ImportError:
    VisionFailSafe = None
    FailSafeConfig = None
    FailSafeState = None
    VisionErrorCounters = None

# 导入新的 VisionTaskOrchestrator 模块
from .vision_task_orchestrator import VisionTaskOrchestrator, VisionTask, VisionResult
from .vision_router import VisionRouter
from .multi_model_engine import MultiModelEngine, ModelSpec, ModelHealth
from .arbiter import Arbiter, ArbiterDecision, ModelScore
from .score_logger import ScoreLogger, ScoreLogEntry, ModelStats
from .vision_debug_service import VisionDebugService, VisionHealthSnapshot

__all__ = [
    "VisionTaskOrchestrator",
    "VisionTask",
    "VisionResult",
    "VisionRouter",
    "MultiModelEngine",
    "ModelSpec",
    "ModelHealth",
    "Arbiter",
    "ArbiterDecision",
    "ModelScore",
    "ScoreLogger",
    "ScoreLogEntry",
    "ModelStats",
    "VisionDebugService",
    "VisionHealthSnapshot",
]

# 条件性导出现有模块
if VisionScheduler is not None:
    __all__.extend(["VisionScheduler", "SchedulerContext", "SchedulerMode"])
if VisionFailSafe is not None:
    __all__.extend(["VisionFailSafe", "FailSafeConfig", "FailSafeState", "VisionErrorCounters"])
