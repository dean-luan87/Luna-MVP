# Decision Resolution Model Definition v1

## Candidate model

`CognitiveDecisionResolutionCandidateV1` may retain:

| Field | Meaning |
| --- | --- |
| `choice_space_reference` / `decision_candidate_references` | Candidate option set and lineage |
| `context_reference` / `goal_reference` | Current situation and goal |
| `survival_constraint_reference` / `mission_constraint_reference` | Highest-order constraints |
| `behavior_boundary_reference` / `constraint_reference` | Current behavior/cognitive limits |
| `value_evaluation_references` | Candidate value, cost, and risk descriptions |
| `time_budget_reference` | Candidate available cognitive window |
| `experience_reference` | Historical pattern candidate reference |
| `resolution_path_candidate` | Narrow, defer, gather information, seek assistance, or maintain uncertainty |
| `rejected_candidate_references` | Constraint-ineligible candidates with reasons |
| `remaining_candidate_references` | Options retained for future commitment |
| `conflict_reference` / `uncertainty` | Unresolved trade-offs and gaps |
| `provenance` / `trace_ref` | Source lineage and trace closure |

The output remains `candidate_only=true`, `not_fact=true`, `not_state=true`, `not_decision=true`, `not_action=true`, `not_permission=true`, and `not_memory=true`.

Resolution does not mean that one candidate was selected. It means the present candidate space has a traceable provisional form for future Commitment consideration.
