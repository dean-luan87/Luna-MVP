from __future__ import annotations

from .budget_state import AdviceBudgetState


def decay_budget(state: AdviceBudgetState, accepted: bool):
    if accepted:
        state.accept_rate = min(1.0, state.accept_rate + 0.05)
        state.suppression_score *= 0.9
    else:
        state.accept_rate *= 0.95
        state.suppression_score = min(1.0, state.suppression_score + 0.1)
