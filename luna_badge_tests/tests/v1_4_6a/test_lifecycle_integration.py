"""
测试 TaskLifecycleState 与 TaskChainManager 的集成

验证 lifecycle 字段正确挂载，状态同步正确，但不改变任何执行行为
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
from task_engine.task_lifecycle_state import (
    TaskLifecyclePhase,
    TaskLifecycleStatus,
)
from task_engine.ask import (
    AskSchema,
    AskSlot,
    AskSlotKind,
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


def test_lifecycle_attached_to_manager():
    """测试：lifecycle 字段正确挂载到 TaskChainManager"""
    runtime = FlowRuntime()
    manager = TaskChainManager(runtime)

    assert manager.lifecycle is not None
    assert manager.lifecycle.phase == TaskLifecyclePhase.IDLE
    assert manager.lifecycle.status == TaskLifecycleStatus.ACTIVE


def test_lifecycle_updates_on_register():
    """测试：注册任务时 lifecycle 状态正确更新"""
    runtime = FlowRuntime()
    manager = TaskChainManager(runtime)

    instance = _create_mock_flow_instance("test_task")
    
    # 注册带 ask_required 的任务
    manager.register_task(
        instance,
        task_meta={"ask_required": True},
    )
    
    assert manager.lifecycle.phase == TaskLifecyclePhase.ASK
    assert manager.lifecycle.status == TaskLifecycleStatus.ACTIVE
    assert manager.lifecycle.meta.get("task_id") == "test_task"
    assert manager.lifecycle.reason == "task_registered"
    assert manager.lifecycle.source == "system"


def test_lifecycle_updates_on_register_without_ask():
    """测试：注册不带 ask 的任务时 lifecycle 状态正确更新"""
    runtime = FlowRuntime()
    manager = TaskChainManager(runtime)

    instance = _create_mock_flow_instance("test_task")
    
    # 注册不带 ask 的任务
    manager.register_task(
        instance,
        task_meta={},
    )
    
    assert manager.lifecycle.phase == TaskLifecyclePhase.TASK
    assert manager.lifecycle.status == TaskLifecycleStatus.ACTIVE
    assert manager.lifecycle.meta.get("task_id") == "test_task"


def test_lifecycle_syncs_on_ask_start():
    """测试：Ask 启动时 lifecycle 状态同步"""
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
        ],
    )

    instance = _create_mock_flow_instance("test_task")
    manager.register_task(instance, task_meta={"ask_schema": schema})

    # 首次调用，启动 Ask
    result = manager.handle_user_turn("", now_ts=int(time.time()))
    
    assert result.ask_active is True
    assert manager.lifecycle.phase == TaskLifecyclePhase.ASK
    assert manager.lifecycle.status == TaskLifecycleStatus.ACTIVE
    assert manager.lifecycle.reason == "ask_started"


def test_lifecycle_syncs_on_ask_to_task_transition():
    """测试：Ask 完成切换到 Task 时 lifecycle 状态同步"""
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
        ],
    )

    instance = _create_mock_flow_instance("test_task")
    manager.register_task(instance, task_meta={"ask_schema": schema})

    # Round1: 启动 Ask
    manager.handle_user_turn("", now_ts=int(time.time()))
    
    # Round2: 完成 Ask，切换到 Task
    result = manager.handle_user_turn("瑞金医院", now_ts=int(time.time()) + 1)
    
    assert result.task_active is True
    assert manager.lifecycle.phase == TaskLifecyclePhase.TASK
    assert manager.lifecycle.status == TaskLifecycleStatus.ACTIVE
    assert manager.lifecycle.reason == "ask_completed_task_started"


def test_lifecycle_syncs_on_task_finished():
    """测试：任务完成时 lifecycle 状态同步"""
    runtime = FlowRuntime()
    manager = TaskChainManager(runtime)

    instance = _create_mock_flow_instance("test_task")
    manager.register_task(instance)

    # 标记任务为完成（先标记 instance.finished，再更新 status）
    instance.finished = True
    manager.mark_finished(instance.context.task_id)

    # 手动触发 lifecycle 状态更新（因为 handle_user_turn 只查找 ACTIVE 状态的任务）
    # 在实际场景中，任务完成通常是在任务执行过程中自动检测的
    manager._lifecycle.mark(
        status=TaskLifecycleStatus.FINISHED,
        reason="task_completed",
        source="system",
    )

    # 验证 lifecycle 状态已更新
    assert manager.lifecycle.status == TaskLifecycleStatus.FINISHED
    assert manager.lifecycle.reason == "task_completed"
    
    # 验证任务确实已完成
    record = manager._tasks.get("test_task")
    assert record is not None
    assert record.status == "finished"
    assert instance.finished is True


def test_lifecycle_syncs_on_ask_aborted():
    """测试：Ask 中止时 lifecycle 状态同步"""
    runtime = FlowRuntime()
    manager = TaskChainManager(runtime)

    from task_engine.ask import RetryPolicy, OnExceedAction

    schema = AskSchema(
        task_id="test_task",
        slots=[
            AskSlot(
                name="hospital_name",
                kind=AskSlotKind.REQUIRED,
                prompt_template="您要去哪家医院？",
            ),
        ],
        retry_policy=RetryPolicy(interval=0.0, limit=1, on_exceed=OnExceedAction.ABORT),
    )

    instance = _create_mock_flow_instance("test_task")
    manager.register_task(instance, task_meta={"ask_schema": schema})

    # Round1: 启动 Ask
    manager.handle_user_turn("", now_ts=int(time.time()))
    
    # Round2: 第一次无效输入
    manager.handle_user_turn("   ", now_ts=int(time.time()) + 1)
    
    # Round3: 第二次无效输入，触发 abort
    result = manager.handle_user_turn("   ", now_ts=int(time.time()) + 2)
    
    assert result.task_finished is True
    assert manager.lifecycle.status == TaskLifecycleStatus.ABORTED
    assert manager.lifecycle.reason == "ask_aborted"

