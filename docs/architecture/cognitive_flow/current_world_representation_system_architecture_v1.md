# Current World Representation System Architecture v1

## 1. Position and definition

- Phase: `Phase-A2.7-Current-World-Representation-Integration-Planning-v1-001`
- Execution Mode: Planning Only
- Status: integration architecture proposal pending human review

The **Current World Representation System** (CWR System) is Luna's single-direction, traceable composition of governed Field structure, current State, temporal evolution, Snapshot, Read Model, and Current Cognitive Context. It answers only:

> What does Luna currently represent this Field as being like, and what minimum governed portion is relevant to a declared cognitive scope?

It is not a World Brain, Reality Engine, Cognitive World Model, Active Reality, Working World, or Mini World. It is neither a database mandate nor World Understanding. Causal explanation, prediction, Hypothesis, Decision, Experience, Self, and Hive remain outside this system.

## 2. Frozen layers and data flow

| Layer | Components | Responsibility | Authority limit |
| --- | --- | --- | --- |
| A. World Input Governance | Cognitive Primitive, Field Event Candidate, Field Event Admission | Preserve candidate provenance and decide admission. | Does not mutate Field State. |
| B. World Mutation Core | Field State Reducer, Field State | Reduce an Admitted Event into governed current State. | Reducer is the sole State mutation authority. |
| C. World Temporal Organization | State Version, Transition Record, Field History Projection | Organize post-reduction change and uncertainty. | Does not generate State or explain cause. |
| D. World Read Representation | Field Identity, Unit, Relation, Snapshot, Read Model | Compose and expose governed current/historical read views. | Does not own a second State store. |
| E. Cognitive Relevance Interface | Current Cognitive Context, inclusion/exclusion, gap, sufficiency | Select a recoverable minimum-sufficient view for a declared scope. | Does not write State, Snapshot, or Evidence. |
| F. Cognitive Analysis Boundary | future Cognitive Analysis | Read Context and necessary source references. | Has no CWR write-back route. |

```text
Cognitive Primitive
  -> Field Event Candidate
  -> Field Event Admission
  -> Admitted Event
  -> Field State Reducer
  -> Field State
  -> State Version
  -> Transition Record
  -> Field History Projection
  -> Field Snapshot
  -> Read Model Query
  -> Current Cognitive Context
  -> Cognitive Analysis Boundary
```

Every stage consumes only the prior governed object(s). Raw Observation, Evidence, Primitive, or Candidate Event never directly becomes Field State. If a later analysis result suggests a world change, it is only a new Event Candidate and must return to Field Event Admission; it never writes backward.

## 3. Object chain

```text
Field Identity -> Field Unit -> Field Relation -> Field State
  -> State Version -> Transition Record -> Field History Projection
  -> Field Snapshot -> Current Cognitive Context
```

| Object | Meaning in the system |
| --- | --- |
| Field Identity | What Field is in physical, social, task, and provenance scope; not its current condition. |
| Field Unit | A manageable part of that Field. |
| Field Relation | A structural association only; never a causal claim. |
| Field State | Reducer-owned, time-bounded current description with evidence and source lineage. |
| State Version | Immutable temporal reference to a Reducer-originated State. |
| Transition Record | Governed description of a version change with event reference; not a cause. |
| Field History Projection | Read-only temporal organization of versions and transitions; not Experience. |
| Field Snapshot | Full derived current Field view; not a State source or storage owner. |
| Current Cognitive Context | A task/subject/goal/attention/time-scoped, recoverable subset of a Snapshot; not State or Understanding. |

## 4. Snapshot and Context separation

Field Snapshot is the complete governed current view for one Field. Current Cognitive Context is the **Minimum Sufficient Field Representation** for one declared subject, task, goal, attention, permission, and temporal scope.

- One Snapshot may support multiple Context versions without change to Snapshot or Field State.
- Context exclusions remain recoverable, are current-context-only, and never delete Snapshot material.
- Context cannot become a storage copy, an alternative State source, or a Read Model bypass.
- Snapshot contains no Hypothesis; Context contains no causal reason, prediction, Decision, Experience, or Value.

## 5. Time and versioning invariants

The CWR System preserves rather than conflates Event Time, Observation Time, Admission Time, State Valid Time, Snapshot Time, and Context temporal scope. Unknown, estimated, stale, revoked, and unavailable conditions remain explicit; system-current time is never substituted as fact time.

Required references are `snapshot_version`, `source_state_version_refs`, `source_history_projection_ref`, `context_version`, `source_snapshot_ref`, and `previous_context_ref`.

- A State update produces a new State/State Version and cannot mutate an older Snapshot.
- A new Snapshot cannot overwrite older Context; a refresh produces a new Context version.
- Context lifecycle may mark `stale`, `refresh_required`, `superseded`, or `archived` without State mutation.

## 6. Failure and degradation rules

| Failure code | Owning boundary | Required handling |
| --- | --- | --- |
| `admission_rejected` | Admission | Block State ingress; preserve decision and trace. |
| `reducer_input_invalid` | Reducer ingress | Block reduction; preserve invalid reason; no partial write. |
| `reducer_transition_invalid` | Reducer / temporal handoff | Block invalid transition representation; do not repair by guessing. |
| `state_version_chain_incomplete` | Temporal Evolution | Keep history incomplete; preserve unknown predecessor/order. |
| `temporal_order_unknown` | Temporal Evolution | Retain unknown ordering; no fabricated chronology. |
| `snapshot_incomplete` | Snapshot | Return incomplete/unavailable read representation; never synthesize a second store. |
| `snapshot_stale` | Snapshot / Read Model | Mark stale and require governed refresh; do not imply current validity. |
| `read_model_unavailable` | Read Model | Degrade to unavailable; no raw-event or direct-store fallback. |
| `context_input_incomplete` | Context | Produce explicit construction failure or incomplete result; no missing-value fill. |
| `context_insufficient` | Context sufficiency | Block entry to bounded Cognitive Analysis unless a future contract explicitly permits conditional limits. |
| `context_stale` | Context lifecycle | Preserve prior Context and request a new version when applicable. |
| `evidence_revoked` | Provenance / Context | Preserve revocation, mark affected read objects `refresh_required`; no model guess. |
| `permission_restricted` | Query / Context | Preserve the restriction and related gap; do not broaden access. |

## 7. Historical asset alignment findings

The reviewed historical assets are preserved as read-only compatibility inputs, not rewritten definitions of CWR:

| Historical asset family | Future input/governance potential | CWR non-confusion rule |
| --- | --- | --- |
| World Model write-level and contamination policies | Candidate quarantine, expiry, provenance, revalidation, and audit considerations at future admission/governance boundaries. | Historical memory/write-level terms do not create CWR Field State or a parallel mutation owner. |
| World Context evidence contracts | Evidence, spatial/temporal anchor, TTL, source/trace, and revalidation references. | `WorldContextEvidence` remains historical candidate/evidence vocabulary, not Snapshot or Context. |
| Scene Delta contracts | Candidate-only delta, repeated-evidence, anchor, expiry, and replay governance. | Scene Delta is not Field State, Temporal Evolution, or a State Version. |
| Task/Scene Context policy | A possible future Task Context input discipline. | Historical `scene_context` does not equal Current Cognitive Context. |

Naming overlap is recorded for future governance only. No historical asset is deleted, declared obsolete, renamed, or converted into a new CWR state.

## 8. Terminology change candidates

The Canonical Terminology Registry is unchanged. A future controlled amendment should consider: Current World Representation System, Current World Representation Envelope, Current Cognitive Context, Minimum Sufficient Field Representation, Context Inclusion Record, Context Exclusion Record, and Context Sufficiency Result. The prohibited aliases in section 1 remain forbidden aliases if retained for historical search.

## 9. Phase boundary and stop condition

This architecture creates no runtime, model, database, network, mutation path, protocol/registry/manifest/baseline/lifecycle change, Cognitive Analysis, Hypothesis, Decision, Experience, Self, or Hive function. Stop this phase once the chain, references, authority, failure behavior, and Snapshot/Context isolation are expressed in the required contracts.
