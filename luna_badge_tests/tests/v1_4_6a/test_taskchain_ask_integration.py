"""
测试 TaskChainManager 与 AskChainRuntime 的集成

覆盖场景：
1. 有 AskSchema 的任务：首次调用 → 不执行主任务，只给 prompt
2. REQUIRED slot 正常填写 → AskChain 完成 → ask_result 注入 context
3. limit=1，多次错误 → 触发 abort → 任务被终止
4. 有 Ask 的任务执行完问询 → 下次 handle_user_turn 开始正常跑主任务链

新增：AskIntegrationService 的独立测试
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
    AskIntegrationService,
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


def test_ask_schema_task_first_call_gives_prompt():
    """场景1: 有 AskSchema 的任务，首次调用 → 不执行主任务，只给 prompt"""
    runtime = FlowRuntime()
    manager = TaskChainManager(runtime)

    # 创建带 AskSchema 的任务
    schema = AskSchema(
        task_id="hospital_task",
        slots=[
            AskSlot(
                name="hospital_name",
                kind=AskSlotKind.REQUIRED,
                prompt_template="您要去哪家医院？",
            ),
        ],
    )

    instance = _create_mock_flow_instance("hospital_task")
    manager.register_task(instance, task_meta={"ask_schema": schema})

    # 首次调用 handle_user_turn（无用户输入）
    response = manager.handle_user_turn("", now_ts=int(time.time()))

    # 断言：TaskChain 没前进；response 只有问医院的那句
    assert isinstance(response, TaskExecutionResult)
    assert response.ask_active is True
    assert response.ask_output is not None
    assert "医院" in response.ask_output
    assert manager.ask_integration.has_active


def test_required_slot_normal_fill_injects_context():
    """场景2: REQUIRED slot 正常填写 → AskChain 完成 → ask_result 注入 context"""
    runtime = FlowRuntime()
    manager = TaskChainManager(runtime)

    schema = AskSchema(
        task_id="hospital_task",
        slots=[
            AskSlot(
                name="hospital_name",
                kind=AskSlotKind.REQUIRED,
                prompt_template="您要去哪家医院？",
            ),
        ],
    )

    instance = _create_mock_flow_instance("hospital_task")
    manager.register_task(instance, task_meta={"ask_schema": schema})

    # Round1: 首次调用，获取 prompt
    response1 = manager.handle_user_turn("", now_ts=int(time.time()))
    assert isinstance(response1, TaskExecutionResult)
    assert response1.ask_active is True
    assert "医院" in (response1.ask_output or "")

    # Round2: 用户回答
    response2 = manager.handle_user_turn("瑞金医院", now_ts=int(time.time()))

    # 断言：ask_result 已注入 context
    assert not manager.ask_integration.has_active  # Ask 已完成
    assert "ask_result" in instance.context.data
    assert instance.context.data["ask_result"]["hospital_name"] == "瑞金医院"


def test_multiple_errors_trigger_abort():
    """场景3: limit=1，多次错误 → 触发 abort → 任务被终止"""
    runtime = FlowRuntime()
    manager = TaskChainManager(runtime)

    schema = AskSchema(
        task_id="hospital_task",
        slots=[
            AskSlot(
                name="hospital_name",
                kind=AskSlotKind.REQUIRED,
                prompt_template="您要去哪家医院？",
            ),
        ],
        retry_policy=RetryPolicy(
            interval=0.0,
            limit=1,
            on_exceed=OnExceedAction.ABORT,
        ),
    )

    instance = _create_mock_flow_instance("hospital_task")
    manager.register_task(instance, task_meta={"ask_schema": schema})

    # Round1: 首次调用，获取 prompt
    response1 = manager.handle_user_turn("", now_ts=int(time.time()))
    assert isinstance(response1, TaskExecutionResult)
    assert response1.ask_active is True

    # Round2: 用户给空回答，触发 retry
    response2 = manager.handle_user_turn("   ", now_ts=int(time.time()) + 1)
    assert isinstance(response2, TaskExecutionResult)
    assert response2.ask_active is True
    assert "再确认" in (response2.ask_output or "") or "不好意思" in (response2.ask_output or "")

    # Round3: 用户再次给空回答，触发 abort
    response3 = manager.handle_user_turn("   ", now_ts=int(time.time()) + 2)

    # 断言：active_ask 被清空；response 里有终止提示
    assert isinstance(response3, TaskExecutionResult)
    assert not manager.ask_integration.has_active
    assert response3.ask_active is False
    assert response3.ask_output is not None
    assert "结束" in response3.ask_output or "停" in response3.ask_output


def test_ask_completed_then_main_task_runs():
    """场景4: 有 Ask 的任务执行完问询 → 下次 handle_user_turn 开始正常跑主任务链"""
    runtime = FlowRuntime()
    manager = TaskChainManager(runtime)

    schema = AskSchema(
        task_id="hospital_task",
        slots=[
            AskSlot(
                name="hospital_name",
                kind=AskSlotKind.REQUIRED,
                prompt_template="您要去哪家医院？",
            ),
        ],
    )

    instance = _create_mock_flow_instance("hospital_task")
    manager.register_task(instance, task_meta={"ask_schema": schema})

    # Round1: 首次调用，获取 prompt
    response1 = manager.handle_user_turn("", now_ts=int(time.time()))
    assert isinstance(response1, TaskExecutionResult)
    assert response1.ask_active is True

    # Round2: 用户回答，Ask 完成
    response2 = manager.handle_user_turn("瑞金医院", now_ts=int(time.time()) + 1)
    assert isinstance(response2, TaskExecutionResult)
    assert response2.ask_active is False
    assert response2.task_active is True  # Ask 完成后，TaskChain 应该启动
    assert not manager.ask_integration.has_active

    # Round3: 再次调用，应该可以正常处理主任务链
    # 注意：由于 FlowInstance 没有实际的执行逻辑，任务可能会立即完成
    response3 = manager.handle_user_turn("正常输入", now_ts=int(time.time()) + 2)
    assert isinstance(response3, TaskExecutionResult)
    assert response3.ask_active is False
    # 主任务链可能正在运行或已完成（取决于 FlowInstance 的实际执行逻辑）
    # 这里只验证 Ask 确实已经结束，主任务链已经启动
    assert response3.phase == "task"


# ==================== AskIntegrationService 独立测试 ====================

def make_schema_with_hospital(limit: int = 1) -> AskSchema:
    """辅助函数：创建一个带医院问询的 AskSchema"""
    return AskSchema(
        task_id="hospital_route",
        slots=[
            AskSlot(
                name="hospital_name",
                kind=AskSlotKind.REQUIRED,
                prompt_template="您要去哪个医院？",
            )
        ],
        retry_policy=RetryPolicy(
            interval=0.0,
            limit=limit,
            on_exceed=OnExceedAction.ABORT,
        ),
    )


def test_task_with_ask_schema_runs_ask_before_task():
    """测试：有 AskSchema 的任务应先进入 Ask，问完再跑任务"""
    service = AskIntegrationService()
    task_meta = {
        "ask_schema": make_schema_with_hospital(limit=2),
    }

    # 启动任务 → 应先进入 Ask
    result0 = service.maybe_start_for_task("task1", task_meta, now_ts=time.time())
    assert result0 is not None
    assert result0.consumed is True
    assert result0.done is False
    assert "哪个医院" in (result0.reply or "")

    # Round1: 用户第一次回答无效 → retry
    r1 = service.step_if_active(user_message="   ", now_ts=time.time())
    assert r1 is not None
    assert r1.done is False
    assert "医院" in (r1.reply or "")

    # Round2: 用户回答正常 → ask 完成
    r2 = service.step_if_active(user_message="瑞金医院", now_ts=time.time())
    assert r2 is not None
    assert r2.done is True
    assert r2.aborted is False
    assert r2.answers.get("hospital_name") == "瑞金医院"


def test_task_ask_exceed_abort():
    """测试：limit=1，两次无效输入 → 超限 abort"""
    service = AskIntegrationService()
    task_meta = {
        "ask_schema": make_schema_with_hospital(limit=1),
    }

    # 启动任务 → 获得首次 prompt
    result0 = service.maybe_start_for_task("task2", task_meta, now_ts=time.time())
    assert result0 is not None
    assert not result0.done

    # Round1: 第一次无效 → retry
    service.step_if_active(user_message="", now_ts=time.time())

    # Round2: 第二次仍然无效 → 超限 abort
    r2 = service.step_if_active(user_message="", now_ts=time.time())
    assert r2 is not None
    assert r2.done is True
    assert r2.aborted is True

    # 之后再调用 step_if_active 应该返回 None（因为 session 已清空）
    r3 = service.step_if_active(user_message="随便", now_ts=time.time())
    assert r3 is None

