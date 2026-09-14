"""Ownership guards: Self Governance only interprets candidate evidence."""

from __future__ import annotations

from typing import Iterable

from .self_governance_core_types_v1 import SourceReferenceV1
from .self_governance_registry_v1 import (
    CANONICAL_OWNER,
    FORBIDDEN_PARALLEL_OWNERS,
)


def validate_canonical_owner(owner: str) -> bool:
    return owner == CANONICAL_OWNER


def validate_read_only_refs(refs: Iterable[SourceReferenceV1]) -> bool:
    return all(
        item.read_only is True and item.source_mutation_allowed is False
        for item in refs
    )


def validate_no_parallel_owner(owner_name: str) -> bool:
    return owner_name not in FORBIDDEN_PARALLEL_OWNERS


def validate_source_owner_preserved(source_owner: str, original_owner: str) -> bool:
    return bool(source_owner) and bool(original_owner) and source_owner == original_owner


def validate_inter_owner_boundary(output: object) -> bool:
    return all(
        getattr(output, name, False) is False
        for name in (
            "source_owner_mutation", "personality_mutation", "emotion_mutation",
            "semantic_compression_execution", "runtime_execution",
        )
    )
