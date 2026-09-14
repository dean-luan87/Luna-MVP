# Current World Representation Envelope Contract v1

## 1. Contract object

`CurrentWorldRepresentationEnvelopeV1` is a Markdown-only integration envelope for cross-module **read-only references**. It is not a Field State object, database entity mandate, storage schema, mutation command, Hypothesis, Decision, or source-hiding wrapper.

| Field | Contract |
| --- | --- |
| `schema_version` | Envelope contract version. |
| `representation_id` | Stable governance/caller-defined representation identifier. |
| `field_ref` | Governed Field reference. |
| `field_identity_ref` | Field Identity reference. |
| `field_structure_refs` | Unit and Relation references used by the representation. |
| `current_state_refs` | Reducer-originated current State references only. |
| `state_version_refs` | State Version references; gaps or unknown order remain explicit. |
| `history_projection_ref` | Field History Projection reference or declared unavailable/incomplete state. |
| `snapshot_ref` | Derived Snapshot reference including `snapshot_version`. |
| `context_refs` | Zero or more derived Context references. |
| `active_context_ref` | Optional Context selected by the authorized caller scope; not a global state. |
| `source_event_refs` | Governed source Event references retained for traceability. |
| `source_evidence_refs` | Evidence references retained without truth promotion. |
| `temporal_scope` | Declared State/Snapshot/Context temporal scope and uncertainty. |
| `representation_status` | `ready`, `incomplete`, `stale`, `unavailable`, or `refresh_required`; no truth claim. |
| `incomplete_reason_codes` | Stable explicit reason codes, including chain, permission, evidence, or input gaps. |
| `provenance` | Derivation/source lineage. |
| `trace` | Trace reference or trace structure compatible with source governance. |

## 2. Envelope invariants

- All members are references to governed objects; this envelope owns no State data and cannot hide provenance.
- `current_state_refs` must originate from the Field State Reducer path.
- `snapshot_ref` is derived and cannot authorize State mutation or raw-event fallback.
- `context_refs` may represent multiple different task/subject scopes from the same Snapshot. `active_context_ref` is scoped, not global.
- Unknown, incomplete, stale, revoked, unavailable, and permission-restricted conditions must be preserved through `representation_status`, `incomplete_reason_codes`, temporal scope, provenance, and trace.
- No consumer may use the envelope to emit a Hypothesis, Decision, Action, Fact, State update, or database write.

## 3. Version and lifecycle behavior

An envelope links versions; it never rewrites them. New State produces a later State Version; later Snapshot receives a different `snapshot_version`; Context refresh receives a different `context_version` and points to `previous_context_ref`. Older envelopes remain readable as historical references where retention policy allows.

This contract does not create JSON Schema, Python models, APIs, persistence, or runtime envelope assembly.
