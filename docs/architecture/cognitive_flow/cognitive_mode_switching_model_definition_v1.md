# Cognitive Mode Switching Model Definition v1

## Candidate model

`CognitiveModeSwitchingCandidateV1` may contain:

| Field | Meaning |
| --- | --- |
| `survival_pressure_reference` | Survival pressure candidate reference |
| `field_dynamics_reference` | Field Change/Dynamics candidate reference |
| `context_reference` / `goal_reference` | Current context and goal references |
| `information_value_reference` | Candidate information value input |
| `time_budget_reference` | Candidate cognitive-window input |
| `experience_match_reference` | Traceable historical pattern reference |
| `mode_candidate` | Reactive, Routine, Adaptive, Exploratory, or Reflective |
| `mode_reason` | Candidate basis, uncertainty, and constraints |
| `depth_adjustment_reference` | Future Cognitive Depth candidate relation |
| `provenance` / `trace_ref` | Source lineage and trace closure |

Output remains `candidate_only=true`, `not_fact=true`, `not_state=true`, `not_decision=true`, `not_action=true`, `not_permission=true`, and `not_memory=true`.

## Interpretation

Mode Candidate proposes an appropriate cognitive strategy under current candidate conditions. It does not state what Luna is, what it feels, which role it has, or what it will do.
