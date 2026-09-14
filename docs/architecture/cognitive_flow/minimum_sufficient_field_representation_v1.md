# Minimum Sufficient Field Representation v1

## 1. Definition

Minimum Sufficient Field Representation is the smallest recoverable set of governed Field information that can support the declared next Cognitive Analysis boundary for a specific subject, task, goal, temporal scope, and attention scope.

It is not “less information is always better.” It reduces cognitive redundancy while preserving information needed to avoid unacceptable analysis error, permission error, safety error, or task failure.

## 2. Selection Dimensions

| Dimension | Selection question | Required guard |
| --- | --- | --- |
| Relevance | Is the information materially related to the current task or goal? | Relevance is not truth confidence. |
| Action Proximity | Could it affect a near-term judgement or later authorized action? | It does not authorize action. |
| Risk | Does omission affect safety, permission, or high-cost error? | Task priority is not safety level. |
| Temporal Validity | Is it valid, stale, unknown, or estimated for the Context temporal scope? | Do not fabricate times or freshness. |
| Spatial Relevance | Is it in the current or next declared Field scope? | Do not infer location from missing data. |
| Relational Relevance | Does it have a key structural relation to subject, target, or task? | Structural relation is not causality. |
| Evidence Strength | Is evidence sufficient for inclusion in the Context? | Evidence is not Fact. |
| Information Gap Value | Would a missing item block or materially constrain later analysis? | Gap is not a tool/action permission. |

## 3. Inclusion and Exclusion Rules

Every selection must produce an Inclusion Record or Exclusion Record. Absence of a record is prohibited because it creates silent information loss.

### Inclusion Record

| Field | Meaning |
| --- | --- |
| `source_ref` | Snapshot, History Projection, or Evidence Reference source. |
| `selected_object_ref` | Unit, Relation, State, History, or evidence object selected. |
| `inclusion_reason` | Bounded relevance reason. |
| `relevance_scope` | Subject/task/goal/attention scope to which the reason applies. |
| `priority` | Selection priority only; not truth confidence or safety judgement. |
| `supporting_evidence_refs` | Evidence references supporting contextual inclusion. |

### Exclusion Record

| Field | Meaning |
| --- | --- |
| `source_ref` | Original recoverable source reference. |
| `excluded_object_ref` | Object not selected for this Context. |
| `exclusion_reason` | Reason scoped to the current Context. |
| `excluded_for_current_context_only` | Must be `true`. |
| `recoverable` | Must be `true` unless source-retention governance states otherwise. |
| `source_snapshot_ref` | Snapshot from which the object remains recoverable. |

Supported exclusion reasons:

- `irrelevant_to_current_task`;
- `outside_attention_scope`;
- `temporally_stale`;
- `insufficient_evidence`;
- `duplicate_representation`;
- `outside_subject_permission`;
- `outside_spatial_scope`;
- `deferred_for_later_analysis`.

Exclusion never means false, incorrect, permanently deleted, or unusable in another Context.

## 4. Sufficiency Design

| Sufficiency status | Meaning | Analysis boundary |
| --- | --- |
| `sufficient` | Required current inputs and critical conditions are present for the declared analysis scope. | May enter bounded Cognitive Analysis. |
| `conditionally_sufficient` | Analysis may proceed only with explicit limitation/assumption boundaries. | Limitation and reason codes must be exposed. |
| `insufficient` | Critical input is absent; continuing risks unacceptable error. | Do not silently continue as sufficient. |
| `unknown` | The system cannot safely assess whether the Context is sufficient. | Preserve uncertainty and request later review/observation candidate scope if needed. |

Sufficiency is neither Fact Admission nor truth confidence. It is an analysis-input completeness judgement scoped to one Context version.

## 5. Information Gap Design

Context may emit a descriptive Information Gap, without generating a Hypothesis.

| Field | Meaning |
| --- | --- |
| `gap_id` | Stable caller-defined gap identifier. |
| `gap_type` | Nature of missing, conflicting, stale, or restricted information. |
| `target_ref` | Relevant Field/Unit/Relation/State/Evidence reference. |
| `missing_information` | Explicit description of what is not known. |
| `blocking_level` | Effect on declared analysis sufficiency. |
| `related_goal_ref` / `related_task_ref` | Scope reference. |
| `recommended_observation_scope` | Candidate observation boundary only, never an Action Decision. |
| `evidence_refs`, `provenance`, `trace` | Lineage and recoverability. |

Supported `gap_type` values: `missing_entity`, `missing_relation`, `missing_state`, `missing_time`, `missing_location`, `conflicting_evidence`, `stale_information`, `insufficient_resolution`, and `permission_restricted`.

## 6. Multi-Context Mechanism

One Field Snapshot can yield several Contexts without changing the Snapshot or Field State.

| Shared airport Snapshot | Context A: person meeting arrival | Context B: airport safety staff | Context C: blind pedestrian navigation |
| --- | --- | --- | --- |
| Subject / task | find arrival exit | inspect restricted-area anomaly | reach exit safely |
| Selected content | terminal, arrivals floor, flight, exit, path, key time | restricted zones, entry States, relevant personnel/alerts | location, accessible relation, obstacle State, wayfinding evidence |
| Different gaps | flight/exact exit uncertainty | restricted-area evidence gap | route/obstacle/wayfinding gap |

Different selections are valid because subject, task, goal, permission, and attention differ. No Context may be written back as global Field State.

## 7. Scenario Planning

### 7.1 Airport pickup

Include current terminal, arrivals floor, target flight, arrival exit, subject location, reachable path, and critical temporal State. Exclude unrelated commercial areas and distant units while retaining Exclusion Records.

### 7.2 Shopping-mall shop-status observation

Include closed/renovating shops, temporal changes, regional distribution, mall notices, and foot-traffic-related States. Do not produce “the mall has failed” as a Hypothesis or judgement.

### 7.3 Indoor navigation for a blind user

Include subject location, target, passable Relations, obstacle States, wayfinding Evidence, and route-related Information Gaps. Exclude unrelated advertising and distant objects as current-context exclusions only.

## 8. Over-Compression Guards

- Never remove a source reference merely to reduce payload size.
- Keep critical permission, safety, and temporal uncertainty even when it makes Context larger.
- Preserve conflicting evidence rather than choosing a convenient single representation.
- Keep a Gap when omission prevents a trustworthy sufficiency judgement.
- A later Context may select currently excluded information; no global deletion occurs.

## 9. Phase Boundary

This is a planning definition only. It creates no selection algorithm, scoring model, runtime compression service, database, model call, or automatic observation/action behavior.
