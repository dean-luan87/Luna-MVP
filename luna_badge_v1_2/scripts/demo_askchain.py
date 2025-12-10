#!/usr/bin/env python3
"""
Demo script: How AskChain works (v1.4.6a)

Can run standalone:

    python3 scripts/demo_askchain.py
"""

import sys
import os
import time

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from task_engine.ask import (
    AskSchema,
    AskSlot,
    AskSlotKind,
    AskChainBuilder,
    AskChainRuntime,
    AskManager,
    RetryPolicy,
)


def build_demo_schema():
    return AskSchema(
        task_id="hospital_route",
        slots=[
            AskSlot(
                name="hospital_name",
                kind=AskSlotKind.REQUIRED,
                prompt_template="您要去哪家医院？",
            ),
            AskSlot(
                name="department",
                kind=AskSlotKind.CLARIFY,
                prompt_template="您是要去哪个科室？",
            ),
        ],
    )


def run_demo():
    schema = build_demo_schema()

    print("\n=== DEMO: AskChain Started ===\n")

    builder = AskChainBuilder()
    plan = builder.build_chain(schema, now_ts=int(time.time()))

    ask_manager = AskManager()
    effective_policy = schema.effective_retry_policy()
    runtime = AskChainRuntime(plan, ask_manager, retry_policy=effective_policy)

    user_inputs = [
        None,                # 第 1 轮：系统出 prompt
        "瑞金医院",           # 第 2 轮：回答 REQUIRED slot
        None,                # 第 3 轮：系统问 CLARIFY slot
        "心内科",             # 第 4 轮：最后一个 slot 回答
    ]

    for i, user_msg in enumerate(user_inputs):
        print(f"\n--- Round {i + 1} ---")

        result, state = runtime.step(
            user_input=user_msg,
            now_ts=int(time.time()),
            context={},
        )

        print(f"message = {result.message}")
        print(f"current_node = {state.current_node_id}")
        print(f"done = {state.done}")

        if state.done:
            print("\n=== AskChain Completed ===\n")
            break

    return True


if __name__ == "__main__":
    run_demo()

