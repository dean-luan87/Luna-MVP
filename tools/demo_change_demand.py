"""
最小 Demo：ChangeDemand 接好但未被消费。
"""
from tasks.tasks.traffic_light_task_v2 import TrafficLightTask
from tasks.types import TaskStatus
from observe.change_demand import collect_change_demands


def main():
    task = TrafficLightTask(max_wait_time=5.0)
    task.state = TaskStatus.WAITING
    task.last_reason = "WAIT_RED"

    demands = collect_change_demands([task])
    assert demands[0].demand_type == "signal_state_change"
    print("[OK] change_demands collected:", demands)


if __name__ == "__main__":
    main()
