"""
测试 demo_ask_chain_runtime.py 的稳定性

确保 demo 脚本可以正常运行，不会因为环境变化而失败。
"""

import sys
import os

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pytest
from task_engine.ask import (
    RetryPolicy,
    OnExceedAction,
    AskSlot,
    AskSlotKind,
    AskSchema,
    AskChainBuilder,
    AskChainRuntime,
    AskManager,
)


def test_demo_success_path():
    """测试成功路径"""
    schema = AskSchema(
        task_id="hospital",
        slots=[
            AskSlot(
                name="hospital_name",
                kind=AskSlotKind.REQUIRED,
                prompt_template="请问你想去哪个医院？",
            ),
            AskSlot(
                name="department",
                kind=AskSlotKind.OPTIONAL,
                prompt_template="如果方便的话，请告诉我科室名称。",
            ),
        ],
        retry_policy=RetryPolicy(
            interval=0.0,
            limit=1,
            on_exceed=OnExceedAction.ABORT,
        ),
    )

    builder = AskChainBuilder()
    plan = builder.build_chain(schema, now_ts=1234567890)

    ask_manager = AskManager()
    effective_policy = schema.effective_retry_policy()
    runtime = AskChainRuntime(plan, ask_manager, retry_policy=effective_policy)

    # Round 1: 无输入，应该返回 prompt
    result1, state1 = runtime.step(user_input=None, now_ts=1234567890, context={})
    assert state1.done is False
    assert result1.action == "retry"
    assert "医院" in (result1.message or "")

    # Round 2: 正确回答第一个问题
    result2, state2 = runtime.step(user_input="中山医院", now_ts=1234567891, context={})
    assert state2.done is False
    assert result2.action == "continue"
    assert result2.filled_value == "中山医院"
    assert "科室" in (result2.message or "")

    # Round 3: 正确回答第二个问题
    result3, state3 = runtime.step(user_input="皮肤科", now_ts=1234567892, context={})
    assert state3.done is True
    assert result3.action == "continue"
    assert result3.filled_value == "皮肤科"


def test_demo_failure_path():
    """测试失败路径（超限触发 ABORT）"""
    schema = AskSchema(
        task_id="hospital",
        slots=[
            AskSlot(
                name="hospital_name",
                kind=AskSlotKind.REQUIRED,
                prompt_template="请问你想去哪个医院？",
            ),
        ],
        retry_policy=RetryPolicy(
            interval=0.0,
            limit=1,
            on_exceed=OnExceedAction.ABORT,
        ),
    )

    builder = AskChainBuilder()
    plan = builder.build_chain(schema, now_ts=1234567890)

    ask_manager = AskManager()
    effective_policy = schema.effective_retry_policy()
    runtime = AskChainRuntime(plan, ask_manager, retry_policy=effective_policy)

    # Round 1: 无输入，应该返回 prompt
    result1, state1 = runtime.step(user_input=None, now_ts=1234567890, context={})
    assert state1.done is False
    assert result1.action == "retry"

    # Round 2: 错误回答，应该触发 retry
    result2, state2 = runtime.step(user_input="", now_ts=1234567891, context={})
    assert state2.done is False
    assert result2.action == "retry"
    assert "再确认" in (result2.message or "") or "不好意思" in (result2.message or "")

    # Round 3: 再次错误，应该触发 ABORT
    result3, state3 = runtime.step(user_input="", now_ts=1234567892, context={})
    assert state3.done is True
    assert state3.aborted is True
    assert result3.action == "abort"
    assert result3.message is not None












