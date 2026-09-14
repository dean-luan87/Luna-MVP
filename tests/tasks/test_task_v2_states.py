"""
Task v2 状态机测试：WAITING / BLOCKED / TIMEOUT
"""
import time

from tasks.tasks.traffic_light_task_v2 import TrafficLightTask
from tasks.types import TaskStatus
from dynamic_view.entity import ObservedEntity
from dynamic_view.types import ObservationState


def test_waiting_to_completed():
    """测试 WAITING → COMPLETED 转换。"""
    t0 = time.time()
    task = TrafficLightTask(max_wait_time=5.0)

    # 创建红绿灯实体
    red_light = ObservedEntity("traffic_light_1")
    red_light.state = ObservationState.STABLE
    red_light.last_seen_ts = t0

    green_light = ObservedEntity("traffic_light_1")
    green_light.state = ObservationState.STABLE
    green_light.last_seen_ts = t0 + 1.0

    # 红灯 → WAITING
    attr_map = {"traffic_light_1": {"color": "red"}}
    task.tick({"traffic_light_1": red_light}, t0, attr_map)
    assert task.state == TaskStatus.WAITING
    assert task.last_reason == "WAIT_RED"

    # 绿灯 → COMPLETED
    attr_map = {"traffic_light_1": {"color": "green"}}
    task.tick({"traffic_light_1": green_light}, t0 + 1.0, attr_map)
    assert task.state == TaskStatus.COMPLETED
    assert task.last_reason == "GO_GREEN"


def test_blocked_then_timeout():
    """测试 BLOCKED → TIMEOUT 转换。"""
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

    # 红绿灯消失 → BLOCKED
    task.tick({}, t0 + 0.5, {})
    assert task.state == TaskStatus.BLOCKED
    assert task.last_reason == "LIGHT_INVISIBLE"

    # 超时 → TIMEOUT
    task.tick({}, t0 + 2.0, {})
    assert task.state == TaskStatus.TIMEOUT
    assert task.last_reason == "TIMEOUT"


def test_blocked_when_unstable():
    """测试红绿灯不稳定时进入 BLOCKED。"""
    t0 = time.time()
    task = TrafficLightTask(max_wait_time=5.0)

    # 创建不稳定的红绿灯
    unstable_light = ObservedEntity("traffic_light_1")
    unstable_light.state = ObservationState.APPEARED  # 不稳定
    unstable_light.last_seen_ts = t0

    # 启动任务
    attr_map = {"traffic_light_1": {"color": "red"}}
    task.tick({"traffic_light_1": unstable_light}, t0, attr_map)
    assert task.state == TaskStatus.ACTIVE  # 先启动

    # 不稳定 → BLOCKED
    task.tick({"traffic_light_1": unstable_light}, t0 + 0.1, attr_map)
    assert task.state == TaskStatus.BLOCKED
    assert task.last_reason == "LIGHT_UNSTABLE"


def test_init_to_active():
    """测试 INIT → ACTIVE 转换。"""
    t0 = time.time()
    task = TrafficLightTask(max_wait_time=5.0)

    # 创建红绿灯实体
    light = ObservedEntity("traffic_light_1")
    light.state = ObservationState.STABLE
    light.last_seen_ts = t0

    # 找到红绿灯 → ACTIVE
    attr_map = {"traffic_light_1": {"color": "red"}}
    task.tick({"traffic_light_1": light}, t0, attr_map)
    assert task.state == TaskStatus.WAITING  # 红灯直接进入 WAITING
    assert task.started_at == t0
