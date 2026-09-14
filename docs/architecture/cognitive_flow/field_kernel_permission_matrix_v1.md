# Field Kernel Permission Matrix v1

## 1. Scope

This matrix freezes read/write authority at the Field Kernel composition boundary. “Write” means a governed lifecycle or representation write, not a generic storage permission. Any authority not expressly listed is prohibited.

## 2. Permission Matrix

| Module | Read | Write | Forbidden |
| --- | --- | --- | --- |
| External Capability | Its own input and external sensing context | Observation / Evidence Candidates only | Field State, State Version, Snapshot, Fact, Hypothesis, Decision, Action |
| Cognitive Primitive | Observation/Evidence Candidates and declared provenance | Candidate objects / Field Event Candidate only | Admitted Event, Field State, Snapshot, History, Decision |
| Field Event Admission | Candidate Event, temporal context, evidence/source/trace | Admission result: admitted/rejected/deferred/etc. | Field State, State Version, Snapshot, causal conclusion |
| Temporal Validity | Candidate Event time fields and admission context | Temporal assessment inside Admission boundary | Field State, History Projection, prediction, State Valid Time rewrite |
| Field State Reducer | Admitted Event, governed temporal/evidence/provenance context, existing State context | **Field State only** | raw Candidate acceptance, Evidence rewrite, Snapshot write, Hypothesis, Decision, Action |
| Field Structure (Identity / Unit / Relation) | Governed Field references and structural provenance | Future governed structural objects only | Field State, causal relationship, History judgement, action |
| Field Temporal Evolution | Reducer-originated State, State Version, transition provenance, valid-time context | State Version / Transition Record / History Projection representations | Field State mutation/generation, raw Event ingress, causal explanation, prediction |
| Field Snapshot | Structure, current Field State, temporal context | Derived Snapshot only | persistent State, event reduction, State mutation, History judgement |
| Read Model | Derived Snapshot and future History Projection under declared query scope | Read-only query result only | raw Event query, direct State-store bypass, State/History mutation, dispatch |
| Cognitive Analysis | Read Model Current View, Historical View, Evidence References | Hypothesis Candidate, Information Gap, Decision Candidate | Field Kernel mutation, Fact/State declaration, action execution |
| Experience System | Reviewed outcomes and permitted read contexts | Experience Episode / Kernel candidates under its own future contract | Field State, History as automatic Experience, Decision control |
| Hive Experience Field | Permitted Experience associations and divergence records | Experience links/branches under future governance | Field State, individual Decision, collective truth/value, Field timeline write |

## 3. State Mutation Authority

```text
Only path allowed to change Field State:

Field Event Candidate
  -> Field Event Admission + Temporal Validity
  -> Admitted Event
  -> Field State Reducer
  -> Field State
```

No other row in this matrix receives State write authority. Field Kernel composition, Temporal Evolution, Snapshot, Read Model, Cognitive Analysis, Experience, Hive, and External Capability must treat Field State as read-only.

## 4. Snapshot and History Authority

| Object | Writer / producer | Readers | Permanent restriction |
| --- | --- | --- | --- |
| Field Snapshot | Field Kernel derived composition only | Read Model, authorized Cognitive Analysis through Read Model | Not State source or state store |
| Field History Projection | Field Temporal Evolution derived composition only | Read Model, authorized Cognitive Analysis through Read Model | Not Experience, Knowledge judgement, prediction, or causal proof |
| Read Model Query Result | Read Model only | Authorized requester | Not State mutation input or action command |

## 5. Cognitive Analysis Boundary

Cognitive Analysis receives only read-only representation inputs:

```text
Field Snapshot + Temporal Evolution + Evidence Reference
```

It may produce only candidate outputs under its own future contracts:

```text
Hypothesis Candidate + Information Gap + Decision Candidate
```

It cannot write any Field Identity, Unit, Relation, State, State Version, Transition Record, History Projection, Snapshot, or Read Model result. Any later candidate event follows the ordinary Admission and Reducer gate; no analysis shortcut is authorized.

## 6. Enforcement and Non-Goals

This is an architecture permission matrix, not an ACL implementation. It creates no runtime authorization service, database permission, protocol mutation, registry update, manifest, baseline, lifecycle change, runner, verifier, or test.
