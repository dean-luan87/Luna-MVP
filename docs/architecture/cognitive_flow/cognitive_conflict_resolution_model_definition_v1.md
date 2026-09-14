# Cognitive Conflict Resolution Model Definition v1

## Candidate model

`CognitiveConflictResolutionCandidateV1` may retain:

| Field | Meaning |
| --- | --- |
| `conflict_reference` / `conflicting_candidate_references` | Traceable competing candidate lineage |
| `conflict_type` / `classification_reference` | Candidate conflict category |
| `context_reference` / `goal_reference` | Current Context and goal relations |
| `survival_reference` / `mission_reference` | High-order constraint references |
| `value_evaluation_reference` / `risk_reference` | Candidate comparison information |
| `information_gap_reference` / `uncertainty` | Missing or unresolved basis |
| `experience_reference` | Historical pattern candidate input |
| `resolution_path_candidate` | Preserve, defer, gather information, seek alternative, seek assistance, or maintain uncertainty |
| `provenance` / `trace_ref` | Source lineage and trace closure |

The artifact remains `candidate_only=true`, `not_fact=true`, `not_state=true`, `not_decision=true`, `not_action=true`, `not_permission=true`, and `not_memory=true`.

Resolution Candidate describes a possible conflict-handling path, not a resolved outcome.
