from __future__ import annotations

from typing import Any, Dict

from .policy_evaluation_types_v1 import ConflictEvaluationResult, EvaluationInput


def evaluate_conflict(
    evaluation_input: EvaluationInput,
    conflict_contract: Dict[str, Any],
) -> ConflictEvaluationResult:
    conflict_type = str(evaluation_input.conflict_snapshot.get("conflict_type", ""))
    unresolved = bool(evaluation_input.conflict_snapshot.get("unresolved", False))

    rows = list(conflict_contract.get("conflict_types", []))
    row = next((r for r in rows if r.get("conflict_type") == conflict_type), None)
    if row is None:
        return ConflictEvaluationResult(
            status="eligible_candidate",
            unresolved=False,
            policy_eligibility_allowed=True,
            preserve_conflict=True,
            rejection_reason=None,
        )

    if unresolved:
        return ConflictEvaluationResult(
            status=str(
                row.get("evaluation_status_when_unresolved", "unresolved_conflict")
            ),
            unresolved=True,
            policy_eligibility_allowed=bool(
                row.get("policy_eligibility_allowed", False)
            ),
            preserve_conflict=bool(row.get("preserve_conflict", True)),
            rejection_reason="unresolved_conflict_present",
        )

    return ConflictEvaluationResult(
        status="eligible_candidate",
        unresolved=False,
        policy_eligibility_allowed=True,
        preserve_conflict=bool(row.get("preserve_conflict", True)),
        rejection_reason=None,
    )
