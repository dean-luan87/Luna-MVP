import pytest

from task_engine.ask import (
    AskSlot,
    AskSlotKind,
    AskSchema,
    AskNodeBase,
    StandardAskNode,
    AskNodeResult,
    RetryPolicy,
    OnExceedAction,
)


def test_standard_ask_node_build_prompt_with_template_and_context():
    slot = AskSlot(
        name="destination",
        kind=AskSlotKind.REQUIRED,
        prompt_template="你想去哪里？当前场景是：{scene}",
    )
    node = StandardAskNode(slot=slot)

    context = {"scene": "医院"}
    prompt = node.build_prompt(context)

    assert "你想去哪里" in prompt
    assert "医院" in prompt


def test_standard_ask_node_build_prompt_without_template_fallback():
    slot = AskSlot(
        name="destination",
        kind=AskSlotKind.REQUIRED,
        prompt_template=None,
    )
    node = StandardAskNode(slot=slot)

    prompt = node.build_prompt({})
    # 应该兜底为通用提示
    assert "destination" in prompt


def test_standard_ask_node_extract_answer_accepts_non_empty_text():
    slot = AskSlot(
        name="destination",
        kind=AskSlotKind.REQUIRED,
        prompt_template="你想去哪里？",
    )
    node = StandardAskNode(slot=slot)

    assert node.extract_answer(" 虹口医院 ") == "虹口医院"
    assert node.extract_answer("   ") is None
    assert node.extract_answer("") is None


def test_build_retry_prompt_wraps_base_prompt():
    slot = AskSlot(
        name="destination",
        kind=AskSlotKind.REQUIRED,
        prompt_template="你想去哪里？",
    )
    node = StandardAskNode(slot=slot)
    policy = RetryPolicy.default()

    prompt = node.build_retry_prompt(retry_count=1, policy=policy, context={})
    assert "再确认一次" in prompt or "不好意思" in prompt
    assert "你想去哪里" in prompt


def test_decide_on_exceed_maps_policy_to_actions():
    slot = AskSlot(
        name="destination",
        kind=AskSlotKind.REQUIRED,
        prompt_template="你想去哪里？",
    )
    node = StandardAskNode(slot=slot)

    p_abort = RetryPolicy(interval=1.0, limit=1, on_exceed=OnExceedAction.ABORT)
    res_abort = node.decide_on_exceed(p_abort)
    assert isinstance(res_abort, AskNodeResult)
    assert res_abort.action == "abort"
    assert "结束" in (res_abort.message or "")

    p_fallback = RetryPolicy(interval=1.0, limit=1, on_exceed=OnExceedAction.FALLBACK)
    res_fallback = node.decide_on_exceed(p_fallback)
    assert res_fallback.action == "fallback"

    p_clarify = RetryPolicy(interval=1.0, limit=1, on_exceed=OnExceedAction.CLARIFY)
    res_clarify = node.decide_on_exceed(p_clarify)
    assert res_clarify.action == "clarify"

    p_restart = RetryPolicy(interval=1.0, limit=1, on_exceed=OnExceedAction.ASK_RESTART)
    res_restart = node.decide_on_exceed(p_restart)
    assert res_restart.action == "restart"












