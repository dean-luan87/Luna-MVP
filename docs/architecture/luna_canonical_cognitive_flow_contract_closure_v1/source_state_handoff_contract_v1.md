# Evidence / Result → Source-State Handoff Contract v1

## Purpose

This contract defines the only legal approach from runtime result to a candidate source-state update. It never writes Field, Current World, or World Truth.

## Minimal contract surface

| Field | Meaning |
|---|---|
| `handoff_ref`, `handoff_version` | handoff identity/version |
| `source_result_ref`, `evidence_refs` | Provider/Action and Evidence lineage |
| `target_source_boundary` | `CURRENT_WORLD`, `FIELD`, or explicitly both |
| `target_entity_refs`, `target_field_refs` | target correlation only |
| `source_version_refs`, `expected_target_version` | optimistic source binding |
| `event_time`, `effective_time`, `observed_at` | temporal basis |
| `uncertainty`, `confidence`, `status` | epistemic/execution qualification |
| `provenance_refs`, `trace_ref` | reverse linkage |
| `candidate_only` | must be true before source admission |
| `source_mutation_authorized` | must be false at this boundary |
| `invalidation_refs` | stale/conflicting source context |

## Routing

- Observation evidence may produce a Current World Update Candidate, a Field Event Candidate, or both when separately justified.
- Action Result first becomes effect evidence or observation input, then follows the same candidate path.
- Field Event Candidate requires Field admission/reducer semantics.
- Current World Candidate is consumed by cognition as a representation; it is not World Truth.

## Responsibility

Provider/Action owns result correctness. Gateway owns mapping/admission correlation. Field owns Field mutation. Current World/State Formation owns candidate formation/version. A owns interpretation. No Gateway or handoff consumer may directly mutate source state.

