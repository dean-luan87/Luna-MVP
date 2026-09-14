from __future__ import annotations

from typing import Dict, Iterable, List, Set, Tuple

from .policy_selection_tie_breaker_v1 import deterministic_tie_break
from .policy_selection_types_v1 import EligiblePolicyCandidate, PolicyPrecedenceResult


def resolve_precedence(
    candidates: Iterable[EligiblePolicyCandidate],
    precedence_matrix: Dict[str, object],
) -> Tuple[PolicyPrecedenceResult, Tuple[Dict[str, object], ...]]:
    ordered, tie_steps, tie_unresolved = deterministic_tie_break(candidates)

    rules = list(precedence_matrix.get("precedence_rules", []))
    active_ids = [c.policy_id for c in ordered]
    excluded: Set[str] = set()
    steps: List[Dict[str, object]] = []

    for rule in rules:
        higher = str(rule.get("higher_policy", ""))
        lower = str(rule.get("lower_policy", ""))
        if not higher or not lower:
            continue
        if higher in active_ids and lower in active_ids and lower not in excluded:
            excluded.add(lower)
            steps.append(
                {
                    "higher_policy": higher,
                    "lower_policy": lower,
                    "applied": True,
                    "reason": str(rule.get("reason", "precedence_rule_applied")),
                }
            )

    kept = tuple(c for c in ordered if c.policy_id not in excluded)

    reasons: List[str] = []
    if tie_unresolved:
        reasons.append("unresolved_precedence")

    # Explicit safeguard fallback ordering support in controlled mode.
    if not kept:
        fallback = [c for c in ordered if c.policy_id == "no_state_change"]
        if fallback:
            kept = (fallback[0],)
            reasons.append("no_state_change_fallback")

    result = PolicyPrecedenceResult(
        ordered_candidates=kept,
        ordered_policy_ids=tuple(c.policy_id for c in kept),
        excluded_policy_ids=tuple(sorted(excluded)),
        precedence_steps=tuple(steps),
        unresolved=tie_unresolved,
        rejection_reasons=tuple(dict.fromkeys(reasons)),
    )
    return result, tie_steps
