"""Ownership guard for controlled implementation v1."""

from __future__ import annotations

from capabilities.midplatform.core.cognitive_learning.cognitive_learning_registry_v1 import (
    CANONICAL_OWNER,
)


def validate_canonical_owner(owner: str) -> bool:
    return owner == CANONICAL_OWNER
