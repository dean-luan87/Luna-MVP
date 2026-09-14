# Field Kernel Boundary Definition v1

## 1. Boundary Decision

Field Kernel is the pre-analysis **Current World Representation** boundary in Luna Cognitive Flow.

It answers only:

> What does Luna currently represent as the state and organization of this Field?

It does not answer:

- Why the state exists;
- what the state means beyond its governed representation;
- what may happen next;
- what Luna should decide or do;
- what an Individual Luna should value.

Accordingly, Field Kernel is not Luna's World Model or World Understanding. It is the governed representation layer that Cognitive Analysis may inspect.

## 2. Responsibility Boundary

| Field Kernel may do | Field Kernel must not do |
| --- | --- |
| Organize Field Identity, Field Unit, Field Relation, and Reducer-produced Field State into a current representation. | Receive raw Observation, Evidence, Primitive, or Candidate Event as a state mutation input. |
| Preserve admitted-event, evidence, source-chain, trace, and temporal provenance. | Re-admit, reinterpret, or weaken Admission / Temporal Validity decisions. |
| Define a Field Snapshot and World Representation Query contract. | Create a new Reducer, direct write path, or parallel state store. |
| Supply a read-only surface compatible with the existing Read Model. | Form Hypothesis, causal explanation, prediction, Decision Candidate, Action, Experience, or value judgement. |
| Reserve compatible extension points for history, confidence, temporal evolution, and attention. | Implement those extensions or use them to alter existing runtime semantics in A2.0. |

## 3. Authority Boundary

### 3.1 State authority

```text
Admitted Event
  -> Field State Reducer
  -> Field State
```

The existing Field State Reducer is the exclusive Field State mutation authority. The Field Kernel contract consumes its result for organization and read representation only.

### 3.2 Authority matrix

| Module / layer | Authorized role at this boundary | Explicitly prohibited role |
| --- | --- | --- |
| External Capability | Emit Observation / Evidence Candidates with source and uncertainty | write Field State, declare Fact, decide Action |
| Cognitive Primitive Layer | Organize Observation, Evidence, Entity/Relation/State Candidates | upgrade a candidate to Field State |
| Field Event Admission | Evaluate candidate event eligibility | modify Field State |
| Temporal Validity | Assess expiry, ordering, duplication, and time sufficiency before admission | duplicate a world representation or mutate State |
| Field State Reducer | Reduce Admitted Event to governed Field State | accept raw candidates, rewrite Evidence, make Decisions |
| Field Kernel | Organize current representation and Snapshot contract | mutate State, infer causes, decide actions |
| Field State Read Model | Serve read-only Current World Representation query results | reduce events, mutate State, dispatch downstream work |
| Cognitive Analysis | Read representation and produce Hypothesis / Difference / Information Gap candidates | directly modify Field State or Snapshot source data |
| Task Manager | Govern later task and action authorization boundaries | define cognitive truth or execute analysis directly |
| Experience System / Hive Experience Field | Supply later experience association or context candidates | write Field State, replace individual interpretation, decide truth |

## 4. Existing Module Relationship

```text
External organs
  -> Cognitive Primitive candidates
  -> Field Event Admission + Temporal Validity
  -> Admitted Event
  -> Field State Reducer
  -> Field Kernel current representation
  -> Field State Read Model query
  -> Cognitive Analysis
```

### Contract allocation

- **Field Event Admission** is the Cognitive Admission Boundary. It owns the Candidate Event to Admitted Event transition.
- **Temporal Validity** is the Admission-side temporal decision authority. Field Kernel retains temporal context but does not reproduce duplicate, expiry, ordering, or deferral logic.
- **Field State Reducer** remains Field Kernel Mutation Authority. Future A2 code must compose or adapt it, never replace it.
- **Field State Read Model** is World Representation Query Layer. Field Snapshot must be a compatible query surface, not a storage bypass.
- **Evidence Chain** remains provenance substrate. A2 must retain source/evidence/trace semantics across identity, units, relations, state, and snapshot composition.
- **Cognitive Analysis** begins after Current World Representation. It may query but cannot modify the representation directly.

## 5. Ingress and Egress Guards

### Ingress guards

1. State reduction only accepts an Admitted Event provided by Field Event Admission.
2. The admission result must preserve the temporal assessment and reducer eligibility decision.
3. Evidence references, source-chain, and trace reference must travel as provenance rather than being converted into a state assertion by themselves.
4. A model output, Observation, Evidence, Entity Candidate, Relation Candidate, or State Candidate cannot bypass Admission.

### Egress guards

1. Field State is emitted only through the existing Reducer-owned state lifecycle.
2. Field Snapshot is a read-only composition, never a mutation command or backing authority.
3. World Representation Query Result is descriptive; it is not a Hypothesis, Conclusion, Decision Candidate, Action, or Experience record.
4. A query consumer must form any later analysis under its own authority and must return through Admission if it proposes an event candidate.

## 6. Prohibited Shortcuts

The following are permanent A2 guards:

- `Observation -> Field State`
- `Evidence -> Field State`
- `model output -> Field State`
- `Cognitive Analysis -> Field State`
- `Experience or Hive -> Field State`
- `Field Snapshot -> active state store`
- `Field State -> Hypothesis` without a distinct Cognitive Analysis contract
- `Field Snapshot -> Decision or Action`

The only sanctioned state change path remains:

```text
Field Event Candidate
  -> Admission / Temporal Validity
  -> Admitted Event
  -> Field State Reducer
  -> Field State
```

## 7. Planned Extension Reservations

The following names may be planned for future compatible work, without assigning current implementation authority:

| Reserved extension | Intended boundary | Not implemented now |
| --- | --- | --- |
| Temporal Evolution | Controlled representation of state change across time | history engine, predictive logic, clock correction |
| Field History | Read-only governed history projection | event-store design or alternate state mutation path |
| State Confidence | Representation metadata distinguished from truth | confidence-based admission or automatic fact promotion |
| Attention Context | Link to Observation Attention resource allocation | attention-driven state write or automatic model dispatch |

Hypothesis, Experience, Decision, and Hive are not Field Kernel extensions; they belong to their respective future domains.

## 8. Implementation Preconditions for A2

Before the first Field Kernel implementation begins, human review must confirm:

1. Existing Field Event Admission, Temporal Validity, Field State Reducer, Field State Read Model, and Evidence Chain are reused by contract.
2. No A2 asset will modify those modules, their registry, manifest, baseline, lifecycle, or runtime semantics without a separately authorized phase.
3. Field Snapshot will remain a derived query object.
4. Field Kernel will remain a Current World Representation layer and will not absorb Cognitive Analysis.

## 9. Phase Boundary

This document creates no implementation, runtime, runner, verifier, database connection, model connection, real data ingestion, registry change, or lifecycle change. It awaits human architecture review.
