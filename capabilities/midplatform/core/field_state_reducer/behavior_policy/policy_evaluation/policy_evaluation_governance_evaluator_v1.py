from __future__ import annotations

from typing import Any, Dict, List

from .policy_evaluation_types_v1 import EvaluationInput, GovernanceEvaluationResult


def evaluate_governance(
    evaluation_input: EvaluationInput,
    governance_contract: Dict[str, Any],
) -> GovernanceEvaluationResult:
    missing: List[str] = []
    deps = list(governance_contract.get("governance_dependencies", []))
    snapshot = dict(evaluation_input.governance_snapshot)

    for dep in deps:
        dep_id = str(dep.get("dependency_id", ""))
        required = bool(dep.get("required", False))
        if required and not bool(snapshot.get(dep_id, False)):
            missing.append(dep_id)

    # Hard boundary checks from input flags.
    if evaluation_input.state_write_requested:
        missing.append("runtime_boundary_dependency")
    if evaluation_input.action_trigger_requested:
        missing.append("runtime_boundary_dependency")
    if evaluation_input.runtime_state_dependency_requested:
        missing.append("runtime_boundary_dependency")

    if missing:
        return GovernanceEvaluationResult(
            status="governance_review_required",
            passed=False,
            missing_dependencies=tuple(dict.fromkeys(missing)),
        )

    return GovernanceEvaluationResult(
        status="eligible_candidate",
        passed=True,
        missing_dependencies=tuple(),
    )
