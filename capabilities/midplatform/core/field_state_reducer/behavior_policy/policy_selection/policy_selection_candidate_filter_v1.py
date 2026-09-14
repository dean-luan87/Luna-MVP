from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

from .policy_selection_types_v1 import EligiblePolicyCandidate


_ALLOWED_STATUS = {"eligible_candidate"}
_BLOCKED_STATUS = {
    "ineligible",
    "blocked",
    "insufficient_evidence",
    "unresolved_conflict",
    "temporally_invalid",
    "governance_review_required",
    "invalid_input",
}


def filter_eligible_candidates(
    evaluation_results: Iterable[Dict[str, object]],
    policy_registry_rows: Iterable[Dict[str, object]],
    *,
    state_type: str,
) -> Tuple[Tuple[EligiblePolicyCandidate, ...], Tuple[str, ...], Tuple[str, ...]]:
    registry = {
        str(r.get("policy_id", "")): r
        for r in policy_registry_rows
        if str(r.get("policy_id", ""))
    }

    candidates: List[EligiblePolicyCandidate] = []
    rejected_policy_ids: List[str] = []
    rejection_reasons: List[str] = []

    for idx, row in enumerate(evaluation_results):
        policy_id = str(row.get("policy_id", ""))
        status = str(row.get("evaluation_status", ""))
        allowed = bool(row.get("selection_candidate_allowed", False))

        if not policy_id:
            rejection_reasons.append("invalid_input")
            continue

        if policy_id not in registry:
            rejected_policy_ids.append(policy_id)
            rejection_reasons.append("unknown_policy")
            continue

        if status in _BLOCKED_STATUS or status not in _ALLOWED_STATUS or not allowed:
            rejected_policy_ids.append(policy_id)
            rejection_reasons.append(status if status else "invalid_input")
            continue

        policy_row = registry[policy_id]
        eligible_state_types = tuple(
            str(value)
            for value in policy_row.get("eligible_state_types", [])
            if str(value)
        )
        if state_type not in eligible_state_types:
            rejected_policy_ids.append(policy_id)
            rejection_reasons.append("state_type_not_applicable")
            continue

        candidates.append(
            EligiblePolicyCandidate(
                evaluation_id=str(row.get("evaluation_id", "")),
                policy_id=policy_id,
                policy_version=str(policy_row.get("policy_version", "v1")),
                precedence_class=str(policy_row.get("precedence_class", "fallback")),
                evaluation_status=status,
                selection_candidate_allowed=allowed,
                input_order_index=idx,
            )
        )

    return (
        tuple(candidates),
        tuple(dict.fromkeys(rejected_policy_ids)),
        tuple(dict.fromkeys(rejection_reasons)),
    )
