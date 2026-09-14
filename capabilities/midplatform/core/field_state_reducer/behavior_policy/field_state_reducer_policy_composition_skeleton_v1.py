from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple


COMPOSITION_CONTRACT_SKELETON_V1: Dict[str, Any] = {
    "maximum_composition_depth": 3,
    "policy_side_effect_allowed": False,
    "state_write_during_composition_allowed": False,
    "action_trigger_during_composition_allowed": False,
    "deterministic_composition_order": (
        "revocation_override",
        "conflict_preservation",
        "expiration_degrade",
        "temporary_overlay_separation",
        "multi_event_consensus",
        "highest_confidence_valid_event",
        "latest_valid_event",
        "explicit_owner_override_candidate",
        "insufficient_evidence_unresolved",
        "negative_event_override",
        "no_state_change",
    ),
}


composition_execution_executed = False


def load_composition_contract() -> Dict[str, Any]:
    return dict(COMPOSITION_CONTRACT_SKELETON_V1)


def list_allowed_compositions() -> Tuple[Tuple[str, ...], ...]:
    return (
        ("revocation_override", "no_state_change"),
        ("expiration_degrade", "insufficient_evidence_unresolved"),
        ("multi_event_consensus", "highest_confidence_valid_event"),
        ("explicit_owner_override_candidate", "multi_event_consensus"),
    )


def build_placeholder_composition_sequence(
    precedence_sequence: Iterable[str],
) -> Tuple[str, ...]:
    order = tuple(COMPOSITION_CONTRACT_SKELETON_V1["deterministic_composition_order"])
    selected = [p for p in order if p in set(str(x) for x in precedence_sequence)]
    return tuple(
        selected[: COMPOSITION_CONTRACT_SKELETON_V1["maximum_composition_depth"]]
    )


def validate_composition_boundaries() -> Tuple[bool, Tuple[str, ...]]:
    issues: List[str] = []
    if COMPOSITION_CONTRACT_SKELETON_V1["maximum_composition_depth"] != 3:
        issues.append("maximum_composition_depth_invalid")
    if COMPOSITION_CONTRACT_SKELETON_V1["policy_side_effect_allowed"] is not False:
        issues.append("policy_side_effect_forbidden")
    if (
        COMPOSITION_CONTRACT_SKELETON_V1["state_write_during_composition_allowed"]
        is not False
    ):
        issues.append("state_write_during_composition_forbidden")
    if (
        COMPOSITION_CONTRACT_SKELETON_V1["action_trigger_during_composition_allowed"]
        is not False
    ):
        issues.append("action_trigger_during_composition_forbidden")
    return len(issues) == 0, tuple(issues)
