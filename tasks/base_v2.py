"""
Task v2: BaseTask with WAITING/BLOCKED/TIMEOUT support.
直接读取 world_entities（ObservedEntity），不依赖 snapshot。
"""
import time
from typing import Dict, Optional

from tasks.types import TaskStatus
from dynamic_view.entity import ObservedEntity
from dynamic_view.types import ObservationState


class BaseTask:
    """Task v2 基类：支持 WAITING/BLOCKED/TIMEOUT 状态。"""

    task_name = "BaseTask"

    def __init__(self, *, max_wait_time: float = 10.0):
        self.state = TaskStatus.PENDING
        self.started_at: Optional[float] = None
        self.last_seen_at: Optional[float] = None
        self.max_wait_time = max_wait_time
        self.last_reason: Optional[str] = None

    def _start(self, now: float):
        """启动任务。"""
        self.started_at = now
        self.state = TaskStatus.ACTIVE

    def _timeout(self, now: float) -> bool:
        """检查是否超时。如果超时，设置状态为 TIMEOUT。"""
        if self.started_at is not None and (now - self.started_at) >= self.max_wait_time:
            self.state = TaskStatus.TIMEOUT
            self.last_reason = "TIMEOUT"
            return True
        return False

    def tick(self, world_entities: Dict[str, ObservedEntity], now: float, attr_map: Optional[Dict[str, Dict]] = None):
        """
        子类需实现此方法。
        根据 world_entities 的状态更新任务状态。
        
        Args:
            world_entities: Dynamic View 的实体字典
            now: 当前时间戳
            attr_map: entity_id -> attributes 映射（可选，用于获取实体属性）
        """
        raise NotImplementedError
