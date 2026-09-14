"""Future feedback boundary; no action result is generated here."""
from __future__ import annotations

from typing import Any, Mapping

from .decision_candidate_flow import DecisionCandidate


class FeedbackPlaceholder:
    def create(self, candidate: DecisionCandidate) -> dict[str, Any]:
        return {
            "feedback_status": "future_action_result_required",
            "decision_candidate_id": candidate.decision_candidate_id,
            "action_result": None,
            "learning_execution": False,
        }
