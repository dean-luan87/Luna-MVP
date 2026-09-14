# A3 Translation Layer Real Evidence Contract Mapping Plan v1

## Contract Reuse

This is a field-mapping plan over existing contracts; it introduces no parallel Evidence, Translation, Permission, or Runtime Contract.

| future provider-envelope concept | existing binding/Translation field | retained rule |
| --- | --- | --- |
| provider/source identity | `source_capability_refs` and candidate provenance `source_capability_refs` | provider is provenance, never Cognitive Entity |
| governed Evidence identity | `evidence_refs` and candidate `source_refs` | reference only; no raw payload or Fact claim |
| read-only Context identity | `context_refs` | no Context/Snapshot/State handle or writeback |
| evidence lineage | `provenance_refs` and candidate provenance `source_refs` | source chain remains explicit and immutable in the request |
| trace lineage | `trace_ref` and candidate provenance `trace_ref` | trace retained end-to-end |
| provider uncertainty/confidence | candidate `uncertainty` / optional `confidence` | not truth, Fact authority, or admission authority |
| requested mapping category | `requested_primitive_type` / candidate `primitive_type` | only frozen candidate vocabulary |

## Provenance and Traceability Contract

The required chain is:

```text
Provider source identity
        ↓
Governed Evidence reference
        ↓
Binding request provenance + trace
        ↓
Translation Request
        ↓
Cognitive Primitive Candidate provenance + trace
```

Any missing, replaced, hidden, or untraceable link blocks future binding. Provenance does not validate the world claim, identify an Entity, or permit Fact/Decision/Action/State mutation.

## Runtime Boundary Review

`runtime_authorized=false` remains unchanged. Provider binding planning does not permit model invocation, network/database access, OCR/Vision/Audio/Spatial execution, Runtime Integration, external service calls, or State/Context/Snapshot/Memory writes. A future implementation requires a separate approved Provider Adapter phase and a boundary revision with controlled validation.

