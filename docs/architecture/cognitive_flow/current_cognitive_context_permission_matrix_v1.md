# Current Cognitive Context Permission Matrix v1

## 1. Scope

This matrix freezes Current Cognitive Context authority as a derived, read-only representation interface. All omitted authority is prohibited.

## 2. Module Permissions

| Module | Can Read | Can Produce | Cannot Write | Forbidden Authority |
| --- | --- | --- | --- | --- |
| Field Kernel | governed structural/State inputs and provenance | Field structure, Snapshot composition surface | Admission result, Task State, Context, Hypothesis | alternate State mutation path, causal/decision authority |
| Temporal Evolution | Reducer-originated State, version/transition provenance | State Version, Transition Record, History Projection | Field State, Context, Hypothesis | State generation, prediction, Experience |
| Field Snapshot | Structure, current State, temporal context | derived Snapshot | Field State, Context source objects | State store, event reducer, action |
| Read Model | Snapshot and authorized History Projection | read-only Current/Historical View | Field State, Snapshot, Context | raw Event query, storage bypass, dispatch |
| Current Cognitive Context | Read Model views, permitted Task/Subject/Goal/Attention inputs, Evidence References, Schema References | Context, Inclusion Record, Exclusion Record, Information Gap, Sufficiency Result | Field State, Temporal Evolution, Snapshot, Evidence, Task State | Fact, State, Transition, Hypothesis, Decision, Experience, Value |
| Observation Attention | governed observation/attention candidate context | Attention Context candidate | Field State, Context result, Task State | fact, State mutation, automatic model dispatch |
| Task Manager | task lifecycle and authorized context | Task Context candidate | Field State, Context, cognitive truth | analysis as fact, direct cognitive action |
| Cognitive Analysis | Current Cognitive Context and necessary source references | Hypothesis Candidate, Interpretation Candidate, Information Gap Refinement, Decision Candidate | Context, Field Kernel, Field State | Fact admission, State mutation, action execution |
| Experience | permitted reviewed experience contexts | future Experience candidates / selection-policy candidates | Field State, Context, Snapshot | automatic history-to-experience conversion, value/decision control |
| Self | permitted individual constraint context | future Subject/Preference/Attention-bias candidates | Field State, Context, global truth | value adjudication in this phase, other-Luna control |
| Hive | permitted Experience / Schema candidates | future association candidates | Field State, individual Context, individual Decision | central control, voting truth, collective value |
| External Capability | external inputs and its own source context | Observation/Evidence Candidates | Field State, Snapshot, Context | fact, Context construction from raw output, action |

## 3. Reducer Mutation Authority

```text
Field Event Candidate
  -> Field Event Admission + Temporal Validity
  -> Admitted Event
  -> Field State Reducer
  -> Field State
```

Reducer is the only Field State mutation authority. Context can neither read underneath Snapshot/Read Model boundaries nor write any object in this path.

## 4. Context-Specific Guards

- Context consumes governed Snapshot/History query views, not Raw Observation as fact.
- Attention Priority is not Truth Confidence.
- Task Priority is not Safety Level.
- Exclusion is recoverable and scoped to the current Context; it is not permanent deletion.
- Unknown time, entity, location, relation, or State remains explicitly unknown.
- Context sufficiency cannot promote anything to Fact Admission.
- Cognitive Analysis has no write-back route to Context or Field Kernel.

## 5. Enforcement Boundary

This matrix is architecture governance only. It creates no ACL, runtime authorization, database permission, model policy, runner, verifier, or test.
