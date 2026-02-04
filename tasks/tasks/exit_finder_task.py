from typing import List

from tasks.types import TaskBase, TaskEvent, TaskStatus


class ExitFinderTask(TaskBase):
    def __init__(self, task_id: str, meta: dict = None):
        super().__init__(task_id=task_id, name="exit_finder", meta=meta or {})

    def step(self, snapshot: dict) -> List[TaskEvent]:
        facts = snapshot.get("perception_facts", {})
        exit_found = facts.get("exit_found")

        if exit_found is True:
            self.status = TaskStatus.COMPLETED
            self.last_reason = "EXIT_FOUND"
            return [
                TaskEvent(type="SAY", payload={"template_key": "exit_found", "slots": {}})
            ]

        if exit_found is False:
            self.status = TaskStatus.ACTIVE
            self.last_reason = "SEARCHING_EXIT"
            return [
                TaskEvent(type="SAY", payload={"template_key": "exit_searching", "slots": {}})
            ]

        self.status = TaskStatus.BLOCKED
        self.last_reason = "EXIT_UNKNOWN"
        return [
            TaskEvent(type="SAY", payload={"template_key": "exit_unknown", "slots": {}}),
            TaskEvent(type="TASK_STATE", payload={"status": "blocked", "reason": self.last_reason}),
        ]
