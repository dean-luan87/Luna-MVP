# Field Kernel Model Definition v1

## CurrentFieldViewV1 (planned)

| Field | Meaning | Boundary |
| --- | --- | --- |
| `field_ref`, `context_ref`, `snapshot_ref` | Existing governed Field/Context/Snapshot scope | No Field/Snapshot creation or mutation |
| `structure_refs`, `governed_state_refs` | Existing Unit/Relation/Reducer State references | Read-only; State remains Reducer-owned |
| `primitive_candidate_refs`, `concept_candidate_refs`, `field_representation_refs` | Candidate overlay inputs | Never Fact, State, or admission input |
| `temporal_awareness` | Valid-time, observation, expiry, history, and unknown references | No temporal rewrite or prediction |
| `spatial_refs`, `task_ref`, `attention_context_ref` | Bounded relevance context | Attention is selection, not Action |
| `relevance_partition` | Current/peripheral/historical/possible/unknown/conflicting references | Not deletion, truth ranking, or authority |
| `uncertainty`, `provenance`, `trace_ref` | Required append-only limitations and lineage | Cannot be removed or replaced |
| `view_status` | `candidate_overlay`, `validated_query_view`, `stale`, or `historical_reference` | Never Fact, State, Decision, Memory |

## Conflict record

`CandidateConflictRecord` retains competing references, conflict type, scope, time/spatial applicability, evidence/provenance, trace, and unresolved status. It cannot choose a winner, rewrite a State, or create a causal conclusion.

## Confidence

Confidence is candidate metadata only. It cannot rank a conflict into truth, create an Admission result, modify State confidence, or grant consumer permission.
