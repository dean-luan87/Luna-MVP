# Current World Representation Integration Contract v1

## 1. Contract scope

This Planning Only contract integrates existing Field Kernel planning and controlled skeleton surfaces without changing them. It defines only reference handoffs; it does not authorize invocation, storage, mutation, or runtime composition.

## 2. Boundary contracts

| Boundary | Accepted input | Output | Sole authority | Failure rule |
| --- | --- | --- | --- | --- |
| Admission -> Reducer | `admitted_event` with `reducer_eligible=true`, temporal assessment, evidence/source/trace | Reducer-consumable governed event | Admission decides admission; Reducer decides reduction | Rejected, deferred, duplicate, expired, out-of-order, or invalid candidates never silently enter Reducer. |
| Reducer -> Field State | Valid governed event and existing Reducer context | Reducer-produced Field State | Reducer only | Invalid input or transition blocks a State output; partial State write is forbidden. |
| Field State -> Temporal Evolution | Reducer-originated State and declared State Version lineage | State Version, Transition Record, History Projection | Temporal organization only | Incomplete chains stay incomplete; predecessor/time order is never guessed. |
| Structure + State + temporal -> Snapshot | Identity, Units, Relations, current State refs, temporal context | Derived Field Snapshot | Snapshot composition only | Missing key inputs yield `snapshot_incomplete` or unavailable; no parallel State store is created. |
| Snapshot -> Read Model | Snapshot ref/version and declared current or historical query scope | Read-only World Representation Query Result | Read Model only | `read_model_unavailable` has no raw-event or storage-bypass fallback. |
| Read Model + declared inputs -> Context | Authorized Snapshot/History view, Subject/Task/Goal/Attention/Temporal inputs, evidence/schema refs | Context, inclusion/exclusion records, Information Gaps, sufficiency result | Context construction only | Incomplete inputs or insufficient scope stays explicit; no automatic fill, selection, or admission. |

## 3. Input/output and non-write invariants

1. Field Structure may scope a Snapshot but cannot define or mutate Field State.
2. Temporal Evolution only consumes Reducer-originated State representations; it creates no State and gives no causal explanation or forecast.
3. Snapshot is a derived query view, immutable for its version, and cannot be used as a later State source.
4. Read Model only exposes governed views; it cannot inspect raw Event history or underlying State storage as a bypass.
5. Current Cognitive Context contains references and selection records, not a replacement Snapshot payload or a global copy of the world.
6. Cognitive Analysis may read Context and necessary source references. It cannot change Context, Snapshot, State, Evidence, history, or structural objects.
7. A later proposed state change is a new Event Candidate and must traverse Admission -> Reducer again.

## 4. Time, lineage, and refresh contract

| Reference | Required contract meaning |
| --- | --- |
| `snapshot_version` | Immutable identity of the derived Snapshot version. |
| `source_state_version_refs` | Complete or explicitly incomplete list of State Versions represented by Snapshot. |
| `source_history_projection_ref` | Temporal projection used by the Snapshot, or an explicit unavailable/incomplete status. |
| `context_version` | Immutable version of a Current Cognitive Context. |
| `source_snapshot_ref` | Snapshot version from which Context selection derives. |
| `previous_context_ref` | Context lineage for refresh or supersession; never an in-place update instruction. |

Unknown start/end times, estimated duration, uncertain order, stale data, and revoked evidence remain source-visible. A Context refresh generates a fresh Context version; it does not overwrite an earlier Context or mutate its source Snapshot.

## 5. Future Cognitive Analysis reservation

```text
Current Cognitive Context + necessary governed source references
  -> future Hypothesis Candidate / Information Gap refinement / Decision Candidate
```

This is an interface reservation only. Analysis cannot interpret an output as Fact, mutate CWR, execute an Action, or return a write command. No Hypothesis, Decision, Experience, Self, Hive, or model integration is introduced by this contract.

## 6. Out of scope

No reducer runtime, Read Model implementation, query API, context-selection algorithm, persistence, concurrency, networking, model inference, historical migration, or final-world correctness claim is specified here.
