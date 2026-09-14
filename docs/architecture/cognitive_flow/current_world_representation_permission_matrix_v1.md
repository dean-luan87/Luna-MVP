# Current World Representation Permission Matrix v1

## 1. Interpretation

`Can Produce` means a planned governed representation output, not an authorization to persist, execute, or promote it. `Can Mutate` is deliberately true for only one module: Field State Reducer.

| Module | Can Read | Can Produce | Can Mutate | Cannot Write | Forbidden authority |
| --- | --- | --- | --- | --- | --- |
| Cognitive Primitive Layer | Observation/Evidence candidates and provenance | Candidate objects, Field Event Candidate | No | Admitted Event, State, Snapshot, Context | Fact, Decision, Action |
| Field Event Admission | Candidate Event, temporal/evidence/source/trace context | admission result | No | State, versions, Snapshot, Context | State mutation or causal conclusion |
| Field State Reducer | Admitted Event and governed reducer context | Field State | **Yes — Field State only** | Evidence, Snapshot, Context, Hypothesis | Raw-candidate admission, Decision, Action |
| Field Structure | Governed Field refs and provenance | Identity, Unit, Relation | No | Field State, Context | Causal relation or State assertion |
| Field State | Reducer output and provenance | Read-side State representation only | No | Its own State or any other object | Alternative mutation owner |
| Temporal Evolution | Reducer-originated State/versions and temporal provenance | State Version, Transition Record, History Projection | No | Field State, Snapshot, Context | State generation, prediction, causal explanation |
| Field Snapshot | Structure, State, temporal context | derived Snapshot | No | State, history, Context | State store or event reduction |
| Read Model | Snapshot and authorized History Projection | read-only query result | No | State, Snapshot, Context | Raw-event query, direct-storage bypass, dispatch |
| Current Cognitive Context | Read Model views, declared context inputs, Evidence/schema refs | Context, Inclusion, Exclusion, Gap, Sufficiency | No | State, Snapshot, Evidence, Task State | Fact, Hypothesis, Decision, Experience, Value |
| Cognitive Analysis | Context and necessary source refs | future candidates only | No | all CWR objects | Field mutation, Fact admission, Action execution |
| Observation Attention | Its governed attention inputs | Attention Context candidate | No | State, Context result | Truth/State authority or dispatch |
| Task Manager | Task governance context | Task Context candidate | No | State, Context, cognitive truth | Analysis-as-fact or direct action from CWR |
| Experience | Permitted reviewed contexts | future Experience candidates | No | all CWR objects | History-to-Experience conversion or Decision control |
| Self | Permitted individual constraints | future subject/preference candidates | No | all CWR objects | Global truth or other-Luna control |
| Hive | Permitted Experience/schema candidates | future associations/branches | No | all CWR objects | Central decision, voting truth, collective value |
| External Capability | External source input | Observation/Evidence Candidate | No | State, Snapshot, Context | Fact, Context construction, Action |

## 2. Non-negotiable mutation path

```text
Field Event Candidate
  -> Field Event Admission + Temporal Validity
  -> Admitted Event
  -> Field State Reducer
  -> Field State
```

All remaining modules treat State as read-only. This is an architecture permission matrix, not an ACL, database authorization policy, or runtime enforcement service.
