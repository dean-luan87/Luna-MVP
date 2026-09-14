from __future__ import annotations

from typing import Dict, Iterable, List, Set, Tuple

from .policy_selection_types_v1 import (
    EligiblePolicyCandidate,
    PolicyCompositionCandidate,
)


def resolve_composition_eligibility(
    candidates: Iterable[EligiblePolicyCandidate],
    composition_contract: Dict[str, object],
    policy_registry_rows: Iterable[Dict[str, object]],
) -> PolicyCompositionCandidate:
    rows = list(candidates)
    if not rows:
        return PolicyCompositionCandidate(
            policy_ids=tuple(),
            composition_sequence=tuple(),
            eligible=False,
            reason="no_eligible_candidate",
        )

    order = tuple(
        str(x) for x in composition_contract.get("deterministic_composition_order", [])
    )
    max_depth = int(composition_contract.get("maximum_composition_depth", 3))

    non_composable: Set[Tuple[str, str]] = set()
    for pair in composition_contract.get("non_composable_policy_pairs", []):
        if isinstance(pair, list) and len(pair) == 2:
            a, b = str(pair[0]), str(pair[1])
            non_composable.add((a, b) if a <= b else (b, a))

    selected_ids = [c.policy_id for c in rows]
    registry = {str(r.get("policy_id", "")): r for r in policy_registry_rows}

    for i in range(len(selected_ids)):
        for j in range(i + 1, len(selected_ids)):
            a, b = selected_ids[i], selected_ids[j]
            key = (a, b) if a <= b else (b, a)
            if key in non_composable:
                return PolicyCompositionCandidate(
                    policy_ids=tuple(selected_ids),
                    composition_sequence=tuple(),
                    eligible=False,
                    reason="non_composable_policy_pair",
                )

            a_with = set(str(x) for x in registry.get(a, {}).get("composable_with", []))
            b_with = set(str(x) for x in registry.get(b, {}).get("composable_with", []))
            if b not in a_with and a not in b_with:
                return PolicyCompositionCandidate(
                    policy_ids=tuple(selected_ids),
                    composition_sequence=tuple(),
                    eligible=False,
                    reason="non_composable_policy_pair",
                )

    ordered_sequence: List[str] = [pid for pid in order if pid in set(selected_ids)]
    overflow = len(ordered_sequence) > max_depth
    if overflow:
        return PolicyCompositionCandidate(
            policy_ids=tuple(selected_ids),
            composition_sequence=tuple(ordered_sequence[:max_depth]),
            eligible=False,
            reason="composition_depth_overflow",
        )

    return PolicyCompositionCandidate(
        policy_ids=tuple(selected_ids),
        composition_sequence=tuple(ordered_sequence),
        eligible=len(ordered_sequence) > 1,
        reason=None,
    )
