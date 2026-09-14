# A3 Translation Layer Freeze Authorization v1

## Authorization Scope

This record freezes the A3 Evidence Context Translation Layer v1 as Luna's **Cognitive Input Boundary**. It freezes the reference-only Translation Request to Cognitive Primitive Candidate path; it does not grant a new L1 permission, activate a Capability, or authorize Runtime.

```text
Evidence Envelope (candidate-only)
        ↓
Translation Request (references only)
        ↓
Cognitive Primitive Candidate (candidate-only)
```

## Frozen Input Boundary

Every request must retain non-empty `source_capability_ref`, `evidence_ref`, `context_ref`, `trace_ref`, and provenance reference(s). The input is a reference envelope only: no raw model payload, database handle, State/Snapshot handle, Fact assertion, Decision command, or Action command is accepted.

## Frozen Output and Semantic Boundary

The only output class is `Cognitive Primitive Candidate` with `candidate_only=true` and `fact_status=not_fact`. Permitted primitive types are `entity_candidate`, `relation_candidate`, `semantic_candidate`, `spatial_candidate`, and `temporal_candidate`.

The output cannot state a real-world conclusion and cannot be a Fact, Decision, Action, State, Memory item, or Learning admission.

## Frozen Negative Guards

1. Evidence cannot become Fact.
2. Evidence cannot create Decision or Action.
3. Provenance and trace cannot be removed, replaced, or hidden.
4. External provider/model identity remains provenance and cannot become a Cognitive Entity.
5. Context, Snapshot, Field State, and Memory cannot be modified.

## Runtime Boundary

`runtime_authorized=false` remains frozen. Runtime Integration, Real Evidence Binding, model invocation, external service access, database access, and State mutation are all outside this authorization.

## Authority Statement

This freeze relies on the existing L1 Protocol Governance references described by the A3 Runtime Protocol Admission Mapping: Input/Output Candidate Governance, Protocol Traceability, Permission/Admission, Model/Skill Admission, and Runtime Boundary. It creates no parallel Contract, permission model, admission route, or authorization lifecycle.

