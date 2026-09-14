from dataclasses import dataclass, field
from typing import Dict, Any, List

from tasks.types import TaskEvent


@dataclass
class TaskContext:
    snapshot: Dict[str, Any]
    events: List[TaskEvent] = field(default_factory=list)

    def say(self, template_key: str, slots: Dict[str, Any] = None):
        self.events.append(
            TaskEvent(
                type="SAY",
                payload={"template_key": template_key, "slots": slots or {}},
            )
        )

    def set_task_state_patch(self, patch: Dict[str, Any]):
        self.events.append(TaskEvent(type="TASK_STATE_PATCH", payload=patch))
