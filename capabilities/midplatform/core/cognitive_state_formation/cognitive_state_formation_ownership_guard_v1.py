"""Ownership and boundary guards for Cognitive State Formation controlled implementation v1."""

from __future__ import annotations

from typing import Iterable

from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_core_types_v1 import (
    SourceRefV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_registry_v1 import (
    CANONICAL_OWNER,
)


def validate_canonical_owner(owner: str) -> bool:
    return owner == CANONICAL_OWNER


def validate_ref_read_only(refs: Iterable[SourceRefV1]) -> bool:
    return all(
        ref.read_only is True
        and ref.reference_only is True
        and ref.source_mutation_allowed is False
        for ref in refs
    )


def validate_no_owner_transfer(refs: Iterable[SourceRefV1]) -> bool:
    return all(bool(ref.owner) for ref in refs)


def validate_field_ref_read_only(refs: Iterable[SourceRefV1]) -> bool:
    return all(ref.read_only is True and ref.reference_only is True for ref in refs)
