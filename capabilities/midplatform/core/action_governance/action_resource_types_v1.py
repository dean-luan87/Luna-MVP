"""Resource constraint types for Action Governance controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass


RESOURCE_AVAILABLE = "available"
RESOURCE_UNAVAILABLE = "unavailable"
RESOURCE_UNKNOWN = "unknown"
RESOURCE_STATE_SET = frozenset(
    {RESOURCE_AVAILABLE, RESOURCE_UNAVAILABLE, RESOURCE_UNKNOWN}
)
RESOURCE_PENDING_REACTION = "remain_candidate_pending_resource_resolution"


def normalize_resource_state(value: object) -> str:
    """Normalize untrusted resource input without manufacturing availability."""

    if isinstance(value, str) and value in RESOURCE_STATE_SET:
        return value
    return RESOURCE_UNKNOWN


@dataclass(frozen=True)
class ResourceConstraintStatusV1:
    state: str
    reaction: str
