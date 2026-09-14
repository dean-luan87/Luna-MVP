"""Field Relation object for the Current World Representation Core v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .field_identity_v1 import FIELD_KERNEL_SCHEMA_VERSION_V1


FIELD_RELATION_PREDICATES_V1 = (
    "contains",
    "belongs_to",
    "connected_to",
    "near",
)


@dataclass(frozen=True)
class FieldRelationV1:
    """A scoped, non-causal relationship between two Field references."""

    relation_id: str
    subject_ref: str
    predicate: str
    object_ref: str
    provenance: Mapping[str, Any]
    schema_version: str = FIELD_KERNEL_SCHEMA_VERSION_V1
    candidate_only: bool = True

    def __post_init__(self) -> None:
        if self.predicate not in FIELD_RELATION_PREDICATES_V1:
            raise ValueError("unsupported Field Relation predicate")
