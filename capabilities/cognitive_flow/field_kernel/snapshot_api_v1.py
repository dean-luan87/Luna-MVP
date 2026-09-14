"""Read-only Field Snapshot assembly API v1."""

from __future__ import annotations

from typing import Iterable, Mapping

from capabilities.cognitive_flow.field_kernel.core.field_identity_v1 import FieldIdentityV1
from capabilities.cognitive_flow.field_kernel.core.field_relation_v1 import FieldRelationV1
from capabilities.cognitive_flow.field_kernel.core.field_snapshot_v1 import FieldSnapshotV1
from capabilities.cognitive_flow.field_kernel.core.field_state_v1 import FieldStateV1
from capabilities.cognitive_flow.field_kernel.core.field_unit_v1 import FieldUnitV1


def get_field_snapshot(
    field_id: str,
    field_identity: FieldIdentityV1,
    units: Iterable[FieldUnitV1],
    relations: Iterable[FieldRelationV1],
    states: Iterable[FieldStateV1],
    generated_at: str,
    provenance: Mapping[str, object],
) -> FieldSnapshotV1:
    """Return a derived, read-only current Field Snapshot.

    The caller supplies the governed current representation. This function does
    not hold a store, reduce events, perform I/O, or write Field State.
    """

    if field_identity.field_id != field_id:
        raise ValueError("field_identity must match requested field_id")
    if not isinstance(generated_at, str) or not generated_at:
        raise ValueError("generated_at must be a non-empty timestamp string")

    field_units = tuple(unit for unit in units if unit.parent_field == field_id)
    known_refs = {field_id, *(unit.unit_id for unit in field_units)}
    field_relations = tuple(
        relation
        for relation in relations
        if relation.subject_ref in known_refs and relation.object_ref in known_refs
    )
    field_states = tuple(state for state in states if state.target_ref in known_refs)

    snapshot_provenance = dict(provenance)
    snapshot_provenance.setdefault("field_identity_provenance", dict(field_identity.provenance))
    snapshot_provenance.setdefault("derived_from", "reducer_owned_field_state")

    return FieldSnapshotV1(
        snapshot_id=f"field_snapshot:{field_id}:{generated_at}",
        field_ref=field_id,
        units=field_units,
        relations=field_relations,
        states=field_states,
        generated_at=generated_at,
        provenance=snapshot_provenance,
    )
