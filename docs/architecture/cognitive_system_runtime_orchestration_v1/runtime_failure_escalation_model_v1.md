# Runtime Failure Escalation Model v1

## Failure path

```text
Failure
   ↓
Diagnostics
   ↓
Fallback Candidate
   ↓
Escalation Candidate
   ↓
Brain Evaluation when required
```

Capability failure, state synchronization conflict, resource exhaustion,
stale Evidence, process timeout, and wake-up rejection are diagnosed with
provenance and scope. A failure does not stop the entire cognitive system.

## Boundary

Fallback is a candidate for alternative capability, reduced observation,
backgrounding, suspension, or Brain activation. Runtime does not choose the
fallback, alter Goal, modify Reality, or execute Action. Diagnostics does not
become a second Brain and does not automatically learn from one failure. Runtime does not choose the fallback,
does not alter Goal, does not modify Reality, and does not execute Action.
