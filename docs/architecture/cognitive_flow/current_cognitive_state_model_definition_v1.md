# Current Cognitive State Model Definition v1

## Candidate model

`CurrentCognitiveStateCandidateV1` may contain:

| Field | Meaning |
| --- | --- |
| `role_reference` | Existing role reference; no role generation/evolution |
| `field_reference` / `field_view_reference` | Current external-world references |
| `context_reference` | Current Cognitive Context reference |
| `goal_reference` | Primary/secondary/blocked/completed goal-state candidate reference |
| `survival_constraint_reference` | Current Survival constraint reference |
| `cognitive_mode_reference` | Mode Candidate reference |
| `attention_state_reference` | Attention candidate/lifecycle reference |
| `hypothesis_state_reference` / `belief_state_reference` | Current uncertain interpretation references |
| `reasoning_state_reference` | Reasoning Lifecycle reference |
| `decision_state_reference` | Decision Candidate/Resolution/Commitment reference; not a Decision |
| `time_budget_reference` / `information_gap_reference` | Resource and uncertainty references |
| `provenance` / `trace_ref` | Source lineage and trace closure |

It must remain `candidate_only=true`, `not_fact=true`, `not_state_mutation=true`, `not_decision=true`, `not_action=true`, `not_permission=true`, and `not_memory=true`.

Observing, Understanding, Hypothesis Generation, Validation, Decision Formation, Waiting, Executing-reference, and Reviewing are descriptive candidate labels only. They do not start work, execute action, or mutate any underlying system state.
