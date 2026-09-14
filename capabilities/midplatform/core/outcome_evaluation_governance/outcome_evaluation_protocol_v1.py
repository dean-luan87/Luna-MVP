"""Protocol boundary for the narrow Outcome Evaluation owner."""

from typing import Protocol

from .outcome_evaluation_core_types_v1 import OutcomeEvaluationOutputV1, OutcomeEvaluationRequestV1


class OutcomeEvaluationProtocolV1(Protocol):
    def run_case(self, request: OutcomeEvaluationRequestV1) -> OutcomeEvaluationOutputV1:
        """Return candidate-only comparison/evaluation output."""
