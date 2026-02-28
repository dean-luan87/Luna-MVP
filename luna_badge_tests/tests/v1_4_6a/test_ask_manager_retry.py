import pytest

from task_engine.ask.retry_policy import RetryPolicy, OnExceedAction
from task_engine.ask.ask_manager import AskManager, AskSessionState


def test_ask_manager_uses_default_policy_when_no_meta():
    manager = AskManager()
    policy = manager.resolve_policy_for_task(task_meta=None)

    assert policy.interval == 5.0
    assert policy.limit == 3
    assert policy.on_exceed == OnExceedAction.ABORT


def test_ask_manager_resolves_policy_from_task_meta():
    manager = AskManager()

    task_meta = {
        "retry_policy": {
            "interval": 3.0,
            "limit": 2,
            "on_exceed": "clarify",
            "adaptive": True,
            "ai_adjust_hook": "emotion",
        }
    }

    policy = manager.resolve_policy_for_task(task_meta=task_meta)
    assert policy.interval == 3.0
    assert policy.limit == 2
    assert policy.on_exceed == OnExceedAction.CLARIFY
    assert policy.adaptive is True
    assert policy.ai_adjust_hook == "emotion"


def test_ask_session_retry_flow_until_exceeded():
    manager = AskManager()
    policy = RetryPolicy(interval=1.0, limit=2, on_exceed=OnExceedAction.ABORT)

    session = manager.create_session(slot_id="destination", policy=policy, now=0.0)

    # First retry allowed at t=0
    assert manager.should_retry_now(session, now=0.0) is True
    manager.register_retry(session, now=0.0)
    assert session.retry_count == 1
    assert session.exceeded is False
    assert session.next_retry_at == pytest.approx(1.0)

    # Before next_retry_at, should not retry
    assert manager.should_retry_now(session, now=0.5) is False

    # At t=1.0, second retry allowed
    assert manager.should_retry_now(session, now=1.0) is True
    manager.register_retry(session, now=1.0)
    assert session.retry_count == 2
    assert session.exceeded is False
    assert session.next_retry_at == pytest.approx(2.0)

    # Third retry would exceed limit
    assert manager.should_retry_now(session, now=2.0) is True
    manager.register_retry(session, now=2.0)
    assert session.retry_count == 3
    assert session.exceeded is True

    # Once exceeded, no more retries should be allowed
    assert manager.should_retry_now(session, now=3.0) is False


def test_reset_session_clears_retry_state():
    manager = AskManager()
    session = manager.create_session(slot_id="destination", now=0.0)

    manager.register_retry(session, now=0.0)
    assert session.retry_count == 1

    manager.reset_session(session, now=10.0)
    assert session.retry_count == 0
    assert session.exceeded is False
    assert session.next_retry_at == 10.0












