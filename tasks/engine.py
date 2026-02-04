from typing import Dict, Any, List, Optional

from tasks.types import TaskBase, TaskEvent, TaskStatus


class TaskEngine:
    def __init__(self):
        self.active_task: Optional[TaskBase] = None

    def start_task(self, task: TaskBase) -> List[TaskEvent]:
        self.active_task = task
        self.active_task.status = TaskStatus.ACTIVE
        return [TaskEvent(type="TASK_STATE", payload={"status": "active", "task": task.name})]

    def tick(self, snapshot: Dict[str, Any]) -> List[TaskEvent]:
        if self.active_task is None:
            return []

        events = self.active_task.step(snapshot)

        if self.active_task.status in (
            TaskStatus.COMPLETED,
            TaskStatus.FAILED,
            TaskStatus.CANCELLED,
        ):
            events.append(
                TaskEvent(
                    type="TASK_STATE",
                    payload={
                        "status": self.active_task.status.value,
                        "task": self.active_task.name,
                        "reason": self.active_task.last_reason,
                    },
                )
            )
            self.active_task = None

        return events

    def cancel_active(self, reason: str = "USER_CANCEL") -> List[TaskEvent]:
        if self.active_task is None:
            return []
        events = self.active_task.cancel(reason)
        self.active_task = None
        return events
