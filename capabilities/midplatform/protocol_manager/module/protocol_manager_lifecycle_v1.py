from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.protocol_manager.module.protocol_manager_module_types_v1 import (
    LIFECYCLE_STATES,
    not_fact,
)


def build_protocol_manager_lifecycle_candidate_v1(
    input_candidate: Mapping[str, Any], registry_lookup: Mapping[str, Any]
) -> Dict[str, Any]:
    transition = dict(input_candidate.get("requested_lifecycle_transition") or {})
    from_state = str(
        transition.get("from")
        or ((registry_lookup.get("protocol_record") or {}).get("lifecycle_state"))
        or "candidate"
    )
    to_state = str(transition.get("to") or from_state)

    valid_from = from_state in LIFECYCLE_STATES
    valid_to = to_state in LIFECYCLE_STATES

    return {
        "schema_version": "protocol_manager_lifecycle_candidate_v1",
        "from_state": from_state,
        "to_state": to_state,
        "lifecycle_transition_candidate": {
            "from": from_state,
            "to": to_state,
            "requested": bool(transition),
        },
        "lifecycle_transition_valid": valid_from and valid_to,
        "lifecycle_applied": False,
        **not_fact(),
    }
