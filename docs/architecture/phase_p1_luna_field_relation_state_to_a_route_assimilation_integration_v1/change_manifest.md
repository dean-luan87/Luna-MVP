# Change Manifest

## Added

- Read-only `RelationStateAssimilationAdapterV1`.
- Adapter result type and controlled ROUTE D evaluation package.
- Controlled Runner and fail-closed Verifier.
- Phase documentation.

## Compatibility changes

- `CognitiveRelationInterpretationCandidateV1` now has optional typed relation
  refs, Field State provenance, and unchanged candidate-only boundaries.
- `CognitiveStateFormationInputV1` accepts optional typed relation
  interpretation candidates; empty preserves legacy callers.
- A-Route request and execution evidence expose the optional typed candidate
  and Current World relation interpretation refs while retaining
  `ARouteIngressRefsV1.relation_refs`.
- Cognitive State Formation forwards supplied governed candidates instead of
  reconstructing their semantics from opaque relation strings.

## Preserved

- Field State Reducer / Field Kernel remains the Field relation state owner.
- A-Route and Cognitive State Formation only consume/read candidates.
- `OBSERVED_IN_FIELD != BELONGS_TO_FIELD`.
- No Fact, Field Truth, World Truth, persistence, identity, Target, Memory,
  PCN, Decision, Task, Action, device, SLAM, or Tracking behavior.
- `POLICY_TRACE_COMPATIBILITY_GAP` remains independent and unrepaired.

## Status

`GO — VERIFIED — PHASE CLOSED`.

## First user-terminal repair history

The first terminal attempt crashed before ROUTE D semantic verification with
`A_ROUTE_CONTROLLED_REPLAY_ADMISSION_CONTRACT_MISMATCH`: the A-Route replay
consumer read `evidence_information_refs` from `ControlledReplayAdmissionV1`,
which canonically provides `available_information_refs` instead. The verifier
summary-not-found error was a cascading consequence of that Runner crash.

The consumer now uses an explicit execution-mode mapping: controlled replay
passes no evidence-information binding and retains its canonical available
information refs; LIVE runtime continues to read the runtime admission's
canonical evidence-information binding. This is a stale-consumer repair only.
ROUTE D semantic verification remains unreached and the phase remains
`WAITING_FOR_USER_TERMINAL_REVERIFICATION`.

## Second user-terminal repair history

The second terminal attempt reached the same pre-semantic plumbing boundary
and failed when `_run_admitted_runtime()` read the non-existent
`inherited_information_refs` field from `ControlledReplayAdmissionV1`. This
confirmed a broader admission-shape assumption, classified as
`A_ROUTE_RUNTIME_ADMISSION_CONTRACT_NORMALIZATION_GAP`. The verifier's
summary-not-found error was a cascading Runner failure.

The A-Route now performs one explicit execution-mode normalization of all four
information channels before constructing `CognitiveStateFormationInputV1`:
Controlled Replay retains its canonical required/available refs and explicitly
has no evidence-binding or inherited-information channel; LIVE runtime retains
all four of its canonical channels. This is a local stale-consumer repair and
does not modify admission contracts, relation semantics, adapter semantics,
or cognitive logic. ROUTE D semantic verification remains unreached.

## Final user-terminal closure

The final user-terminal verification passed with:

- `all_checks_passed=true`
- `cognitive_logic_result=PASS`
- `operational_result=PASS`
- `failed_checks=[]`
- `final_decision=GO`

The typed relation semantics were verified through the complete read-only
handoff from `FieldStateCandidate` to A-Route ingress, Cognitive State
Formation, and `CurrentWorldCandidateV1.relation_interpretation_refs`. The
Field State candidate ref, subject, `OBSERVED_IN_FIELD`, Field object,
relation candidate/kind, evidence/source/provenance refs, and unresolved
identity boundary were preserved.

All Truth, persistence, mutation, raw-provider shortcut, reinvocation,
Memory/PCN, Decision/Task/Action, and device-control guards passed.
`POLICY_TRACE_COMPATIBILITY_GAP` remains a known non-blocking independent
debt. ROUTE D is now closed; no ROUTE E or additional feature work is started.
