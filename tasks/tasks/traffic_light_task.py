from typing import List

from tasks.types import TaskBase, TaskEvent, TaskStatus


class TrafficLightTask(TaskBase):
    def __init__(self, task_id: str, meta: dict = None):
        super().__init__(task_id=task_id, name="traffic_light", meta=meta or {})

    def step(self, snapshot: dict) -> List[TaskEvent]:
        facts = snapshot.get("perception_facts", {})
        light = facts.get("traffic_light", "unknown")

        if light == "unknown" or light is None:
            self.status = TaskStatus.BLOCKED
            self.last_reason = "TRAFFIC_LIGHT_UNKNOWN"
            return [
                TaskEvent(
                    type="SAY",
                    payload={"template_key": "traffic_light_unknown", "slots": {}},
                ),
                TaskEvent(
                    type="TASK_STATE",
                    payload={"status": "blocked", "reason": self.last_reason},
                ),
            ]

        if light == "red":
            self.status = TaskStatus.ACTIVE
            self.last_reason = "WAIT_RED"
            return [
                TaskEvent(
                    type="SAY",
                    payload={"template_key": "traffic_light_red_wait", "slots": {}},
                )
            ]

        if light == "green":
            self.status = TaskStatus.COMPLETED
            self.last_reason = "GREEN_GO"
            return [
                TaskEvent(
                    type="SAY",
                    payload={"template_key": "traffic_light_green_go", "slots": {}},
                )
            ]

        self.status = TaskStatus.BLOCKED
        self.last_reason = "TRAFFIC_LIGHT_UNSUPPORTED"
        return [
            TaskEvent(type="TASK_STATE", payload={"status": "blocked", "reason": self.last_reason})
        ]
