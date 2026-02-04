from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, Optional, List


class TaskStatus(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    WAITING = "waiting"  # Task v2: 目标存在但条件未满足
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"  # Task v2: 等待超时


@dataclass
class TaskEvent:
    type: str
    payload: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TaskBase:
    task_id: str
    name: str
    status: TaskStatus = TaskStatus.PENDING
    meta: Dict[str, Any] = field(default_factory=dict)
    last_reason: Optional[str] = None

    def can_start(self, snapshot: dict) -> bool:
        return True

    def step(self, snapshot: dict) -> List[TaskEvent]:
        raise NotImplementedError

    def cancel(self, reason: str = "CANCELLED") -> List[TaskEvent]:
        self.status = TaskStatus.CANCELLED
        self.last_reason = reason
        return [
            TaskEvent(
                type="TASK_STATE",
                payload={"status": self.status.value, "reason": reason},
            )
        ]
