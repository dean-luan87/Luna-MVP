"""
Timeline Task v2 状态记录测试
"""
from observe.timeline.schema import TimelineFrame


def test_timeline_contains_task_v2_state():
    """测试 Timeline 包含 Task v2 的状态信息。"""
    frame = TimelineFrame(
        ts=1.0,
        entities={},
        tasks=[
            {
                "task": "TrafficLightTask",
                "state": "WAITING",
                "reason": "WAIT_RED",
                "since": 0.5,
            }
        ],
        c_decision={},
    )

    j = frame.to_json()
    assert '"WAITING"' in j
    assert '"WAIT_RED"' in j
    assert '"since"' in j
    assert '0.5' in j


def test_timeline_contains_task_v2_timeout():
    """测试 Timeline 包含 TIMEOUT 状态。"""
    frame = TimelineFrame(
        ts=2.0,
        entities={},
        tasks=[
            {
                "task": "TrafficLightTask",
                "state": "TIMEOUT",
                "reason": "TIMEOUT",
                "since": 0.5,
            }
        ],
        c_decision={},
    )

    j = frame.to_json()
    assert '"TIMEOUT"' in j


def test_timeline_contains_task_v2_blocked():
    """测试 Timeline 包含 BLOCKED 状态。"""
    frame = TimelineFrame(
        ts=1.5,
        entities={},
        tasks=[
            {
                "task": "TrafficLightTask",
                "state": "BLOCKED",
                "reason": "LIGHT_INVISIBLE",
                "since": 0.5,
            }
        ],
        c_decision={},
    )

    j = frame.to_json()
    assert '"BLOCKED"' in j
    assert '"LIGHT_INVISIBLE"' in j
