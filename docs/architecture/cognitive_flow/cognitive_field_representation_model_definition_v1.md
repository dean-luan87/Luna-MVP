# Cognitive Field Representation Model Definition v1

## Planned object

`CognitiveFieldRepresentationCandidateV1` is a planned read-only candidate envelope. It composes references and contextual selection; it does not own their truth, lifecycle, or mutation rights.

| Field | Purpose | Boundary |
| --- | --- | --- |
| `representation_id`, `schema_version` | Stable governance-supplied identity and version | No automatic identity/version creation |
| `field_identity_ref` | Existing governed Field identity | Cannot create or redefine Field |
| `context_ref`, `snapshot_ref` | Immutable Context and derived Snapshot scope | Cannot write Context or Snapshot |
| `entity_primitive_refs` | Candidate Entity references | Not final entities or Fact assertions |
| `concept_refs`, `concept_binding_refs` | Meaning/situation/pattern candidate references | Not State, Decision, or Memory |
| `relation_refs` | Existing structural or candidate relation references labelled by origin | Candidate relation is not causal or structural truth |
| `governed_state_refs`, `environment_state_candidate_refs` | Read-only State/Snapshot references distinct from candidate state references | Candidate state must not be materialized as Field State |
| `temporal_binding` | Current-reference, valid-time scope, history window, uncertainty/staleness | Cannot rewrite Admission or State Valid Time |
| `spatial_binding` | Existing Field/Unit/location/relation references and explicit unknowns | Cannot create map/location truth |
| `task_ref`, `goal_ref`, `attention_context_ref` | Bounded relevance scope | Not Decision, command, or Action authority |
| `relevance_partition` | Primary, peripheral, deferred, recoverable exclusion records | Not permanent deletion or value judgement |
| `risk_candidate_refs` | Candidate warning/risk pattern references with uncertainty | Not a safety Fact or Action trigger |
| `confidence`, `uncertainty`, `sufficiency_status` | Candidate metadata and visible limitations | Not Fact confidence, State confidence, or permission |
| `provenance`, `trace_ref` | Complete append-only source lineage | Must not be removed, replaced, or synthesized |
| `candidate_status` | `candidate`, `validated_candidate`, `stale_candidate`, or `historical_reference` | Never `fact`, `active_state`, `decision`, or `memory` |

## Minimum sufficiency

A representation is minimum sufficient only when it has a bounded Field/Context scope, source references for every selected item, a temporal and spatial scope or explicit unknown marker, declared relevance partition, retained uncertainty, and trace/provenance. It must surface `insufficient` or `unknown` rather than fabricate missing Entity, Relation, State, time, or location information.

## Reference separation

| Reference family | Meaning | Can update Field State? |
| --- | --- | --- |
| `governed_state_refs` / `snapshot_ref` | Existing Reducer/Field Kernel representation source | No; read-only |
| Primitive/Concept/State Candidate refs | Candidate cognitive signals | No |
| Context/Task/Goal/Attention refs | Scope and selection constraints | No |
| Temporal/Spatial refs | Bounded source context and unknowns | No |

## Lifecycle

`requested -> composed_candidate -> validated_candidate -> active_context_view -> refreshed/superseded -> historical_reference -> archived`

Every refresh composes a new candidate for a new Context, Snapshot, Task, Goal, Attention, temporal, or permission scope. It cannot mutate a prior representation or any Field State.
