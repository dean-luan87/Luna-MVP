"""
测试 A-5-4-3: Pause / Resume 声明式 API

验证：
1. pause_lifecycle() 和 resume_lifecycle() API 存在
2. 状态切换正常
3. 不影响 AskChain / TaskChain 的执行逻辑
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
    TaskLifecycleStatus,
    TaskLifecyclePhase,
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


def test_pause_resume_api_basic():
    """测试：基本的 pause/resume API 功能"""
    runtime = FlowRuntime()
    manager = TaskChainManager(runtime)

    instance = _create_mock_flow_instance("test_task")
    manager.register_task(instance)

    # 初始必须为 ACTIVE
    assert manager.lifecycle.status == TaskLifecycleStatus.ACTIVE

    # pause
    result = manager.pause_lifecycle()
    assert result.status == TaskLifecycleStatus.PAUSED
    assert manager.lifecycle.status == TaskLifecycleStatus.PAUSED
    assert manager.lifecycle.reason == "manual_pause"
    assert manager.lifecycle.source == "user"

    # resume
    result = manager.resume_lifecycle()
    assert result.status == TaskLifecycleStatus.ACTIVE
    assert manager.lifecycle.status == TaskLifecycleStatus.ACTIVE
    assert manager.lifecycle.reason == "manual_resume"
    assert manager.lifecycle.source == "user"


def test_pause_resume_with_custom_reason():
    """测试：pause/resume 支持自定义原因"""
    runtime = FlowRuntime()
    manager = TaskChainManager(runtime)

    instance = _create_mock_flow_instance("test_task")
    manager.register_task(instance)

    # pause with custom reason
    manager.pause_lifecycle(reason="user_requested_pause")
    assert manager.lifecycle.status == TaskLifecycleStatus.PAUSED
    assert manager.lifecycle.reason == "user_requested_pause"

    # resume with custom reason
    manager.resume_lifecycle(reason="user_requested_resume")
    assert manager.lifecycle.status == TaskLifecycleStatus.ACTIVE
    assert manager.lifecycle.reason == "user_requested_resume"


def test_pause_only_works_on_active():
    """测试：pause 只在 ACTIVE 状态时生效"""
    runtime = FlowRuntime()
    manager = TaskChainManager(runtime)

    instance = _create_mock_flow_instance("test_task")
    manager.register_task(instance)

    # 初始为 ACTIVE，可以 pause
    manager.pause_lifecycle()
    assert manager.lifecycle.status == TaskLifecycleStatus.PAUSED

    # 已经是 PAUSED，再次 pause 应该无效（保持 PAUSED）
    manager.pause_lifecycle()
    assert manager.lifecycle.status == TaskLifecycleStatus.PAUSED


def test_resume_only_works_on_paused():
    """测试：resume 只在 PAUSED 状态时生效"""
    runtime = FlowRuntime()
    manager = TaskChainManager(runtime)

    instance = _create_mock_flow_instance("test_task")
    manager.register_task(instance)

    # 初始为 ACTIVE，resume 应该无效（保持 ACTIVE）
    manager.resume_lifecycle()
    assert manager.lifecycle.status == TaskLifecycleStatus.ACTIVE

    # pause 后再 resume
    manager.pause_lifecycle()
    manager.resume_lifecycle()
    assert manager.lifecycle.status == TaskLifecycleStatus.ACTIVE


def test_pause_resume_blocks_ask_chain():
    """测试：A-5-4-4 阶段，pause/resume 会真正阻塞 AskChain 的执行"""
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

    # 启动 Ask
    result1 = manager.handle_user_turn("", now_ts=int(time.time()))
    assert result1.ask_active is True

    # pause lifecycle（A-5-4-4 会真正阻塞执行）
    manager.pause_lifecycle()
    assert manager.lifecycle.status == TaskLifecycleStatus.PAUSED

    # Ask 应该被阻塞（A-5-4-4 改变了行为）
    result2 = manager.handle_user_turn("瑞金医院", now_ts=int(time.time()) + 1)
    assert result2.paused is True
    assert result2.ask_active is False  # 被暂停阻塞

    # resume 后应该可以继续
    manager.resume_lifecycle()
    result3 = manager.handle_user_turn("瑞金医院", now_ts=int(time.time()) + 2)
    assert result3.paused is False
    assert result3.task_active is True  # Ask 完成，Task 启动


def test_pause_resume_blocks_task_chain():
    """测试：A-5-4-4 阶段，pause/resume 会真正阻塞 TaskChain 的执行"""
    runtime = FlowRuntime()
    manager = TaskChainManager(runtime)

    instance = _create_mock_flow_instance("test_task")
    manager.register_task(instance)

    # pause lifecycle（A-5-4-4 会真正阻塞执行）
    manager.pause_lifecycle()
    assert manager.lifecycle.status == TaskLifecycleStatus.PAUSED

    # TaskChain 应该被阻塞（A-5-4-4 改变了行为）
    result = manager.handle_user_turn("", now_ts=int(time.time()))
    assert result.paused is True
    assert result.phase == "idle"  # 暂停时返回 idle

    # resume 后应该可以继续
    manager.resume_lifecycle()
    result2 = manager.handle_user_turn("", now_ts=int(time.time()) + 1)
    assert result2.paused is False
    assert result2.phase == "task"  # 恢复后进入 Task 执行阶段


def test_multiple_pause_resume_cycles():
    """测试：多次 pause/resume 循环"""
    runtime = FlowRuntime()
    manager = TaskChainManager(runtime)

    instance = _create_mock_flow_instance("test_task")
    manager.register_task(instance)

    # 多次 pause/resume 循环
    for i in range(3):
        manager.pause_lifecycle(reason=f"pause_round_{i}")
        assert manager.lifecycle.status == TaskLifecycleStatus.PAUSED
        
        manager.resume_lifecycle(reason=f"resume_round_{i}")
        assert manager.lifecycle.status == TaskLifecycleStatus.ACTIVE

    # 最终应该是 ACTIVE
    assert manager.lifecycle.status == TaskLifecycleStatus.ACTIVE

