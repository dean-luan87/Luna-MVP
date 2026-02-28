import pytest

from task_engine.ask import (
    AskSlotKind,
    AskSlot,
    AskSchema,
    AskChainBuilder,
    AskManager,
    RetryPolicy,
    OnExceedAction,
)
from task_engine.ask.ask_runtime import AskChainRuntime


def _make_simple_schema() -> AskSchema:
    return AskSchema(
        task_id="go_hospital",
        slots=[
            AskSlot(
                name="destination",
                kind=AskSlotKind.REQUIRED,
                prompt_template="你想去哪个医院？",
            ),
            AskSlot(
                name="department",
                kind=AskSlotKind.OPTIONAL,
                prompt_template="需要看哪个科室？",
            ),
        ],
    )


def test_runtime_first_step_without_input_gives_prompt():
    schema = _make_simple_schema()
    builder = AskChainBuilder()
    plan = builder.build_chain(schema, now_ts=1234567890)

    ask_manager = AskManager()
    # 使用 schema 的 retry_policy
    effective_policy = schema.effective_retry_policy()
    runtime = AskChainRuntime(plan, ask_manager, retry_policy=effective_policy)

    # 第一次调用，没有用户输入，只是给出第一个节点的 prompt
    result, state = runtime.step(user_input=None, now_ts=1234567890)

    assert state.done is False
    assert state.current_node_id is not None
    assert result.action == "retry"
    assert "你想去哪个医院" in (result.message or "")


def test_runtime_happy_path_two_slots():
    schema = _make_simple_schema()
    builder = AskChainBuilder()
    plan = builder.build_chain(schema, now_ts=1111111111)

    ask_manager = AskManager()
    # 使用 schema 的 retry_policy
    effective_policy = schema.effective_retry_policy()
    runtime = AskChainRuntime(plan, ask_manager, retry_policy=effective_policy)

    # 第一次：触发第一个 slot 的提问
    r1, s1 = runtime.step(user_input=None, now_ts=1111111111)
    assert s1.done is False
    assert s1.current_node_id is not None
    first_node = s1.current_node_id

    # 第二次：用户回答第一问
    r2, s2 = runtime.step(user_input="虹口医院", now_ts=1111111112)
    assert r2.filled_value == "虹口医院"
    assert r2.action == "continue"
    # runtime 应该已经切换到第二个节点，并给出第二问的 prompt
    assert s2.done is False
    assert s2.current_node_id is not None
    assert s2.current_node_id != first_node
    assert "科室" in (r2.message or "")

    # 第三次：用户回答第二问
    r3, s3 = runtime.step(user_input="口腔科", now_ts=1111111113)
    assert r3.filled_value == "口腔科"
    assert r3.action == "continue"
    # 第二问结束后，整个链应该完成
    assert s3.done is True
    assert s3.current_node_id is None


def test_runtime_retry_and_exceed_abort():
    # 使用更严格的策略：limit=1，也就是只允许一次失败，第二次失败就 ABORT
    schema = AskSchema(
        task_id="go_hospital",
        slots=[
            AskSlot(
                name="destination",
                kind=AskSlotKind.REQUIRED,
                prompt_template="你想去哪个医院？",
            )
        ],
        retry_policy=RetryPolicy(
            interval=0.0,
            limit=1,
            on_exceed=OnExceedAction.ABORT,
        ),
    )
    builder = AskChainBuilder()
    plan = builder.build_chain(schema, now_ts=2222222222)

    ask_manager = AskManager()
    # 使用 schema 的 retry_policy
    effective_policy = schema.effective_retry_policy()
    runtime = AskChainRuntime(plan, ask_manager, retry_policy=effective_policy)

    # 第一次：给出提问
    r1, s1 = runtime.step(user_input=None, now_ts=2222222222)
    assert s1.done is False
    assert r1.action == "retry"

    # 第二次：用户给出无效回答（空），第一次失败 -> 进入 retry
    r2, s2 = runtime.step(user_input="   ", now_ts=2222222223)
    assert s2.done is False
    assert r2.action == "retry"
    # 应该提示"再确认一次"
    assert "再确认" in (r2.message or "") or "不好意思" in (r2.message or "")

    # 第三次：用户再次无效，达到 limit=1 的上限后再失败 -> ABORT
    r3, s3 = runtime.step(user_input="   ", now_ts=2222222224)
    assert s3.done is True
    assert s3.aborted is True
    assert r3.action == "abort"
    assert r3.message is not None


def test_runtime_exceed_restart_flag():
    schema = AskSchema(
        task_id="go_hospital",
        slots=[
            AskSlot(
                name="destination",
                kind=AskSlotKind.REQUIRED,
                prompt_template="你想去哪个医院？",
            )
        ],
        retry_policy=RetryPolicy(
            interval=0.0,
            limit=1,
            on_exceed=OnExceedAction.ASK_RESTART,
        ),
    )
    builder = AskChainBuilder()
    plan = builder.build_chain(schema, now_ts=3333333333)

    ask_manager = AskManager()
    # 使用 schema 的 retry_policy
    effective_policy = schema.effective_retry_policy()
    runtime = AskChainRuntime(plan, ask_manager, retry_policy=effective_policy)

    # 给出第一次提问
    r1, s1 = runtime.step(user_input=None, now_ts=3333333333)
    assert s1.done is False
    assert r1.action == "retry"

    # 用户连续两次给出空回答 → 先 retry，再触发 ASK_RESTART
    _r2, _s2 = runtime.step(user_input="   ", now_ts=3333333334)
    r3, s3 = runtime.step(user_input="   ", now_ts=3333333335)

    assert s3.done is True
    assert s3.restarted is True
    assert r3.action == "restart"


class TestAskRuntimeRetryLimit:
    """专门盯住 limit=1 + retry 行为的回归测试"""

    def _build_simple_chain(self, limit: int = 1) -> AskChainRuntime:
        schema = AskSchema(
            task_id="hospital_route",
            slots=[
                AskSlot(
                    name="hospital_name",
                    kind=AskSlotKind.REQUIRED,
                    prompt_template="去哪家医院？",
                ),
            ],
            retry_policy=RetryPolicy(
                interval=0.0,
                limit=limit,
                on_exceed=OnExceedAction.ABORT,
            ),
        )
        builder = AskChainBuilder()
        plan = builder.build_chain(schema)
        ask_manager = AskManager()
        effective_policy = schema.effective_retry_policy()
        runtime = AskChainRuntime(
            plan=plan,
            ask_manager=ask_manager,
            retry_policy=effective_policy,
        )
        return runtime

    def test_limit_1_first_invalid_then_retry_then_exceed(self):
        """limit=1: 第一次无效 → retry → 第二次无效 → 超限 abort"""
        runtime = self._build_simple_chain(limit=1)

        # Round 0: 进入链路，先要 prompt
        result, state = runtime.step(user_input=None, now_ts=1000)
        assert not state.done
        assert state.current_node_id is not None
        assert result.message is not None

        # Round 1: 第一次输入无效 → retry，不推进节点
        result, state = runtime.step(user_input="   ", now_ts=1001)
        assert not state.done
        assert state.current_node_id is not None
        assert result.message is not None  # retry prompt

        # Round 2: 第二次还是无效 → 超限，abort + done
        result, state = runtime.step(user_input="   ", now_ts=1002)
        assert state.done is True
        assert state.aborted is True
        # current_node_id 在终止时是否为 None 视实现而定，这里允许两种
        # 关键是 done+aborted=True，不再继续 ask

    def test_limit_1_first_invalid_then_valid(self):
        """limit=1: 第一次无效 → retry → 第二次有效 → 链路结束"""
        runtime = self._build_simple_chain(limit=1)

        # prompt
        runtime.step(user_input=None, now_ts=2000)

        # 第一次无效 → retry
        runtime.step(user_input="", now_ts=2001)

        # 第二次有效 → 链路应结束，且 aborted=False
        result, state = runtime.step(user_input="瑞金医院", now_ts=2002)
        assert state.done is True
        assert state.aborted is False
        # 如果 runtime.answers 中记录了值，这里也可以断言：
        if hasattr(runtime, "answers"):
            assert runtime.answers.get("hospital_name") == "瑞金医院"

