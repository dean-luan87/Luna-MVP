"""
测试 TaskChainManager 与 AskResultBinder 的集成

验证 Ask 结果能够正确绑定到 task_context 的 params 字段
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


def test_task_manager_binds_ask_results_into_params():
    """测试：TaskChainManager 使用 AskResultBinder 将 Ask 结果绑定到 params"""
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
        }
    )

    # Round1: 系统应该输出首次 ask 提示
    result = manager.handle_user_turn("", now_ts=int(time.time()))
    assert isinstance(result, TaskExecutionResult)
    assert result.ask_active is True

    # Round2: 用户提供正确答案
    result = manager.handle_user_turn("瑞金医院", now_ts=int(time.time()) + 1)

    # Ask结束后应写入 task_context
    ctx = instance.context.data
    assert ctx["ask_result"]["hospital_name"] == "瑞金医院"
    assert ctx["params"]["hospital"] == "瑞金医院"


def test_manager_does_not_start_ask_chain_twice():
    """测试：Ask 完成后不应重复启动 AskChain"""
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
        }
    )

    # Round1: start ask
    result = manager.handle_user_turn("", now_ts=int(time.time()))
    assert isinstance(result, TaskExecutionResult)
    assert result.ask_active is True

    # Round2: valid reply completes ask
    result = manager.handle_user_turn("瑞金医院", now_ts=int(time.time()) + 1)
    assert isinstance(result, TaskExecutionResult)
    assert result.ask_active is False  # Ask finished

    # Round3: 再次 handle，不应启动第二次 Ask
    result = manager.handle_user_turn("随便输入", now_ts=int(time.time()) + 2)
    assert isinstance(result, TaskExecutionResult)
    assert result.ask_active is False


def test_binder_with_multiple_slots():
    """测试：多个 slot 的绑定"""
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
        }
    )

    # Round1: 首次 prompt
    manager.handle_user_turn("", now_ts=int(time.time()))

    # Round2: 回答第一个 slot
    manager.handle_user_turn("瑞金医院", now_ts=int(time.time()) + 1)

    # Round3: 回答第二个 slot
    result = manager.handle_user_turn("下午三点", now_ts=int(time.time()) + 2)

    # 验证两个 slot 都正确绑定到 params
    ctx = instance.context.data
    assert ctx["params"]["hospital"] == "瑞金医院"
    assert ctx["params"]["time"] == "下午三点"
    assert ctx["ask_result"]["hospital_name"] == "瑞金医院"
    assert ctx["ask_result"]["time_slot"] == "下午三点"

