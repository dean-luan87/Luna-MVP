from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

from .policy_selection_types_v1 import EligiblePolicyCandidate


_PRECEDENCE_CLASS_RANK = {
    "override_top": 0,
    "safety_top": 1,
    "override_high": 2,
    "overlay_high": 3,
    "safety_high": 4,
    "selection_high": 5,
    "selection_mid": 6,
    "governed_mid": 7,
    "selection_low": 8,
    "fallback": 9,
}


def _rank_for(candidate: EligiblePolicyCandidate) -> Tuple[int, str, str, str, int]:
    return (
        _PRECEDENCE_CLASS_RANK.get(candidate.precedence_class, 100),
        candidate.evaluation_status,
        candidate.policy_id,
        candidate.policy_version,
        candidate.input_order_index,
    )


def deterministic_tie_break(
    candidates: Iterable[EligiblePolicyCandidate],
) -> Tuple[Tuple[EligiblePolicyCandidate, ...], Tuple[Dict[str, object], ...], bool]:
    rows: List[EligiblePolicyCandidate] = list(candidates)
    unresolved = any(c.input_order_index < 0 for c in rows)

    sorted_rows = sorted(rows, key=_rank_for)
    steps: List[Dict[str, object]] = []
    for idx, c in enumerate(sorted_rows, start=1):
        steps.append(
            {
                "step": idx,
                "policy_id": c.policy_id,
                "precedence_class": c.precedence_class,
                "evaluation_status": c.evaluation_status,
                "policy_version": c.policy_version,
                "input_order_index": c.input_order_index,
            }
        )
    return tuple(sorted_rows), tuple(steps), unresolved
