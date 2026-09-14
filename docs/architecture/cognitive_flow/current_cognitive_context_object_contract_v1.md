# Current Cognitive Context Object Contract v1

## 1. Contract Position

This Markdown contract plans object shapes for a future Current Cognitive Context implementation. It is not a Python model, JSON Schema, runtime API, database schema, or fact-admission contract.

All objects below must preserve `schema_version`, `provenance`, and `trace`. No object may use system time as fact time or generate a random identifier.

## 2. CurrentCognitiveContextV1

| Field | Contract |
| --- | --- |
| `schema_version` | Version of this Context contract. |
| `context_id` | Stable caller/governance-defined identifier. |
| `context_version` | Immutable Context version. |
| `previous_context_ref` / `superseded_by_ref` | Version lineage references. |
| `field_ref` / `snapshot_ref` | Governed Field and source Snapshot references. |
| `subject_context`, `task_context`, `goal_context`, `temporal_context`, `attention_context` | Required bounded input Contexts. |
| `schema_refs` | Organizational schema references only. |
| `selected_field_units`, `selected_relations`, `selected_states`, `selected_history_refs`, `selected_evidence_refs` | Recoverable selected source references. |
| `excluded_information_refs` | References to Exclusion Records, not deleted source data. |
| `information_gaps` | Information Gap references or embedded contract objects. |
| `sufficiency_status`, `sufficiency_reason_codes` | Analysis-boundary sufficiency result; never Fact Admission. |
| `context_boundary` | Declared subject/task/goal/attention/temporal scope. |
| `provenance`, `trace`, `created_from_refs` | Source lineage and derivation trace. |

Required invariants: derived-only, read-only, no silent deletion, explicit unknown preservation, and no Hypothesis/Decision/Experience content.

## 3. Input Context Objects

### SubjectContextV1

`subject_ref`, `subject_role`, `subject_location_ref`, `subject_capability_constraints`, `subject_permission_scope`, `provenance`, `trace`, `schema_version`.

It represents current subject constraints only. It introduces no personality score, value judgement, or global identity claim.

### TaskContextV1

`task_ref`, `task_type`, `task_stage`, `task_priority`, `task_constraints`, `task_status`, `provenance`, `trace`, `schema_version`.

Task priority is selection relevance only; it does not become safety level, Fact confidence, or action authorization.

### GoalContextV1

`goal_ref`, `primary_goal`, `secondary_goal_refs`, `success_condition_refs`, `stop_condition_refs`, `provenance`, `trace`, `schema_version`.

Goal expresses selection scope, not a Decision or Action command.

### AttentionContextV1

`attention_scope`, `attention_targets`, `attention_priority`, `excluded_targets`, `attention_reason_refs`, `provenance`, `trace`, `schema_version`.

Attention priority controls information selection only. It is not truth confidence and does not mutate Observation Attention or Field State.

### TemporalContextV1

`current_time_reference`, `valid_time_scope`, `history_window_reference`, `temporal_uncertainty`, `stale_state_reference`, `provenance`, `trace`, `schema_version`.

The object distinguishes current reference, State Valid Time, history window, and uncertainty. Unknowns remain explicit and no time is auto-completed.

## 4. Selection Record Objects

### ContextInclusionRecordV1

`source_ref`, `selected_object_ref`, `inclusion_reason`, `relevance_scope`, `priority`, `supporting_evidence_refs`, `provenance`, `trace`, `schema_version`.

### ContextExclusionRecordV1

`source_ref`, `excluded_object_ref`, `exclusion_reason`, `excluded_for_current_context_only`, `recoverable`, `source_snapshot_ref`, `provenance`, `trace`, `schema_version`.

`excluded_for_current_context_only=true` and `recoverable=true` are required unless future source-retention governance explicitly states otherwise.

## 5. InformationGapV1

`gap_id`, `gap_type`, `target_ref`, `missing_information`, `blocking_level`, `related_goal_ref`, `related_task_ref`, `recommended_observation_scope`, `evidence_refs`, `provenance`, `trace`, `schema_version`.

Supported `gap_type`: `missing_entity`, `missing_relation`, `missing_state`, `missing_time`, `missing_location`, `conflicting_evidence`, `stale_information`, `insufficient_resolution`, `permission_restricted`.

`recommended_observation_scope` is only a candidate observation boundary; it is not a task, action, model call, or decision.

## 6. ContextSufficiencyResultV1

`sufficiency_status`, `reason_codes`, `context_ref`, `critical_gap_refs`, `assumption_boundary_refs`, `provenance`, `trace`, `schema_version`.

Allowed status values: `sufficient`, `conditionally_sufficient`, `insufficient`, `unknown`.

This object may state whether Context is enough for bounded analysis. It cannot declare Fact, Truth, safe action, final decision, or a complete world representation.

## 7. Lifecycle Contract

```text
Requested -> Built -> Validated -> Active -> Refreshed -> Superseded -> Archived
```

Refresh always derives a new Context version from a new Snapshot, Task, Goal, Subject, Attention, Temporal, or permission input. It must not mutate an existing Context version. Invalidations result in `stale`, `superseded`, or `refresh_required` markers rather than Field State mutation.

## 8. Forbidden Object Content

- Raw Observation promoted to Fact;
- model-guessed missing State/entity/location/time/relation;
- Hypothesis, causal explanation, prediction, Decision, Experience, or Value;
- a Field State or Transition Record replacement;
- untraceable selected/excluded information;
- permanent deletion represented as contextual exclusion.

## 9. Terminology Note

These planned object names are terminology-change candidates pending a separate Registry Amendment. This document does not alter the existing Canonical Terminology Registry.
