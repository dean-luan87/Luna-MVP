from __future__ import annotations

from typing import Dict, Iterable, List, Set, Tuple

from .policy_selection_types_v1 import EligiblePolicyCandidate, PolicyExclusionResult


def _pair_key(a: str, b: str) -> Tuple[str, str]:
    return (a, b) if a <= b else (b, a)


def resolve_mutual_exclusion(
    ordered_candidates: Iterable[EligiblePolicyCandidate],
    policy_registry_rows: Iterable[Dict[str, object]],
    composition_contract: Dict[str, object],
    conflict_policy: Dict[str, object],
) -> PolicyExclusionResult:
    rows = list(ordered_candidates)
    registry = {str(r.get("policy_id", "")): r for r in policy_registry_rows}

    prohibited_pairs: Set[Tuple[str, str]] = set()
    for pair in composition_contract.get("non_composable_policy_pairs", []):
        if isinstance(pair, list) and len(pair) == 2:
            prohibited_pairs.add(_pair_key(str(pair[0]), str(pair[1])))

    for case in conflict_policy.get("conflict_cases", []):
        allowed = set(str(x) for x in case.get("allowed_policies", []))
        prohibited = set(str(x) for x in case.get("prohibited_policies", []))
        for a in allowed:
            for b in prohibited:
                prohibited_pairs.add(_pair_key(a, b))

    kept: List[EligiblePolicyCandidate] = []
    excluded_ids: List[str] = []
    steps: List[Dict[str, object]] = []
    unresolved = False
    reasons: List[str] = []

    for candidate in rows:
        pid = candidate.policy_id
        current_exclusive = set(
            str(x)
            for x in registry.get(pid, {}).get("mutually_exclusive_with", [])
            if str(x)
        )

        blocked_by_pair = False
        for kept_candidate in kept:
            kept_pid = kept_candidate.policy_id
            pair = _pair_key(pid, kept_pid)
            reverse_exclusive = set(
                str(x)
                for x in registry.get(kept_pid, {}).get("mutually_exclusive_with", [])
                if str(x)
            )

            if (
                kept_pid in current_exclusive
                or pid in reverse_exclusive
                or pair in prohibited_pairs
            ):
                if candidate.input_order_index == kept_candidate.input_order_index:
                    unresolved = True
                    reasons.append("unresolved_exclusion")
                    steps.append(
                        {
                            "left_policy": kept_pid,
                            "right_policy": pid,
                            "resolved": False,
                            "reason": "same_input_order_unresolved_exclusion",
                        }
                    )
                    continue

                blocked_by_pair = True
                excluded_ids.append(pid)
                steps.append(
                    {
                        "left_policy": kept_pid,
                        "right_policy": pid,
                        "resolved": True,
                        "winner": kept_pid,
                        "reason": "mutual_exclusion_or_prohibited_combination",
                    }
                )
                break

        if not blocked_by_pair:
            kept.append(candidate)

    return PolicyExclusionResult(
        kept_candidates=tuple(kept),
        excluded_policy_ids=tuple(dict.fromkeys(excluded_ids)),
        exclusion_steps=tuple(steps),
        unresolved=unresolved,
        rejection_reasons=tuple(dict.fromkeys(reasons)),
    )
