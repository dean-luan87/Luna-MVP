from __future__ import annotations

from .schema import AdviceCandidate, AdviceDecision
from .budget_state import AdviceBudgetState


def evaluate_advice(
    advice: AdviceCandidate,
    state: AdviceBudgetState,
    now_ts: float,
) -> AdviceDecision:
    if advice.is_safety:
        return AdviceDecision(
            allow=True,
            urgency="hard",
            cooldown_s=0,
            reason="safety_override",
        )

    score = advice.value * (1 - state.suppression_score) * state.accept_rate

    if score < 0.4:
        return AdviceDecision(
            allow=False,
            urgency="soft",
            cooldown_s=30,
            reason="low_budget_score",
        )

    return AdviceDecision(
        allow=True,
        urgency="soft",
        cooldown_s=10,
        reason="budget_ok",
    )
