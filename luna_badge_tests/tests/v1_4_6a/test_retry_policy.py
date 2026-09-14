import pytest

from task_engine.ask.retry_policy import RetryPolicy, OnExceedAction


def test_default_retry_policy_values():
    policy = RetryPolicy.default()
    assert policy.interval == 5.0
    assert policy.limit == 3
    assert policy.on_exceed == OnExceedAction.ABORT
    assert policy.adaptive is False
    assert policy.ai_adjust_hook is None


def test_retry_policy_with_overrides():
    base = RetryPolicy.default()
    updated = base.with_overrides(interval=2.5, limit=1, on_exceed=OnExceedAction.CLARIFY)

    assert updated.interval == 2.5
    assert updated.limit == 1
    assert updated.on_exceed == OnExceedAction.CLARIFY

    # Unchanged fields stay the same as base.
    assert updated.adaptive == base.adaptive
    assert updated.ai_adjust_hook == base.ai_adjust_hook


def test_retry_policy_from_raw_dict():
    base = RetryPolicy.default()

    raw = {
        "interval": 4.0,
        "limit": 2,
        "on_exceed": "fallback",
        "adaptive": True,
        "ai_adjust_hook": "emotion",
    }

    # Simulate AskManager.resolve_policy_for_task behaviour in a simplified way.
    # We don't import AskManager here to keep this test focused on RetryPolicy.
    from task_engine.ask.retry_policy import OnExceedAction

    updated = base.with_overrides(
        interval=raw.get("interval"),
        limit=raw.get("limit"),
        on_exceed=OnExceedAction(raw.get("on_exceed")),
        adaptive=raw.get("adaptive"),
        ai_adjust_hook=raw.get("ai_adjust_hook"),
    )

    assert updated.interval == 4.0
    assert updated.limit == 2
    assert updated.on_exceed == OnExceedAction.FALLBACK
    assert updated.adaptive is True
    assert updated.ai_adjust_hook == "emotion"












