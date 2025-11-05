"""
Luna-mid 学习系统核心模块
"""

__version__ = "1.0.0"
__version_info__ = (1, 0, 0)

# 导出学习系统相关模块

# 错误学习引擎
from .error_learning import (
    ErrorLearningEngine,
    ErrorType,
    CorrectionSource,
    ErrorRecord,
    ErrorAnalysis
)

# 任务优化引擎
from .task_optimizer import (
    TaskOptimizer,
    OptimizationSource,
    TaskExecution,
    TaskOptimization
)

# 用户习惯分析引擎
from .user_habit_analyzer import (
    UserHabitAnalyzer,
    WalkingSession,
    UserHabitProfile
)

# 视觉学习引擎
from .visual_learning import (
    VisualLearningEngine,
    RecognitionSource,
    ObjectCategory,
    VisualObject,
    ObjectKnowledge
)

# 统一管理模块
from .learning_manager import LearningSystemManager

__all__ = [
    # 错误学习
    "ErrorLearningEngine",
    "ErrorType",
    "CorrectionSource",
    "ErrorRecord",
    "ErrorAnalysis",
    # 任务优化
    "TaskOptimizer",
    "OptimizationSource",
    "TaskExecution",
    "TaskOptimization",
    # 用户习惯
    "UserHabitAnalyzer",
    "WalkingSession",
    "UserHabitProfile",
    # 视觉学习
    "VisualLearningEngine",
    "RecognitionSource",
    "ObjectCategory",
    "VisualObject",
    "ObjectKnowledge",
    # 统一管理
    "LearningSystemManager",
]


