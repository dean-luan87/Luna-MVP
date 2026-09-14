from __future__ import annotations

from typing import Any, Dict, Optional

from .policy_evaluation_types_v1 import ConfidenceEvaluationResult, EvaluationInput


def evaluate_confidence(
    evaluation_input: EvaluationInput,
    confidence_contract: Dict[str, Any],
) -> ConfidenceEvaluationResult:
    rows = list(confidence_contract.get("state_type_contracts", []))
    row: Optional[Dict[str, Any]] = None
    for item in rows:
        if item.get("state_type") == evaluation_input.state_type:
            row = item
            break

    if row is None:
        return ConfidenceEvaluationResult(
            status="invalid_input",
            passed=False,
            measured_confidence=None,
            threshold=None,
            rejection_reason="unknown_state_type",
        )

    measured = evaluation_input.confidence_policy_snapshot.get("measured_confidence")
    if measured is None:
        return ConfidenceEvaluationResult(
            status="ineligible",
            passed=False,
            measured_confidence=None,
            threshold=float(row.get("minimum_threshold", 1.0)),
            rejection_reason="confidence_below_threshold",
        )

    if not isinstance(measured, (int, float)):
        return ConfidenceEvaluationResult(
            status="invalid_input",
            passed=False,
            measured_confidence=None,
            threshold=float(row.get("minimum_threshold", 1.0)),
            rejection_reason="confidence_below_threshold",
        )

    minimum_threshold = float(row.get("minimum_threshold", 1.0))
    maximum_cap = float(row.get("maximum_cap", 1.0))

    if bool(row.get("no_automatic_100", True)) and measured >= 1.0:
        measured = maximum_cap

    if bool(row.get("fabricated_confidence_allowed", False)):
        return ConfidenceEvaluationResult(
            status="blocked",
            passed=False,
            measured_confidence=float(measured),
            threshold=minimum_threshold,
            rejection_reason="external_dependency_requested",
        )

    measured = min(float(measured), maximum_cap)
    passed = measured >= minimum_threshold
    return ConfidenceEvaluationResult(
        status="eligible_candidate" if passed else "ineligible",
        passed=passed,
        measured_confidence=measured,
        threshold=minimum_threshold,
        rejection_reason=None if passed else "confidence_below_threshold",
    )
