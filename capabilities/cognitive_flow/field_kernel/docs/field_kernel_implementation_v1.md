# Field Kernel Implementation v1

## 1. Module Position

Field Kernel v1 is Luna's **Current World Representation Core**. It describes the current structure and governed state of a Field. It is not a World Model, Knowledge Base, Database, reasoning engine, or action engine.

Its question is: **what does Luna currently represent this Field as being like?** It does not explain causes, predict the future, generate Hypotheses, produce Decisions, record Experience, or participate in Hive behavior.

## 2. Implemented Object Surface

| Object | Role |
| --- | --- |
| `FieldIdentityV1` | Field identity plus physical, social, and task context. A Field is not merely a map region. |
| `FieldUnitV1` | Manageable Field component, such as an entrance, shop, service desk, gate, or crossing. |
| `FieldRelationV1` | Scoped Unit/Field relationship using `contains`, `belongs_to`, `connected_to`, or `near`. |
| `FieldStateV1` | Immutable representation of one Reducer-produced, current time-bounded State. |
| `FieldSnapshotV1` | Derived, read-only composition of Units, Relations, and current States for one Field. |

Every object has `schema_version = luna.field_kernel.v1`.

## 3. Reducer Relationship

```text
Admitted Event
  -> FieldKernelReducerAdapterV1 (validate and preserve only)
  -> existing Field State Reducer
  -> FieldStateV1 representation
  -> FieldSnapshotV1
```

`FieldKernelReducerAdapterV1` only accepts `admission_status=admitted_event` with `reducer_eligible=true`. It creates no Reducer, invokes no Reducer, performs no temporal judgment, and writes no State.

`field_state_from_reducer_output_v1()` accepts only a mapping marked `produced_by=field_state_reducer`. It is a read-side projection conversion, not a reduction or mutation path.

## 4. Snapshot Mechanism

`get_field_snapshot()` receives the caller's already governed current representation and returns a derived `FieldSnapshotV1` for one Field. Units are scoped by `parent_field`; Relations and States are scoped by Field/Unit references. The API stores nothing, performs no I/O, and modifies no input. A Snapshot is never a second State store.

## 5. Simulation Boundary

The fixture-only simulation has `shopping_mall`, `airport`, and `street` scenarios. Each includes an admitted-event-shaped input plus a separately declared Reducer-produced State fixture. It composes a Snapshot only; it does not admit an event or reduce it.

No OCR, SLAM, LLM, database, network, or external capability is called.

## 6. Permission Boundaries

- Field Event Admission and Temporal Validity retain event-eligibility authority.
- Field State Reducer remains the sole Field State mutation authority.
- Field Kernel does not accept raw Observation, Evidence, Primitive, or Candidate Event for state mutation.
- Read Model remains the compatible read/query authority.
- Cognitive Analysis, Experience, Hive, models, and Snapshot consumers cannot directly modify Field State.

## 7. Future Extension Points

Only contract-level extension points are reserved for Field History, Temporal Evolution, State Confidence, Attention Context, stable Field identity lifecycle, and cross-Field representation. None is implemented in v1.

## 8. Phase Boundary

This module creates no runner, verifier, database, model connection, real data path, Admission implementation, Temporal Validity implementation, Reducer implementation, Read Model change, Registry change, Manifest change, Baseline change, or Lifecycle change.
