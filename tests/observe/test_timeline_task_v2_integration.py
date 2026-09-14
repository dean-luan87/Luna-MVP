"""
Timeline Task v2 集成测试：验证 Task v2 状态能正确写入 Timeline
"""
import time

from tasks.tasks.traffic_light_task_v2 import TrafficLightTask
from tasks.types import TaskStatus
from dynamic_view.entity import ObservedEntity
from dynamic_view.types import ObservationState
from observe.timeline.schema import TimelineFrame


def test_task_v2_state_in_timeline():
    """测试 Task v2 的状态能正确写入 Timeline。"""
    t0 = time.time()
    task = TrafficLightTask(max_wait_time=5.0)

    # 创建红绿灯实体
    red_light = ObservedEntity("traffic_light_1")
    red_light.state = ObservationState.STABLE
    red_light.last_seen_ts = t0

    # 红灯 → WAITING
    attr_map = {"traffic_light_1": {"color": "red"}}
    task.tick({"traffic_light_1": red_light}, t0, attr_map)
    assert task.state == TaskStatus.WAITING

    # 创建 TimelineFrame（模拟 snapshot_timeline）
    frame = TimelineFrame(
        ts=t0 + 0.1,
        entities={},
        tasks=[
            {
                "task": task.task_name,
                "state": task.state.name,
                "reason": task.last_reason,
                "since": task.started_at,
            }
        ],
        c_decision={},
    )

    # 验证 Timeline 包含 Task v2 状态
    j = frame.to_json()
    assert '"WAITING"' in j
    assert '"WAIT_RED"' in j
    assert '"TrafficLightTask"' in j
    assert str(task.started_at) in j


def test_task_v2_timeout_in_timeline():
    """测试 TIMEOUT 状态能正确写入 Timeline。"""
    t0 = time.time()
    task = TrafficLightTask(max_wait_time=1.0)

    # 创建红灯实体
    red_light = ObservedEntity("traffic_light_1")
    red_light.state = ObservationState.STABLE
    red_light.last_seen_ts = t0

    # 红灯 → WAITING
    attr_map = {"traffic_light_1": {"color": "red"}}
    task.tick({"traffic_light_1": red_light}, t0, attr_map)
    assert task.state == TaskStatus.WAITING

    # 超时 → TIMEOUT
    task.tick({}, t0 + 2.0, {})
    assert task.state == TaskStatus.TIMEOUT

    # 创建 TimelineFrame
    frame = TimelineFrame(
        ts=t0 + 2.0,
        entities={},
        tasks=[
            {
                "task": task.task_name,
                "state": task.state.name,
                "reason": task.last_reason,
                "since": task.started_at,
            }
        ],
        c_decision={},
    )

    # 验证 Timeline 包含 TIMEOUT 状态
    j = frame.to_json()
    assert '"TIMEOUT"' in j
