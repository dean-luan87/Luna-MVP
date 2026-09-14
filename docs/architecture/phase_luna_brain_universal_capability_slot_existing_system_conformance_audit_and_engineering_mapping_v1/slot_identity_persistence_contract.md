# Slot Identity Persistence Contract

`slot_id` is a governed identity owned by Capability Registry/Governance. It
is not derived from Module name, model name, provider name, safety class,
official origin, or visual domain.

## Persistence rules

- Slot identity persists through EMPTY, AVAILABLE, BOUND, SUSPENDED,
  DEGRADED, UNBOUND, RESTORE-CANDIDATE, and REBOUND states.
- A new Module binding creates a new binding record, not a new Slot identity.
- A compatible Implementation or Model replacement does not rename the Slot
  or Module.
- A retired Slot may retain an audit tombstone and history; retirement does
  not convert the Slot into a capability type.
- Binding, unbinding, rebinding, restore, and rollback require trace,
  provenance, compatibility, permission, resource, integrity, and safety
  references where applicable.

## Ownership boundary

Capability Governance owns the binding lifecycle. Model Manager owns model
resource identity. Provider Governance owns provider qualification. System
Maintenance supplies diagnostic/recovery evidence. Capability Self consumes a
read-only projection. Brain and user requests are not direct Slot mutation.

## Future extension

A future binding record should preserve `slot_id`, Module identity, selected
Implementation identity, admission references, temporal lifecycle references,
reason/source, and recovery linkage. The record should be append-oriented and
must not overwrite historical identity.
