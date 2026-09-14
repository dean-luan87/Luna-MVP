# Governed observation continuation

## Contract

`REQUEST_MORE_EVIDENCE` is a Cognitive Flow disposition. It is not a provider
invocation request and it is not an automatic retry.

The only permitted planning path is:

```text
RECONSIDER / REQUEST_MORE_EVIDENCE
  -> loop state update
  -> Need reassessment
  -> select current minimum necessary Need
  -> Cognitive Need -> Capability Requirement Bridge
  -> Scope validation
  -> Capability Resolution
  -> Resource / Permission / Safety / Observation admission
  -> next Observation Candidate
```

The final object in this phase is an `ObservationCandidateV1` or a B4
`ReobserveCandidateV1`-compatible handoff candidate. No provider is called and
no camera is activated.

## Required gates

1. The incoming disposition must be linked to a specific loop and source state
   version.
2. The old Requirement must be reassessed against that version. A stale or
   superseded Requirement cannot be reused.
3. Only the current minimum Need can be bridged into a Requirement. Remaining
   plan candidates stay non-binding and loop-local.
4. Scope and Resolution must be recomputed or explicitly retained by contract;
   stale resolution cannot authorize a candidate.
5. Resource, permission, Safety / Survival, and Active Observation Control
   gates must produce candidate approvals or blockers.
6. The Observation Gateway must preserve candidate-only and non-Truth status.
7. A next Observation Candidate must carry loop, state-version, Need,
   Requirement, evidence, Context / Field / Current World, trace, and
   provenance references.

## Capability and observation boundary

Capability execution outcome, Requirement satisfaction, Task contribution, and
cognitive sufficiency remain separate. A successful capability result can
produce `REQUEST_MORE_EVIDENCE`; that result does not imply a second provider
call. A failed capability result can be irrelevant when the loop is already
sufficient. An admitted Observation Candidate is not World Truth.

