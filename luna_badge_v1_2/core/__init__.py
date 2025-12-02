"""
Luna Badge v1.3.0 Core Modules
"""

# 导出主要模块
from .model_router import ModelRouter
from .qwen_loader import QwenModelLoader, load_l1, load_l2
from .tracking import TrackingSystem, EventType
from .error_codes import ErrorCode, ErrorInfo, create_error_response, create_success_response
from .inference_wrapper import InferenceWrapper
from .replay_manager import ReplayManager, ReplayMode
# 修复导入路径 - 从 task.task_chain 导入
try:
    from .task.task_chain import TaskChain
    # 提供兼容的占位
    TaskNode = None
    def new_task_chain(name="default"):
        return TaskChain(name)
except ImportError:
    # 如果导入失败，提供占位类
    class TaskChain:
        def __init__(self, name="default"):
            self.name = name
    TaskNode = None
    def new_task_chain(name="default"):
        return TaskChain(name)
from .task_chain_manager import TaskChainManager
from .luna_engine import LunaEngine
from .config import CONFIG, Config

__all__ = [
    "ModelRouter",
    "QwenModelLoader",
    "load_l1",
    "load_l2",
    "TrackingSystem",
    "EventType",
    "ErrorCode",
    "ErrorInfo",
    "create_error_response",
    "create_success_response",
    "InferenceWrapper",
    "ReplayManager",
    "ReplayMode",
    "TaskNode",
    "TaskChain",
    "new_task_chain",
    "TaskChainManager",
    "LunaEngine",
    "CONFIG",
    "Config",
]
