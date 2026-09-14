"""Derived Field Snapshot object for the Current World Representation Core v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Tuple

from .field_identity_v1 import FIELD_KERNEL_SCHEMA_VERSION_V1
from .field_relation_v1 import FieldRelationV1
from .field_state_v1 import FieldStateV1
from .field_unit_v1 import FieldUnitV1


@dataclass(frozen=True)
class FieldSnapshotV1:
    """Read-only composition of a Field's current governed representation.

    A Snapshot is derived at query time. It is not a second Field State store
    and has no mutation authority.
    """

    snapshot_id: str
    field_ref: str
    units: Tuple[FieldUnitV1, ...]
    relations: Tuple[FieldRelationV1, ...]
    states: Tuple[FieldStateV1, ...]
    generated_at: str
    provenance: Mapping[str, object]
    schema_version: str = FIELD_KERNEL_SCHEMA_VERSION_V1
    derived_only: bool = True
    state_store_write_executed: bool = False
