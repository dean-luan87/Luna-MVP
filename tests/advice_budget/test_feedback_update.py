from advice_budget.budget_state import AdviceBudgetState
from advice_budget.feedback import AdviceFeedback


def test_feedback_updates_ema():
    st = AdviceBudgetState(last_spoken_ts=None, accept_rate=0.5, suppression_score=0.0)
    fb = AdviceFeedback(
        kind="path_hint",
        source="pal",
        accepted=False,
        latency_s=3.2,
        context_hash=None,
    )
    st.update_feedback(fb)
    ema1 = st.stats[("path_hint", "pal")]["ema_accept"]
    st.update_feedback(fb)
    ema2 = st.stats[("path_hint", "pal")]["ema_accept"]
    assert ema2 < ema1
