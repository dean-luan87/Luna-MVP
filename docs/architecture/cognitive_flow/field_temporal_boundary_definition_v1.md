# Field Temporal Boundary Definition v1

## 1. Boundary Decision

Field Temporal Evolution is the post-reduction temporal representation boundary inside Field Kernel. It answers how a current governed Field State came to be the current representation through prior governed State versions and validity changes.

It is not a prediction service, causal engine, knowledge-history system, Experience System, or automatic action trigger.

## 2. Ingress-to-Egress Boundary

```text
Event Time / Observation Time / Received Time
  -> Field Event Admission + Temporal Validity
  -> Admitted Event
  -> Field State Reducer
  -> Field State Version + State Valid Time
  -> Field Temporal Evolution
  -> Current Snapshot and future Field History Projection
```

Temporal Validity is an ingress guard: it determines whether a candidate event has sufficient, ordered, non-expired time information for admission.

Temporal Evolution is a post-reduction representation concern: it describes State Version chronology, valid-time, expiry, uncertainty, and history projection after a Reducer-governed State exists.

## 3. Time Boundary Rules

1. Event Time, Observation Time, Admission Time, State Valid Time, and Snapshot Time are distinct coordinates.
2. Admission Time must not be substituted for Event Time or State Valid Time.
3. Snapshot Time must not be treated as the time a world condition began or ended.
4. Missing time must result in explicit Unknown/Estimated/Uncertain representation, not inferred chronology.
5. Only a clearly timezoned and governed timestamp may support an asserted temporal ordering.
6. A State's expiry does not create a successor value or a future prediction.

## 4. Authority Matrix

| Module / layer | May do | Must not do |
| --- | --- | --- |
| External Capability | Emit time-stamped Observation/Evidence Candidates | establish State Valid Time or modify Field State |
| Field Event Admission / Temporal Validity | Evaluate event timestamp completeness, ordering, duplication, and expiry before admission | create Field State or Field History judgement |
| Field State Reducer | Produce and govern State changes from Admitted Events | infer causal reason, predict future, write Experience |
| Field Temporal Evolution | Represent State Version sequence, State Valid Time, expiry, uncertainty, and read-only History semantics | mutate State, admit events, infer causes, make forecasts |
| Field State Read Model | Query current temporal representation and future History projection | alter chronology or State validity |
| Cognitive Analysis | Later read a trajectory and form Hypothesis/Information Gap candidates | write State versions, transitions, or history record directly |
| Experience System | Later record reviewed learning about a process/outcome | treat Field History as Experience or mutate State |
| Hive Experience Field | Later associate Experiences across Lunas | impose a collective timeline or modify a Field State |

## 5. Forbidden Temporal Shortcuts

- `Observation Time -> State Valid Time` without a governed State reduction;
- `Admission Time -> world change time`;
- `model-predicted time -> active Field State`;
- `State expiry -> assumed opposite State`;
- `History sequence -> causal conclusion`;
- `History sequence -> Experience`;
- `Cognitive Analysis -> temporal State transition`;
- `Snapshot query -> State mutation`;
- `Hive or Experience -> Field State timeline`.

## 6. Field History Guard

Field History is descriptive and provenance-preserving. It may answer:

- which governed State versions were effective at a given time;
- which transition records connect the retained versions; and
- which time boundaries are unknown or estimated.

It must not answer:

- whether a Field is good, stable, successful, safe, or valuable;
- why a State changed;
- what it will do next; or
- what action Luna should take.

Those questions belong, respectively, to Experience, Hypothesis/Cognitive Analysis, Prediction (when separately authorized), and Decision/Action Governance.

## 7. Integration Boundary with Existing Assets

| Existing asset | Required A2.1 compatibility |
| --- | --- |
| Field Event Admission | Preserve `admission_status`, admitted event reference, `reducer_eligible`, evidence, source chain, trace, and temporal assessment. Do not duplicate admission. |
| Temporal Validity | Preserve its event-time assessment and defer/order/expiry decision. Do not replace it with State lifecycle logic. |
| Field State Reducer | Remains exclusive State mutation authority. Temporal Evolution records its output relationships only. |
| Field State Read Model | Remains read-only query owner. Future temporal query surfaces must be compatible rather than bypass it. |
| Evidence Chain | Retain non-substitution, source, evidence, and trace lineage through State transitions and history projection. |
| A2 Field Kernel objects | Use Field State and Field Snapshot as current representation inputs/outputs; do not convert Snapshot into a history store. |

## 8. Reserved, Not Implemented

- Temporal Graph;
- State Transition Graph;
- Field Evolution Pattern;
- historical storage and retention policy;
- state replay and temporal query API;
- complex timezone or cross-device clock correction;
- causal analysis, prediction, Hypothesis, Experience, Decision, Action, or Hive integration.

## 9. Phase Boundary

This document creates no code, runner, verifier, database, model, real data connection, Reducer modification, Read Model modification, Registry update, Manifest update, Baseline update, Lifecycle update, or protocol mutation. It awaits human architecture review.
