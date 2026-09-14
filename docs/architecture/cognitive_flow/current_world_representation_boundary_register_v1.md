# Current World Representation Boundary Register v1

All boundary entries are architecture/fixture closure records, not runtime ACLs. Any later result that seeks to change Field State must first become a Field Event Candidate and re-enter Admission.

| Boundary ID | Source Module | Target Module | Allowed Input | Allowed Output | Mutation Authority | Failure Mode | Negative Guard | Runtime Status | Closure Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CWR-B01 | Cognitive Primitive | Field Event Candidate | Observation/Evidence candidate with provenance | Candidate Event | none | incomplete candidate | no Fact/State promotion | not_integrated | boundary frozen |
| CWR-B02 | Field Event Candidate | Field Event Admission | Candidate Event, temporal/evidence/source/trace | admitted/rejected/deferred/etc. result | Admission only | rejection/defer/expiry/duplicate/order failure | no State write | not_integrated | boundary frozen |
| CWR-B03 | Field Event Admission | Field State Reducer | `admitted_event`, `reducer_eligible=true` | reducer-consumable governed input | Reducer only after admission | `admission_rejected`, invalid input | no raw candidate ingress | fixture_only | evidence reviewed |
| CWR-B04 | Field State Reducer | Field State | Reducer-owned output | time-bounded Field State | **Reducer only** | invalid reduction/transition, no partial State | no alternative state writer | fixture_only | evidence reviewed |
| CWR-B05 | Field State | Temporal Evolution | Reducer-originated State/version lineage | State Version, Transition, History | none | incomplete chain, unknown temporal order | no State generation or prediction | fixture_only | evidence reviewed |
| CWR-B06 | Temporal Evolution + Structure + State | Field Snapshot | structure, current State, temporal refs | derived Snapshot | none | `snapshot_incomplete`, stale/unknown context | no parallel State store | fixture_only | boundary frozen |
| CWR-B07 | Field Snapshot | Read Model | Snapshot ref/version and query scope | read-only query result | none | unavailable/stale/partial query | no raw Event/store bypass | fixture_only | evidence reviewed |
| CWR-B08 | Read Model | Current Cognitive Context | authorized read view plus declared subject/task/goal/attention/time inputs | Context, inclusion/exclusion, gap, sufficiency | none | input incomplete/insufficient/restricted | no automatic selection/fact completion | fixture_only | evidence reviewed |
| CWR-B09 | Current Cognitive Context | Cognitive Analysis Boundary | sufficient or explicitly bounded Context plus source refs | future candidate-only analysis inputs | none | `context_insufficient` blocks entry | no Context/Field writeback | prohibited_in_current_phase | boundary frozen |
| CWR-B10 | Representation Envelope | External Read Consumer | Envelope references under future permission scope | read-only representation reference surface | none | unavailable/stale/restricted envelope | no unified writable entity or source hiding | fixture_only | boundary frozen |

## Return-path rule

```text
future downstream result that proposes a world change
  -> Field Event Candidate
  -> Field Event Admission
  -> Admitted Event
  -> Field State Reducer
  -> Field State
```

No return path may write Context, Envelope, Snapshot, Temporal Evolution, or Field State directly.
