# Field Kernel Boundary Contract v1

## Accepted references

Field Kernel Current Field View may read traceable Primitive, Concept, Field Representation, Context, Temporal, Spatial, Task, Attention, governed Field Structure/State/Snapshot, Evidence, and source-capability references. Raw model output, provider payload, Memory, Knowledge Base, Fact Store, Decision, Action, database handles, and State write targets are prohibited.

## Reducer relationship

`Field Kernel != Reducer`. Reducer is the sole Field State mutation authority. Kernel neither reduces Candidate input nor writes State, Snapshot, State Version, Transition, History, or Temporal Valid Time.

```text
Candidate / Current Field View -> (future separate Field Event Candidate) -> Admission -> Reducer
```

No direct conversion is defined by this plan.

## Temporal boundary

Kernel references valid time, observation time, admission time, expiration/reconfirmation, snapshot time, and candidate confidence decay as distinct metadata. Missing/estimated/stale/conflicting time remains visible. Kernel does not establish temporal truth, expiry consequence, causal sequence, or forecast.

## Governance boundary

L1 Governance owns input/output eligibility, traceability, permission, lifecycle, and diagnostics. Field Kernel cannot self-grant execution/consumer permission or redefine Protocol/Contract.

## Negative guards

Candidate is not Fact; Kernel is not Memory or Decision; Attention is not Action; external model output cannot enter directly; Kernel cannot bypass Reducer; confidence has no Admission authority.
