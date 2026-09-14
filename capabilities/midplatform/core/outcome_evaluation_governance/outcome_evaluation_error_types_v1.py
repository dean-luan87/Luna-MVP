"""Errors owned only by the Outcome Evaluation candidate layer."""

from dataclasses import dataclass
from typing import Tuple

ERROR_NAMESPACE = "OUTCOME_EVALUATION_GOVERNANCE"


@dataclass(frozen=True)
class OutcomeEvaluationErrorV1:
    code: str
    message: str
    related_refs: Tuple[str, ...] = ()
    fatal: bool = False
    trace_ref: str = ""
    namespace: str = ERROR_NAMESPACE
