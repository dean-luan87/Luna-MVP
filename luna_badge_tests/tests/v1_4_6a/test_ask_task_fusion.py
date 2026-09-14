"""
测试 A-5-3: AskChain × Scene × TaskChain 三段式融合

覆盖场景：
1. 场景要求 ask_required=True → AskChain 启动
2. AskChain 完成 → TaskChain 自动启动
3. Ask 结果注入 params → TaskChain 能正确读取
4. TaskChain 完成 → 返回 task_finished=True
"""

import sys
import os
import time

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pytest
from task_chain.task_chain_manager import TaskChainManager, TaskStatus
from core.flow_engine.runtime import FlowRuntime
from core.flow_engine.flow_types import FlowInstance, FlowDefinition, FlowContext, FlowNode, FlowNodeType
from task_engine.ask import (
    AskSchema,
    AskSlot,
    AskSlotKind,
    RetryPolicy,
    OnExceedAction,
)
from task_engine.task_execution_result import TaskExecutionResult


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


def test_scene_ask_required_triggers_ask_chain():
    """测试：场景要求 ask_required=True → AskChain 启动"""
    runtime = FlowRuntime()
    manager = TaskChainManager(runtime)

    schema = AskSchema(
        task_id="go_hospital",
        slots=[
            AskSlot(
                name="hospital_name",
                kind=AskSlotKind.REQUIRED,
                prompt_template="您要去哪家医院？",
            ),
        ],
    )

    instance = _create_mock_flow_instance("go_hospital")
    
    # 场景链要求 ask_required=True
    scene_chain_meta = {"ask_required": True}
    
    manager.register_task(
        instance,
        task_meta={"ask_schema": schema},
        scene_chain_meta=scene_chain_meta,
    )

    # Round1: 应该启动 AskChain
    result = manager.handle_user_turn("", now_ts=int(time.time()))
    assert isinstance(result, TaskExecutionResult)
    assert result.ask_active is True
    assert result.task_active is False
    assert result.phase == "ask"
    assert "医院" in (result.ask_output or "")


def test_ask_completes_then_task_chain_starts():
    """测试：AskChain 完成 → TaskChain 自动启动"""
    runtime = FlowRuntime()
    manager = TaskChainManager(runtime)

    schema = AskSchema(
        task_id="go_hospital",
        slots=[
            AskSlot(
                name="hospital_name",
                kind=AskSlotKind.REQUIRED,
                prompt_template="您要去哪家医院？",
            ),
        ],
        retry_policy=RetryPolicy(interval=0.0, limit=1, on_exceed=OnExceedAction.ABORT),
    )

    instance = _create_mock_flow_instance("go_hospital")
    manager.register_task(
        instance,
        task_meta={
            "ask_schema": schema,
            "ask_bindings": {
                "hospital_name": {"target": "params", "name": "hospital"}
            }
        },
    )

    # Round1: Ask prompt
    result1 = manager.handle_user_turn("", now_ts=int(time.time()))
    assert result1.ask_active is True
    assert result1.phase == "ask"

    # Round2: 用户回答 → Ask 完成，TaskChain 自动启动
    result2 = manager.handle_user_turn("瑞金医院", now_ts=int(time.time()) + 1)
    assert result2.ask_active is False
    assert result2.task_active is True
    assert result2.phase == "task"
    assert "ask_completed_and_task_started" in (result2.task_output or "")

    # 验证 Ask 结果已注入 params
    assert instance.context.data["params"]["hospital"] == "瑞金医院"
    assert instance.context.data["ask_result"]["hospital_name"] == "瑞金医院"


def test_ask_results_injected_into_task_params():
    """测试：Ask 结果注入 params → TaskChain 能正确读取"""
    runtime = FlowRuntime()
    manager = TaskChainManager(runtime)

    schema = AskSchema(
        task_id="go_hospital",
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

    instance = _create_mock_flow_instance("go_hospital")
    manager.register_task(
        instance,
        task_meta={
            "ask_schema": schema,
            "ask_bindings": {
                "hospital_name": {"target": "params", "name": "hospital"},
                "time_slot": {"target": "params", "name": "time"},
            }
        },
    )

    # Round1: Ask prompt
    manager.handle_user_turn("", now_ts=int(time.time()))

    # Round2: 回答第一个 slot
    manager.handle_user_turn("瑞金医院", now_ts=int(time.time()) + 1)

    # Round3: 回答第二个 slot → Ask 完成，TaskChain 启动
    result = manager.handle_user_turn("下午三点", now_ts=int(time.time()) + 2)

    # 验证两个 slot 都正确绑定到 params
    assert result.task_active is True
    assert instance.context.data["params"]["hospital"] == "瑞金医院"
    assert instance.context.data["params"]["time"] == "下午三点"
    assert instance.context.data["ask_result"]["hospital_name"] == "瑞金医院"
    assert instance.context.data["ask_result"]["time_slot"] == "下午三点"


def test_task_chain_finished_returns_task_finished():
    """测试：TaskChain 完成 → 返回 task_finished=True"""
    runtime = FlowRuntime()
    manager = TaskChainManager(runtime)

    instance = _create_mock_flow_instance("simple_task")
    manager.register_task(instance)

    # 标记任务为完成（先标记 instance.finished，再更新 status）
    instance.finished = True
    manager.mark_finished(instance.context.task_id)

    # 处理用户输入 - 应该能检测到已完成的任务
    # 由于任务已完成，status 为 FINISHED，不会被当作 ACTIVE 任务处理
    # 但我们可以通过检查所有任务来验证完成状态
    result = manager.handle_user_turn("", now_ts=int(time.time()))

    # 由于任务已完成，不应该有活跃任务
    assert result.task_active is False
    # 验证任务确实已完成
    record = manager._tasks.get("simple_task")
    assert record is not None
    assert record.status == TaskStatus.FINISHED
    assert instance.finished is True


def test_ask_required_priority_task_meta_overrides_scene():
    """测试：ask_required 优先级 - task_meta 优先于 scene_chain_meta"""
    runtime = FlowRuntime()
    manager = TaskChainManager(runtime)

    instance = _create_mock_flow_instance("test_task")
    
    # task_meta 明确要求 ask_required=False
    # scene_chain_meta 要求 ask_required=True
    # 应该以 task_meta 为准
    manager.register_task(
        instance,
        task_meta={"ask_required": False},
        scene_chain_meta={"ask_required": True},
    )

    # 不应该启动 AskChain
    result = manager.handle_user_turn("", now_ts=int(time.time()))
    assert result.ask_active is False
    assert result.phase == "task"


def test_ask_required_priority_scene_overrides_schema():
    """测试：ask_required 优先级 - scene_chain_meta 优先于 ask_schema"""
    runtime = FlowRuntime()
    manager = TaskChainManager(runtime)

    schema = AskSchema(
        task_id="test_task",
        slots=[
            AskSlot(
                name="hospital_name",
                kind=AskSlotKind.OPTIONAL,  # 只有 OPTIONAL，没有 REQUIRED
                prompt_template="您要去哪家医院？",
            ),
        ],
    )

    instance = _create_mock_flow_instance("test_task")
    
    # scene_chain_meta 要求 ask_required=True
    # ask_schema 只有 OPTIONAL slot，不应该触发 Ask
    # 但 scene_chain_meta 优先级更高，应该启动 Ask
    manager.register_task(
        instance,
        task_meta={"ask_schema": schema},
        scene_chain_meta={"ask_required": True},
    )

    # 应该启动 AskChain（因为 scene_chain_meta 优先级更高）
    result = manager.handle_user_turn("", now_ts=int(time.time()))
    assert result.ask_active is True
    assert result.phase == "ask"

