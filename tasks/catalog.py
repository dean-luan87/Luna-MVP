from tasks.tasks.traffic_light_task import TrafficLightTask
from tasks.tasks.floor_arrival_task import FloorArrivalTask
from tasks.tasks.elevator_button_task import ElevatorButtonTask
from tasks.tasks.exit_finder_task import ExitFinderTask


def create_task(task_name: str, task_id: str, meta: dict = None):
    meta = meta or {}
    if task_name == "traffic_light":
        return TrafficLightTask(task_id=task_id, meta=meta)
    if task_name == "floor_arrival":
        return FloorArrivalTask(task_id=task_id, meta=meta)
    if task_name == "elevator_button":
        return ElevatorButtonTask(task_id=task_id, meta=meta)
    if task_name == "exit_finder":
        return ExitFinderTask(task_id=task_id, meta=meta)
    raise ValueError(f"Unknown task: {task_name}")
