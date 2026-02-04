"""
Task State

任务状态定义。

v1.5 设计原则：
- TaskChain 是"任务状态主权者"
- 状态是第一等公民
- FAILED ≠ ABORTED
"""

from enum import Enum


class TaskState(Enum):
    """
    任务状态枚举
    
    职责：
    - 定义任务链的所有可能状态
    - 状态是第一等公民，所有操作必须基于状态
    
    关键原则：
    - FAILED ≠ ABORTED
    - FAILED：还有 PlanB，可以恢复
    - ABORTED：系统/策略禁止继续，不可恢复
    """
    PENDING = "pending"      # 等待启动
    RUNNING = "running"      # 正在执行
    PAUSED = "paused"        # 已暂停（可恢复）
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"        # 失败（有 PlanB，可恢复）
    ABORTED = "aborted"      # 已中止（系统/策略禁止继续，不可恢复）
    
    def is_terminal(self) -> bool:
        """
        判断是否为终止状态（不可继续执行）
        
        Returns:
            True 如果是 COMPLETED 或 ABORTED
        """
        return self in (TaskState.COMPLETED, TaskState.ABORTED)
    
    def can_resume(self) -> bool:
        """
        判断是否可以恢复
        
        Returns:
            True 如果是 PAUSED 或 FAILED
        """
        return self in (TaskState.PAUSED, TaskState.FAILED)
    
    def can_pause(self) -> bool:
        """
        判断是否可以暂停
        
        Returns:
            True 如果是 RUNNING
        """
        return self == TaskState.RUNNING





