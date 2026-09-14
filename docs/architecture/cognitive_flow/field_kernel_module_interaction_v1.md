# Field Kernel Module Interaction v1

## 1. Purpose

This document defines the unidirectional interaction model among Field Kernel components and their direct upstream/downstream boundaries. It is a planning artifact and grants no runtime call authority.

## 2. System Interaction Flow

```text
External Capability
  -> Observation / Evidence Candidate
  -> Cognitive Primitive
  -> Field Event Candidate
  -> Field Event Admission + Temporal Validity
  -> Admitted Event
  -> Field State Reducer
  -> Field State
  -> State Version / Transition Record / History Projection
  -> Field Snapshot
  -> Read Model Query
  -> Cognitive Analysis (read-only future consumer)
```

The Field Kernel begins its State path at Reducer-produced Field State. Field Structure may be prepared under its own future governed identity lifecycle, but it cannot change this ingress sequence.

## 3. Field Structure and Field Evolution Interaction

| Source component | Target component | Permitted handoff | Prohibited handoff |
| --- | --- | --- | --- |
| Field Identity | Field Unit | Field scope / parent reference | current State assertion |
| Field Unit | Field Relation | Unit reference and structural scope | causal claim |
| Field Identity / Unit / Relation | Field Snapshot | current structural composition input | State write command |
| Field State Reducer | Field State | sole governed current State output | raw candidate or model output as State |
| Field State | Temporal Evolution | State reference, valid-time, evidence, source, trace, version lineage | State mutation instruction |
| Temporal Evolution | Field Snapshot | temporal context, history/version references, uncertainty | predicted State or causal explanation |
| Field Snapshot | Read Model | current query view source | store-write or event-reduction instruction |
| Read Model | Cognitive Analysis | read-only Current/Historical View plus provenance | mutable Field Kernel access |

## 4. Detailed Component Contracts

### 4.1 Admission to Reducer

Admission supplies an Admitted Event with temporal assessment, evidence references, source chain, trace, and `reducer_eligible=true`. The Reducer alone decides whether it emits a governed State output. Field Kernel does not re-run admission or temporal validity.

### 4.2 Reducer to State

Reducer output is the only source for Field State. Its State representation is immutable at the Field Kernel composition boundary and must preserve State value, State Valid Time, Evidence References, provenance, and trace.

### 4.3 State to Temporal Evolution

Temporal Evolution can construct State Version and Transition Record representations only around an existing Reducer-originated State. It cannot accept raw Event input, emit a replacement State, or derive causality from transition order.

### 4.4 Structure plus State plus Temporal Context to Snapshot

Snapshot composition gathers scoped Field Identity, Units, Relations, current Field State, and relevant temporal context. It derives a single Field query view. It neither persists the view as State nor changes a component input.

### 4.5 Snapshot to Read Model

Read Model receives a derived representation surface, a request scope, required fields, temporal scope where authorized, trace, and replay/provenance context. It returns a descriptive query result only. It never queries raw Event input or uses a Snapshot as permission to alter State.

## 5. Interaction Prohibitions

```text
Forbidden feedback paths

Read Model ----X----> Field State / Reducer
Snapshot -----X-----> Field State / Admission
Temporal Evolution -X-> Field State
Cognitive Analysis -X-> Field Kernel write
Experience -----------X-> Field Kernel write
Hive -----------------X-> Field Kernel write
External Capability --X-> Field State
```

There is no circular dependency between Field Structure and Field Evolution. They meet only at the read-only Snapshot composition boundary around Reducer-owned State.

## 6. Cognitive Analysis Interface Reservation

### Read-only input package

| Input | Required content | Purpose |
| --- | --- | --- |
| Field Snapshot | current structure, State, snapshot time, provenance | current world representation |
| Temporal Evolution | State Versions, Transition Records, History Projection, uncertainty | change trajectory without causal conclusion |
| Evidence Reference | source/evidence/trace context relevant to the query | provenance-aware analysis |

### Permitted future outputs

- Hypothesis Candidate;
- Information Gap;
- Decision Candidate.

### Interface guards

- Cognitive Analysis has no Field Kernel write method.
- A Hypothesis Candidate is not a State, Event, Fact, transition, or Snapshot update.
- Any later event candidate proposed from analysis must return to the normal Candidate → Admission → Reducer path.
- Decision Candidate must remain downstream of its own authorization boundary; it cannot execute or mutate Field Kernel.

## 7. Interaction Lifecycle

```text
Field identity scope
  -> admitted event reaches Reducer
  -> current State and temporal representation are available
  -> Snapshot is generated for a query
  -> Read Model returns a bounded view
  -> Cognitive Analysis may consume the view read-only
```

History is an optional read projection after Temporal Evolution, not a prerequisite for every current Snapshot. A Field without retained history remains a valid current representation; it must not fabricate prior versions.

## 8. Phase Boundary

No invocation API, implementation, dependency wiring, runtime loop, runner, verifier, external data connection, model connection, or database behavior is created by this document.
