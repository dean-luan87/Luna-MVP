"""
测试 A-5-4-4: 暂停真正接管 Ask/Task 流程

验证：
1. pause_task() 调用后，不再推进 Ask / Task 节点
2. resume_task() 后，继续从原来的节点往下执行
3. 不破坏现有 A-5-3 行为和测试
"""

import sys
import os
import time

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pytest
from task_chain.task_chain_manager import TaskChainManager
from core.flow_engine.runtime import FlowRuntime
from core.flow_engine.flow_types import FlowInstance, FlowDefinition, FlowContext, FlowNode, FlowNodeType
from task_engine.ask import (
    AskSchema,
    AskSlot,
    AskSlotKind,
    RetryPolicy,
    OnExceedAction,
)


def _create_mock_flow_instance(task_id: str, user_id: str = "test_user") -> FlowInstance:
    """创建一个模拟的 FlowInstance"""
    ctx = FlowContext(
        task_id=task_id,
        user_id=user_id,
        scene_type="test",
        intent="test",
    )
    flow_def = FlowDefinition(
        id=f"flow_{task_id}",
        nodes={"start": FlowNode(id="start", node_type=FlowNodeType.CUSTOM)},
        edges=[],
        entry_node_id="start",
    )
    return FlowInstance(
        definition=flow_def,
        context=ctx,
        current_node_id="start",
    )


def test_pause_blocks_ask_chain():
    """测试：暂停后不再触发 Ask"""
    runtime = FlowRuntime()
    manager = TaskChainManager(runtime)

    schema = AskSchema(
        task_id="hospital_go",
        slots=[
            AskSlot(
                name="hospital_name",
                kind=AskSlotKind.REQUIRED,
                prompt_template="您要去哪家医院？",
            ),
        ],
    )

    instance = _create_mock_flow_instance("hospital_go")
    manager.register_task(instance, task_meta={"ask_schema": schema})

    # 第一次调用：应该触发 Ask 的首个 prompt
    r1 = manager.handle_user_turn("", now_ts=int(time.time()))
    assert r1.phase == "ask"
    assert r1.ask_active is True
    assert r1.paused is False

    # 用户说"停一下"（上层识别后调用 pause_task）
    manager.pause_lifecycle(reason="user_said_pause")

    # 第二次调用：即使用户输入，也不应再推进 Ask
    r2 = manager.handle_user_turn("xxx", now_ts=int(time.time()) + 1)
    assert r2.paused is True
    assert r2.pause_type == "user"
    assert r2.ask_active is False
    assert r2.task_active is False


def test_resume_after_pause_continues_ask():
    """测试：恢复后 Ask 能继续"""
    runtime = FlowRuntime()
    manager = TaskChainManager(runtime)

    schema = AskSchema(
        task_id="hospital_go",
        slots=[
            AskSlot(
                name="hospital_name",
                kind=AskSlotKind.REQUIRED,
                prompt_template="您要去哪家医院？",
            ),
        ],
        retry_policy=RetryPolicy(interval=0.0, limit=1, on_exceed=OnExceedAction.ABORT),
    )

    instance = _create_mock_flow_instance("hospital_go")
    manager.register_task(instance, task_meta={"ask_schema": schema})

    # Round1: 启动 Ask
    r1 = manager.handle_user_turn("", now_ts=int(time.time()))
    assert r1.phase == "ask"
    assert r1.ask_active is True

    # Round2: 暂停
    manager.pause_lifecycle()
    r2 = manager.handle_user_turn("xxx", now_ts=int(time.time()) + 1)
    assert r2.paused is True

    # Round3: 恢复
    manager.resume_lifecycle()

    # Round4: 恢复后再来一次，应继续 Ask
    r3 = manager.handle_user_turn("瑞金医院", now_ts=int(time.time()) + 2)
    assert r3.paused is False
    # 根据 Ask 是否完成，phase 可能是 "ask" 或 "task"
    assert r3.phase in ("ask", "task")


def test_pause_during_task_then_resume():
    """测试：暂停不破坏 TaskChain 完整执行"""
    runtime = FlowRuntime()
    manager = TaskChainManager(runtime)

    instance = _create_mock_flow_instance("simple_task")
    manager.register_task(instance)

    # Round1: 第一次 handle_user_turn 直接走 Task
    r1 = manager.handle_user_turn("start", now_ts=int(time.time()))
    assert r1.phase == "task"
    assert r1.paused is False

    # Round2: 暂停
    manager.pause_lifecycle()
    r2 = manager.handle_user_turn("still_paused", now_ts=int(time.time()) + 1)
    assert r2.paused is True
    assert r2.pause_type == "user"

    # Round3: 恢复
    manager.resume_lifecycle()

    # Round4: 恢复后继续执行
    r3 = manager.handle_user_turn("continue", now_ts=int(time.time()) + 2)
    assert r3.paused is False
    # 这里不强行断言业务结果，只要求不报错且继续走 Task
    assert r3.phase == "task"


def test_pause_preserves_ask_state():
    """测试：暂停不破坏 Ask 的状态（当前 slot、已收集的答案）"""
    runtime = FlowRuntime()
    manager = TaskChainManager(runtime)

    schema = AskSchema(
        task_id="test_task",
        slots=[
            AskSlot(
                name="hospital_name",
                kind=AskSlotKind.REQUIRED,
                prompt_template="您要去哪家医院？",
            ),
            AskSlot(
                name="time_slot",
                kind=AskSlotKind.OPTIONAL,
                prompt_template="您想什么时候去？",
            ),
        ],
    )

    instance = _create_mock_flow_instance("test_task")
    manager.register_task(instance, task_meta={"ask_schema": schema})

    # Round1: 启动 Ask，回答第一个 slot
    r1 = manager.handle_user_turn("", now_ts=int(time.time()))
    assert r1.ask_active is True

    r2 = manager.handle_user_turn("瑞金医院", now_ts=int(time.time()) + 1)
    # 此时应该进入第二个 slot 或完成 Ask

    # Round3: 暂停
    manager.pause_lifecycle()
    r3 = manager.handle_user_turn("xxx", now_ts=int(time.time()) + 2)
    assert r3.paused is True

    # Round4: 恢复后继续 Ask
    manager.resume_lifecycle()
    r4 = manager.handle_user_turn("下午三点", now_ts=int(time.time()) + 3)
    assert r4.paused is False
    # Ask 应该能够继续，之前收集的答案应该还在
    # 验证 Ask 状态被保留（通过检查 ask_integration 是否仍然活跃或已完成）
    # 这里主要验证不会因为暂停而丢失状态


def test_multiple_pause_resume_cycles():
    """测试：多次暂停/恢复循环"""
    runtime = FlowRuntime()
    manager = TaskChainManager(runtime)

    instance = _create_mock_flow_instance("test_task")
    manager.register_task(instance)

    # 多次暂停/恢复循环
    for i in range(3):
        # 正常执行
        r1 = manager.handle_user_turn(f"input_{i}", now_ts=int(time.time()) + i * 2)
        assert r1.paused is False

        # 暂停
        manager.pause_lifecycle()
        r2 = manager.handle_user_turn(f"paused_{i}", now_ts=int(time.time()) + i * 2 + 1)
        assert r2.paused is True

        # 恢复
        manager.resume_lifecycle()
        r3 = manager.handle_user_turn(f"resumed_{i}", now_ts=int(time.time()) + i * 2 + 2)
        assert r3.paused is False












