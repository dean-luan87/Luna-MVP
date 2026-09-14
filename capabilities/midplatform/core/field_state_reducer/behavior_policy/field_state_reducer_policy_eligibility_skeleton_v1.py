from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple

from .field_state_reducer_behavior_policy_registry_skeleton_v1 import (
    FIELD_STATE_REDUCER_BEHAVIOR_POLICY_REGISTRY_SKELETON_V1,
)
from .field_state_reducer_behavior_policy_types_v1 import (
    BehaviorPolicyEligibilityInputV1,
    BehaviorPolicyEligibilityResultV1,
    BehaviorPolicyEligibilityStatusV1,
)


def validate_eligibility_input(
    eligibility_input: BehaviorPolicyEligibilityInputV1,
) -> Tuple[bool, Tuple[str, ...]]:
    issues: List[str] = []
    if not eligibility_input.state_type:
        issues.append("missing_state_type")
    if eligibility_input.no_provider_recall is not True:
        issues.append("provider_recall_forbidden")
    if eligibility_input.no_external_lookup is not True:
        issues.append("external_lookup_forbidden")
    if eligibility_input.no_action_trigger is not True:
        issues.append("action_trigger_forbidden")
    return len(issues) == 0, tuple(issues)


def list_candidate_policies(state_type: str) -> Tuple[str, ...]:
    candidates: List[str] = []
    for row in FIELD_STATE_REDUCER_BEHAVIOR_POLICY_REGISTRY_SKELETON_V1:
        if state_type in tuple(row.get("eligible_state_types", tuple())):
            candidates.append(str(row["policy_id"]))
    if not candidates:
        candidates = ["no_state_change"]
    return tuple(candidates)


def build_placeholder_eligibility_results(
    candidate_policy_ids: Iterable[str],
) -> Tuple[BehaviorPolicyEligibilityResultV1, ...]:
    return tuple(
        BehaviorPolicyEligibilityResultV1(
            policy_id=str(policy_id),
            status=BehaviorPolicyEligibilityStatusV1.PLACEHOLDER_ELIGIBLE.value,
            reasons=("placeholder_only",),
            eligibility_executed=False,
            placeholder_only=True,
        )
        for policy_id in candidate_policy_ids
    )


def placeholder_eligibility_payload(
    candidate_policy_ids: Iterable[str],
) -> Dict[str, Any]:
    return {
        "candidate_policy_ids": tuple(str(x) for x in candidate_policy_ids),
        "eligibility_results": [
            {
                "policy_id": r.policy_id,
                "status": r.status,
                "reasons": r.reasons,
                "eligibility_executed": r.eligibility_executed,
                "placeholder_only": r.placeholder_only,
            }
            for r in build_placeholder_eligibility_results(candidate_policy_ids)
        ],
        "eligibility_executed": False,
        "placeholder_only": True,
    }
