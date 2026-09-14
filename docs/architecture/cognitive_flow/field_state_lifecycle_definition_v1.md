# Field State Lifecycle Definition v1

## 1. Purpose

This document defines the planned lifecycle semantics for Field State within Field Temporal Evolution. It describes the lifecycle of a governed representation, not an explanation of world causes and not an Experience lifecycle.

The lifecycle applies to a Reducer-produced State Version and its temporal representation. It must be mapped compatibly to existing Reducer statuses in a separately authorized implementation phase; it does not rename or modify those statuses now.

## 2. Lifecycle States

```text
Admitted Event
  -> Reducer
  -> Created
  -> Active
  -> Updated / Uncertain / Expired
  -> Archived
```

| Lifecycle state | Definition | Entry condition | Exit condition | Must not mean |
| --- | --- | --- | --- | --- |
| Created | A new governed Field State Version has been emitted by the Reducer with provenance. | Reducer produces a State from Admitted Event(s). | It becomes effective, is superseded, is uncertain, or expires. | Fact without provenance, causal explanation, or direct Field Kernel write. |
| Active | The State Version is currently effective within known valid-time context. | Its State Valid Time supports present effectiveness. | A Reducer-produced successor, uncertainty condition, or expiry changes its representation. | Permanent truth or forecast. |
| Updated | A successor State Version has been produced from a later governed reduction. | Reducer produces a successor State associated with the same target/State lineage. | Prior version is retained as historical or archived; successor becomes current when effective. | In-place overwrite without lineage. |
| Uncertain | Temporal or State information is insufficient to safely assert a precise active condition or transition. | Reducer / temporal representation retains an unknown, estimated, ambiguous, or reconfirmation-needed condition. | New governed information resolves, supersedes, or expires it. | Permission to fabricate a value, cause, or future outcome. |
| Expired | The State's known valid-time has ended and no governed successor currently replaces it. | Valid interval ends or governed expiry applies. | A new Reducer-produced State supersedes it, or it is archived. | Automatic reversal to a previous or assumed normal State. |
| Archived | A non-current State Version is retained only as a historical representation under future retention governance. | It is no longer part of the current representation and is retained. | Retention/retraction policy governs later disposition. | Experience, historical judgement, or active State. |

`Updated` describes a relationship between versions, not mutable replacement of the earlier version. The earlier State remains available to a future Field History projection with its original provenance.

## 3. Lifecycle Ownership

| Lifecycle activity | Owner | Field Temporal Evolution role | Prohibited owner |
| --- | --- | --- | --- |
| Candidate Event eligibility | Field Event Admission / Temporal Validity | Preserve admitted temporal context | Field Kernel, Read Model, Cognitive Analysis |
| State creation or successor production | Field State Reducer | Represent resulting version and temporal relation | Field Kernel composition, model, Hive, Experience |
| Current-State composition | Field Kernel / Read Model boundary | Surface current lifecycle state in Snapshot/query | Snapshot consumer |
| History projection | Future Field Temporal Evolution read contract | Order retained versions and transitions read-only | Experience System as automatic judgement maker |
| Experience formation | Experience System | None | Field Temporal Evolution |

## 4. Transition Rules

### 4.1 Initial State

```text
Admitted Event -> Reducer -> Created -> Active or Uncertain
```

The Reducer determines whether a governed State is produced. Field Temporal Evolution cannot convert an Admitted Event into Created State on its own.

### 4.2 State Update

```text
Active State Version A
  + later Admitted Event
  -> Reducer
  -> successor State Version B
  -> A is Updated / historical; B is Created then Active or Uncertain
```

No module performs an in-place, untraceable mutation. The predecessor/successor link must preserve event, reduction, valid-time, evidence, source-chain, and trace provenance.

### 4.3 Uncertainty

```text
Active or Created State
  + unknown/ambiguous temporal basis
  -> Reducer-governed representation
  -> Uncertain
```

Uncertainty may arise from unknown start/end time, estimated duration, non-comparable ordering, incomplete validity, or elapsed reconfirmation window. It does not bypass Admission and does not cause a new observation or model result to write State.

### 4.4 Expiration

```text
Active State
  + valid-time ended and no successor State
  -> Expired
  -> Archived (if future retention policy retains it)
```

Expiration removes current effectiveness; it does not assert the inverse value, a normal condition, or a forecast.

### 4.5 Archival

```text
Updated or Expired State
  -> Archived historical representation
```

Archive is a planned historical lifecycle location, not a database instruction. Retention duration, deletion, replay, and historical query implementation remain unspecified.

## 5. State Validity and Snapshot Time

| Question | Correct time basis |
| --- | --- |
| When did the real-world reported event occur? | Event Time |
| When was it observed? | Observation Time |
| When did the system accept it? | Admission Time |
| During what interval is the State considered effective? | State Valid Time |
| When was the current view assembled? | Snapshot Time |

Snapshot Time may select which State Versions are current in the query view, but it must not overwrite Event Time, Observation Time, Admission Time, or State Valid Time.

## 6. State Lineage Requirements

Each planned State Version and transition representation must retain, where applicable:

- `state_id` and target reference;
- predecessor / successor State references;
- admitted event reference(s);
- reduction reference / version;
- Event, Observation, Admission, State Valid, and Snapshot time context;
- evidence references, source chain, and trace reference;
- uncertainty and expiry representation;
- lifecycle status and no in-place mutation claim.

Lineage allows a reader to see the governed path from an earlier State to the current representation. It does not establish causality or produce a reusable experience pattern.

## 7. Non-Goals

This lifecycle does not define domain-specific State-value transitions, a State Transition Graph implementation, replay/event-store mechanics, confidence promotion, prediction, causal explanation, decision, Experience, Hive behavior, or automatic reconfirmation action.

## 8. Phase Boundary

This is a lifecycle definition document only. It changes no existing Reducer lifecycle or status enum and creates no implementation artifact.
