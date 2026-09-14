# Cognitive Analysis Permission Matrix v1

## 1. Permission principle

All omitted authority is prohibited. `Create`, `update`, `supersede`, and
`revoke` below describe planned candidate-object lifecycle authority only; they
do not authorize persistence, runtime execution, Fact admission, or Field
State mutation.

| Object / boundary | Read | Create | Update | Supersede | Revoke | Mutate Field State | Emit candidate | Execute action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Current Cognitive Context | A3 read-only | No | No | No | No | No | No | No |
| Cognitive Analysis Admission | Context metadata only | Yes | No | Yes, by new result | No | No | No | No |
| Analysis Frame | admitted Context refs | Yes | No | Yes, by new frame | No | No | No | No |
| Hypothesis Candidate | frame/evidence refs | Yes | status only, future governed lifecycle | Yes | status/revocation reference only | No | Yes | No |
| Competing Hypothesis Set | hypothesis refs | Yes | coverage/status only | Yes | No | No | Yes | No |
| Evidence Assessment | evidence and hypothesis refs | Yes | reassessment only | Yes | relation `revoked` only | No | Yes | No |
| Information Gap Refinement | Context gap and frame refs | Yes | refinement only | Yes | No | No | Yes | No |
| Analysis Sufficiency | all A3 candidate refs | Yes | reassessment only | Yes | No | No | No | No |
| Cognitive Analysis Result | governed A3 refs | Yes | No | Yes | mark stale/revoked dependency only | No | Yes | No |
| Decision Admission Boundary | eligible Analysis Result only | Future separate owner | No | Future separate owner | Future separate owner | No | may receive Decision Candidate | No |
| Field Event Candidate | A3 result only when a possible world change is expressed | Future event-candidate owner | No | Future event-candidate owner | No | No | Yes, only as candidate | No |
| Field State | governed Read Model/Context surface only | No | No | No | No | **Reducer only** | No | No |

## 2. State writeback boundary

Only the Field State Reducer may mutate Field State:

```text
Field Event Candidate
  -> Field Event Admission + Temporal Validity
  -> Admitted Event
  -> Field State Reducer
  -> Field State
```

A3 has no exception, escalation, or convenience path around Admission and the
Reducer. It cannot write Field State, State Version, Transition Record, History
Projection, Snapshot, Read Model result, Context, or Envelope.

## 3. Decision boundary

The A3-to-Decision relation is planned only:

```text
Cognitive Analysis Result
  -> Decision Admission Boundary
  -> future Decision Candidate
```

Passing Analysis Sufficiency is necessary for a candidate to approach this
boundary, but is neither a Decision requirement nor a decision authorization.
Task Manager and action authority remain outside A3.

## 4. External and downstream guards

- A3 may not call External Capability, Camera, OCR, SLAM, Network, database,
  Model, device, or runtime.
- An Observation Request Candidate is not permission or execution to observe.
- A Decision Candidate is not Action.
- Experience, Self, and Hive receive no A3 writeback authority in this phase.
- Analysis cannot use missing information, unknown values, or high confidence
  as a substitute for governance admission.
