from typing import List

from tasks.types import TaskBase, TaskEvent, TaskStatus


class FloorArrivalTask(TaskBase):
    def __init__(self, task_id: str, meta: dict = None):
        super().__init__(task_id=task_id, name="floor_arrival", meta=meta or {})

    def step(self, snapshot: dict) -> List[TaskEvent]:
        nav = snapshot.get("navigation_state", {})
        state = nav.get("floor_state", "unknown")

        if state == "unknown" or state is None:
            self.status = TaskStatus.BLOCKED
            self.last_reason = "FLOOR_STATE_UNKNOWN"
            return [
                TaskEvent(
                    type="SAY",
                    payload={"template_key": "floor_state_unknown", "slots": {}},
                ),
                TaskEvent(
                    type="TASK_STATE",
                    payload={"status": "blocked", "reason": self.last_reason},
                ),
            ]

        if state == "moving":
            self.status = TaskStatus.ACTIVE
            self.last_reason = "FLOOR_MOVING"
            return [
                TaskEvent(
                    type="SAY",
                    payload={"template_key": "floor_moving", "slots": {}},
                )
            ]

        if state == "arrived":
            self.status = TaskStatus.COMPLETED
            self.last_reason = "FLOOR_ARRIVED"
            return [
                TaskEvent(
                    type="SAY",
                    payload={"template_key": "floor_arrived", "slots": {}},
                )
            ]

        self.status = TaskStatus.BLOCKED
        self.last_reason = "FLOOR_STATE_UNSUPPORTED"
        return [
            TaskEvent(type="TASK_STATE", payload={"status": "blocked", "reason": self.last_reason})
        ]
