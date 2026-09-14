from tasks.tasks.traffic_light_task_v2 import TrafficLightTask
from tasks.types import TaskStatus
from observe.change_demand import collect_change_demands


def test_task_change_demand_generation_is_readonly():
    task = TrafficLightTask(max_wait_time=5.0)
    task.state = TaskStatus.WAITING
    task.last_reason = "WAIT_RED"
    prev_state = task.state
    prev_reason = task.last_reason

    demands = task.change_demands()

    assert len(demands) == 1
    assert demands[0].demand_type == "signal_state_change"
    assert demands[0].constraints["object_type"] == "traffic_light"
    assert demands[0].source == "task"
    assert task.state == prev_state
    assert task.last_reason == prev_reason


def test_collect_change_demands():
    task = TrafficLightTask(max_wait_time=5.0)
    task.state = TaskStatus.WAITING
    task.last_reason = "WAIT_RED"

    demands = collect_change_demands([task])

    assert len(demands) == 1
    assert demands[0].demand_type == "signal_state_change"
