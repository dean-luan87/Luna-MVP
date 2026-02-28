from core.task.task_transition_manager import (
    TaskTransitionManager,
    TaskContext,
    PositionState,
    UserIntentState,
    TaskDecision,
)


def test_end_when_user_want_stop():
    called = {"ask": 0}

    def ask_cb():
        called["ask"] += 1

    mgr = TaskTransitionManager(ask_cb)
    ctx = TaskContext(
        position=PositionState(at_target=False, distance_to_target=5.0, stationary_seconds=0),
        intent=UserIntentState(want_stop=True, want_continue=False),
    )
    decision = mgr.decide(ctx)
    assert decision == TaskDecision.END
    assert called["ask"] == 0


def test_ask_end_when_near_target():
    called = {"ask": 0}

    def ask_cb():
        called["ask"] += 1

    mgr = TaskTransitionManager(ask_cb)
    ctx = TaskContext(
        position=PositionState(at_target=False, distance_to_target=1.0, stationary_seconds=0),
        intent=UserIntentState(want_stop=False, want_continue=True),
    )
    decision = mgr.decide(ctx)
    assert decision == TaskDecision.ASK_END
    assert called["ask"] == 1
