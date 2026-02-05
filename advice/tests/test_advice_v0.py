"""
Advice v0 测试：验证建议生成功能。
"""
import time

from advice.engine import AdviceEngine
from tasks.types import TaskStatus


class DummyTask:
    """模拟 Task v2 用于测试。"""

    def __init__(self, state, reason, since=None):
        self.task_name = "TrafficLightTask"
        self.state = state
        self.last_reason = reason
        self.started_at = since if since is not None else time.time() - 5


def test_waiting_advice():
    """测试 WAITING 状态生成建议。"""
    eng = AdviceEngine()
    adv = eng.generate(
        [DummyTask(TaskStatus.WAITING, "WAIT_RED")],
        time.time()
    )
    assert len(adv) == 1
    assert adv[0].advice_id == "wait_condition"
    assert adv[0].category == "TASK_STATE"
    assert "等待" in adv[0].text
    assert adv[0].confidence == 0.7
    assert "WAITING" in adv[0].evidence["state"]
    assert "WAIT_RED" in adv[0].evidence["reason"]
    assert adv[0].is_safety is False


def test_blocked_advice():
    """测试 BLOCKED 状态生成建议。"""
    eng = AdviceEngine()
    adv = eng.generate(
        [DummyTask(TaskStatus.BLOCKED, "LIGHT_INVISIBLE")],
        time.time()
    )
    assert len(adv) == 1
    assert adv[0].advice_id == "adjust_view"
    assert adv[0].category == "TASK_STATE"
    assert "视野" in adv[0].text
    assert adv[0].confidence == 0.6
    assert "BLOCKED" in adv[0].evidence["state"]
    assert adv[0].is_safety is False


def test_timeout_advice():
    """测试 TIMEOUT 状态生成建议。"""
    eng = AdviceEngine()
    adv = eng.generate(
        [DummyTask(TaskStatus.TIMEOUT, "TIMEOUT")],
        time.time()
    )
    assert len(adv) == 1
    assert adv[0].advice_id == "ask_next_step"
    assert adv[0].category == "TASK_STATE"
    assert "等待时间" in adv[0].text
    assert adv[0].confidence == 0.8
    assert "TIMEOUT" in adv[0].evidence["state"]
    assert adv[0].is_safety is False


def test_no_advice_for_completed():
    """测试已完成任务不生成建议。"""
    eng = AdviceEngine()
    adv = eng.generate(
        [DummyTask(TaskStatus.COMPLETED, "GO_GREEN")],
        time.time()
    )
    assert len(adv) == 0


def test_multiple_tasks():
    """测试多个任务生成多个建议。"""
    eng = AdviceEngine()
    adv = eng.generate(
        [
            DummyTask(TaskStatus.WAITING, "WAIT_RED"),
            DummyTask(TaskStatus.BLOCKED, "LIGHT_INVISIBLE"),
        ],
        time.time()
    )
    assert len(adv) == 2
    assert adv[0].advice_id == "wait_condition"
    assert adv[1].advice_id == "adjust_view"
