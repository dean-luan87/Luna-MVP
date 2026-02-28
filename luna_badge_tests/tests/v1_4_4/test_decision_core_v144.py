# tests/v1_4_4/test_decision_core_v144.py
from decision_core.builder_v144 import build_decision_core_v144
from decision_core.decision_core import DecisionRequest
from task_chain.task_chain_manager import TaskStatus, TaskChainManager


def test_new_hospital_task_flow():
    core = build_decision_core_v144()

    req = DecisionRequest(
        user_id="u1",
        utterance="我想去医院看病",
        extra={"scene_type": "outdoor"},
    )
    reply = core.handle(req)
    assert "你要去哪个医院" in reply


def test_cancel_task_query_and_confirm():
    core = build_decision_core_v144()

    # 1. 发起任务
    req1 = DecisionRequest(
        user_id="u1",
        utterance="我想去医院看病",
        extra={"scene_type": "outdoor"},
    )
    _ = core.handle(req1)

    # 2. 触发取消意图
    req2 = DecisionRequest(
        user_id="u1",
        utterance="不用去了",
        extra={},
    )
    reply2 = core.handle(req2)
    assert "停止当前任务" in reply2 or "终止当前任务" in reply2 or "取消" in reply2 or "停止" in reply2

    # 3. 回答"是的"确认取消
    req3 = DecisionRequest(
        user_id="u1",
        utterance="是的",
        extra={},
    )
    reply3 = core.handle(req3)
    assert "已经取消" in reply3 or "任务已取消" in reply3 or "这个任务已经取消" in reply3

    # 4. 检查 TaskChainManager 状态
    manager: TaskChainManager = core._tasks
    active = manager.get_active_task_for_user("u1")
    assert active is None
    cancelled = [t for t in manager._tasks.values() if t.status == TaskStatus.CANCELLED]
    assert len(cancelled) == 1


def test_pause_and_resume_task():
    core = build_decision_core_v144()

    # 1. 发起任务
    req1 = DecisionRequest(
        user_id="u1",
        utterance="我想去医院看病",
        extra={"scene_type": "outdoor"},
    )
    _ = core.handle(req1)

    # 2. 暂停任务
    req2 = DecisionRequest(
        user_id="u1",
        utterance="暂停",
        extra={},
    )
    reply2 = core.handle(req2)
    assert "暂停" in reply2

    # 3. 检查任务状态
    manager: TaskChainManager = core._tasks
    record = manager.get_active_task_for_user("u1")
    assert record is not None
    assert record.status == TaskStatus.PAUSED

    # 4. 恢复任务
    req3 = DecisionRequest(
        user_id="u1",
        utterance="继续",
        extra={},
    )
    reply3 = core.handle(req3)
    assert "继续" in reply3

    # 5. 检查任务状态
    record2 = manager.get_active_task_for_user("u1")
    assert record2 is not None
    assert record2.status == TaskStatus.ACTIVE

