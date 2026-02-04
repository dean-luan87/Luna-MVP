"""
Demo: AskChainRuntime 简单演示脚本

运行方式:
    python scripts/demo_ask_chain_runtime.py

演示内容:
    1. 成功路径：用户正确回答所有问题
    2. 失败路径：用户连续失败，触发超限处理
"""

import sys
import os
import time

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

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


def simple_schema():
    """创建一个简单的医院问询 Schema"""
    return AskSchema(
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


def run_demo_success_path():
    """演示成功路径"""
    print("=" * 50)
    print("演示：成功路径")
    print("=" * 50)

    schema = simple_schema()

    # 构建链
    builder = AskChainBuilder()
    plan = builder.build_chain(schema, now_ts=int(time.time()))

    # 创建 Runtime
    ask_manager = AskManager()
    effective_policy = schema.effective_retry_policy()
    runtime = AskChainRuntime(plan, ask_manager, retry_policy=effective_policy)

    user_inputs = [
        None,  # 第一次 → prompt
        "中山医院",  # 正确回答第一个问题
        "皮肤科",  # 正确回答第二个问题
    ]

    for i, user_input in enumerate(user_inputs):
        print(f"\n--- Round {i + 1} ---")
        print(f"User input: {repr(user_input)}")

        result, state = runtime.step(
            user_input=user_input,
            now_ts=int(time.time()),
            context={},
        )

        print(f"State: done={state.done}, current_node={state.current_node_id}")
        if result.message:
            print(f"Output: {result.message}")
        if result.filled_value:
            print(f"Filled value: {result.filled_value}")

        if state.done:
            print("\n✅ AskChain 成功完成！")
            break


def run_demo_failure_path():
    """演示失败路径（超限触发 ABORT）"""
    print("\n" + "=" * 50)
    print("演示：失败路径（超限触发 ABORT）")
    print("=" * 50)

    schema = simple_schema()

    # 构建链
    builder = AskChainBuilder()
    plan = builder.build_chain(schema, now_ts=int(time.time()))

    # 创建 Runtime
    ask_manager = AskManager()
    effective_policy = schema.effective_retry_policy()
    runtime = AskChainRuntime(plan, ask_manager, retry_policy=effective_policy)

    user_inputs = [
        None,  # 第一次 → prompt
        "",  # 错误回答 → retry
        "",  # 再次错误 → abort
    ]

    for i, user_input in enumerate(user_inputs):
        print(f"\n--- Round {i + 1} ---")
        print(f"User input: {repr(user_input)}")

        result, state = runtime.step(
            user_input=user_input,
            now_ts=int(time.time()),
            context={},
        )

        print(f"State: done={state.done}, aborted={state.aborted}, current_node={state.current_node_id}")
        print(f"Action: {result.action}")
        if result.message:
            print(f"Output: {result.message}")

        if state.done or state.aborted:
            print("\n❌ AskChain 因超限而终止")
            break


def run_demo():
    """运行所有演示"""
    print("\n" + "=" * 50)
    print("AskChainRuntime Demo")
    print("=" * 50)

    # 成功路径
    run_demo_success_path()

    # 失败路径
    run_demo_failure_path()

    print("\n" + "=" * 50)
    print("Demo 完成")
    print("=" * 50)


if __name__ == "__main__":
    run_demo()

