from typing import List

from dynamic_view.events import ObservationEvent
from dynamic_view.types import ObservationState
from task_adapter.types import TaskTrigger, TaskAction


class TaskAdapter:
    """
    最小 Task Adapter：
    - 订阅 ObservationEvent
    - 生成一次性 Task Action
    """

    def __init__(self, triggers: List[TaskTrigger]):
        self.triggers = triggers
        self._fired = set()

    def handle_events(self, events: List[ObservationEvent]):
        actions = []

        for ev in events:
            for trig in self.triggers:
                key = (trig.entity_id, trig.on_state)

                if ev.entity_id != trig.entity_id:
                    continue
                if ev.new_state != trig.on_state:
                    continue
                if key in self._fired:
                    continue
                if ev.new_state == ObservationState.INVISIBLE:
                    continue

                actions.append(
                    {
                        "action": trig.action,
                        "message": trig.message,
                        "entity_id": ev.entity_id,
                    }
                )
                self._fired.add(key)

        return actions
