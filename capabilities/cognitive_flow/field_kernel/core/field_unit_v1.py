"""Field Unit object for the Current World Representation Core v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Tuple

from .field_identity_v1 import FIELD_KERNEL_SCHEMA_VERSION_V1


@dataclass(frozen=True)
class FieldUnitV1:
    """A manageable unit within a declared Field.

    A unit may reference Entity Candidates, but it does not independently
    promote an entity identity or mutate the Field State.
    """

    unit_id: str
    unit_type: str
    parent_field: str
    attributes: Mapping[str, Any]
    relation_refs: Tuple[str, ...] = field(default_factory=tuple)
    provenance: Mapping[str, Any] = field(default_factory=dict)
    schema_version: str = FIELD_KERNEL_SCHEMA_VERSION_V1
    candidate_only: bool = True
