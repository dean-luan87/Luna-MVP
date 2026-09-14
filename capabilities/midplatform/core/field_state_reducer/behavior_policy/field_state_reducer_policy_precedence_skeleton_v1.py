from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple


PRECEDENCE_RULES_SKELETON_V1: Tuple[Dict[str, Any], ...] = (
    {
        "higher_policy": "revocation_override",
        "lower_policy": "latest_valid_event",
        "condition": "revocation_event_valid_and_active",
        "registered": True,
        "fact_promotion_allowed": False,
    },
    {
        "higher_policy": "conflict_preservation",
        "lower_policy": "highest_confidence_valid_event",
        "condition": "contradiction_unresolved_or_unsafe_single_winner",
        "registered": True,
        "fact_promotion_allowed": False,
    },
    {
        "higher_policy": "insufficient_evidence_unresolved",
        "lower_policy": "latest_valid_event",
        "condition": "evidence_below_threshold",
        "registered": True,
        "fact_promotion_allowed": False,
    },
    {
        "higher_policy": "temporary_overlay_separation",
        "lower_policy": "latest_valid_event",
        "condition": "overlay_and_substrate_both_present",
        "registered": True,
        "fact_promotion_allowed": False,
    },
)


precedence_execution_executed = False


def load_precedence_rules() -> Tuple[Dict[str, Any], ...]:
    return PRECEDENCE_RULES_SKELETON_V1


def build_placeholder_precedence_sequence(
    candidate_policy_ids: Iterable[str],
) -> Tuple[str, ...]:
    sequence = tuple(str(x) for x in candidate_policy_ids)
    return sequence if sequence else ("no_state_change",)


def validate_no_unsafe_override(
    rules: Iterable[Dict[str, Any]],
) -> Tuple[bool, Tuple[str, ...]]:
    issues: List[str] = []
    required_pairs = {
        ("revocation_override", "latest_valid_event"),
        ("conflict_preservation", "highest_confidence_valid_event"),
        ("insufficient_evidence_unresolved", "latest_valid_event"),
        ("temporary_overlay_separation", "latest_valid_event"),
    }
    got = {
        (str(r.get("higher_policy", "")), str(r.get("lower_policy", ""))) for r in rules
    }
    missing = required_pairs - got
    if missing:
        issues.append("missing_required_precedence_rules")
    if any(r.get("fact_promotion_allowed") is True for r in rules):
        issues.append("fact_promotion_forbidden")
    return len(issues) == 0, tuple(issues)
