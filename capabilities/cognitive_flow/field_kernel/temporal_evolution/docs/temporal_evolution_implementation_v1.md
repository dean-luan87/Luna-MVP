# Field Temporal Evolution Skeleton Implementation v1

## 1. Module Position

This skeleton belongs to L1 Cognitive Flow / Field Kernel. It describes the version history of a Reducer-produced Field State and answers only:

> What governed State Version preceded the current State Version?

It is not a time prediction system, causal analysis engine, Experience System, Hypothesis system, Decision system, Temporal Graph, database, or event stream.

## 2. Implemented Object Surface

| Object | Purpose |
| --- | --- |
| `StateVersionV1` | Immutable Field State Version with predecessor reference, valid-time boundary, provenance, and trace. |
| `TransitionRecordV1` | Provenance-preserving descriptive record linking State Versions with a governed `event_ref`. |
| `LifecycleValidationResultV1` | Deterministic result for a planned lifecycle transition without changing State. |
| `FieldHistoryProjectionV1` | Read-only composition of State Versions, Transition Records, and input-order-preserving timeline. |

Every contract object includes `schema_version`, `provenance`, and a trace field. IDs and all times are caller-/fixture-supplied; the skeleton creates neither random IDs nor system timestamps.

## 3. Reducer and Field Kernel Relationship

```text
Admitted Event
  -> existing Field State Reducer
  -> Field State
  -> StateVersionV1
  -> TransitionRecordV1
  -> FieldHistoryProjectionV1
  -> Field Snapshot / future Read Model query
```

Temporal Evolution consumes only the representation of Reducer-produced State. It does not call the Reducer, turn raw events into State, update State, alter Field Snapshot, or replace the Read Model.

`event_ref` is required on every Transition Record as a governed transition source. It is not a causal assertion about why the world changed.

## 4. Lifecycle Validation

Supported lifecycle states are `created`, `active`, `updated`, `uncertain`, `expired`, and `archived`.

The validator accepts planned paths such as `Created -> Active`, `Active -> Updated`, `Active -> Expired`, and `Expired -> Archived`. It rejects, among other cases, `Archived -> Active`, `Expired -> Updated`, a non-created transition without a source State Version, and a Transition Record without `event_ref`.

Validation returns `validation_result` and a stable `reason_code`; it has no mutation, time lookup, external I/O, or decision side effect.

## 5. History Projection and Time Boundary

`build_field_history_projection_v1()` creates an immutable, read-only Field History Projection. It preserves caller input order instead of sorting unknown or estimated time into fabricated chronology.

The object keeps Event, Observation, Admission, State Valid, Snapshot, and Transition Recorded time as distinct semantic coordinates. Unknown start/end, estimated duration, and uncertain lifecycle detail are carried explicitly in State Version uncertainty metadata or Transition Record time status.

## 6. Fixed Simulation Fixtures

The simulation module provides fixed data construction functions for:

- shopping-mall shop status: operating -> renovating -> closed;
- airport entrance status: open -> restricted -> open;
- incomplete time: Unknown, Estimated, and Uncertain retained explicitly.

It is not a runner and is not executed in this phase. It calls no real Reducer, database, network, model, or system clock.

## 7. Boundaries and Non-Goals

- Reducer is the sole Field State mutation authority.
- Temporal Evolution cannot generate a new State or accept a raw event.
- Field History is not Experience, knowledge judgement, causal explanation, prediction, Hypothesis, Decision, or Action.
- No temporal graph, state transition graph, persistence, replay store, real-time update loop, or cross-device clock correction exists in this skeleton.

## 8. Phase Boundary

This phase adds only the isolated Temporal Evolution skeleton assets. It does not modify Reducer, Admission, Temporal Validity, Read Model, Field Kernel core objects, Registry, Manifest, Baseline, Lifecycle, or Protocol governance.
