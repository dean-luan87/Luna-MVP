"""Ownership and boundary guards for controlled implementation v1."""

from __future__ import annotations

from capabilities.midplatform.core.cognitive_memory_experience.cognitive_memory_experience_registry_v1 import (
    CANONICAL_OWNER,
)


def validate_canonical_owner(owner: str) -> bool:
    return owner == CANONICAL_OWNER
