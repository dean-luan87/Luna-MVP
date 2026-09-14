from typing import List

from tasks.types import TaskBase, TaskEvent, TaskStatus


class ElevatorButtonTask(TaskBase):
    def __init__(self, task_id: str, meta: dict = None):
        super().__init__(task_id=task_id, name="elevator_button", meta=meta or {})

    def step(self, snapshot: dict) -> List[TaskEvent]:
        target = self.meta.get("target_floor")

        if not target:
            self.status = TaskStatus.FAILED
            self.last_reason = "MISSING_TARGET_FLOOR"
            return [
                TaskEvent(
                    type="SAY",
                    payload={"template_key": "elevator_missing_target", "slots": {}},
                )
            ]

        self.status = TaskStatus.COMPLETED
        self.last_reason = "INSTRUCT_PRESS"
        return [
            TaskEvent(
                type="SAY",
                payload={"template_key": "elevator_press_floor", "slots": {"target_floor": target}},
            )
        ]
